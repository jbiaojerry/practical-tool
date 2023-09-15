#!/usr/bin/env python
# -*- coding: utf-8 -*-

import spacy

# 加载spaCy的英语模型
nlp = spacy.load("en_core_web_sm")

# 输入要分析的文本
text = "The quick brown fox jumps over the lazy dog. Cats are cute and playful."

# 使用spaCy处理文本
doc = nlp(text)

# 分句
sentences = list(doc.sents)

# 遍历每个句子
for i, sentence in enumerate(sentences):
    print(f"Sentence {i + 1}: {sentence.text}")

    # 分词和词性标注
    for token in sentence:
        print(f"Token: {token.text}")
        print(f"Part of Speech (Coarse-grained): {token.pos_}")
        print(f"Part of Speech (Fine-grained): {token.tag_}")
        print(f"Dependency Relation: {token.dep_}")
        print("------")

# 过滤名词和动词
nouns = [token.text for token in doc if token.pos_ == "NOUN"]
verbs = [token.text for token in doc if token.pos_ == "VERB"]

print("Nouns:", nouns)
print("Verbs:", verbs)

# 查找特定依赖关系
target_relation = "prep"
target_tokens = [token.text for token in doc if token.dep_ == target_relation]

print(f"Tokens with dependency relation '{target_relation}': {target_tokens}")

