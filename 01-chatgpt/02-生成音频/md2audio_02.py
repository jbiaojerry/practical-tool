from gtts import gTTS
import markdown

# 读取Markdown文件
markdown_file = 'README.md'
with open(markdown_file, 'r', encoding='utf-8') as file:
    markdown_text = file.read()

# 将Markdown转换为HTML
html_text = markdown.markdown(markdown_text)

# 使用gTTS生成音频
tts = gTTS(html_text, lang='zh-cn')

# 保存音频文件
output_audio_file = 'output_audio_02.mp3'
tts.save(output_audio_file)

# 打印成功消息
print(f'音频文件已生成：{output_audio_file}')
