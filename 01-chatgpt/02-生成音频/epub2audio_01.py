import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import pyttsx3
import os

# 定义epub文件路径和输出音频文件路径
epub_file = 'ali.epub'
output_audio_file = 'output_audio_epub_01.mp3'

# 打开epub文件
book = epub.read_epub(epub_file)

# 提取epub文件中的文本
text = ''
for item in book.get_items():
    if isinstance(item, epub.EpubHtml):
        content = item.content
        soup = BeautifulSoup(content, 'html.parser')
        text += soup.get_text() + '\n'

# 初始化文本到语音引擎
engine = pyttsx3.init()

# 将文本转换为语音
engine.save_to_file(text, output_audio_file)

# 等待语音引擎完成转换
engine.runAndWait()

# 打印成功消息
print(f'音频文件已生成：{output_audio_file}')
