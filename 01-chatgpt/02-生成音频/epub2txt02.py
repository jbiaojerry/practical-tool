import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import concurrent.futures

# 输入EPUB文件和输出TXT文件的路径
epub_file_path = 'input.epub'
txt_file_path = 'output.txt'

# 打开EPUB文件
book = epub.read_epub(epub_file_path)

# 定义一个函数来处理单个项目
def process_item(item):
    if isinstance(item, epub.EpubHtml):
        soup = BeautifulSoup(item.get_content(), 'html.parser')
        text = soup.get_text()
        return text
    else:
        return ''

# 使用多线程处理项目
with concurrent.futures.ThreadPoolExecutor() as executor:
    results = executor.map(process_item, book.items)

# 创建并打开TXT文件
with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
    for result in results:
        txt_file.write(result)
        txt_file.write('\n')

print(f'已将EPUB文件中的文本提取并保存到TXT文件：{txt_file_path}')
