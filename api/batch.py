# -*- coding: utf-8 -*-
"""API

  File: 
    /bwt/api/batch

  Description: 
    Batch API
    使用 CSV 批量更新模块(代更正)
"""


import re
import csv
import pandas as pd

from bwt.api.wiki import edit
from bwt.api.utils import clone, update, from_parse


def batch_clone(root, titles, suffix='.wikitext', log=True):
  """api.batch.batch_clone

    将给定的多个标题的页面内容批量保存到本地文件

    Args:
      root: 要保存的文件的路径
      titles: List, 页面标题列表
      suffix: 文件后缀名, 默认'.wikitext'
      log: (可选)是否在控制台输出保存信息
  
    Console.out:
      "Clone: {文件名}"
  """
  for title in titles:
    clone(root, title, suffix=suffix, log=log)


def batch_update(filename, titles, log=True):
  """api.batch.batch_update

    将多个本地文件批量更新到给定标题的页面

    Args:
      root: 要保存的文件的路径
      titles: List, 页面标题列表
      suffix: 文件后缀名, 默认'.wikitext'
      log: (可选)是否在控制台输出保存信息
  
    Console.out:
      "Clone: {文件名}"
  """
  for title in titles:
    update(filename, title, log=log)


def handle_file(filename):
  """api.batch.handle_file

    读取CSV或者Excel表，并返回标题和内容
    *表格的空值会被转换为空字符

    Args:
      filename: 文件名
  
    Returns:
      (header, content)
      header: 标题，即表格第一行
      content: 内容，即表格第二行以下的部分
  """
  header = []
  content = []
  ext = filename.split('.')[-1]
  # == CSV ==
  if ext == 'csv':
    with open(filename, 'r', encoding='utf-8') as f:
      f_csv = csv.reader(f)
      for inx, i in enumerate(f_csv):
        if inx:
          content.append(i)
        else:
          header = i
  # == Excel ==
  elif ext in ['xlsx', 'xls']:
    data = pd.read_excel(filename, header=0)
    data = data.where(data.notnull(), '')
    header = data.columns.tolist()
    for i in range(data.shape[0]):
      content.append(data.loc[i].tolist())
  return header, content


def _normalize_template(header, row):
  title = row[0]
  template = row[1]
  text = "{{" + template + "\n"
  for i in range(2, len(row)):
    text += "|" + header[i] + "=" + row[i] + "\n"
  text += "}}\n"
  return title, template, text


def _replace_template(wikitext, template, text):
  if wikitext:
    if "{{" + template in wikitext:
      return re.sub("{{" + template + "\n((.|\n)*?)\n}}\n", text, wikitext, 1)
    return text + wikitext
  return text


def table_update(filename, template_only=True):
  """api.batch.table_update

    使用CSV或者Excel表批量更新对应标题的模板
    *表格的空值会被转换为空字符

    Args:
      filename: 文件名
      template_only: (可选)是否只更新模板部分
  """
  header, content = handle_file(filename)
  for row in content:
    title, template, text = _normalize_template(header, row)
    if template_only:
      page_content = from_parse(title)
      new_text = _replace_template(page_content, template, text)
      print(f"{row[0]}: {edit(title, new_text)['edit']['result']}")
    else:
      print(f"{row[0]}: {edit(title, text)['edit']['result']}")


# test part
if __name__ == "__main__":
  # print(handle_file("unpush/test.csv"))
  # print(handle_file("unpush/英雄UP表.xlsx"))
  # update_with_file("unpush/test.csv")
  table_update("unpush/test道具.xlsx", template_only=True)

  # print([getPageContent("盖亚的钥匙")])
  # print('1234{{1}}'[0:2])
  # _wikiext = "123{{muban\n|12={{ganrao|1}}\n|23={{{canshu|}}}\n}}\n==exp==1243{{show}}"
  # _template = '{{muban\n((.|\n)*?)\n}}\n'
  # _span = re.search(_template, _wikiext).span()
  # print([_wikiext[_span[0]:_span[1]]])
  # print(re.sub(_template, "{{tihuan}}", _wikiext, 1))
