import os
import threading
from gtts import gTTS

# 定义输入文本文件和输出音频文件
input_text_file = 'input.txt'
output_audio_file = 'output_audio_txt_ali.mp3'

# 读取大文本文件
with open(input_text_file, 'r', encoding='utf-8') as file:
    text = file.read()


# 分块处理的函数
def process_text_chunk(chunk):
    tts = gTTS(chunk, lang='zh-CN')  # 指定语言为中文
    tts.save(f'chunk_{threading.get_ident()}.mp3')


# 将文本分成多个块（每块1000字符）
chunk_size = 1000
text_chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

# 使用多线程处理文本块
threads = []
for chunk in text_chunks:
    thread = threading.Thread(target=process_text_chunk, args=(chunk, ))
    threads.append(thread)
    thread.start()

# 等待所有线程完成
for thread in threads:
    thread.join()

# 合并音频块
os.system(f'cat chunk_*.mp3 > {output_audio_file}')

# 删除临时音频块文件
for thread in threads:
    os.remove(f'chunk_{thread.ident}.mp3')

# 打印成功消息
print(f'音频文件已生成：{output_audio_file}')
