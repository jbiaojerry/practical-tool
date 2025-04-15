import aiohttp
import asyncio
import openpyxl
from bs4 import BeautifulSoup
import re
from urllib.parse import unquote
import time
import os

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
async def extract_urls(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    block_tags_div = soup.find('div', class_='block-tags')
    a_tags = block_tags_div.find_all('a')

    tag_data = {}  # 以标签名称为键的字典
    tag_book_counts = {}

   # 创建"ebooks"目录，如果不存在的话
    ebooks_directory = "ebooks"
    if not os.path.exists(ebooks_directory):
        os.mkdir(ebooks_directory)
    # 创建总目录README.md
    with open(os.path.join(ebooks_directory, 'README.md'), 'w', encoding='utf-8') as readme_file:
        markdown_content = """\
<p align="center">
<img src=".github/logo.png" alt="Project Logo">
</p>

# 电子书下载宝库

![GitHub](https://img.shields.io/github/license/jbiaojerry/ebook-treasure-chest)
![GitHub stars](https://img.shields.io/github/stars/jbiaojerry/ebook-treasure-chest?style=social)
![GitHub forks](https://img.shields.io/github/forks/jbiaojerry/ebook-treasure-chest?style=social)

欢迎来到电子书下载宝库，一个汇聚了各类电子书下载链接的地方。无论你是喜欢阅读经典文学、经管励志、终身学习、职场创业、技术手册还是其他类型的书籍，这里都能满足你的需求。
该库涵盖了帆书app(原樊登读书)、微信读书、京东读书、喜马拉雅等读书app的大部分电子书。

## 简介

我们从各个电子书网站上精心收集了各种电子书下载链接，并根据常用的标签对它们进行了简单分类。每本书都包括了三种常见格式文件：epub、mobi 和 azw3，以满足不同阅读设备和喜好的需求。

## 如何使用

浏览我们的下载宝库非常简单：
1. 在下方目录索引点击关键词或者“Ctrl+f”搜索标签，以找到你感兴趣的电子书类型;
2. 点击标签或搜索结果，即可进入详细的下载链接页面，点击书名可以查看图书封面;
3. 在下载链接页面，你将找到包含epub、mobi、azw3格式的下载链接，点击下载即可。

## 支持我们

如果你有电子书资源想要分享，或者发现了链接失效或有其他问题，请不要犹豫，立刻提出问题或贡献你的资源。我们欢迎任何形式的贡献，让这个宝库变得更加丰富和有用。

## 许可证

该项目基于开源许可证（例如，MIT许可证）发布。请查看 [LICENSE](LICENSE) 文件以获取详细信息。

![Happy Reading](https://media.giphy.com/media/l2SpQRuiLWz8K/giphy.gif)

让我们一起享受阅读的乐趣吧！如果你喜欢这个项目，请不要忘记给它点个星星⭐️以表示支持。感谢你的参与和支持！
            """
        readme_file.write(markdown_content)
        # 在总目录README.md中创建带锚点链接的工作表列表
        readme_file.write('\n\n\n# 目录\n\n')  

    # 创建字典来存储每个sheet的数据行数
    tag_book_counts = {}
    for a_tag in a_tags:
        text = a_tag.get_text()
        href = a_tag['href']
        num = int(text.split('(')[1].split(')')[0])
        count = 0
        tag_data = {} 

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
                    result = await process_url(page_url, new_session)

                if result is not None:
                    tag_name, book_info = result
                    if len(book_info) == 0:
                        break
                    tag_book_counts[tag_name] = len(book_info)
                    if tag_name not in tag_data:
                        tag_data[tag_name] = []  # 如果标签名称不在字典中，则创建一个新的列表
                    tag_data[tag_name].extend(book_info)  # 将书籍信息添加到相应的标签列表中
                   
                    page += 1
                else:
                    break

        # 将数据保存到 md
        for tag_name, book_info in tag_data.items():
            # 清理 tag_name
            cleaned_tag_name = clean_sheet_title(tag_name)
            # 创建Markdown文件，文件名与工作表名称相同，保存在"ebooks/md"目录下
            md_directory = os.path.join(ebooks_directory, 'md')
            if not os.path.exists(md_directory):
                os.mkdir(md_directory)
            md_filename = os.path.join(md_directory, f'{cleaned_tag_name}.md')
            with open(md_filename, 'w', encoding='utf-8') as md_file:
                # 写入工作表名称作为Markdown的一级标题
                md_file.write(f'# 版权声明\n\n本站内容均从网上搜集，版权归著作人及版权方所有，如侵犯您的权益，请通知我们，我们将会及时删除！ 下载链接仅供宽带测试研究用途，请下载后在24小时内删除，请勿用于商业目的。请支持正版！\n\n')

                md_file.write(f'# {cleaned_tag_name}\n\n')
                # 写入表头作为Markdown的表头
                md_file.write('| 书名 | 作者 | epub/mobi/azw3 |\n')
                md_file.write('| --- | --- | --- |\n')

                # 遍历每一行数据并写入Markdown文件
                for info in book_info:
                    # print("==== info type:", type(info), info)
                    # _, title, author, _, _, download_link = info 
                    # 使用"书名"作为默认链接
                    md_file.write(
                        f'| [{info[1]} (点击查看图片)]({info[6]}) | {info[2]} | [下载]({info[5]}) |\n'
                    )

            print(f"Markdown文件 '{md_filename}' 已生成。")
    
    # 根据值降序排序
    sorted_dict_desc = dict(sorted(tag_book_counts.items(), key=lambda item: item[1], reverse=True))
    count_list = list(sorted_dict_desc)
    with open(os.path.join(ebooks_directory, 'README.md'), 'a', encoding='utf-8') as readme_file:
      for i in range(0, len(count_list), 8):
          batch = count_list[i:i + 8]
          for tag_name, count in batch:
              readme_file.write(
                  f'- [{tag_name}({count})](md/{tag_name}.md) ')
              print(f'==== {tag_name}:{count}')
          readme_file.write('\n')
        

    print("Markdown文件和总目录README.md已成功生成，并保存在'ebooks'目录中。")

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
async def process_url(url, session):
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

    await extract_urls(html_content)

    end_time = time.time()
    print(f"Step 2: Data extraction completed. Execution time: {end_time - start_time:.2f} seconds")

if __name__ == '__main__':
    asyncio.run(main())
