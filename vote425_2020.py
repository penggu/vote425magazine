from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import datetime
import random


def a_to_z():
    return 'abcdefghijklmnopqrstuvwxyz'


def random_letter():
    return random.choice(a_to_z())


def get_user_names():
    return [
        'mithrandirland',
        'omitbrails',
        'turdiformfibber',
        'vluckerboast',
        'intensetatham',
        'prickletwice',
        'damagingleg',
        'convertingsource',
        'equatorialwilderness',
        'seizegoud',
        'ascensionarcher',
        'occiputbleet',
        'hardlydull',
        'gildjoker',
        'uriahproduct',
        'stizzardsway',
        'glamoroustite',
        'unseasonedbaseball',
        'phalangeludibrious',
        'sockdolagerwatchful',
        'strengthenhole',
        'zephyrhuorn',
        'huggerarmor',
        'subduedsalesman',
        'financeidentity',
        'doxybox',
        'standardvex',
        'sunflowerlute',
        'barefacedshoulders',
        'tweezerstap',
        'fangmulticack',
        'holdmarinated',
        'necktiedantic',
        'dilberdacket',
        'vizgigromp',
        'secondhandkiwifruit',
        'titchdisclose',
        'sliderskewtimersome',
        'predicthighlight',
        'cutespill',
        'iraqifrequently',
        'strocolatemeerkat',
        'sheldrakepattern',
        'sourborkie',
        'newymacho',
        'equalflow',
        'intrigueposition',
        'puscleever',
        'juliusequable',
        'seanutsunruly',
        'challengesore',
        'allianzgoring',
        'acrobatjackyard',
        'mayorshass',
        'thumbbeacon',
        'nurseryafter',
        'prawnbuzz',
        'hibernaclecluckets',
        'bakehurry',
        'outcomeoverlook',
        'lovelywhair',
        'ensignoffice',
        'frieseuphoric',
        'glowstonepointless',
        'thrarmshundery',
        'gristycracked',
        'cirithmodest',
        'cultivatedrefuse',
        'jaialaibob',
        'convertoblivate',
        'rimbingbull',
        'cowdelirious',
        'pepperonilustrous',
        'wiltedremove',
        'stutterkench',
        'gruntsimple',
        'perseverewestwood',
        'kaputunhealthy',
        'warmpickaxe',
        'cakeddefeated',
        'sluncturejodge',
        'cofflebacon',
        'flavorsandals',
        'chagflick',
        'projectkind',
        'dressminhiriath',
        'snictoreriador',
        'affairmanette',
        'labourerranchers',
        'hiddenwhiffle',
        'constructreact',
        'homeworkpopplestooan',
        'crabvhs',
        'omeletteheel',
        'bustardbelong',
        'neckedmewling',
        'remorsefulcustomer',
        'luciusbonney',
        'flintwinchflawless',
        'bartholomewwhiteness',
        'deadbeatajar',
        'cratchingmountains',
        'informpeb',
        'customerdiscrete',
        'tithedwell',
        'processstammer',
        'ligamentaguamenti',
        'emnetmagazine',
        'argumentrasp',
        'sardonicshield',
        'dirstymessage',
        'headedmar',
        'pardigglongford',
        'statementnest',
        'pomachtoucan',
        'dunedainversatile',
        'rascalchutton',
        'satisfyingexalted',
        'goiledrepublic',
        'accidentill',
        'agonizingcolorless',
        'couplekissquisby',
        'repulsivemonger',
        'haredalebars',
        'impatiencecheeryble',
        'competitorthine',
        'barelyjoshua',
        'spottletoesunflower',
        'meaglesgodzend',
        'croustyjint',
        'folkswimmer',
        'puddlingrower',
        'mortismetacarpus',
        'suckerdolge',
        'pollutionvigorous',
        'throwporch',
        'burnbilbo',
        'thankfullooring',
        'daggermemory',
        'choardplups',
        'glaintrace',
        'smokeperturbed',
        'flangecontain',
        'bicyclistmistake',
        'rohancricky',
        'nunchunboil',
        'gigglepeppery',
        'tulkinghornchicolate',
        'ningersdive',
        'gloxingsparkins',
        'phraseforget',
        'ledbreezy',
        'stryverbet',
        'vinegarybonus',
        'pigwidgeonboing',
        'stogodecade',
        'kagicalwopping',
        'redwingassignment',
        'artificialregularly',
        'urbancelery',
        'projectorsternum',
        'unhealthycheer',
        'anguishedsake',
        'ruffiandependent',
        'hagridfluther',
        'themselvesnaughty',
        'whimsicalwicked',
        'cabindoxy',
        'savingsmodified',
        'difficultcails',
        'wastefulturducken',
        'yawlscandalous',
        'junnycompany',
        'depictsyrian',
        'citrusyincantato',
        'pantyboiled',
        'impressiontrall',
        'smashingmeeting',
        'cowardiceborder',
        'bubbishpeplow',
        'properforn',
        'hootenannybong',
        'linkinwaterintroduce',
        'erstwhilecastic',
        'spelltoofing',
        'militarymoo',
        'clunkblame',
        'liarhelves',
        'posecrall',
        'improverisotto',
        'groolwhimper',
        'ledgerfolk',
        'papayamissile',
        'threatenedslace',
        'spritsaillow',
        'exitcruit',
        'wearcroor',
        'cobblerslackumtrance',
        'activistperfect',
        'furtivelacking',
    ]


def get_random_user():
    return random.choice(get_user_names()) + random_letter() + random_letter()


def get_credential():
    cred = {}
    user = get_random_user()
    cred['Username'] = user.title()
    cred['Password'] = 'passFor' + user.title()
    cred['Email'] = user + '@gmail.com'
    return cred


def random_sleep():
    r = random.randint(3, 5)
    time.sleep(r)


def browse():
    browser = webdriver.Firefox()
    try:
        # 1. go to website
        url = 'https://vote.425magazine.com/'
        browser.get(url)
        title_text = 'Vote for the best of 425'
        assert title_text in browser.title

        # 2. Register for an account
        registerButton = browser.find_element_by_xpath(
            '//html/body/main/div/div[1]/div/div/section[5]/div/div/div/div/div/section/div/div/div['
            '2]/div/div/div/div/div/a')
        registerButton.click()

        cred = get_credential()
        textbox_user = browser.find_element_by_xpath(
            '//html/body/main/div/div[1]/div/div/section[3]/div/div/div/div/div/div/div/div/div/form/div[1]/div['
            '1]/input')
        textbox_email = browser.find_element_by_xpath(
            '//html/body/main/div/div[1]/div/div/section[3]/div/div/div/div/div/div/div/div/div/form/div[1]/div['
            '2]/input')
        textbox_pass = browser.find_element_by_xpath(
            '//html/body/main/div/div[1]/div/div/section[3]/div/div/div/div/div/div/div/div/div/form/div[1]/div['
            '3]/div/div[1]/input')
        textbox_pass2 = browser.find_element_by_xpath(
            '//html/body/main/div/div[1]/div/div/section[3]/div/div/div/div/div/div/div/div/div/form/div[1]/div['
            '3]/div/div[2]/input')
        button_submit = browser.find_element_by_xpath(
            '//html/body/main/div/div[1]/div/div/section[3]/div/div/div/div/div/div/div/div/div/form/div[2]/button')
        textbox_user.send_keys(cred['Username'])
        textbox_email.send_keys(cred['Email'])
        textbox_pass.send_keys(cred['Password'])
        textbox_pass2.send_keys(cred['Password'])
        browser.execute_script('arguments[0].scrollIntoView();', button_submit)  # 拖动到可见的元素去
        button_submit.click()

        # 3. Login
        title_text = 'Login – Best of 425'
        assert title_text in browser.title  # make sure we are on the login page
        textbox_email = browser.find_element_by_xpath(
            '//html/body/main/div/div[1]/div/div/section[3]/div/div/div/div/div/div/div/div/div/form/div[1]/div['
            '1]/input')
        textbox_pass = browser.find_element_by_xpath(
            '//html/body/main/div/div[1]/div/div/section[3]/div/div/div/div/div/div/div/div/div/form/div[1]/div['
            '2]/input')
        button_submit = browser.find_element_by_xpath(
            '//html/body/main/div/div[1]/div/div/section[3]/div/div/div/div/div/div/div/div/div/form/div[2]/button')
        textbox_email.send_keys(cred['Email'])
        textbox_pass.send_keys(cred['Password'])
        button_submit.click()

        # 4. Go to the vote page
        url = 'https://vote.425magazine.com/health-wellness/'
        browser.get(url)
        title_text = 'Health & Wellness – Best of 425'
        assert title_text in browser.title

        # 5. Cast the vote
        textbox_best_acu = browser.find_element_by_xpath(
            '//html/body/main/div/div[1]/div/div/section[5]/div/div/div/div/div/div/div/div/div/form/div[1]/div[22]/input')
        button_submit = browser.find_element_by_xpath(
            '//html/body/main/div/div[1]/div/div/section[5]/div/div/div/div/div/div/div/div/div/form/div[2]/button')
        textbox_best_acu.send_keys(random.choice([
            'Yanling Xiao, Swiss Acupuncture'
        ]))

        browser.execute_script('arguments[0].scrollIntoView();', button_submit)  # 拖动到可见的元素去
        random_sleep()
        button_submit.click()

    except Exception as e:
        print(e)

    browser.quit()


def main():
    total_votes = 1
    for i in range(total_votes):
        now = datetime.datetime.now()
        r = random.randint(15, 300)
        print(f'\t\t\t\t\t{now}\tvoting: {i + 1} out of {total_votes}, sleep for {r} seconds')
        browse()
        time.sleep(r)


if __name__ == '__main__':
    main()
