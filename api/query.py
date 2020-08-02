# -*- coding: utf-8 -*-
"""API

  File: 
    /bwt/api/query

  Description: 
    Query API
"""


import json
import requests

from bwt.api.utils import from_parse
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


def referenced_category(category):
  """api.query.referenced_category
  
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
  if len(category) <= 3 or category[:3] not in ['分类:']:
    category = '分类:' + category
  data = {}
  data.update(query)
  data.pop('token')
  data["action"] = "query"
  data["list"] = "categorymembers"
  data["cmtitle"] = category
  data["cmlimit"] = "max"
  return _get_all(data, "categorymembers", "cmcontinue")


def referenced_template(template):
  """api.query.referenced_template
  
    获取引用了给定模板的所有页面

    Args:
      template: 模板名
        如果没有'模板:'会自动填充

    Returns:
      List Of Response(py.Dict)
    
    Response:
      {
        'pageid': 页面id,
        'ns': 0,
        'title': 标题,
      }
  """
  # 保证标题名带有命名空间 模板
  if len(template) <= 3 or template[:3] not in ['模板:']:
    template = '模板:' + template
  data = {}
  data.update(query)
  data.pop('token')
  data["action"] = "query"
  data["list"] = "embeddedin"
  data["eititle"] = template
  data["eilimit"] = "max"
  return _get_all(data, "embeddedin", "eicontinue")


def referenced_file(filename):
  """api.query.referenced_file
  
    获取引用了给定文件的所有页面

    Args:
      filename: 文件名
        如果没有'文件:'会自动填充
        必须带有后缀名，如'.png'

    Returns:
      List Of Response(py.Dict)
    
    Response:
      {
        'pageid': 页面id,
        'ns': 0,
        'title': 标题,
      }
  """
  # 保证标题名带有命名空间 文件
  if len(filename) <= 3 or filename[:3] not in ['文件:']:
    filename = '文件:' + filename
  data = {}
  data.update(query)
  data.pop('token')
  data["action"] = "query"
  data["list"] = "imageusage"
  data["iutitle"] = filename
  data["iulimit"] = "max"
  return _get_all(data, "imageusage", "iucontinue")


def referenced_title(title):
  """api.query.referenced_title
  
    获取链接至指定标题页面的所有页面

    Args:
      title: 标题

    Returns:
      List Of Response(py.Dict)
    
    Response:
      {
        'pageid': 页面id,
        'ns': 0,
        'title': 标题,
      }
  """
  # pageid = str(from_parse(title, name='pageid'))
  data = {}
  data.update(query)
  data.pop('token')
  data["action"] = "query"
  data["prop"] = "linkshere"
  data["titles"] = title
  data["lhlimit"] = "max"
  receiver = []
  flag = True
  continue_ = ""
  while flag:
    if continue_:
      data["lhcontinue"] = continue_
    response = json.loads(requests.post(url=url, cookies=cookies, data=data).text)
    _resdict = response["query"]["pages"].popitem()[1]
    if "linkshere" in _resdict:
      receiver.extend(_resdict["linkshere"])
    if "continue" in response:
      continue_ = response["continue"]["lhcontinue"]
    else:
      flag = False
  return receiver


if __name__ == "__main__":
  # ress = ns_main()
  # ress = ns_categories()
  # ress = referenced_category('公告')
  # ress = referenced_template('黑幕')
  # ress = referenced_file('达芙妮.png')
  ress = referenced_title('达芙妮')
  # ttls = to_titles(ress, 'title')
  print(ress)
  # print(ttls)

