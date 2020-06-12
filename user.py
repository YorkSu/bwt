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
  # r"C:\Users\York\AppData\Local\Microsoft\Edge\User Data\Default\Cookies"
  if browser.lower() == 'edge':
    browser_dir = r"Microsoft\Edge"
  elif browser.lower() == 'chrome':
    browser_dir = r"Google\Chrome"
  local_state = os.environ['LOCALAPPDATA'] + '\\' + browser_dir + r'\User Data\Local State'
  cookie_path = os.environ['LOCALAPPDATA'] + '\\' + browser_dir + r"\User Data\Default\Cookies"
  sql = f"select host_key,name,encrypted_value from cookies where host_key='{host}' and path='{path}'"
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
  path = config["path"]
  browser = config["browser"]
  url = f"https://{host}{path}/api.php"
  cookies = get_cookie(host, path, browser)
  cookies["SESSDATA"] = config["SESSDATA"]
  query = {
      "format": "json",
      "token": get_token(cookies)}
  check_token(cookies, query)
