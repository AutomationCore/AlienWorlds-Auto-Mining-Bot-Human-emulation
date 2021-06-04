import json
import logging
import time

from selenium.common.exceptions import NoSuchElementException
from seleniumwire import webdriver

import config


def get_valid_cookies(cookies_amount):
    

    options = webdriver.FirefoxOptions()
    options.headless = True  

    driver = webdriver.Firefox(options=options, executable_path='drivers/geckodriver.exe')

    valid_cookies_index = []

    for i in range(1, cookies_amount + 1):
        logging.info(f'Checking %s cookies', i)

        driver.delete_all_cookies()  

        driver.get('https://all-access.wax.io')
        with open(f'cookies/{i}.json', 'r') as f:  
            for cookie in json.loads(f.read()):
                del cookie['sameSite']
                driver.add_cookie(cookie)

        driver.get(config.WORK_SITE_DIR)

        try:
            driver.execute_script('wax.login()')
        except Exception as e:
            logging.info(f'Cookies %s failed verification. ({e.__str__()})', i)
            continue

        
        while len(driver.window_handles) < 2:
            time.sleep(1)

        
        for window in driver.window_handles:
            driver.switch_to.window(window)
            if driver.current_url == 'https://all-access.wax.io/cloud-wallet/login/':
                break

        while driver.execute_script('return document.readyState;') != 'complete':
            time.sleep(2)

        time.sleep(1)

        try:
            checked_element = driver.find_element_by_xpath('//span[@class="action-title"]')
        except NoSuchElementException:
            checked_element = None
        if checked_element and checked_element.text == 'You must login into WAX Cloud Wallet first':
            logging.info(f'Cookies %s failed verification.', i)
            continue

        
        for window in driver.window_handles[1:]:
            driver.switch_to.window(window)
            driver.close()

        driver.switch_to.window(driver.window_handles[0])  

        logging.info('Cookies %s passed the check.', i)
        valid_cookies_index.append(i)

    logging.info('Checking the cookie for validity is over.')

    driver.close()

    return valid_cookies_index
