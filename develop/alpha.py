# -*- coding: utf-8 -*-
"""Develop alpha

  File: 
    /bwt/develop/alpha

  Description: 
    Bilibili Wiki Tools Develop function - Alpha
"""


import re

from bwt.api import purge, ns_main, to_titles


def _list_splitter(lists, a):
  _len = len(lists)
  outputs = []
  for i in range(_len):
    if not i % a:
      outputs.append([])
    outputs[i // a].append(lists[i])
  return outputs


def purge_main():
  """develop.alpha.purge_main

    刷新[主]命名空间中所有页面的缓存

    Returns:
      List of Response(py.Dict)(from purge)
  """
  main_titles = to_titles(ns_main())
  receiver = []
  for titles in _list_splitter(main_titles, 50):
    receiver.append(purge(titles))
  return receiver


def search_title(key):
  """develop.alpha.search_title

    从[主]命名空间中所有页面的标题中查找指定标题

    Args:
      key: 匹配规则，可以是字符串，也可以是正则表达式

    Returns:
      List of Title(py.Str)
  """
  main_titles = to_titles(ns_main())
  receiver = []
  for title in main_titles:
    result = re.search(key, title)
    if result is not None:
      receiver.append(title)
  return receiver


def multi_template_table_update():
  """develop.alpha.multi_template_table_update

    使用CSV或者Excel表批量更新对应标题的多个模板
    *表格的空值会被转换为空字符

    Args:
      key: 匹配规则，可以是字符串，也可以是正则表达式

    Returns:
      List of Title(py.Str)
  """
  pass


if __name__ == "__main__":
  # purge_main()
  print(search_title('达芙妮'))

