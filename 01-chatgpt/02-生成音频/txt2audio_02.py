from gtts import gTTS

# 读取txt文件
txt_file = 'reame.txt'
with open(txt_file, 'r', encoding='utf-8') as file:
    txt_text = file.read()

# 使用gTTS生成中文男声语音
tts = gTTS(txt_text, lang='zh-cn', tld='com', gender='male')

# 保存中文男声语音文件
output_audio_file = 'output_male_audio.mp3'
tts.save(output_audio_file)

# 打印成功消息
print(f'中文男声语音文件已生成：{output_male_audio_file}')
