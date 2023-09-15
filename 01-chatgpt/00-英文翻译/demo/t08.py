#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 导入必要的库
from translate import Translator
import spacy
import json

# 第一部分：使用translate-python实现从本地文件中读取一段英文翻译成中文保存到本地
with open('english.txt', 'r') as file:
    english_text = file.read()

translator = Translator(to_lang="zh")
translation = translator.translate(english_text)

with open('chinese.txt', 'w') as file:
    file.write(translation)

# 第二部分：用spacy实现每个英语单词的词性，并将每个单词出现的词性，按照单词以json格式分类统计
nlp = spacy.load('en_core_web_sm')
doc = nlp(english_text)

word_pos = {}
for token in doc:
    if token.is_alpha:
        if token.text not in word_pos:
            word_pos[token.text] = []
        word_pos[token.text].append(token.pos_.lower())

# 输出英语单词在这段英文意境的中文翻译，并将结果保存在本地
word_translation = {
    word: translator.translate(word)
    for word in word_pos.keys()
}

with open('word_translation.json', 'w') as file:
    json.dump(word_translation, file)
