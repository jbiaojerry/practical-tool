from gtts import gTTS

# 读取txt文件
txt_file = 'reame.txt'
with open(txt_file, 'r', encoding='utf-8') as file:
    txt_text = file.read()

# 使用gTTS生成中文语音
tts = gTTS(txt_text, lang='zh-cn')

# 保存中文语音文件
output_audio_file = 'output_audio_txt_01.mp3'
tts.save(output_audio_file)

# 打印成功消息
print(f'中文语音文件已生成：{output_audio_file}')
