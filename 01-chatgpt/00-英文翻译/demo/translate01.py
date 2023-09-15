#!/usr/bin/env python
# -*- coding: utf-8 -*-


from translate import Translator
import spacy

# 从本地文件读取英文文本
with open('input.txt', 'r', encoding='utf-8') as file:
    english_text = file.read()

# 创建翻译器对象，将目标语言设置为中文
translator = Translator(to_lang="zh")

# 使用翻译器进行翻译
chinese_translation = translator.translate(english_text)

# 将中文翻译保存到本地文件
with open('translation.txt', 'w', encoding='utf-8') as translation_file:
    translation_file.write(chinese_translation)

# 使用 spaCy 加载英语模型
nlp = spacy.load("en_core_web_sm")

# 处理英文文本并获取词性
doc = nlp(english_text)

# 将词性分析结果保存到本地文件
with open('pos_analysis.txt', 'w', encoding='utf-8') as pos_file:
    for token in doc:
        pos_file.write(f"{token.text}\t")
    for token in doc:
        pos_file.write(f"{token.pos_}\t")

print("Translation and POS analysis completed. Results saved to files.")

