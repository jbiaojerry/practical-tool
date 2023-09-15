from translate import Translator
import spacy
import json

# 1. 从本地文件中读取英文文本
with open('input.txt', 'r', encoding='utf-8') as file:
    english_text = file.read()

# 创建翻译器对象，将目标语言设置为中文
translator = Translator(to_lang="zh")

# 2. 使用翻译器进行翻译
chinese_translation = translator.translate(english_text)

# 将中文翻译保存到本地文件
with open('translation.txt', 'w', encoding='utf-8') as translation_file:
    translation_file.write(chinese_translation)

# 使用 spaCy 加载英语模型
nlp = spacy.load("en_core_web_sm")

# 用于存储每个英语单词的中文翻译和词性的字典
word_data = {}

# 3. 处理英文文本并获取每个英语单词的词性和中文翻译
for token in nlp(english_text):
    # 仅处理英语单词
    if token.is_alpha:
        word = token.text.lower()
        # 检查是否已经有该单词的翻译，避免重复翻译
        if word not in word_data:
            chinese_translation = translator.translate(word)
            pos = token.pos_
            word_data[word] = {
                "pos": pos.lower(),  # 词性转为小写字母表示
                "chinese_translation": chinese_translation
            }

# 4. 将每个英语单词的中文翻译和词性保存为 JSON 格式到本地文件
with open('word_data.json', 'w', encoding='utf-8') as json_file:
    json.dump(word_data, json_file, ensure_ascii=False, indent=2)

print("Translation, Word translations, and POS analysis completed. Results saved to files.")
 
