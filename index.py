from selenium import webdriver
import logging
from config import get_general, get_batch
import platform
import os
import time
import argparse
from xvfbwrapper import Xvfb


general_config = get_general()
DEBUG_MODE = general_config['debug']

if DEBUG_MODE:
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

def get_driver(proxy, lang, mobile=None):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server={0}'.format(proxy))
    chrome_options.add_argument('--lang={0}'.format(lang))

    # mobile emulate
    if mobile:
        mobile_emulation = {
            'deviceName': mobile
        }
        chrome_options.add_experimental_option('mobileEmulation', mobile_emulation)

    driver = webdriver.Chrome(options=chrome_options)

    if DEBUG_MODE:
        logging.info('Driver created with: ({0}, {1}, {2})'.format(proxy, lang, mobile))

    return driver

def main():
    parser = argparse.ArgumentParser(description='Selenium proxy - O_o')
    parser.add_argument('--batch', nargs=1, required=True, help='name of batch to start')
    parser.add_argument('--vdisplay', nargs='?', help='use virtual display')
    args = parser.parse_args()

    if args.vdisplay:
        vdisplay = Xvfb(width=1280, height=740, colordepth=16)
        vdisplay.start()

    batch_name = args.batch[0]

    try:
        settings = get_batch(batch_name)
    except KeyError:
        print('Invalid name batch')
        return

    i = 0
    while (True):
        i = i + 1
        if DEBUG_MODE:
            logging.info('Iterration: {0}'.format(i))
            i += 1

        for proxy in settings['proxy']:
            mobile = None

            if settings['mobile']:
                mobile = settings['mobile']

            driver = get_driver(
                proxy=proxy,
                lang=settings['lang'],
                mobile=mobile
            )

            for link in settings['links']:
                driver.get(link)

                if settings['linksType'] == 'ban':
                    link = driver.find_element_by_xpath('//a/img')
                    link.click()

                if DEBUG_MODE:
                    filename = '{0}/screenshot/{1}.png'.format(os.path.dirname(os.path.realpath(__file__)), int(time.time()))
                    driver.save_screenshot(filename)
                    logging.info('Save screenshot: {0}'.format(filename))

            driver.close()

    if args.vdisplay:
        vdisplay.close()

if __name__ == '__main__':
    main()
