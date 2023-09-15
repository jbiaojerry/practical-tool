import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import pyttsx3
import concurrent.futures

# 定义epub文件路径和输出音频文件路径
epub_file = 'ali.epub'
output_audio_file = 'output_audio_epub_02.mp3'

# 打开epub文件
book = epub.read_epub(epub_file)

# 提取epub文件中的章节列表
chapters = [item for item in book.get_items() if isinstance(item, epub.EpubHtml)]

# 初始化文本到语音引擎
engine = pyttsx3.init()

# 定义处理章节的函数
def process_chapter(chapter):
    content = chapter.content
    soup = BeautifulSoup(content, 'html.parser')
    text = soup.get_text()
    return text

# 使用多线程处理章节
with concurrent.futures.ThreadPoolExecutor() as executor:
    chapter_texts = list(executor.map(process_chapter, chapters))

# 合并章节文本
text = '\n'.join(chapter_texts)

# 将文本转换为音频
engine.save_to_file(text, output_audio_file)

# 等待语音引擎完成转换
engine.runAndWait()

# 打印成功消息
print(f'音频文件已生成：{output_audio_file}')
