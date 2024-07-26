import socket
import urllib.request
import urllib.parse
import sys
import configparser
import zlib
import base64
import os
import uuid
import time

serverHost = '127.0.0.1'
serverPort = 30003

config = configparser.ConfigParser()
config.read(os.path.join(sys.path[0], 'config.ini'))

uuid_file = os.path.join(sys.path[0], 'UUID')

if os.path.exists(uuid_file):
    with open(uuid_file, 'r') as file_object:
        mid = file_object.read().strip()
else:
    mid = uuid.uuid1().hex[16:]
    with open(uuid_file, 'w') as file_object:
        file_object.write(mid)

sockobj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockobj.connect((serverHost, serverPort))

def send_message(source_data):
    try:
        source_data = base64.b64encode(zlib.compress(source_data.encode('utf-8'))).decode('utf-8')
        response = urllib.request.urlopen(
            url=config.get("global", "sendurl"),
            data=urllib.parse.urlencode({'from': mid, 'code': source_data}).encode('utf-8'),
            timeout=2
        )
        return True
    except Exception as e:
        print(str(e))
        return False

tmp_buf = ''

while True:
    buf = sockobj.recv(8192)
    if not buf:
        break
    tmp_buf += buf.decode('utf-8')
    if buf[-1:] == b'\n':
        if send_message(tmp_buf):
            tmp_buf = ''
time.sleep(0)

