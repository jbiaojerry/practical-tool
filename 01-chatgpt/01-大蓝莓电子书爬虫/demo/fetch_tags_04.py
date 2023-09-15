import requests
from bs4 import BeautifulSoup
import openpyxl
import time

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

# 步骤 3：将生成的 URL 保存到 txt 文件
with open('urls_04.txt', 'w') as file:
    for url in url_list:
        file.write(url + '\n')

# 步骤 4：从txt文件中读取URL列表
url_list = []
with open('urls_04.txt', 'r') as file:
    url_list = [line.strip() for line in file]

# 步骤 5：创建Excel文件
workbook = openpyxl.Workbook()
for url in url_list:
    # 解析网页内容
    response = send_request_with_retry(url)
    if response is None:
        print(f"无法连接到URL: {url}")
        continue

    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')

    # 提取数据
    portfolio_book_ul = soup.find('ul', class_='portfolio-book')
    if portfolio_book_ul is not None:
        portfolio_items = portfolio_book_ul.find_all('li', class_='portfolio-item')

        # 创建新的sheet，以URL中的标签名作为sheet名
        tag_name = url.split('/')[-1].split('.')[0]
        sheet = workbook.create_sheet(tag_name)

        # 写入数据
        for i, item in enumerate(portfolio_items, 2):
            title = item.find('div', class_='portfolio-title').find('a').text
            author = item.find('div', class_='portfolio-author').text
            time = item.find('div', class_='portfolio-line').find('div').text
            link = item.find('div', class_='portfolio-title').find('a')['href']

            sheet[f'A{i}'] = title
            sheet[f'B{i}'] = author
            sheet[f'C{i}'] = time
            sheet[f'D{i}'] = f"https://www.dalanmei.com{link}"

# 删除默认的sheet
workbook.remove(workbook['Sheet'])

# 保存Excel文件
workbook.save('books_04.xlsx')
