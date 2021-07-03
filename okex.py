#!/usr/bin/python3

from datetime import datetime
import hmac
import base64

import requests
from config import API_URL


class Client(object):
    def __init__(self, passphrase, apikey, secret_key) -> None:
        self._passphrase = passphrase
        self._apikey = apikey
        self._secret_key = secret_key
        
    def _get_current_timestamp(self):
        return  datetime.utcnow().isoformat(sep='T', timespec='milliseconds') + 'Z'

    def _sign(self, timestamp, method, request_path, body):
        if body == None: body = ''
        message = str(timestamp) + str.upper(method) + request_path + str(body)
        signed = hmac.new(bytes(self._secret_key, 'utf-8'), msg=bytes(message, 'utf-8'), digestmod='sha256').digest()
        return base64.b64encode(signed)

    def _get_header(self, method, endpoint):
        timestamp = self._get_current_timestamp()

        return {
            'OK-ACCESS-KEY': self._apikey,
            'OK-ACCESS-SIGN': self._sign(timestamp, method, endpoint, None),
            'OK-ACCESS-TIMESTAMP': timestamp,
            'OK-ACCESS-PASSPHRASE': self._passphrase,
        }
    
    def deposit_history(self, ccy):
        method, endpoint = 'GET', f'/api/v5/asset/deposit-history?ccy={ccy}'
        request_url = API_URL + endpoint

        headers = self._get_header(method, endpoint)
        response = requests.get(url=request_url, headers=headers)

        if response.ok:
            return response.json()
