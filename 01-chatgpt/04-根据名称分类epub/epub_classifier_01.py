import os
import ebooklib
from ebooklib import epub
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# 1. 数据准备
# 假设您已经有一些epub文件和它们的标签
epub_files = ["如何阅读一本书.epub", "高效沟通：如何让沟通精准有效.epub", "丰田精益管理：企业文化建设.epub"]
labels = ["学习类", "沟通类", "管理类"]

# 2. 特征提取
# 从epub文件中提取文本信息
def extract_text_from_epub(epub_file):
    book = epub.read_epub(epub_file)
    text = ""
    for item in book.items:
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            # 将字节数据解码为字符串
            text += item.content.decode('utf-8', 'ignore')
    return text

# 提取文本
texts = [extract_text_from_epub(file) for file in epub_files]

# 3. 训练模型
# 使用TF-IDF向量化文本
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

# 划分数据集为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.2, random_state=42)

# 训练朴素贝叶斯分类器
clf = MultinomialNB()
clf.fit(X_train, y_train)

# 4. 预测
# 预测新的epub文件
new_epub_file = "德鲁克论领导力：现代管理学之父的新教诲.epub"
new_text = extract_text_from_epub(new_epub_file)
X_new = vectorizer.transform([new_text])
predicted_label = clf.predict(X_new)

print("预测的书籍类型:", predicted_label[0])



