import requests
from bs4 import BeautifulSoup
import openpyxl
import time
from concurrent.futures import ThreadPoolExecutor

# 函数用于发送请求并处理连接中断的情况
def send_request_with_retry(url, max_retries=3):
    for i in range(max_retries):
        try:
            response = requests.get(url)
            return response
        except requests.exceptions.RequestException as e:
            print(f"Request failed. Retrying ({i+1}/{max_retries})...")
            time.sleep(5)  # 等待一段时间后重试
    return None

# 函数用于处理单个URL的数据提取和保存
def process_url(url):
    # 解析网页内容
    response = send_request_with_retry(url)
    if response is None:
        print(f"无法连接到URL: {url}")
        return None

    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')

    # 提取数据
    portfolio_book_ul = soup.find('ul', class_='portfolio-book')
    if portfolio_book_ul is not None:
        portfolio_items = portfolio_book_ul.find_all('li', class_='portfolio-item')
        tag_name = url.split('/')[-1].split('.')[0]

        # 返回书籍信息
        book_info = []
        for item in portfolio_items:
            title = item.find('div', class_='portfolio-title').find('a').text
            author = item.find('div', class_='portfolio-author').text
            time = item.find('div', class_='portfolio-line').find('div').text
            link = item.find('div', class_='portfolio-title').find('a')['href']
            book_info.append([title, author, time, f"https://www.dalanmei.com{link}"])
        
        return tag_name, book_info
    else:
        return None

# 步骤 1：从网页读取内容
url = "https://www.dalanmei.com/book-tags.html"
response = send_request_with_retry(url)
if response is None:
    print("无法连接到网站。")
    exit()

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
    
    # 添加条件判断，排除 num 小于 5 的情况
    if num >= 5:
        num_pages = (num + 19) // 20  # 计算需要的页数

        for page in range(1, num_pages + 1):
            if page == 1:
                page_url = f"https://www.dalanmei.com{href[:-5]}.html"
            else:
                page_url = f"https://www.dalanmei.com{href[:-5]}-{page}.html"
            url_list.append(page_url)

# 步骤 3：使用线程池处理 URL 列表
book_data = []  # 用于保存所有书籍信息

with ThreadPoolExecutor(max_workers=5) as executor:
    # 使用线程池并发处理 URL
    futures = {executor.submit(process_url, url): url for url in url_list}

    for future in futures:
        url = futures[future]
        result = future.result()
        if result is not None:
            tag_name, book_info = result
            book_data.append((tag_name, book_info))

# 步骤 4：创建Excel文件并保存数据
workbook = openpyxl.Workbook()

for tag_name, book_info in book_data:
    sheet = workbook.create_sheet(tag_name)
    sheet.append(["标题", "作者", "时间", "链接"])
    for info in book_info:
        sheet.append(info)

# 删除默认的sheet
workbook.remove(workbook['Sheet'])

# 保存Excel文件
workbook.save('books.xlsx')

print("数据提取完成，已保存到 books.xlsx 文件。")
