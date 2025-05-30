import aiohttp
import asyncio
import openpyxl
from bs4 import BeautifulSoup
import re
from urllib.parse import unquote
import time

# 步骤 1：从网页读取内容
async def fetch_html_content(session, url):
    while True:
        try:
            async with session.get(url) as response:
                html_content = await response.text()
            return html_content
        except aiohttp.ClientError:
            print("Network error. Retrying...")
            await asyncio.sleep(2)  # 等待2秒后重新尝试连接

def clean_sheet_title(title):
    # 移除无效字符
    return re.sub(r'[\\/*?:"<>|]', '', title)

# 步骤 2：解析 HTML 内容并生成 URL 列表
async def extract_urls(html_content, session, workbook):
    soup = BeautifulSoup(html_content, 'html.parser')
    block_tags_div = soup.find('div', class_='block-tags')
    a_tags = block_tags_div.find_all('a')

    tag_data = {}  # 以标签名称为键的字典

    for a_tag in a_tags:
        text = a_tag.get_text()
        href = a_tag['href']
        num = int(text.split('(')[1].split(')')[0])

        if num > 0:
            page = 1
            while True:
                if num <=0:
                    break
                
                if page == 1:
                    page_url = f"https://www.dushupai.com{href[:-5]}.html"
                else:
                    page_url = f"https://www.dushupai.com{href[:-5]}-{page}.html"
                
                num -= 20
                print(f"Fetching URL: {unquote(page_url)}, num: {num}")  # 打印状态

                # 重新创建会话，以便继续下载 URL
                async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=100)) as new_session:
                    result = await process_url(page_url, new_session, workbook)

                if result is not None:
                    tag_name, book_info = result
                    if len(book_info) == 0:
                        break
                    if tag_name not in tag_data:
                        tag_data[tag_name] = []  # 如果标签名称不在字典中，则创建一个新的列表
                    tag_data[tag_name].extend(book_info)  # 将书籍信息添加到相应的标签列表中
                    page += 1
                else:
                    break
    
    # 将数据保存到 Excel
    for tag_name, book_info in tag_data.items():
         # 清理 tag_name
        cleaned_tag_name = clean_sheet_title(tag_name)
        sheet = workbook.create_sheet(cleaned_tag_name)
        sheet.append(["ID", "书名", "作者", "时间", "详情", "下载链接", "图片"])  # 添加ID字段
        for info in book_info:
            sheet.append(info)

# 函数用于处理下载链接URL的数据提取
async def process_download_url(url, session):
     while True:
        try:
            async with session.get(url) as response:
                html_content = await response.text()
                soup = BeautifulSoup(html_content, 'html.parser')

                download_url_div = soup.find("div", id="download_url")
                link_element = download_url_div.find("a", string="诚通网盘 提取码：8866")
                link = link_element.get(
                    "href") if link_element else "链接未找到"
                print("download url:", link)
                return link
        except aiohttp.ClientError:
            print("Network error. Retrying...")
            await asyncio.sleep(2)  # 等待2秒后重新尝试连接

# 函数用于处理单个URL的数据提取
async def process_url(url, session, workbook):
    while True:
        try:
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
                        img = item.find('div', class_ = 'portfolio-thumb book').find('img')['src']
                        print("==== img: ", img)
                        link = f"https://www.dushupai.com{link}"
                        book_id = re.search(r'/book-content-(\d+)\.html',
                                            link).group(1)
                        
                        download_url = f"https://www.dushupai.com/download-book-{book_id}.html"
                        # 重新创建会话，以便继续下载 URL
                        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=100)) as new_session:
                            download_link = await process_download_url(download_url, new_session)

                        book_info.append([
                            book_id, title, author, time, link, download_link, img
                        ])

                    tag_name = unquote(url.split('-')[2].split('.')[0], 'utf-8')
                    return tag_name, book_info
                else:
                    return None
        except aiohttp.ClientError:
            print("Network error. Retrying...")
            await asyncio.sleep(2)  # 等待2秒后重新尝试连接

# 主函数
async def main():
    start_time = time.time()

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=100)) as session:  # 调整并发数量
        url = "https://www.dushupai.com/book-tags.html"
        html_content = await fetch_html_content(session, url)
    
    print("Step 1: HTML content fetched")

    # 创建 Excel 文件并保存数据
    workbook = openpyxl.Workbook()

    await extract_urls(html_content, session, workbook)

    # 删除默认的 sheet
    workbook.remove(workbook['Sheet'])

    # 保存 Excel 文件
    workbook.save('02-fetch_books_by_tags_1030.xlsx')

    end_time = time.time()
    print(f"Step 4: Data extraction completed. Execution time: {end_time - start_time:.2f} seconds")

if __name__ == '__main__':
    asyncio.run(main())
