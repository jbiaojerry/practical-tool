import asyncio
from gtts import gTTS
import multiprocessing

# 读取文本文件
txt_file_path = 'input.txt'
with open(txt_file_path, 'r', encoding='utf-8') as txt_file:
    text = txt_file.read()

# 定义一个异步函数来将文本转换为音频
async def text_to_audio_async(text_chunk, output_file_path):
    tts = gTTS(text_chunk, lang='zh-cn')  # 使用中文语音引擎
    tts.save(output_file_path)
    print(f'已将文本转换为音频文件：{output_file_path}')

# 将大文本分成多个小块
chunk_size = len(text) // 4  # 分成四块，可以根据需要调整
text_chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

# 创建一个多进程池，使用所有可用的核心
num_processes = multiprocessing.cpu_count()

# 使用异步循环
async def main():
    loop = asyncio.get_event_loop()
    tasks = []
    
    # 生成输出文件名
    output_files = [f'ali_{i}.mp3' for i in range(len(text_chunks))]
    
    # 使用多进程处理每个文本块
    with multiprocessing.Pool(num_processes) as pool:
        for text_chunk, output_file in zip(text_chunks, output_files):
            print("11111", output_file)
            task = loop.run_in_executor(None, text_to_audio_async, text_chunk, output_file)
            tasks.append(task)
    
    await asyncio.gather(*tasks)

# 运行异步事件循环
if __name__ == '__main__':
    asyncio.run(main())
    
print("所有文本块已转换为音频。")
