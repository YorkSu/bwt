# -*- coding: utf-8 -*-
"""API

  File: 
    /bwt/api/query

  Description: 
    Query API
"""


import json
import requests

from bwt.user import url, cookies, query


def _get_all(data, list_name, continue_name, action='query'):
  receiver = []
  flag = True
  continue_ = ""
  while flag:
    if continue_:
      data[continue_name] = continue_
    response = json.loads(requests.post(url=url, cookies=cookies, data=data).text)
    receiver.extend(response[action][list_name])
    if "continue" in response:
      continue_ = response["continue"][continue_name]
    else:
      flag = False
  return receiver


def _abstract_ns_allpages(ns):
  """api.query._abstract_ns_allpages
  
    获取指定命名空间所有页面的抽象方法，不应直接调用

    Args:
      ns: 命名空间id

    Returns:
      List Of Response(py.Dict)
    
    Response:
      {
        'pageid': 页面id,
        'ns': 命名空间id,
        'title': 标题,
      }
  """
  data = {}
  data.update(query)
  data.pop('token')
  data["action"] = "query"
  data["list"] = "allpages"
  data["aplimit"] = "max"
  data["apnamespace"] = str(ns)
  return _get_all(data, "allpages", "apcontinue")


def to_titles(responses, value='title'):
  assert isinstance(responses, (list, tuple))
  titles = []
  for item in responses:
    titles.append(item[value])
  return titles


def from_category(category):
  """api.query.from_category
  
    获取给定分类中的所有页面

    Args:
      category: 分类名
        如果没有'分类:'会自动填充

    Returns:
      List Of Response(py.Dict)
    
    Response:
      {
        'pageid': 页面id,
        'ns': 0,
        'title': 标题,
      }
  """
  # 保证标题名带有命名空间 分类
  if len(category) <= 3 and category[:3] not in ['分类:']:
    category = '分类:' + category
  data = {}
  data.update(query)
  data.pop('token')
  data["action"] = "query"
  data["list"] = "categorymembers"
  data["cmtitle"] = category
  data["cmlimit"] = "max"
  return _get_all(data, "categorymembers", "cmcontinue")


def ns_main():
  """api.query.ns_main
  
    获取[主]命名空间中所有页面

    Returns:
      List Of Response(py.Dict)
    
    Response:
      {
        'pageid': 页面id,
        'ns': 0,
        'title': 标题,
      }
  """
  return _abstract_ns_allpages(0)


def ns_file():
  """api.query.ns_file
  
    获取[文件]命名空间中所有页面

    Returns:
      List Of Response(py.Dict)
    
    Response:
      {
        'pageid': 页面id,
        'ns': 6,
        'title': 标题,
      }
  """
  return _abstract_ns_allpages(6)


def ns_template():
  """api.query.ns_template
  
    获取[模板]命名空间中所有页面

    Returns:
      List Of Response(py.Dict)
    
    Response:
      {
        'pageid': 页面id,
        'ns': 10,
        'title': 标题,
      }
  """
  return _abstract_ns_allpages(10)


def ns_categories():
  """api.query.ns_categories
  
    获取[分类]命名空间中所有页面

    Returns:
      List Of Response(py.Dict)
    
    Response:
      {
        'pageid': 页面id,
        'ns': 14,
        'title': 标题,
      }
  """
  return _abstract_ns_allpages(14)


if __name__ == "__main__":
  # ress = from_category('公告')
  # ress = ns_main()
  ress = ns_categories()
  ttls = to_titles(ress, 'title')
  print(ress)
  print(ttls)

