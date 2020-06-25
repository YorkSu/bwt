# -*- coding: utf-8 -*-
"""API

  File: 
    /bwt/api/utils

  Description: 
    Utils API
"""


import os

from bwt.api.wiki import parse


def clone(root, title, suffix='.wikitext', log=True):
  """api.utils.clone

    将给定标题的页面内容保存到本地文件

    Args:
      root: 要保存的文件的路径
      title: 页面标题
      suffix: 文件后缀名, 默认'.wikitext'
      log: (可选)是否在控制台输出保存信息
  
    Console.out:
      "Clone: {文件名}"
  """
  if not os.path.exists(root):
    os.mkdir(root)
  filename = os.path.join(root, title) + suffix
  with open(filename, 'w', encoding='utf-8') as f:
    f.write(parse_content(title))
  if log:
    print(f'Clone: {filename}')


def parse_content(title):
  """api.utils.parse_content

    从parse返回的Response获取wikitext

    Args:
      title: 页面标题
  
    Returns:
      wikitext(py.Str)
  """
  response = parse(title)
  if "error" in response:
    return ""
  return response["parse"]["wikitext"]["*"]


def to_titles(responses, value='title'):
  """api.utils.to_titles

    将Response转换为title

    Args:
      responses: List or Tuple Of Response(py.Dict)
      value: Str, 默认'title'
  
    Returns:
      List of Title(py.Str)
  """
  assert isinstance(responses, (list, tuple))
  titles = []
  for item in responses:
    titles.append(item[value])
  return titles


