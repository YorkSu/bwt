# -*- coding: utf-8 -*-
"""API

  File: 
    /bwt/api/utils

  Description: 
    Utils API
"""


import os

from bwt.api.wiki import parse


def clone(root, title, suffix='.wikitext'):
  if not os.path.exists(root):
    os.mkdir(root)
  filename = os.path.join(root, title) + suffix
  with open(filename, 'w', encoding='utf-8') as f:
    f.write(parse_content(title))
  print(f'Clone: {filename}')


def parse_content(title):
  response = parse(title)
  if "error" in response:
    return ""
  return response["parse"]["wikitext"]["*"]

