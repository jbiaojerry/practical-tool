from translate import Translator
import spacy
from collections import defaultdict
import json

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

# 统计每个英语单词的词性和中文翻译
word_pos_counts = defaultdict(lambda: {"pos": set()})
for token in doc:
    word = token.text
    pos = token.pos_.lower()
    word_pos_counts[word]["pos"].add(pos)

# 将词性统计结果保存为 JSON 格式到本地文件
result_dict = {}
for word, data in word_pos_counts.items():
    result_dict[word] = {
        "pos": list(data["pos"]),
    }

with open('word_pos_counts.json', 'w', encoding='utf-8') as json_file:
    json.dump(result_dict, json_file, ensure_ascii=False, indent=2)

print(
    "Translation, POS analysis, and word POS counts completed. Results saved to files."
)
