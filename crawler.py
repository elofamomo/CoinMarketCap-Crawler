import asyncio
import json
import os
import timeit
from datetime import datetime
from json.decoder import JSONDecodeError

import aiohttp
import orjson
import pandas as pd

import response_handler

key_dir = "config/key.json"
cmc_api = "https://pro-api.coinmarketcap.com"
cmc_api_header_key = "X-CMC_PRO_API_KEY"
categories = ['cryptocurrency', 'exchange', 'global-metrics', 'tools', 'blockchain', 'flat', 'partners', 'key',
              'content']
data_cols = ['rank', 'name', 'symbol', 'market_cap', 'price', 'circulating_supply', 'volume', 'percent_change_7d']
endpoint_paths = ['latest', 'historical', 'info', 'map']
actions = ['listings', 'quotes', 'ohlcv', 'trending']
aux_needed = "cmc_rank,circulating_supply"
number_of_repeat = 5
data_dirs = "data/"


class Crawler:

    def __init__(self, no_of_row: int, live: bool, historical: str):
        print("--------INITIALIZING CRAWLER---------")
        self.no_of_row = no_of_row
        self.live = live
        self.historical = historical
        self.api_key = self.get_basic_api_key(key_dir)

    @staticmethod
    def get_basic_api_key(key_dir):
        with open(key_dir, 'r') as json_file:
            data = json.load(json_file)
        try:
            key = data['basic']
            api_key = key['apiKey']
        except (JSONDecodeError, ValueError, KeyError) as e:
            print("Config file not correct or missing API key")
            exit(1)
        return api_key

    def attach(self, dic, key, value):
        dic[key] = value

    def get_concurrency_data(self, endpoint_ver: str, headers, params):
        endpoint_path = ''
        if self.historical == 'latest':
            endpoint_path = endpoint_paths[0]
        else:
            endpoint_path = 'historical'
            self.attach(params, 'date', self.historical)
        endpoint = '/'.join([endpoint_ver, categories[0], actions[0], endpoint_path])
        self.attach(params, 'limit', str(self.no_of_row))
        self.attach(params, 'aux', aux_needed)
        status_code, data = self.do_concurrency_request(endpoint, headers, params)
        response_handler.switch_case_response(status_code, data)
        if status_code == 200:
            data = data['data']
            self.to_csv(data)
            execute_time = timeit.timeit(lambda: self.to_csv(data), number=number_of_repeat) / number_of_repeat
            print(f"Average time for writing {self.no_of_row} records for {number_of_repeat} times is {execute_time}")
        return

    def to_csv(self, data):
        df = pd.DataFrame.from_dict(data)
        quotes_df = pd.json_normalize(df['quote'])
        df = pd.concat([df[['cmc_rank', 'name', 'symbol', 'circulating_supply']],
                        quotes_df[['USD.market_cap', 'USD.price', 'USD.volume_24h', 'USD.percent_change_7d']]], axis=1)
        file_name, file_dir = self.get_csv_file_name()
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        df.to_csv(file_name)

    @staticmethod
    def get_csv_file_name():
        now = datetime.now()
        return data_dirs + now.strftime("%Y/%m/%d/%H/%M.csv"), data_dirs + now.strftime("%Y/%m/%d/%H/")

    @staticmethod
    def do_concurrency_request(endpoint: str, headers, params):
        async def concurrency_api_session():
            async with aiohttp.ClientSession() as session:
                async with session.get(cmc_api + '/' + endpoint, headers=headers, params=params) as response:
                    status_code = response.status
                    data = await response.json(loads=orjson.loads)
            return status_code, data

        return asyncio.run(concurrency_api_session())

    def run(self):
        print("running...")
        if os.name == 'nt':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        headers, params = {}, {}
        self.attach(headers, cmc_api_header_key, self.api_key)
        self.get_concurrency_data('v1', headers, params)
