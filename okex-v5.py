#!/usr/bin/python3

from datetime import datetime
import hmac
import base64

import requests
from config import API_URL, PASSPHRASE, API_KEY, SECRET_KEY


def get_current_timestamp():
    return  datetime.utcnow().isoformat(sep='T', timespec='milliseconds') + 'Z'

def sign(timestamp, method, request_path, body, secret_key):
    if body == None:
        body = ''
        message = str(timestamp) + str.upper(method) + request_path + str(body)
        signed = hmac.new(bytes(secret_key, 'utf-8'), msg=bytes(message, 'utf-8'), digestmod='sha256').digest()
        return base64.b64encode(signed)

def get_header(api_key, passphrase, secret_key, method, endpoint):
    timestamp = get_current_timestamp()

    return {
        'OK-ACCESS-KEY': api_key,
        'OK-ACCESS-SIGN': sign(timestamp, method, endpoint, None, secret_key),
        'OK-ACCESS-TIMESTAMP': timestamp,
        'OK-ACCESS-PASSPHRASE': passphrase,
    }


method, endpoint = 'GET', '/api/v5/asset/deposit-history?ccy=XCH'
request_url = API_URL + endpoint

headers = get_header(API_KEY, PASSPHRASE, SECRET_KEY, method, endpoint)
response = requests.get(url=request_url, headers=headers)

if response.ok:
    data = response.json()
    if data['code'] == '0':
        total_amount = float(0)
        for withdraw in data['data']:
            time = datetime.fromtimestamp(int(withdraw['ts'][:-3])).isoformat()
            amount = withdraw['amt']
            total_amount += float(amount)
            print(f'{time} - {amount}')
        print(f'Total: {total_amount}')
