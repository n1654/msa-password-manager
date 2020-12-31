#!/usr/bin/env python3

import threading
import time
import json
import crypto.py
from flask import Flask, jsonify, request
from OpenSSL import SSL


context = SSL.Context(SSL.PROTOCOL_TLSv1_2)
context.use_privatekey_file('/start/cert/key.pem')
context.use_certificate_file('/start/cert/cert.pem')

# Set key "field1": http://localhost:5000/set/field1?value=42
# Get key "field1": http://localhost:5000/get/field1
# Get all :         http://localhost:5000/get
# Clear all :       http://localhost:5000/clear

app = Flask(__name__)
lock = threading.Lock()

with open('/start/storage.json', 'r') as f:
    storage = json.load(f)


@app.route('/', methods=['GET'])
def welcome():
    with lock:
        return "Welcome Message"


def update_thread():
    global storage
    while True:
        with lock:
            storage['uptime'] = storage.get('uptime', 0) + 1
        time.sleep(1.0)


@app.route('/clear', methods=['GET'])
def clear():
    global storage
    with lock:
        storage['keys'] = []
        return jsonify(storage)


@app.route('/all-keys', methods=['GET'])
def allkeys():
    with lock:
        return jsonify(storage['keys'])


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


@app.route('/key/<id>', methods=['GET'])
def get_key_by_id(id):
    with lock:
        return jsonify(check_key(id)[0])


# url?id=value1&name=value2&value=value3&description=value4
@app.route('/key/<id>', methods=['POST'])
def create_key(id):
    id = int(id)
    key = check_key(id)
    global storage
    with lock:
        if len(key[0]) == 0:
            storage['keys'].append(key[0])
        index = key[1]
        storage['keys'][index]['id'] = int(request.args.get('id'))
        storage['keys'][index]['name'] = request.args.get('name', '...')
        storage['keys'][index]['value'] = request.args.get('value', '...')
        storage['keys'][index]['description'] = request.args.get('description', '...')
        with open('/start/storage.json', 'w') as f:
            json.dump(storage, f)
        return jsonify(storage)


if __name__ == '__main__':
    threading.Thread(target=update_thread).start()
    app.run(host='0.0.0.0', threaded=True, debug=True, ssl_context=context)
