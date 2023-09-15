from gtts import gTTS
import concurrent.futures
import asyncio

# 读取文本文件
txt_file_path = 'input.txt'
with open(txt_file_path, 'r', encoding='utf-8') as txt_file:
    text = txt_file.read()

# 定义一个函数来将文本转换为音频
def text_to_audio(text_chunk):
    tts = gTTS(text_chunk, lang='zh-cn')  # 使用中文语音引擎
    audio_file_path = 'output_ali_04.mp3'  # 输出的音频文件路径
    tts.save(audio_file_path)
    print(f'已将文本转换为音频文件：{audio_file_path}')

# 将大文本分成多个小块
chunk_size = len(text) // 4  # 分成四块，可以根据需要调整
text_chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

# 使用多线程处理每个文本块
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(text_to_audio, chunk) for chunk in text_chunks]

# 等待所有任务完成
concurrent.futures.wait(futures)

# 使用异步编程来处理
async def async_text_to_audio(text_chunk):
    loop = asyncio.get_event_loop()
    future = loop.run_in_executor(None, text_to_audio, text_chunk)
    await asyncio.wait([future])

async def main():
    await asyncio.gather(*(async_text_to_audio(chunk) for chunk in text_chunks))

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
