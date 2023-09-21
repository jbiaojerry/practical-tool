import os
import shutil
import ebooklib
from ebooklib import epub
from gensim.models import Word2Vec
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
import numpy as np
import re  # 导入正则表达式库

# 1. 数据准备
# 准备已知的epub文件和标签（用于训练模型）
known_epub_files = ["如何阅读一本书.epub", "高效沟通：如何让沟通精准有效.epub", "丰田精益管理：企业文化建设.epub"]
known_labels = ["学习类", "沟通类", "管理类"]

# 指定需要分类的epub文件所在的目录
classify_directory = "epub"  # 这里假设您的epub文件存放在一个名为"epub"的目录下

# 指定存储分类结果的目录
output_directory = "output"

# 2. 特征提取和模型训练
# 从epub文件中提取文本信息
def extract_text_from_epub(epub_file):
    book = epub.read_epub(epub_file)
    text = ""
    for item in book.items:
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            # 将字节数据解码为字符串，并进行预处理
            content = item.content.decode('utf-8', 'ignore')
            content = re.sub(r'[^\w\s]', '', content)  # 删除特殊字符
            content = content.strip()  # 删除多余的空格
            text += content
    return text

# 提取已知的epub文件的文本
known_texts = [extract_text_from_epub(file) for file in known_epub_files]

# 使用Word2Vec词嵌入来提取文本特征
word2vec_model = Word2Vec([text.split() for text in known_texts], vector_size=100, window=5, min_count=1, sg=1)
word_vectors = word2vec_model.wv

# 训练一个多分类SVM模型
classifier = SVC(kernel='linear', C=1, decision_function_shape='ovr')
le = LabelEncoder()
known_labels_encoded = le.fit_transform(known_labels)

X_known = [np.mean([word_vectors[word] for word in text.split() if word in word_vectors], axis=0) for text in known_texts]

# 3. 模型训练
classifier.fit(X_known, known_labels_encoded)

# 4. 遍历需要分类的epub目录并分类
for epub_file in os.listdir(classify_directory):
    if epub_file.endswith(".epub"):
        epub_file_path = os.path.join(classify_directory, epub_file)
        text = extract_text_from_epub(epub_file_path)
        
        # 使用Word2Vec词嵌入提取特征
        text_vector = np.mean([word_vectors[word] for word in text.split() if word in word_vectors], axis=0)
        
        # 使用模型进行分类
        predicted_label_encoded = classifier.predict([text_vector])[0]
        predicted_label = le.inverse_transform([predicted_label_encoded])
        
        # 创建存储分类结果的目录
        category_directory = os.path.join(output_directory, predicted_label[0])
        os.makedirs(category_directory, exist_ok=True)
        
        # 移动epub文件到相应的目录
        new_file_path = os.path.join(category_directory, epub_file)
        shutil.move(epub_file_path, new_file_path)
        
        # 打印文件名、分类类型和移动路径
        print(f"文件名: {epub_file}, 分类类型: {predicted_label[0]}, 移动到: {new_file_path}")
