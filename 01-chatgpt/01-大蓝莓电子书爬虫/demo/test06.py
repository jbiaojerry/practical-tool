#!/usr/bin/env python
# -*- coding: utf-8 -*-

import openpyxl
import requests
from bs4 import BeautifulSoup

# 创建一个Excel工作簿和工作表
workbook = openpyxl.Workbook()
worksheet = workbook.active

# 添加Excel表头
worksheet.append(["ID", "URL", "文件名", "MOBI下载链接", "EPUB下载链接", "AZW3下载链接"])

# 循环生成URL并爬取页面内容
#  for i in range(1, 13385):
for i in range(1, 220):
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
        #  mobi_link = download_url_div.find("a", string="MOBI格式下载")["href"]
        #  epub_link = download_url_div.find("a", string="EPUB格式下载")["href"]
        #  azw3_link = download_url_div.find("a", string="AZW3格式下载")["href"]
        # 查找MOBI下载链接
        mobi_link_element = download_url_div.find("a", string="MOBI格式下载")
        if mobi_link_element:
            mobi_link = mobi_link_element.get("href")
        else:
            mobi_link = "链接未找到"

        # 查找EPUB下载链接
        epub_link_element = download_url_div.find("a", string="EPUB格式下载")
        if epub_link_element:
            epub_link = epub_link_element.get("href")
        else:
            epub_link = "链接未找到"

        # 查找AZW3下载链接
        azw3_link_element = download_url_div.find("a", string="AZW3格式下载")
        if azw3_link_element:
            azw3_link = azw3_link_element.get("href")
        else:
            azw3_link = "链接未找到"

        # 文件名格式为id+文件名
        file_name_with_id = f"{i}-{file_name}"

        # 添加数据到Excel工作表
        worksheet.append(
            [i, url, file_name_with_id, mobi_link, epub_link, azw3_link])

        print(f"已处理：{i}")
    else:
        print(f"无法访问网页：{url}")

# 保存Excel文件
workbook.save("book_data_1_220.xlsx")
