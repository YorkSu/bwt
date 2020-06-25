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
from bwt.api.utils import clone, parse_content


def batch_clone(root, titles, suffix='.wikitext'):
  for title in titles:
    clone(root, title, suffix=suffix)


def batch_titles(inputs):
  assert isinstance(inputs, (list, tuple))
  titles = []
  for item in inputs:
    titles.append(item['title'])
  return titles


def handle_file(filename):
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
    data = data.where(data.notnull(), None)
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


def update_with_file(filename, template_only=True):
  header, content = handle_file(filename)
  for row in content:
    title, template, text = _normalize_template(header, row)
    if template_only:
      page_content = parse_content(title)
      new_text = _replace_template(page_content, template, text)
      print(edit(title, new_text))
    else:
      print(edit(title, text))


# test part
if __name__ == "__main__":
  # print(handle_file("unpush/test.csv"))
  # print(handle_file("unpush/英雄UP表.xlsx"))
  # update_with_file("unpush/test.csv")
  update_with_file("unpush/test道具.xlsx", template_only=True)

  # print([getPageContent("盖亚的钥匙")])
  # print('1234{{1}}'[0:2])
  # _wikiext = "123{{muban\n|12={{ganrao|1}}\n|23={{{canshu|}}}\n}}\n==exp==1243{{show}}"
  # _template = '{{muban\n((.|\n)*?)\n}}\n'
  # _span = re.search(_template, _wikiext).span()
  # print([_wikiext[_span[0]:_span[1]]])
  # print(re.sub(_template, "{{tihuan}}", _wikiext, 1))
