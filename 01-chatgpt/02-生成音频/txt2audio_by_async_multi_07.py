from gtts import gTTS
from pydub import AudioSegment
import multiprocessing
import os

# 读取文本文件
txt_file_path = 'input.txt'
with open(txt_file_path, 'r', encoding='utf-8') as txt_file:
    text = txt_file.read()

# 定义一个函数来将文本转换为音频
def text_to_audio(text_chunk, output_file_path):
    # tts = gTTS(text_chunk, lang='zh-cn', slow=False)  # 使用默认引擎
    tts = gTTS(text_chunk, lang='zh-cn', tld='com', lang_check=True, slow=False)
    tts.save(output_file_path)

if __name__ == '__main__':
    # 将大文本分成多个小块
    chunk_size = len(text) // 20  # 分成四块，可以根据需要调整
    text_chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

    # 创建一个多进程池，使用所有可用的核心
    num_processes = multiprocessing.cpu_count()

    # 生成输出文件名
    output_files = [f'output_{i}.mp3' for i in range(len(text_chunks))]

    # 使用多进程处理每个文本块
    with multiprocessing.Pool(num_processes) as pool:
        for text_chunk, output_file in zip(text_chunks, output_files):
            # 确保文本块不为空
            if text_chunk.strip():
                pool.apply(text_to_audio, args=(text_chunk, output_file))
                
    # 合并音频块
    audio_segments = []
    for output_file in output_files:
        if os.path.exists(output_file):
            audio_segments.append(AudioSegment.from_mp3(output_file))
        else:
            print(f"文件 {output_file} 不存在，已跳过。")

    # 保存合并后的音频
    combined_audio = sum(audio_segments)
    combined_audio.export('output_combined.mp3', format='mp3')

    # 删除临时生成的文本块文件
    for output_file in output_files:
        if os.path.exists(output_file):
            os.remove(output_file)

    print("所有文本块已转换并合并为音频，临时文件已删除。")


