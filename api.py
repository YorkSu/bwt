# -*- coding: utf-8 -*-
"""API

  File: 
    /bwt/api

  Description: 
    MediaWiki API
"""

import json
import requests

from bwt.user import url, headers, query


def edit(title, text):
  data = {}
  data.update(query)
  data["action"] = "edit"
  data["title"] = title
  data["text"] = text
  response = json.loads(requests.post(url=url, headers=headers, data=data).text)
  return response


def getPageContent(title):
  data = {}
  data.update(query)
  data["action"] = "parse"
  data["page"] = title
  data["prop"] = "wikitext"
  response = json.loads(requests.post(url=url, headers=headers, data=data).text)
  return response["parse"]["wikitext"]["*"]


def getAllPage():
  data = {}
  data.update(query)
  data["action"] = "query"
  data["list"] = "allpages"
  data["aplimit"] = "max"
  flag = True
  apcontinue = ""
  titles = []
  while flag:
    if apcontinue:
      data["continue"] = "-||"
      data["apcontinue"] = apcontinue
    response = json.loads(requests.post(url=url, headers=headers, data=data).text)
    titles.extend(response['query']['allpages'])
    if "continue" in response:
      apcontinue = response["continue"]["apcontinue"]
    else:
      flag = False
  return titles


# test part
if __name__ == "__main__":
  # print(edit("TestPython", "Hello, World. [From York|VS Code]"))
  # print(getPageContent("TestPython"))
  print(len(getAllPage()))
