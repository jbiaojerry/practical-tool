#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

# 目标网站URL
url = "https://www.dalanmei.com/book-tags.html"

# 发送HTTP请求获取网页内容
response = requests.get(url)

# 检查请求是否成功
if response.status_code == 200:
    # 使用Beautiful Soup解析HTML内容
    soup = BeautifulSoup(response.text, "html.parser")

    #  print(soup)
    element_with_id = soup.find("div", class_="block-tags")
    print(element_with_id)
    if element_with_id:
        name = element_with_id.find("h2").text
        print(name)
        text_content = element_with_id.get_text()
        print(text_content)
    else:
        print("未找到具有指定id的元素")

    # 查找所有书籍元素
    #  book_name = soup.find("h4", class_="post-title").text
    #  print(book_name)

else:
    print("Failed to retrieve the webpage. Status code:", response.status_code)
