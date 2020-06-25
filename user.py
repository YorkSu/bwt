# -*- coding: utf-8 -*-
"""User

  File: 
    /bwt/user

  Description: 
    Setting User Config
"""


import os
import sqlite3
import base64
from win32crypt import CryptUnprotectData
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import json
import requests

_LOCALAPPDATA = os.environ['LOCALAPPDATA']
EDGE_LOCAL_STATE = _LOCALAPPDATA + r'\Microsoft\Edge\User Data\Local State'
EDGE_COOKIE_PATH = _LOCALAPPDATA + r'\Microsoft\Edge\User Data\Default\Cookies'
CHROME_LOCAL_STATE = _LOCALAPPDATA + r'\Google\Chrome\User Data\Local State'
CHROME_COOKIE_PATH = _LOCALAPPDATA + r'\Google\Chrome\User Data\Default\Cookies'


def get_string(local_state):
    with open(local_state, 'r', encoding='utf-8') as f:
        s = json.load(f)['os_crypt']['encrypted_key']
    return s


def pull_the_key(base64_encrypted_key):
    encrypted_key_with_header = base64.b64decode(base64_encrypted_key)
    encrypted_key = encrypted_key_with_header[5:]
    key = CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    return key


def decrypt_string(key, data):
    nonce, cipherbytes = data[3:15], data[15:]
    aesgcm = AESGCM(key)
    plainbytes = aesgcm.decrypt(nonce, cipherbytes, None)
    plaintext = plainbytes.decode('utf-8')
    return plaintext


def get_cookie(host, path, browser):
  if browser.lower() == 'edge':
    local_state = EDGE_LOCAL_STATE
    cookie_path = EDGE_COOKIE_PATH
  elif browser.lower() == 'chrome':
    local_state = CHROME_LOCAL_STATE
    cookie_path = CHROME_COOKIE_PATH
  sql = f"select host_key,name,encrypted_value from cookies where host_key='{host}'"
  if path:
    sql += f" and path='{path}'"
  with sqlite3.connect(cookie_path) as conn:
    cu = conn.cursor()
    res = cu.execute(sql).fetchall()
    cu.close()
    cookies = {}
    key = pull_the_key(get_string(local_state))
    for host_key, name, encrypted_value in res:
      if encrypted_value[0:3] == b'v10':
        cookies[name] = decrypt_string(key, encrypted_value)
      else:
        cookies[name] = CryptUnprotectData(encrypted_value)[1].decode()
    return cookies


def get_token(cookies):
    params = {}
    params["action"] = "query"
    params["format"] = "json"
    params["meta"] = "tokens"
    response = json.loads(requests.get(
        url=url, cookies=cookies, params=params).text)
    return response["query"]["tokens"]["csrftoken"]


def check_token(cookies, query):
    data = {}
    data.update(query)
    data["action"] = "checktoken"
    data["type"] = "csrf"
    response = json.loads(requests.post(
        url=url, cookies=cookies, data=data).text)
    # return response
    print("登录状态:", response["checktoken"]["result"])


with open("config.json", 'r') as f:
  config = json.loads(f.read())
  host = config["host"]
  host2 = config["host2"]
  path = config["path"]
  browser = config["browser"]
  url = f"https://{host}{path}/api.php"
  cookies = get_cookie(host, path, browser)
  cookies2 = get_cookie(host2, "/", browser)
  cookies["SESSDATA"] = cookies2["SESSDATA"]
  query = {
      "format": "json",
      "utf8": 1,
      "token": get_token(cookies)}
  check_token(cookies, query)

