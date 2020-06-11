# -*- coding: utf-8 -*-
"""Batch

  File: 
    /bwt/batch

  Description: 
    使用 CSV 批量更新模块
"""


import csv
import pandas as pd

from api import edit


def normalize_template(header, row):
  title = row[0]
  template = "{{" + row[1] + "\n"
  for i in range(2, len(row)):
    template += "|" + header[i] + "=" + row[i] + "\n"
  template += "}}"
  return title, template


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
    header = data.columns.tolist()
    for i in range(data.shape[0]):
      content.append(data.loc[i].tolist())
  return header, content


def update_with_csv(filename):
  header, content = handle_file(filename)
  for row in content:
    title, template = normalize_template(header, row)
    # TODO: 后续会加上更复杂的功能，比如仅更新模板部分等
    print(edit(title, template))


# test part
if __name__ == "__main__":
  # print(handle_file("unpush/test.csv"))
  # print(handle_file("unpush/英雄UP表.xlsx"))
  update_with_csv("unpush/test.csv")
  
