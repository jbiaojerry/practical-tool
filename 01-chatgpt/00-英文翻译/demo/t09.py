#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import spacy
from collections import defaultdict

# 读取翻译字典
with open('word_translation.json', 'r') as f:
    translation_dict = json.load(f)

# 读取英文文本
with open('english.txt', 'r') as f:
    english_text = f.read()

# 翻译英文文本
translated_text = ' '.join(
    translation_dict.get(word, word) for word in english_text.split())

# 将翻译后的文本保存到本地
with open('translated_text.txt', 'w') as f:
    f.write(translated_text)

# 加载spacy的英文模型
nlp = spacy.load('en_core_web_sm')

# 对英文文本进行处理
doc = nlp(english_text)

# 创建一个字典来统计每个单词的词性
word_pos_dict = defaultdict(list)

for token in doc:
    # 只统计英文单词
    if token.text.isalpha():
        word_pos_dict[token.text.lower()].append(token.pos_.lower())

# 将结果保存到本地
with open('word_pos_09.json', 'w') as f:
    json.dump(word_pos_dict, f)
