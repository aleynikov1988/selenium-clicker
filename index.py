from selenium import webdriver
import logging
from config import get_config

CONFIG = get_config()

if CONFIG['general']['debug']:
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

def get_driver(proxy, foregraund = False, windows_size = None):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server=%s' % proxy)

    if foregraund:
        chrome_options.add_argument("--headless")

        if windows_size:
            chrome_options.add_argument("--window-size=%s" % windows_size)

    driver = webdriver.Chrome(options=chrome_options)

    if CONFIG['general']['debug']:
        logging.info('Create driver: ({0}, {1}, {2})'.format(proxy, foregraund, windows_size))

    return driver

def main():
    # here mus be implemented correct logic to loop of URLs via PROXies
    i = 0
    while (True):
        if CONFIG['general']['debug']:
            logging.info('Iterration: {0}'.format(i))
            i += 1

        for proxy in CONFIG['proxy']:
            driver = get_driver(
                proxy,
                CONFIG['general']['foreground'],
                CONFIG['general']['window_size']
            )

            for link in CONFIG['links']:
                driver.get(link)
            driver.close()

if __name__ == '__main__':
    main()
