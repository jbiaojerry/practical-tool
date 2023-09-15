#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
import spacy

# 加载spaCy的英语模型
nlp = spacy.load("en_core_web_sm")

# 创建 Flask 应用程序
app = Flask(__name__)


# 定义一个路由来处理单词词性的请求
@app.route('/get_pos', methods=['GET'])
def get_word_pos():
    # 从请求参数中获取单词
    word = request.args.get('word')

    if word:
        # 处理单词并获取词性
        doc = nlp(word)
        pos = [token.pos_ for token in doc]

        # 构建响应
        response = {
            'word': word,
            'pos': pos
        }
        return jsonify(response)
    else:
        return jsonify({'error': 'Please provide a word in the "word" parameter.'})


if __name__ == '__main__':
    # 运行应用程序
    app.run(debug=True)
