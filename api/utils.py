# -*- coding: utf-8 -*-
"""API

  File: 
    /bwt/api/utils

  Description: 
    Utils API
"""


import os

from bwt.api.wiki import edit, parse


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
    f.write(from_parse(title))
  if log:
    print(f'Clone: {filename}')


def update(filename, title, log=True):
  """api.utils.update

    将本地文件更新到给定标题的页面

    Args:
      filename: 本地文件的路径
      title: 页面标题
      log: (可选)是否在控制台输出保存信息
  
    Console.out:
      1. "Success"
      2. "File Not Exist: {filename}"
  """
  if not os.path.exists(filename):
    print(f"File Not Exist: {filename}")
    return
  with open(filename, 'r', encoding='utf-8') as f:
    wikitext = "".join(f.readlines())
  response = edit(title, wikitext)
  if log:
    print(response['edit']['result'])


def to_titles(responses, value='title'):
  """api.utils.to_titles

    将List of Response转换为List of Title

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


def from_parse(title=None, response=None, name='wikitext'):
  """api.utils.from_parse

    从parse返回的Response获取相应内容

    Args:
      title: 页面标题
      response: 从parse返回的Response
      *title和response必须输入其中一个
      *若两者均有值，优先处理Response
      name: 默认'wikitext', 可选:
        wikitext: wiki原始文本
        categories: 页面所属的分类
        links: 页面引用的本站链接
        templates: 页面使用到的模板
        images: 页面使用到的文件/图片
        externallinks: 页面引用的外部链接
        redirects: 页面的重定向信息
        pageid: 页面id
  
    Returns:
      * wikitext -> wikitext(py.Str)
      * categories -> List of Category(py.Str)
          分类不带命名空间'分类:'
      * links -> List of Link(py.Str)
      * templates -> List of Template(py.Str)
          模板带有命名空间'模板:'
      * images -> List of File(py.Str)
          文件不带命名空间'文件:'
      * externallinks -> List of External Link(py.Str)
      * redirects -> List of Redirect(py.Dict)
          {
            'from': 重定向
            'to': 重定向到
          }
      * pageid -> id(py.Int)
    
    Console.out:
      1. "[APIError.from_parse] Both None."
      2. "parse Error"
      3. "Error: {name} is not Supported."
  """
  if title is None and response is None:
    print("[APIError.from_parse] Both None.")
    return None
  if response is None:
    response = parse(title)
  if "error" in response:
    print("parse Error")
    return ""
  if name in ["wikitext"]:
    return response["parse"]["wikitext"]["*"]
  if name in ["categories"]:
    return to_titles(response["parse"]["categories"], '*')
  if name in ["links"]:
    return to_titles(response["parse"]["links"], '*')
  if name in ["templates"]:
    return to_titles(response["parse"]["templates"], '*')
  if name in ["images"]:
    return response["parse"]["images"]
  if name in ["externallinks"]:
    return response["parse"]["externallinks"]
  if name in ["redirects"]:
    return response["parse"]["redirects"]
  if name in ["pageid"]:
    return response["parse"]["pageid"]
  print(f"Error: {name} is not Supported.")
  return None


if __name__ == "__main__":
  res = parse("kepu")
  cat = from_parse(response=res, name='pageid')
  # print(res)
  print(cat)

