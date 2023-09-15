import spacy

# 加载spaCy的英语模型
nlp = spacy.load("en_core_web_sm")

# 输入包含单词的文本
text = "This is an example sentence with the word 'example'."

# 处理文本
doc = nlp(text)

# 找到目标单词的上下文及其词性
target_word = "example"
for token in doc:
    if token.text == target_word:
        context = [t.text for t in token.sent]
        pos_tags = [t.pos_ for t in token.sent]
        print(f"Word: {token.text}")
        print(f"Context: {context}")
        print(f"POS Tags: {pos_tags}")

