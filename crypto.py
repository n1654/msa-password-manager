#!/usr/bin/env python3

import json
import os


# call os function to encrypt value
def encrypt(plain_text, enc_key):
    stream = os.popen(f'./encrypt.sh {plain_text} {enc_key}')
    enc_value = stream.read().strip("\n")
    return enc_value


# call os function to decrypt
def decrypt(enc_value, enc_key):
    stream = os.popen(f'./decrypt.sh {enc_value} {enc_key}')
    plain_text = stream.read().strip("\n")
    return plain_text


def check_key(id):
    with open('/start/storage.json', 'r') as f:
        storage = json.load(f)
    item_index = 0
    for item in storage['keys']:
        if ('id' in item.keys()) and (item['id'] == int(id)):
            result = item
            break
        else:
            result = {}
        item_index += 1
    # either item index or last index
    return result, item_index


def get_item_by_id(id, enc_key):
    enc_value = check_key(id)[0]['value']
    return decrypt(enc_value, enc_key)
