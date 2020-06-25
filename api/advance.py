# -*- coding: utf-8 -*-
"""API

  File: 
    /bwt/api/advance

  Description: 
    Advance API
    based on mediwwiki API
"""


import json
import requests

from bwt.user import url, cookies, query


def get_titles_from_category(category):
  # 保证标题名带有命名空间 分类
  if len(category) <= 3 and category[:3] not in ['分类:']:
    category = '分类:' + category
  data = {}
  data.update(query)
  data["action"] = "query"
  data["list"] = "categorymembers"
  data["cmtitle"] = category
  data["cmlimit"] = "max"
  flag = True
  cmcontinue = ""
  titles = []
  while flag:
    if cmcontinue:
      data["cmcontinue"] = cmcontinue
    response = json.loads(requests.post(url=url, cookies=cookies, data=data).text)
    titles.extend(response['query']['categorymembers'])
    if "continue" in response:
      cmcontinue = response["continue"]["cmcontinue"]
    else:
      flag = False
  return titles


def get_titles_from_main():
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
      data["apcontinue"] = apcontinue
    response = json.loads(requests.post(url=url, cookies=cookies, data=data).text)
    titles.extend(response['query']['allpages'])
    if "continue" in response:
      apcontinue = response["continue"]["apcontinue"]
    else:
      flag = False
  return titles





