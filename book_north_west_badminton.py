from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select
import time
from datetime import datetime
from nwb_data import zen_planner
import calendar
import bson
from colorama import Fore, Style


def print_dbg(msg):
    print(f'{Fore.GREEN}DEBUG: {datetime.now()} {msg}{Style.RESET_ALL}')


def print_err(msg):
    print(f'{Fore.RED}ERROR: {datetime.now()} {msg}{Style.RESET_ALL}')


def print_inf(msg):
    print(msg)


def seconds_before_saturday_10am():
    return seconds_before_day_time(5, 10)


def seconds_before_wednesday_4pm():
    return seconds_before_day_time(2, 16)


def seconds_before_day_time(day, hour):
    """
    Monday = 0, ... Sunday = 6
    """
    now: datetime = datetime.now()
    hour_at_today = datetime(now.year, now.month, now.day, hour, 0, 0)
    delta_hour = hour_at_today - now
    delta_days = (day - now.weekday()) % 7
    ans = delta_days * 24 * 60 * 60 + delta_hour.total_seconds()
    return ans


def get_delay_in_seconds():
    """
    if today is Saturday AND it is after 10am
        wait for 30 seconds before retry
    else:
        wait for seconds until half way to Saturday 10am
    """
    today = datetime.today()
    weekday = today.weekday()
    current_hour = today.hour

    delay = seconds_before_saturday_10am() / 2  # TODO: choose this one during weekend
    # delay = seconds_before_wednesday_4pm() / 2  # TODO: choose this one during weekday
    print_dbg(f'seconds before next booking window = {delay}')

    min_delay = 30  # this will make sure delay is a positive number
    max_delay = 300  # this will make sure browser login does not expire
    delay = max(delay, min_delay)
    delay = min(delay, max_delay)
    return delay


def seconds_to_duration(seconds):
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    days, hours, minutes, seconds = int(days), int(hours), int(minutes), int(seconds)
    return f'{days} days {hours}:{str(minutes).zfill(2)}:{str(seconds).zfill(2)}'


def days_before_next(target_day):
    day_names = list(calendar.day_name)
    target_day_number = day_names.index(target_day)
    today = datetime.today().weekday()
    this_sunday = 6  # index of Sunday in calendar.day_name is always 6
    days_before_sunday = this_sunday - today
    # debug(f'There are {days_before_sunday} days before Sunday')
    days_before_target_day = target_day_number - today
    # TODO: enable the next two lines if we need to skip current week
    if days_before_target_day <= days_before_sunday:
        days_before_target_day += 7
    print_dbg(f'There are {days_before_target_day} days before next {target_day}')
    return days_before_target_day


def login():
    # launch browser
    browser = webdriver.Firefox()
    browser.implicitly_wait(0.5)

    logged_in = False
    retry_interval = 5 * 60  # seconds

    while not logged_in:
        try:
            # navigate to login page
            browser.get(zen_planner['login']['url'])
            title_text = zen_planner['login']['title']
            print_dbg(f'{title_text} in {browser.title}')
            assert title_text in browser.title  # make sure we are at the right log in page

            email_text_box = browser.find_element_by_id('idUsername')
            email_text_box.send_keys(zen_planner['login']['email'])
            password_text_box = browser.find_element_by_id('idPassword')
            password_bson = bson.BSON.encode({'A': zen_planner['login']['password']})
            password_text_box.send_keys(bson.BSON(password_bson).decode()['A'])
            submit_button = browser.find_element_by_xpath('/html/body/div[1]/table/tbody/tr/td[2]/fieldset['
                                                          '1]/div/form/input')
            submit_button.click()
            time.sleep(1)
            logged_in = True

        except Exception as e:
            print_err(f'Exception occurred while trying to log in: {e}. Retrying in {retry_interval} seconds')
            time.sleep(retry_interval)

    return browser


def get_slot_button_on_day(day, slot, browser):
    while True:
        for row_number in range(20):  # scan all possible calendar rows on the day
            try:  # an exception will occur if a row number does not exist in the calendar
                slot_button = browser.find_element_by_xpath(f'/html/body/div/table/'
                                                            f'tbody/tr/td[2]/table[2]/tbody/tr[{row_number}]/td[1]/div')
            except NoSuchElementException as e:  # we don't care if an row does not exist
                pass
            else:
                if slot_button.text == slot.upper():   # make sure it is the right row by matching the text
                    return slot_button
        print_dbg(f'{slot} on {day} is not open yet, keep trying until it shows up.')
        time.sleep(3)
        browser.refresh()


def book_single_user_single_slot_with_browser(user, day, slot, browser):
    success = False
    try:
        # navigate to calendar page
        browser.get(zen_planner['bookings']['url'])

        # forward all the way to the target date in calendar
        days_later = days_before_next(day)
        # keep clicking the next button ">" until we reach the target date
        for _ in range(days_later):
            next_day_button = browser.find_element_by_xpath('/html/body/div/table/tbody/tr/td[2]/table[1]/tbody/tr/td['
                                                            '1]/div/a[3]/i')
            next_day_button.click()

        # click on the time slot
        slot_button = get_slot_button_on_day(day, slot, browser)
        slot_button.click()

        # select family member
        family_member_select_box = Select(browser.find_element_by_id('familyMembers'))
        family_member_select_box.select_by_visible_text(user)

        time.sleep(2)

        # book time slot for selected family member
        try:
            reserve_button = browser.find_element_by_id('reserve_1')
            reserve_button.click()
        except NoSuchElementException as e:
            print_dbg(f'Reserve button is not available.')

        # done, we should be able to see the cancel option now
        try:
            action = 'book'  # default behavior is to reserve
            if zen_planner['bookings']['action'] == 'cancel':
                action = 'cancel'

            cancel_button = browser.find_element_by_xpath('//a[contains(@id, "cancel_")]')  # *[@id="cancel_2"]

            if zen_planner['bookings']['action'] == 'cancel':
                cancel_button.click()

            print_inf(f'Successfully {action}ed for {user} on {day} at {slot}')
            success = True
        except NoSuchElementException as e:
            print_dbg(f'Cancel button is not available.')
            print_err(f'Failed to {action} for {user} on {day} at {slot}')

    except Exception as e:
        print_dbg(f'Unexpected exception occurred: {str(e).rstrip()}')

    return success


def book_court(booked, browser):
    # for each slot, for each person, try booking
    all_success = True
    for day in zen_planner['bookings']['time_slots'].keys():
        slots = zen_planner['bookings']['time_slots'][day]
        for slot in slots:
            for username in zen_planner['bookings']['users'].keys():
                booking = [username, day, slot]
                if booking not in booked:
                    print_inf(f'\nTrying to book for {username} on {day} at {slot}')
                    success = book_single_user_single_slot_with_browser(username, day, slot, browser)
                    all_success = success and all_success
                    if success:
                        booked.append(booking)
    return all_success


def book_for_all():
    booked = []

    # login
    browser = login()

    success = False
    while not success:
        success = book_court(booked, browser)
        print_inf(f'\nbooked = {booked}')
        if success:
            break
        delay = get_delay_in_seconds()
        print_inf(f'\n==================================================\n'
                  f'waiting to try again in {seconds_to_duration(delay)}\n')
        time.sleep(delay)

    # close browser
    browser.quit()


def main():
    book_for_all()


if __name__ == '__main__':
    main()
