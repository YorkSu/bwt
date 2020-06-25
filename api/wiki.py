# -*- coding: utf-8 -*-
"""API

  File: 
    /bwt/api/wiki

  Description: 
    Bilibili Wiki API
"""


import json
import requests

from bwt.user import url, cookies, query


def edit(title, text, minor=False, bot=False, createonly=False, prependtext="", appendtext=""):
  data = {}
  data.update(query)
  data["action"] = "edit"
  data["title"] = title
  data["text"] = text
  response = json.loads(requests.post(url=url, cookies=cookies, data=data).text)
  return response


def move(fr, to, reason=""):
  data = {}
  data.update(query)
  data["action"] = "move"
  data["from"] = fr
  data["to"] = to
  data["reason"] = reason
  response = json.loads(requests.post(url=url, cookies=cookies, data=data).text)
  return response


def purge(titles):
  data = {}
  data.update(query)
  if isinstance(titles, (list, tuple)):
    # make sure titles <= 50
    if len(titles) > 50: 
      return None
    data["titles"] = "|".join(titles)
  else:
    data["titles"] = titles
  data["action"] = "purge"
  response = json.loads(requests.post(url=url, cookies=cookies, data=data).text)
  return response


def parse(title):
  data = {}
  data.update(query)
  data["action"] = "parse"
  data["page"] = title
  data["prop"] = "wikitext"
  response = json.loads(requests.post(url=url, cookies=cookies, data=data).text)
  return response


# test part
if __name__ == "__main__":
  # print(edit("TestPython", "Hello, World. [From York|VS Code]"))
  # print(parse("TestPython"))
  # print(purge("好友"))
  # print(purge(["达芙妮", "莉莉丝"]))
  # print(move("TestPython", "TestMovePython"))
  print(parse("TestMovePython"))
  # print(parse("不存在的页面"))

