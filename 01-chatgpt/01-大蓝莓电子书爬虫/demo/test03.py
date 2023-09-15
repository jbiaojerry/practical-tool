#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

# HTML内容示例
html_content = '<h4 class="post-title">发现你的管理优势</h4>'

# 使用Beautiful Soup解析HTML内容
soup = BeautifulSoup(html_content, "html.parser")

# 查找<h4>标签，并提取其中的文本
h4_element = soup.find("h4", class_="post-title")
text = h4_element.text

# 打印提取的文本
print(text)
