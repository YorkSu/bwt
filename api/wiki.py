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


def edit(title, text):
  """api.wiki.edit
  
    使用指定的文本，编辑指定标题页面

    Args:
      title: 页面标题
      text: 文本，格式为'wikitext'

    Returns:
      Response(py.Dict)
    
    Response:
      {
        'edit': {
          'new': '', 
          'result': 状态, 
          'pageid': 页面id, 
          'title': 标题, 
          'contentmodel': 'wikitext', 
          'oldrevid': 修订id, 
          'newrevid': 修订id, 
          'newtimestamp': 时间戳
        }
      }
  """
  data = {}
  data.update(query)
  data["action"] = "edit"
  data["title"] = title
  data["text"] = text
  response = json.loads(requests.post(url=url, cookies=cookies, data=data).text)
  return response


def move(fr, to, reason="", noredirect=True):
  """api.wiki.move
  
    移动指定标题页面到新标题

    Args:
      fr: 原标题
      to: 新标题
      reason: (可选)移动原因
      noredirect: (可选)不要创建重定向，默认不创建

    Returns:
      Response(py.Dict)
    
    Response:
      {
        'move': {
          'from': 原标题, 
          'to': 新标题, 
          'reason': 移动原因, 
          'redirectcreated': ''
        }
      }
  """
  data = {}
  data.update(query)
  data["action"] = "move"
  data["from"] = fr
  data["to"] = to
  data["reason"] = reason
  data["noredirect"] = noredirect
  response = json.loads(requests.post(url=url, cookies=cookies, data=data).text)
  return response


def purge(titles):
  """api.wiki.purge
  
    刷新指定标题页面的缓存

    Args:
      titles: Str or List of Str.
        单个标题或者标题列表
        *列表不能超过50个标题

    Returns:
      Response(py.Dict)
    
    Response:
      {
        'batchcomplete': '', 
        'purge': [ # 如果输入的titles为列表，此处会列出所有标题
          {
            'ns': 命名空间, 
            'title': 标题, 
            'purged': ''
          }
        ]
      }
  """
  data = {}
  data.update(query)
  data.pop('token')
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
  """api.wiki.purge
  
    解析指定标题页面

    Args:
      title: 标题

    Returns:
      Response(py.Dict)
    
    Response:
      {
        'parse': {
          'title': 页面标题, 
          'pageid': 页面id, 
          'redirects': [{
            'from': 重定向,
            'to': 重定向到
          }], 
          'categories': [{
            'sortkey': '',
            '*': 分类
          }], 
          'links': [{
            'ns': 命名空间,
            'exists': '', # 链接存在才出现exists
            '*': 链接标题
          }], 
          'templates': [{
            'ns': 10,
            'exists': '', # 模板存在才出现exists
            '*': 模板标题
          }], 
          'images': [
            '文件名'
          ], 
          'externallinks': [
            '外链地址'
          ], 
          'wikitext': {
            '*': 内容
          }
        }
      }
  """
  props = [
      "categories",
      "links",
      "templates",
      "images",
      "externallinks",
      "wikitext",]
  data = {}
  data.update(query)
  data.pop('token')
  data["action"] = "parse"
  data["page"] = title
  data["prop"] = '|'.join(props)
  data["redirects"] = 1
  response = json.loads(requests.post(url=url, cookies=cookies, data=data).text)
  return response


def expand_templates(text):
  """api.wiki.expand_templates
  
    展开给定文本的所有模板

    Args:
      text: 要解析的文本，格式为'wikitext'

    Returns:
      Response(py.Dict)
    
    Response:
      {
        'expandtemplates': {
          'wikitext': 展开后的内容
        }
      }
  """
  data = {}
  data.update(query)
  data.pop('token')
  data["action"] = "expandtemplates"
  data["text"] = text
  data["prop"] = "wikitext"
  response = json.loads(requests.post(url=url, cookies=cookies, data=data).text)
  return response


# test part
if __name__ == "__main__":
  # print(edit("Python", "Hello, World. [BWT v1.0a]"))
  print(move("Python", "TestMovePython"))
  # print(parse("Python"))
  # print(parse("不存在的页面"))
  # print(purge("好友"))
  # print(purge(["达芙妮", "莉莉丝"]))
  # print(expand_templates('{{失效|Python}}'))

