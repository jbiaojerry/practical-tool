import openai

# 替换为您自己的API密钥
api_key = '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'

# 读取Markdown文件
markdown_file = 'README.md'
with open(markdown_file, 'r', encoding='utf-8') as file:
    markdown_text = file.read()

# 调用OpenAI API生成语音
response = openai.Completion.create(
    engine="davinci",  # 使用GPT-3或GPT-4模型
    prompt=markdown_text,
    max_tokens=10000,  # 调整生成的语音长度
    api_key=api_key
)

# 提取生成的语音
audio_output = response.choices[0].text

# 保存音频文件
output_audio_file = 'output_audio.mp3'
with open(output_audio_file, 'wb') as audio_file:
    audio_file.write(audio_output.encode('utf-8'))

# 打印成功消息
print(f'音频文件已生成：{output_audio_file}')
