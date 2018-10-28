from selenium import webdriver
import logging
from config import get_general, get_batch
import platform
import os
import time
import argparse
from xvfbwrapper import Xvfb
from random import choice
import pymongo
from datetime import datetime, timedelta


general_config = get_general()
DEBUG_MODE = general_config['debug']
DRIVER_DELAY=3

if DEBUG_MODE:
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

def get_driver(proxy, lang, device_name=None):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server={0}'.format(proxy))
    chrome_options.add_argument('--lang={0}'.format(lang))

    # mobile emulate
    if device_name:
        mobile_emulation = {
            'deviceName': device_name
        }
        chrome_options.add_experimental_option('mobileEmulation', mobile_emulation)

    driver = webdriver.Chrome(options=chrome_options)

    if DEBUG_MODE:
        logging.info('Driver created with: ({0}, {1}, {2})'.format(proxy, lang, device_name))

    return driver

def make_screenshot(driver):
    filename = '{0}/screenshot/_{1}.png'.format(os.path.dirname(os.path.realpath(__file__)), int(time.time()))
    driver.save_screenshot(filename)

    if DEBUG_MODE:
        logging.info('Save screenshot: {0}'.format(filename))

def mongo_db():
    client = pymongo.MongoClient('mongodb://selenim:selenium@mongodb:27017/')
    return client['selenium']

def track_click(db, batch_name, link):
    db.clicks.insert_one({
        'batch_name': batch_name,
        'link': link,
        'created_at': datetime.now()
    })

    if DEBUG_MODE:
        logging.info('Tracked click: {0}|{1}'.format(batch_name, link))

def is_capped(db, batch_name, mc_interval, mc_count):
    cursor = db.clicks.find({
        'created_at': {
            '$gte': datetime.now() - timedelta(hours=mc_interval),
            '$lt': datetime.now(),
        },
        'batch_name': batch_name
    })

    return cursor.count() > mc_count

def main():
    parser = argparse.ArgumentParser(description='Selenium proxy - O_o')
    parser.add_argument('--batch', nargs=1, required=True, help='name of batch to start')
    parser.add_argument('--vdisplay', nargs='?', help='use virtual display')
    args = parser.parse_args()

    if args.vdisplay:
        vdisplay = Xvfb(width=1280, height=740, colordepth=16)
        vdisplay.start()

    batch_name = args.batch[0]
    settings = get_batch(batch_name)

    if settings == None:
        print('Invalid name batch')
        return

    db = mongo_db()

    i = 0
    while (True):
        i = i + 1

        if DEBUG_MODE:
            logging.info('Iterration: {0}'.format(i))
            i += 1

        lang = settings['lang']
        proxies = settings['proxy']['default'][lang]

        mc_interval = settings['maxclick']['interval_h']
        mc_count = settings['maxclick']['count']

        for proxy in proxies:
            device_name = None

            if settings['device']['type'] == 'mobile':
                device_name = choice(settings['device']['name'])

            driver = get_driver(proxy, lang, device_name)

            links = settings['links']
            links_ban = links['ban'] if 'ban' in links else []
            links_pop = links['pop'] if 'pop' in links else []

            for link in links_ban:
                if is_capped(db, batch_name, mc_interval, mc_count):
                    continue

                _link = link
                driver.get(link)

                link = driver.find_element_by_xpath('//a/img')
                link.click()

                track_click(db, batch_name, _link)

                if DEBUG_MODE:
                    make_screenshot(driver)

            for link in links_pop:
                driver.get(link)

                if DEBUG_MODE:
                    make_screenshot(driver)
            
            time.sleep(DRIVER_DELAY)
            driver.quit()

    if args.vdisplay:
        vdisplay.close()

if __name__ == '__main__':
    main()
