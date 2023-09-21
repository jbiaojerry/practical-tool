import os
import shutil
import ebooklib
from ebooklib import epub
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# 1. 数据准备
# 准备已知的epub文件和标签（用于训练模型）
known_epub_files = ["如何阅读一本书.epub", "高效沟通：如何让沟通精准有效.epub", "丰田精益管理：企业文化建设.epub"]
known_labels = ["学习类", "沟通类", "管理类"]

# 指定需要分类的epub文件所在的目录
classify_directory = "epub"

# 指定存储分类结果的目录
output_directory = "output"

# 2. 特征提取和模型训练
# 从epub文件中提取文本信息
def extract_text_from_epub(epub_file):
    book = epub.read_epub(epub_file)
    text = ""
    for item in book.items:
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            # 将字节数据解码为字符串
            text += item.content.decode('utf-8', 'ignore')
    return text

# 提取已知的epub文件的文本
known_texts = [extract_text_from_epub(file) for file in known_epub_files]

# 使用TF-IDF向量化文本
vectorizer = TfidfVectorizer()
X_known = vectorizer.fit_transform(known_texts)

# 训练朴素贝叶斯分类器
clf = MultinomialNB()
clf.fit(X_known, known_labels)

# 3. 遍历需要分类的epub目录并分类
for epub_file in os.listdir(classify_directory):
    if epub_file.endswith(".epub"):
        epub_file_path = os.path.join(classify_directory, epub_file)
        text = extract_text_from_epub(epub_file_path)
        
        # 使用已有模型进行分类
        X_new = vectorizer.transform([text])
        predicted_label = clf.predict(X_new)
        
        # 创建存储分类结果的目录
        category_directory = os.path.join(output_directory, predicted_label[0])
        os.makedirs(category_directory, exist_ok=True)
        
        # 移动epub文件到相应的目录
        new_file_path = os.path.join(category_directory, epub_file)
        shutil.move(epub_file_path, new_file_path)
        
        # 打印文件名、分类类型和移动路径
        print(f"文件名: {epub_file}, 分类类型: {predicted_label[0]}, 移动到: {new_file_path}")
