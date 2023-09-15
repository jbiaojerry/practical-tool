import requests
from bs4 import BeautifulSoup

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
    if num <= 5:
        continue
    num_pages = (num + 19) // 20  # 计算需要的页数

    for page in range(1, num_pages + 1):
        if page == 1:
            page_url = f"https://www.dalanmei.com{href[:-5]}.html"
        else:
            page_url = f"https://www.dalanmei.com{href[:-5]}-{page}.html"
        url_list.append(page_url)

# 步骤 3：将生成的 URL 保存到 txt 文件
with open('urls_02.txt', 'w') as file:
    for url in url_list:
        file.write(url + '\n')

print(f"生成的 URL 已保存到 urls.txt 文件中，共有 {len(url_list)} 个 URL。")
