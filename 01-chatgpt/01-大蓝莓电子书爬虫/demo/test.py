#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import os

# 目标网站URL
url = "https://www.dalanmei.com/"

# 发送HTTP请求获取网页内容
response = requests.get(url)

# 检查请求是否成功
if response.status_code == 200:
    # 使用Beautiful Soup解析HTML内容
    soup = BeautifulSoup(response.text, "html.parser")

    # 查找所有包含epub链接的元素
    epub_links = soup.find_all("a", href=True, text="epub")

    # 提取epub文件名称
    epub_names = [os.path.basename(link['href']) for link in epub_links]

    # 打印所有epub文件名称
    for name in epub_names:
        print(name)
else:
    print("Failed to retrieve the webpage. Status code:", response.status_code)
