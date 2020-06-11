# -*- coding: utf-8 -*-
"""User

  File: 
    /bwt/user

  Description: 
    Setting User Config
"""


import json
import requests


def getHeaders(cookie):
  header = {}
  header["Cookie"] = cookie
  return header


def getToken(headers):
  params = {}
  params["action"] = "query"
  params["format"] = "json"
  params["meta"] = "tokens"
  response = json.loads(requests.get(url=url, headers=headers, params=params).text)
  # query["token"] = response["query"]["tokens"]["csrftoken"]
  # print(response["query"]["tokens"]["csrftoken"])
  return response["query"]["tokens"]["csrftoken"]


def checkToken(headers, query):
  data = {}
  data.update(query)
  data["action"] = "checktoken"
  data["type"] = "csrf"
  response = json.loads(requests.post(url=url, headers=headers, data=data).text)
  print("登录状态:", response["checktoken"]["result"])


url = ""
cookie = ""

with open("config.json", 'r') as f:
  config = json.loads(f.read())
  url = config["url"]
  cookie = config["cookie"]

headers = getHeaders(cookie)
query = {
    "format": "json",
    "token": getToken(headers)}
checkToken(headers, query)

