import json
import logging
import time

from selenium.common.exceptions import NoSuchElementException, MoveTargetOutOfBoundsException, ElementClickInterceptedException
from selenium.webdriver.support.wait import WebDriverWait
from seleniumwire import webdriver

import config
from utils.account import Account
from utils.exceptions import ButtonNotFound


class Control:
    def __init__(self, driver: webdriver.Firefox, index, game_account_name: str):
        

        self.driver = driver
        self.index = index
        self.game_account_name = game_account_name

    def login(self):
        

        logging.info('WAX Login')

        self.driver.get('https://all-access.wax.io')
        with open(f'cookies/{self.index}.json', 'r') as f:
            for cookie in json.loads(f.read()):
                del cookie['sameSite']
                self.driver.add_cookie(cookie)

        self.driver.get(config.WORK_SITE_DIR)

        self.driver.execute_script('wax.login()')

        self.wait_windows_amount(2, '<')

        self.wait_page_load()

        self.click_approve_button()

        self.wait_windows_amount(1)

        self.change_window(0)

        time.sleep(5)

        user_account = Account.get_current_user_account(self.driver)

        self.game_account_name = user_account

        logging.info(f'Authorization passed successfully ({user_account}).')

        return user_account

    def change_window(self, window_index: int):
        

        
        if len(self.driver.window_handles) > window_index:
            window_after = self.driver.window_handles[window_index]  
            self.driver.switch_to.window(window_after)  

    def add_cookies_from_response_to_browser(self, response):
        

        dict_resp_cookies = response.cookies.get_dict()
        response_cookies_browser = [{'name': name, 'value': value} for name, value in dict_resp_cookies.items()]
        for cookie in response_cookies_browser:
            self.driver.add_cookie(cookie)

    def add_cookies_from_browser_to_session(self, session):
        

        for cookie in self.driver.get_cookies():
            session.cookies.set(cookie['name'], cookie['value'])
        return session

    def click_button(self, x: int, y: int, max_attempts: int = 30):
        

        fail_click_count = 0
        while fail_click_count < max_attempts:
            try:
                webdriver.ActionChains(self.driver).move_by_offset(x, y).click().perform()
                webdriver.ActionChains(self.driver).move_by_offset(-x, -y).perform()
                return
            except MoveTargetOutOfBoundsException:
                max_attempts += 1

                time.sleep(5)

        raise ButtonNotFound(f"Button ({x}, {y}) not found for {max_attempts} attempts.")

    def wait_page_load(self):
        

        while self.driver.execute_script('return document.readyState;') != 'complete':
            logging.info(f'Waiting for the page to load {self.driver.current_url}.')

            time.sleep(5)

        logging.info(f'Page ({self.driver.current_url}) loaded.')

    def switch_to_frame(self, par, arg):
        

        try:
            iframe = self.driver.find_element_by_xpath(f'//iframe[@{par}="{arg}"]')
        except NoSuchElementException:
            iframe = None
        if iframe:
            self.driver.switch_to.frame(iframe)
        else:
            logging.warning(f'FRAME "{par}={arg}" NOT FOUND')

    def click_approve_button(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        self.change_window(1)

        fail_click_button_count = 0
        while len(self.driver.window_handles) == 2:
            if fail_click_button_count == 10:
                raise ButtonNotFound("APPROVE button not found 10 times. Restart.")

            time.sleep(10)

            self.wait_page_load()

            fail_click_button_count = 0
            approve_button = self.driver.find_element_by_xpath('//button[@class="button button-secondary button-large text-1-5rem text-bold mx-1"]')
            while True:
                if fail_click_button_count == 10:
                    raise ButtonNotFound("APPROVE button not found.")

                try:
                    approve_button.click()

                    break
                except ElementClickInterceptedException:
                    time.sleep(5)

                    self.driver.refresh()
                fail_click_button_count += 1

            time.sleep(6)
        self.change_window(0)

    def wait_windows_amount(self, amount: int, action: str = '!='):
        

        actions = {'==': len(self.driver.window_handles) == amount,
                   '!=': len(self.driver.window_handles) != amount,
                   '<=': len(self.driver.window_handles) <= amount,
                   '>=': len(self.driver.window_handles) >= amount,
                   '>': len(self.driver.window_handles) > amount,
                   '<': len(self.driver.window_handles) < amount}
        action = actions[action]

        while action:
            logging.info(f'Waiting {amount} window.')

            time.sleep(5)

        logging.info(f'{amount} window found.')
