#!/usr/local/bin/python3
#coding=utf-8
import time
import datetime
import urllib2, requests # http request and response
import codecs # read/write Unicode files
from bs4 import BeautifulSoup as Soup # parse html elements
import selenium # browser
from selenium import webdriver # Supports Firefox, Chrome, PhantomJS, etc
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import subprocess # Handles Unicode command, which os.system() can't do
import os # File path, etc
import threading # Multi-threading support
import random
import inspect # for retrieve current function name
import io
import json
from multiprocessing.dummy import Pool as ThreadPool

work_queue = []
download_in_progress = 0
pending_download = True

def global_const():
    return {
        'LOGIN': {
            'USERNAME': 'baraici',
            'EMAIL': 'baraici@yahoo.com',
            'PASSWORD': '123456'
        },
        'DOWNLOAD_DIR': u'/home/USER/Downloads',
        'DOWNLOAD_THREAD': 8,
        'PROGRESS_REPORT_INTERVAL': 20,
        'DOWNLOAD_TIME_OUT': 60 * 15,
        'SOCKET_TIMEOUT': 60,
        'PATH_NAME_SEPARATOR': '/'
    }

def printd(msg, level='DEBUG'):
    allowed = ['CRIT', 'ERROR', 'WARN', 'INFO', 'DEBUG', 'TRACE']
    # allowed = ['CRIT', 'ERROR', 'WARN', 'INFO']
    if level in allowed:
        mapping = {
            'CRIT': u'严重',
            'ERROR': u'错误',
            'WARN': u'警告',
            'INFO': u'信息',
            'DEBUG': u'调试',
            'TRACE': u'追踪'
        }
        print(u'[{0}][{1}]: {2}'.format(mapping[level], datetime.datetime.now(), msg))

def printi(msg):
    printd(msg, 'INFO')

def trace_enter(msg='', level='TRACE'):
    parent_funcname = inspect.getouterframes(inspect.currentframe())[1][3]
    printd(u'{0}() Entering... {1}'.format(parent_funcname, msg), level)
def trace_exit(msg='', level='TRACE'):
    parent_funcname = inspect.getouterframes(inspect.currentframe())[1][3]
    printd(u'{0}() Exiting... {1}'.format(parent_funcname, msg), level)
def trace_abort(msg='', level='TRACE'):
    parent_funcname = inspect.getouterframes(inspect.currentframe())[1][3]
    printd(u'{0}() Aborting... {1}'.format(parent_funcname, msg), level)

def unicode_example():
    tutorial = u'''
    >>> u = u'aBC中'
    >>> v = 'aBC中'
    >>> u
    u'aBC\\u4e2d'
    >>> v
    'aBC\\xe4\\xb8\\xad'
    >>> u == v
    False
    >>> u.encode('utf-8') == v
    True
    >>> v.decode('utf-8') == u
    True
    '''
    printd(u'{0}'.format(tutorial), 'INFO')

def get_url_content(url):
    response = requests.get(url, stream=True)
    html = response.content
    return html

def get_url_content_2(url):
    response = urllib2.urlopen(url)
    html = response.read()
    return html

def tag_has_basic_attr(tag):
    return (
        tag.name == 'a' and
        tag.has_attr('href') and
        tag.has_attr('class') and
        tag['href'].startswith('http://vdisk.weibo.com/s/') and
        (tag.has_attr('id') or tag.has_attr('title')) and
        ('vd_icon32_v2' in tag['class'] or 'short_name' in tag['class'])
    )

def tag_has_desired_attr(tag):
    return tag_has_basic_attr(tag)

def tag_has_desired_id(tag):
    return tag_has_basic_attr(tag) and tag.has_attr('id')

def tag_has_desired_title(tag):
    return tag_has_basic_attr(tag) and tag.has_attr('title')

def is_desired_folder_with_id(tag):
    return tag_has_desired_id(tag) and ('vd_folder' in tag['class'])

def is_desired_file_with_id(tag):
    return tag_has_desired_id(tag) and not is_desired_folder_with_id(tag)

def doc_id_from_url(url):
    ret = ''
    if url.startswith('http://vdisk.weibo.com/s/'):
        ret = url[25:38]
    return ret

def make_os_path(raw_path_name):
    s = raw_path_name.split(global_const()['PATH_NAME_SEPARATOR'])
    if len(s) < 2:
        raise ValueError(u'Invalid path: {0}'.format(raw_path_name))
    s[0] = global_const()['PATH_NAME_SEPARATOR']
    os_path = os.path.join(*s)
    return os_path

def chrome_download(url, default_file_path, target_file_path):
    global download_in_progress
    download_in_progress += 1
    my_thread_id = download_in_progress
    trace_enter()
    printd(u'Default download directory: {0}'.format(global_const()['DOWNLOAD_DIR']), 'DEBUG')
    chromedriver = '/home/USER/bin/chromedriver'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('prefs', {'download.default_directory': global_const()['DOWNLOAD_DIR'] })
    chrome_options.add_experimental_option( "prefs", {'profile.default_content_settings.images': 2}) # Disable image
    # chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy))
    browser = webdriver.Chrome(chromedriver, chrome_options = chrome_options)
    browser.implicitly_wait(global_const()['SOCKET_TIMEOUT']) # seconds, after that we will give up waiting for element
    printd(u'Starting new download thread [{0}] {1} {2}'.format(my_thread_id, default_file_path, target_file_path), 'INFO')
    try:
        printd(u'#1. Retrieve URL', 'DEBUG')
        browser.get(url)
        printd(u'#2. Click the "下载" button', 'DEBUG')
        browser.find_element_by_id("download_small_btn").click()
        printd(u'#3. Fill in loginForm', 'DEBUG')
        printd(u'#3.1 Click the "马上登录" button', 'DEBUG')
        browser.find_element_by_xpath("/html/body/div[7]/div/div/div/div[2]/div/a[1]").click()
        printd(u'#3.2 Click the "账号登录" button', 'DEBUG')
        browser.find_element_by_link_text(u'账号登录').click()
        printd(u'#3.3 Fill in username', 'DEBUG')
        username = browser.find_element_by_name('username')
        password = browser.find_element_by_name('password')
        username.send_keys(global_const()['LOGIN']['USERNAME'])
        password.send_keys(global_const()['LOGIN']['PASSWORD'])
        printd(u'#3.4 Click login button', 'DEBUG')
        browser.find_element_by_class_name("W_btn_a").click()
        # printd(u'#4. Click the "下载" button again', 'DEBUG')
        # printd(u'#4.1 Reload URL', 'DEBUG')
        # browser.get(url)
        # printd(u'#4.2 Click the "下载" button again', 'DEBUG')
        # browser.find_element_by_id("download_small_btn").click()
    except (selenium.common.exceptions.NoSuchElementException,
        selenium.common.exceptions.WebDriverException) as e:
        printd(u'#9.1 {0}'.format(e), 'ERROR')
    try:
        printd(u'#5 Wait for download to complete', 'DEBUG')
        # printd(u'#5.1 Open a new tab', 'DEBUG')
        # body = browser.find_element_by_tag_name("body")
        # body.send_keys(Keys.CONTROL + 't')
        # printd(u'#5.2 Switch to the new tab', 'DEBUG')
        # for handle in browser.window_handles:
        #     browser.switch_to.window(handle)
        printd(u'#5.3 load "chrome://download/" page', 'DEBUG')
        browser.get("chrome://downloads/")
        printd(u'#5.4 Wait for the sign of download complete', 'DEBUG')
        start = time.time()
        elapsed = time.time() - start
        while not os.path.exists(default_file_path) and elapsed < global_const()['DOWNLOAD_TIME_OUT'] :
            printd(u'File downloading. {0} {1} seconds elasped'.format(default_file_path, int(elapsed)), 'DEBUG')
            time.sleep(global_const()['PROGRESS_REPORT_INTERVAL'])
            elapsed = time.time() - start
        # browser.get("chrome://downloads/")
        # browser.find_element_by_id("show");
        # browser.close()
        #browser.switch_to.window(browser.window_handles[0])
    except (selenium.common.exceptions.NoSuchElementException,
        selenium.common.exceptions.WebDriverException) as e:
        printd(u'#9.2 {0}'.format(e), 'ERROR')
    printd(u'#10 Close all tabs', 'DEBUG')
    for handle in browser.window_handles:
        browser.switch_to.window(handle)
        browser.close()
    printd(u'Finished download thread [{0}] {1} {2}'.format(my_thread_id, default_file_path, target_file_path), 'INFO')
    download_in_progress -= 1
    move_file(default_file_path, target_file_path)
    trace_exit()

def move_file(source, target):
    if os.path.exists(source) and not os.path.exists(target):
        printd(u'Executing "mv {0} {1}"'.format(source, target), 'INFO')
        cmd = u'mv {0} {1}'.format(source, target)
        subprocess.call(['mv', source, target])

def make_dir(dir_name):
    if not os.path.exists(make_os_path(dir_name)):
        os.makedirs(make_os_path(dir_name))

def create_utf8_file(fname, unicode_content):
    # with codecs.open(fname, "w", "utf-8-sig") as handle:
    #    handle.write(unicode_content)
    with open(fname, "w") as handle:
        handle.write(unicode_content)

def read_utf8_file(fname):
    with codecs.open(fname, "r", "utf-8-sig") as handle:
        return handle.read()

def retrieve_url(web_root, doc_id, dir_name, use_cache=True):
    html_doc = ''
    trace_enter()
    make_dir(dir_name)
    cache_file = make_os_path(u'{0}{1}{2}'.format(dir_name, global_const()['PATH_NAME_SEPARATOR'], doc_id))
    try:
        if not use_cache or not os.path.isfile(cache_file):
            url = web_root + doc_id
            html_doc = get_url_content_2(url)
            create_utf8_file(cache_file, html_doc)
        else:
            printd(u'Reading from cache file: {0}'.format(cache_file), 'DEBUG')
            html_doc = read_utf8_file(cache_file)
    except IOError as e:
        printd(u'URL = {0}, cache_file = {1}: {2}'.format(url, cache_file, e), 'ERROR')
        trace_abort('', 'ERROR')
        return html_doc

    #printd(u'html_doc:{0}'.format(html_doc), 'DEBUG')
    trace_exit()
    return html_doc

def download_file_2(web_root, doc_id, save_dir, fname):
    trace_enter()
    global download_in_progress
    default_file_path = make_os_path(u'{0}{1}{2}'.format(global_const()['DOWNLOAD_DIR'], global_const()['PATH_NAME_SEPARATOR'], fname))
    target_file_path = make_os_path(u'{0}{1}{2}'.format(save_dir, global_const()['PATH_NAME_SEPARATOR'],fname))
    if os.path.exists(target_file_path):
        trace_abort(u'Target file exists: {0}'.format(target_file_path), 'INFO')
        return
    if os.path.exists(default_file_path):
        trace_abort(u'File already downloaded. Executing "mv {0} {1}"'.format(default_file_path, target_file_path), 'INFO')
        move_file(default_file_path, target_file_path)
        return
    url = web_root + doc_id
    # chrome_download(url, default_file_path, target_file_path)
    while download_in_progress >= global_const()['DOWNLOAD_THREAD']:
        time.sleep(random.randint(1, global_const()['PROGRESS_REPORT_INTERVAL'])) # waiting for other thread to finish
    thread = threading.Thread(target=chrome_download, args=(url, default_file_path, target_file_path,))
    # thread.setDaemon(True)
    time.sleep(random.randint(1, global_const()['PROGRESS_REPORT_INTERVAL']))
    thread.start()
    trace_exit()

def download_file(web_root, doc_id, save_dir, file_name):
    file_path = u'{0}{1}{2}'.format(save_dir, global_const()['PATH_NAME_SEPARATOR'], file_name)
    printd(u'Downloading file {0} as {1}'.format(doc_id, make_os_path(file_path)), 'DEBUG')
    download_file_2(web_root, doc_id, save_dir, file_name) # Note: asynchronous
    printd(u'Download launched: {0}'.format(file_path), 'DEBUG')

def add_to_work_queue(web_root, doc_id, save_dir, file_name):
    # Instead of downloading the file, we simply put it in our work queue
    global work_queue
    work_queue.append({
        'web_root': web_root,
        'doc_id': doc_id,
        'save_dir': save_dir,
        'file_name': file_name
    })


def print_item(item):
    printd(u'ID: {0}, IsFolder: {1}, Url: {2}, Title: {3}'.format(
        item['id'], item['folder'], item['url'], item['title']), 'INFO')

def build_download_list(html_doc):
    soup = Soup(html_doc, 'lxml')
    my_list = {}
    for tag in soup.find_all(tag_has_desired_attr):
        if tag_has_desired_id(tag):
            my_id = tag['id']
            is_folder = is_desired_folder_with_id(tag)
            if my_id not in my_list:
                item = {
                    'id': my_id,
                    'url': tag['href'],
                    'folder': is_folder,
                    'title': None
                }
                my_list[my_id] = item
            else:
                my_list[my_id]['folder'] = is_folder
        elif tag_has_desired_title(tag):
            my_url = tag['href']
            my_id = doc_id_from_url(my_url)
            my_title = tag['title']
            if my_id not in my_list:
                item = {
                    'id': my_id,
                    'url': my_url,
                    'folder': None,
                    'title': my_title
                }
                my_list[my_id] = item
            else:
                my_list[my_id]['title'] = my_title
        #print_item(my_list[my_id])
    return my_list

def download_folder(web_root, doc_id, save_dir):
    trace_enter()
    url = web_root + doc_id
    os_path = make_os_path(save_dir)
    printd(u'Downloading folder {0} as {1}'.format(doc_id, os_path), 'DEBUG')
    printd(u'#1 Make sure folder exist: {0}'.format(os_path), 'DEBUG')
    make_dir(save_dir)
    printd(u'#2 Retrieve URL html document: {0}/{1}'.format(web_root, doc_id), 'DEBUG')
    html_doc = retrieve_url(web_root, doc_id, save_dir)
    if not html_doc:
        trace_abort(u'Failed to retrieve URL: {0}'.format(url), 'ERROR')
        return
    to_download = build_download_list(html_doc)
    for k in to_download.keys():
        item = to_download[k]
        if item['folder']:
            download_folder(web_root, item['id'], u'{0}{1}{2}'.format(save_dir, global_const()['PATH_NAME_SEPARATOR'], item['title']))
        else: # download file, if not already exists
            file_name = u'{0}'.format(item['title'])
            # Two choices, both are OK:
            # Choice #1: Start downloading directly (async)
            # download_file(web_root, item['id'], save_dir, file_name)
            # Choice #2: Add to work queue and download later with ThreadPool
            add_to_work_queue(web_root, item['id'], save_dir, file_name)
    trace_exit()

def print_work_item(item):
    json_str = json.dumps(item, ensure_ascii=False)
    printd(json_str, 'INFO')

def is_download_filtered(save_dir, file_name):
    try:
        default_file_path = make_os_path(u'{0}{1}{2}'.format(global_const()['DOWNLOAD_DIR'], global_const()['PATH_NAME_SEPARATOR'], file_name))
        target_file_path = make_os_path(u'{0}{1}{2}'.format(save_dir, global_const()['PATH_NAME_SEPARATOR'],file_name))
        if os.path.exists(target_file_path):
            printd(u'Target file exists: {0}'.format(target_file_path), 'INFO')
            return True
        if os.path.exists(default_file_path):
            printd(u'File already downloaded. Executing "mv {0} {1}"'.format(default_file_path, target_file_path), 'INFO')
            move_file(default_file_path, target_file_path)
            return True
    except e:
        printd(u'Failed to determine if file should be filtered. Try downloading anyway: {0}. {1}'.format(target_file_path, e), 'WARN')
        pass
    return False

def download_file_3(web_root, doc_id, save_dir, file_name):
    trace_enter()
    global pending_download
    if not is_download_filtered(save_dir, file_name):
        pending_download = True
        url = web_root + doc_id
        default_file_path = make_os_path(u'{0}{1}{2}'.format(global_const()['DOWNLOAD_DIR'], global_const()['PATH_NAME_SEPARATOR'], file_name))
        target_file_path = make_os_path(u'{0}{1}{2}'.format(save_dir, global_const()['PATH_NAME_SEPARATOR'],file_name))
        printd(u'Downloading {0} ...'.format(target_file_path), 'INFO')
        time.sleep(random.randint(1, global_const()['PROGRESS_REPORT_INTERVAL']))
        chrome_download(url, default_file_path, target_file_path)
    trace_exit()

def download_one_file(work_item):
    #print_work_item(work_item)
    i = work_item
    web_root, doc_id, save_dir, file_name = i['web_root'], i['doc_id'], i['save_dir'], i['file_name']
    download_file_3(web_root, doc_id, save_dir, file_name)

def populate_work_queue():
    global work_queue
    save_dir = u'/media/USER/D500GB1/ebook'
    web_root = 'http://vdisk.weibo.com/s/'
    # root_doc_id = 'Cb1ItMmDIM8dQ'
    # root_doc_id = 'FaZ_rZnf-TD5Q'
    root_doc_id = 'C3AWjT1HpWs1K'
    work_queue_file = root_doc_id + '.wkq'

    # Build work queue and save to file
    if not os.path.exists(work_queue_file):
        printd(u'Work queue file: {0} not found'.format(work_queue_file), 'INFO')
        download_folder(web_root, root_doc_id, save_dir)
        with io.open(work_queue_file, 'w') as json_file:
            data = json.dumps(work_queue, ensure_ascii=False)
            # unicode(data) auto-decodes data to unicode if str
            json_file.write(unicode(data))

    # Load work queue from disk file
    with io.open(work_queue_file, 'r') as json_file:
        data = json_file.read()
        work_queue = json.loads(data)

def download_in_parallel():
    global work_queue
    global pending_download
    while pending_download: # Retry on download failures
        pending_download = False
        # Make the Pool of workers
        pool = ThreadPool(global_const()['DOWNLOAD_THREAD'])
        # Download one file in its own thread and return the results
        results = pool.map(download_one_file, work_queue)
        #close the pool and wait for the work to finish
        pool.close()
        pool.join()

def main():
    populate_work_queue()
    download_in_parallel()

if __name__ == '__main__':
    main()

