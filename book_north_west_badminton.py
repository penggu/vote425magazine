from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time
from datetime import datetime
import random
from nwb_data import zen_planner
import calendar
import json
from colorama import Fore, Back, Style


def debug(msg):
    print(f'{Fore.GREEN}DEBUG: {datetime.now()} {msg}{Style.RESET_ALL}')


def info(msg):
    print(msg)


def days_before_next(target_day):
    day_names = list(calendar.day_name)
    target_day_number = day_names.index(target_day)
    today = datetime.today().weekday()
    this_sunday = 6  # index of Sunday in calendar.day_name is always 6
    days_before_sunday = this_sunday - today
    debug(f'There are {days_before_sunday} days until Sunday')
    days_before_target_day = target_day_number - today
    if days_before_target_day <= days_before_sunday:
        days_before_target_day += 7
    debug(f'There are {days_before_target_day} days before next {target_day}')
    return days_before_target_day


def book_single_user_single_slot(user, day, slot):
    booked = False

    # launch browser
    browser = webdriver.Firefox()
    browser.implicitly_wait(0.5)

    try:
        # navigate to login page
        browser.get(zen_planner['login']['url'])
        title_text = zen_planner['login']['title']
        debug(f'{title_text} in {browser.title}')
        assert title_text in browser.title

        # login
        email_text_box = browser.find_element_by_id('idUsername')
        email_text_box.send_keys(zen_planner['login']['email'])

        password_text_box = browser.find_element_by_id('idPassword')
        password_text_box.send_keys(zen_planner['login']['password'])

        submit_button = browser.find_element_by_xpath('/html/body/div[1]/table/tbody/tr/td[2]/fieldset['
                                                      '1]/div/form/input')
        submit_button.click()

        # navigate to calendar page
        browser.get(zen_planner['bookings']['url'])

        # forward all the way to the target date in calendar
        days_later = days_before_next(day)
        for _ in range(days_later):
            next_day_button = browser.find_element_by_xpath('/html/body/div/table/tbody/tr/td[2]/table[1]/tbody/tr/td['
                                                            '1]/div/a[3]/i')
            next_day_button.click()

        # click on the time slot
        slot_button = browser.find_element_by_xpath(f'/html/body/div/table/tbody/tr/td[2]/table[2]/tbody/tr['
                                                    f'{zen_planner["bookings"]["slot_numbers"][slot]}]/td[1]/div')
        slot_button.click()

        # select family member
        family_member_select_box = Select(browser.find_element_by_id('familyMembers'))
        family_member_select_box.select_by_visible_text(user)

        # book time slot for selected family member
        try:
            reserve_button = browser.find_element_by_id('reserve_1')
            reserve_button.click()
        except Exception as e:
            debug(f'Failed to locate Reserve button. {e}')

        # done, we should be able to see the cancel option now

        cancel_button = browser.find_element_by_xpath('//a[contains(@id, "cancel_")]')  # *[@id="cancel_2"]
        # cancel_button.click()  # TODO: delete this line
        booked = True
        info(f'Successfully booked for {user} on {day} at {slot}')

    except Exception as e:
        info(f'failed to book for {user} on {day} at {slot}')
        debug(f'Exception occurred: {e}')

    browser.quit()
    return booked


def book_court(booked=[]):
    all_success = True
    for day in zen_planner['bookings']['time_slots'].keys():
        slots = zen_planner['bookings']['time_slots'][day]
        for slot in slots:
            for username in zen_planner['bookings']['users'].keys():
                booking = [username, day, slot]
                if booking not in booked:
                    info(f'Booking for {username} on {day} at {slot}')
                    success = book_single_user_single_slot(username, day, slot)
                    all_success = success and all_success
                    if success:
                        booked.append(booking)
    return all_success


def seconds_before_saturday_10am():
    return seconds_before_day_time(5, 10)


def seconds_before_day_time(day, hour):
    """
    Monday = 0, ... Sunday = 6
    """
    now: datetime = datetime.now()
    today_10am = datetime(now.year, now.month, now.day, hour, 0, 0)
    delta = today_10am - now
    debug(f'now is {now}, {seconds_to_duration(delta.total_seconds())} before today at {hour}:00:00')
    days = (day - now.weekday()) % 7
    ans = days * 24 * 60 * 60 + delta.total_seconds()
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
    if weekday == 5 and current_hour >= 10:
        delay = 30
    else:
        delay = seconds_before_saturday_10am()
        debug(f'seconds_before_saturday_10am = {delay}')
        delay /= 2
    return max(delay, 30)


def seconds_to_duration(seconds):
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    days, hours, minutes, seconds = int(days), int(hours), int(minutes), int(seconds)
    return f'{days} days {hours}:{str(minutes).zfill(2)}:{str(seconds).zfill(2)}'


def main():
    with open('booked.json', 'r') as log_file:
        booked = json.load(log_file)
        debug(f'01 booked = {booked}')

    success = book_court(booked)
    with open('booked.json', 'w') as log_file:
        debug(f'02 booked = {booked}')
        json.dump(booked, log_file)

    while not success:
        delay = get_delay_in_seconds()
        debug(f'waiting to try again in {seconds_to_duration(delay)}\n\n\n')
        time.sleep(delay)
        success = book_court(booked)
        with open('booked.json', 'w') as log_file:
            debug(f'03 booked = {booked}')
            json.dump(booked, log_file)

    return


if __name__ == '__main__':
    main()
