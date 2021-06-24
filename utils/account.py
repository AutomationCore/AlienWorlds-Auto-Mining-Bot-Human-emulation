import json
import os

import requests
from selenium.common.exceptions import JavascriptException

import config


class Account:
    def __init__(self, account_name: str = None):
        self.account_name = account_name

        self.api_url2 = 'https://wax.api.atomicassets.io/atomicassets/v1/'
        self.api_url3 = 'https://wax.greymass.com/v1/'
        self.api_url4 = 'https://api.waxsweden.org/v1/'

    def get_user_assets(self):
        

        r = requests.Session()

        response = r.get(self.api_url2 + f'assets?collection_name=alien.worlds&owner={self.account_name}&limit=200')

        return json.loads(response.content.decode())

    def get_account(self):
        r = requests.Session()

        response = r.get(self.api_url3 + f'chain/get_account', data=json.dumps({'account_name': self.account_name}))

        return json.loads(response.content.decode())

    def get_table_rows(self, lower_bound, upper_bound, index_position=1, key_type="", code="m.federation", limit=10,
                       reverse=False, scope="m.federation", show_payer=False, table="bags", table_key=""):
        r = requests.Session()

        response = r.post(self.api_url4 + f'chain/get_table_rows', data=json.dumps({'code': code,
                                                                                    'index_position': index_position,
                                                                                    'json': True,
                                                                                    'key_type': key_type,
                                                                                    'limit': limit,
                                                                                    'lower_bound': lower_bound,
                                                                                    'reverse': reverse,
                                                                                    'scope': scope,
                                                                                    'show_payer': show_payer,
                                                                                    'table': table,
                                                                                    'table_key': table_key,
                                                                                    'upper_bound': upper_bound}),
                          headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36',
                                   'origin': 'https://play.alienworlds.io/',
                                   'referer': 'https://play.alienworlds.io/'})

        return json.loads(response.content.decode())

    def get_asset(self, asset_id):
        r = requests.Session()

        response = r.get(self.api_url2 + f'assets/{asset_id}')

        return json.loads(response.content.decode())

    @staticmethod
    def get_current_user_account(driver):
        if os.path.normpath(driver.current_url) != os.path.normpath(config.WORK_SITE_DIR):
            return

        try:
            driver.execute_script(f'eval("window.userAccount = wax.userAccount;")')
        except JavascriptException:
            return None

        user_account = driver.execute_script('return window.userAccount;')

        return user_account

    def get_delay(self):
        

        miners = self.get_table_rows(upper_bound=self.account_name,
                                     lower_bound=self.account_name, table='miners', limit=1)
        miner = miners['rows'][0]

        current_land = miner['current_land']
        land = self.get_asset(current_land)
        land_multiplier = land['data']['data']['delay'] / 10

        two_bag_items = []  
        bags = self.get_table_rows(upper_bound=self.account_name,
                                   lower_bound=self.account_name, table='bags', limit=1)
        bag = bags['rows'][0]['items']
        for item in bag:
            asset = self.get_asset(item)
            delay = asset['data']['data']['delay']

            if len(two_bag_items) >= 2:
                if delay > two_bag_items[0]:
                    two_bag_items[0] = delay
                elif delay > two_bag_items[1]:
                    two_bag_items[1] = delay
            else:
                two_bag_items.append(delay)

        return int(sum(two_bag_items) * land_multiplier)
