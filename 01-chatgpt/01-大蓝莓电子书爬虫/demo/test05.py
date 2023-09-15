#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import openpyxl

# 创建一个Excel工作簿和工作表
workbook = openpyxl.Workbook()
worksheet = workbook.active

# 添加Excel表头
worksheet.append(["ID", "URL", "文件名", "MOBI下载链接", "EPUB下载链接", "AZW3下载链接"])

# 循环生成URL并爬取页面内容
for i in range(1, 11):
    url = f"https://www.dalanmei.com/download-book-{i}.html"

    # 发送HTTP请求获取网页内容
    response = requests.get(url)

    # 检查请求是否成功
    if response.status_code == 200:
        # 使用Beautiful Soup解析HTML内容
        soup = BeautifulSoup(response.text, "html.parser")

        # 查找<h2>标签
        h2_element = soup.find("h2")
        file_name = h2_element.text.strip()

        # 查找下载链接
        download_url_div = soup.find("div", id="download_url")
        mobi_link = download_url_div.find("a", string="MOBI格式下载")["href"]
        epub_link = download_url_div.find("a", string="EPUB格式下载")["href"]
        azw3_link = download_url_div.find("a", string="AZW3格式下载")["href"]

        # 添加数据到Excel工作表
        worksheet.append([i, url, file_name, mobi_link, epub_link, azw3_link])

        print(f"已处理：{i}")
    else:
        print(f"无法访问网页：{url}")

# 保存Excel文件
workbook.save("book_data05.xlsx")
