#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import openpyxl

# 步骤 1：从网页读取内容
url = "https://www.dalanmei.com/book-tags.html"
response = requests.get(url)
html_content = response.text

# 步骤 2：解析 HTML 内容并生成 URL 列表
soup = BeautifulSoup(html_content, 'html.parser')
block_tags_div = soup.find('div', class_='block-tags')
a_tags = block_tags_div.find_all('a')

url_list = []

for a_tag in a_tags:
    text = a_tag.get_text()
    href = a_tag['href']
    num = int(text.split('(')[1].split(')')[0])
    num_pages = (num + 19) // 20  # 计算需要的页数

    for page in range(1, num_pages + 1):
        if page == 1:
            page_url = f"https://www.dalanmei.com{href[:-5]}.html"
        else:
            page_url = f"https://www.dalanmei.com{href[:-5]}-{page}.html"
        url_list.append(page_url)

# 步骤 3：将生成的 URL 保存到 txt 文件
with open('urls_03.txt', 'w') as file:
    for url in url_list:
        file.write(url + '\n')

# 步骤 4：遍历生成的 URL 并获取书籍信息
book_info_list = []

with open('urls_03.txt', 'r') as file:
    urls = file.read().splitlines()

for url in urls:
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    portfolio_items = soup.find_all('li', class_='portfolio-item')

    for item in portfolio_items:
        book_info = {}
        title = item.find('div', class_='portfolio-title').find('a').text
        author = item.find('div', class_='portfolio-author').text
        time = item.find('div',
                         class_='portfolio-line').find_all('div')[0].text
        href = item.find('div', class_='portfolio-title').find('a')['href']
        book_id = int(href.split('-')[-1].split('.')[0])

        book_info['Title'] = title
        book_info['Author'] = author
        book_info['Time'] = time
        book_info['ID'] = book_id
        book_info_list.append(book_info)

# 步骤 5：创建 Excel 文件并保存书籍信息
wb = openpyxl.Workbook()

# 步骤 6：按照 tags 分类创建 sheet 并保存数据
for a_tag in a_tags:
    tag_name = a_tag.get_text().split('(')[0]
    sheet = wb.create_sheet(tag_name)
    sheet.append(['Title', 'Author', 'Time', 'ID'])

    for book_info in book_info_list:
        if book_info['Title'].startswith(tag_name):
            sheet.append([
                book_info['Title'], book_info['Author'], book_info['Time'],
                book_info['ID']
            ])

# 删除默认的 Sheet
del wb['Sheet']

# 保存 Excel 文件
wb.save('book_info_03.xlsx')
print("书籍信息已保存到 book_info.xlsx 文件中。")
