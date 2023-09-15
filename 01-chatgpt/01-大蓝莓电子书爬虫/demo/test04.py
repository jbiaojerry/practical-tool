#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import openpyxl

# 创建一个Excel工作簿和工作表
workbook = openpyxl.Workbook()
worksheet = workbook.active

# 添加Excel表头
worksheet.append(["URL", "文件名", "下载链接"])

# 循环生成URL并爬取页面内容
for i in range(1, 11):
    url = f"https://www.dalanmei.com/download-book-{i}.html"

    # 发送HTTP请求获取网页内容
    response = requests.get(url)

    # 检查请求是否成功
    if response.status_code == 200:
        # 使用Beautiful Soup解析HTML内容
        soup = BeautifulSoup(response.text, "html.parser")

        # 查找<div>标签的id属性为download_declaration的元素
        download_declaration = soup.find("div", id="download_declaration")

        if download_declaration:
            # 查找<h2>标签
            h2_element = download_declaration.find("h2")
            file_name = h2_element.text.strip()

            # 查找<a>标签中的href属性
            a_element = download_declaration.find("a", href=True)
            download_link = a_element["href"]

            # 添加数据到Excel工作表
            worksheet.append([url, file_name, download_link])

        else:
            print(f"未找到指定id的元素：{url}")
    else:
        print(f"无法访问网页：{url}")

# 保存Excel文件
workbook.save("book_data.xlsx")
