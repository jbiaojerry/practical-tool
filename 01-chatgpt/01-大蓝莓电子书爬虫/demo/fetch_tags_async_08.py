import asyncio
import re

import aiohttp
import openpyxl
from bs4 import BeautifulSoup


# 函数用于处理单个URL的数据提取
async def process_url(session, url):
    async with session.get(url) as response:
        html_content = await response.text()
        soup = BeautifulSoup(html_content, 'html.parser')

        portfolio_book_ul = soup.find('ul', class_='portfolio-book')
        if portfolio_book_ul is not None:
            portfolio_items = portfolio_book_ul.find_all(
                'li', class_='portfolio-item')

            book_info = []
            for item in portfolio_items:
                title = item.find('div',
                                  class_='portfolio-title').find('a').text
                author = item.find('div', class_='portfolio-author').text
                time = item.find('div',
                                 class_='portfolio-line').find('div').text
                link = item.find('div',
                                 class_='portfolio-title').find('a')['href']
                book_id = re.search(r'/book-content-(\d+)\.html',
                                    link).group(1)
                book_info.append([
                    title, author, time, f"https://www.dalanmei.com{link}",
                    book_id
                ])

            tag_name = url.split('/')[-1].split('.')[0].split('-').[1]
            print(tag_name)
            return tag_name, book_info
        else:
            return None


# 步骤 1：从网页读取内容
url = "https://www.dalanmei.com/book-tags.html"


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html_content = await response.text()

    # 步骤 2：解析 HTML 内容并生成 URL 列表
    soup = BeautifulSoup(html_content, 'html.parser')
    block_tags_div = soup.find('div', class_='block-tags')
    a_tags = block_tags_div.find_all('a')

    url_list = []

    for a_tag in a_tags:
        text = a_tag.get_text()
        href = a_tag['href']
        num = int(text.split('(')[1].split(')')[0])

        if num >= 5:
            num_pages = (num + 19) // 20

            for page in range(1, num_pages + 1):
                if page == 1:
                    page_url = f"https://www.dalanmei.com{href[:-5]}.html"
                else:
                    page_url = f"https://www.dalanmei.com{href[:-5]}-{page}.html"
                url_list.append(page_url)

    # 步骤 3：使用异步并发处理 URL 列表
    async with aiohttp.ClientSession() as session:
        tasks = [process_url(session, url) for url in url_list]
        results = await asyncio.gather(*tasks)

    # 创建 Excel 文件并保存数据
    workbook = openpyxl.Workbook()

    tag_data = {}  # 以标签名称为键的字典

    for result in results:
        if result is not None:
            tag_name, book_info = result
            if tag_name not in tag_data:
                tag_data[tag_name] = []  # 如果标签名称不在字典中，则创建一个新的列表
            tag_data[tag_name].extend(book_info)  # 将书籍信息添加到相应的标签列表中

    for tag_name, book_info in tag_data.items():
        sheet = workbook.create_sheet(tag_name)
        sheet.append(["标题", "作者", "时间", "链接", "ID"])  # 添加ID字段
        for info in book_info:
            sheet.append(info)

    # 删除默认的 sheet
    workbook.remove(workbook['Sheet'])

    # 保存 Excel 文件
    workbook.save('books_async_0801.xlsx')

    print("数据提取完成，已保存到 books.xlsx 文件。")


if __name__ == '__main__':
    asyncio.run(main())
