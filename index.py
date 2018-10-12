from selenium import webdriver
import logging
from config import get_config
import platform
from xvfbwrapper import Xvfb
import os
import time


CONFIG = get_config()

if CONFIG['general']['debug']:
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

def get_driver(proxy):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--proxy-server=%s' % proxy)

    # mobile emulate
    if CONFIG['mobile']['enable']:
        mobile_emulation = {
            'deviceName': CONFIG['mobile']['deviceName']
        }
        chrome_options.add_experimental_option('mobileEmulation', mobile_emulation)

    driver = webdriver.Chrome(options=chrome_options)

    if CONFIG['general']['debug']:
        logging.info('Use proxy: ({0})'.format(proxy))

    return driver

def main():
    vdisplay = Xvfb(width=1024, height=768, colordepth=24)
    vdisplay.start()

    i = 0
    while (True):
        i = i + 1

        if CONFIG['general']['debug']:
            logging.info('Iterration: {0}'.format(i))
            i += 1

        for proxy in CONFIG['proxy']:
            driver = get_driver(proxy)

            for link in CONFIG['links']:
                driver.get(link)
                filename = '{0}/screenshot/{1}.png'.format(os.path.dirname(os.path.realpath(__file__)), int(time.time()))
                driver.save_screenshot(filename)
                logging.info('Save screenshot: {0}'.format(filename))

            driver.close()

    vdisplay.stop()

if __name__ == '__main__':
    main()
