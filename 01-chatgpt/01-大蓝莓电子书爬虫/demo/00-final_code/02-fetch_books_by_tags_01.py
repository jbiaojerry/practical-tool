import aiohttp
import asyncio
import openpyxl
from bs4 import BeautifulSoup
import re
from urllib.parse import unquote

# 函数用于处理单个URL的数据提取
async def process_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html_content = await response.text()
    # ... process_url 函数的其余部分保持不变 ...

# 步骤 1：从网页读取内容
url = "https://www.dalanmei.com/book-tags.html"

async def main():
    # 步骤 2：解析 HTML 内容并生成 URL 列表
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html_content = await response.text()

    soup = BeautifulSoup(html_content, 'html.parser')
    block_tags_div = soup.find('div', class_='block-tags')
    a_tags = block_tags_div.find_all('a')

    url_list = []

    for a_tag in a_tags:
        text = a_tag.get_text()
        href = a_tag['href']
        num = int(text.split('(')[1].split(')')[0])

        if num > 0:
            page = 1  # 从第一页开始
            while True:
                if page == 1:
                    page_url = f"https://www.dalanmei.com{href[:-5]}.html"
                else:
                    page_url = f"https://www.dalanmei.com{href[:-5]}-{page}.html"
                result = await process_url(page_url)
                if result is None:
                    break
                url_list.append(page_url)
                page += 1
                
    # 步骤 3：使用异步并发处理 URL 列表
    async with aiohttp.ClientSession() as session:
        tasks = [process_url(url) for url in url_list]
        results = await asyncio.gather(*tasks)

    # 创建 Excel 文件并保存数据
    workbook = openpyxl.Workbook()

    # 如果没有数据，创建一个名为 "未知" 的工作表并添加一条消息
    if not results:
        sheet = workbook.active
        sheet.title = "未知"
        sheet.append(["无数据可用"])

    tag_data = {}  # 以标签名称为键的字典

    for result in results:
        if result is not None:
            tag_name, book_info = result
            if tag_name not in tag_data:
                tag_data[tag_name] = []  # 如果标签名称不在字典中，则创建一个新的列表
            tag_data[tag_name].extend(book_info)  # 将书籍信息添加到相应的标签列表中

    for tag_name, book_info in tag_data.items():
        sheet = workbook.create_sheet(tag_name)
        sheet.append(["ID", "书名", "作者", "时间", "详情"])  # 添加ID字段
        for info in book_info:
            sheet.append(info)

    # 删除默认的 sheet
    workbook.remove(workbook['Sheet'])

    # 保存 Excel 文件
    workbook.save('02-fetch_books_by_tags_01.xlsx')

    print("数据提取完成，已保存到 02-fetch_books_by_tags_01.xlsx 文件。")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())




    # ... 之前的代码 ...



