import os

def count_downloads_in_md_files(md_directory):
    download_counts = {}

    for filename in os.listdir(md_directory):
        if filename.endswith('.md'):
            tag_name = os.path.splitext(filename)[0]
            md_file_path = os.path.join(md_directory, filename)
            with open(md_file_path, 'r', encoding='utf-8') as md_file:
                content = md_file.read()
                download_count = content.count('下载')
                download_counts[tag_name] = download_count - 2

    return download_counts

def write_counts_to_readme(download_counts, readme_path):
    with open(readme_path, 'w', encoding='utf-8') as readme_file:
        markdown_content = """\
<p align="center">
<img src=".github/logo.png" alt="Project Logo">
</p>

# 电子书下载宝库

![GitHub](https://img.shields.io/github/license/jbiaojerry/ebook-treasure-chest)
![GitHub stars](https://img.shields.io/github/stars/jbiaojerry/ebook-treasure-chest?style=social)
![GitHub forks](https://img.shields.io/github/forks/jbiaojerry/ebook-treasure-chest?style=social)

欢迎来到电子书下载宝库，一个汇聚了各类电子书下载链接的地方。无论你是喜欢阅读经典文学、经管励志、终身学习、职场创业、技术手册还是其他类型的书籍，这里都能满足你的需求。
该库涵盖了帆书app(原樊登读书)、微信读书、京东读书、喜马拉雅等读书app的大部分电子书。

## 简介

我们从各个电子书网站上精心收集了各种电子书下载链接，并根据常用的标签对它们进行了简单分类。每本书都包括了三种常见格式文件：epub、mobi 和 azw3，以满足不同阅读设备和喜好的需求。

## 如何使用

浏览我们的下载宝库非常简单：
1. 在下方目录索引点击关键词或者“Ctrl+F”搜索标签，以找到你感兴趣的电子书类型;
2. 点击标签或搜索结果，即可进入详细的下载链接页面，点击书名可以查看图书封面;
3. 在下载链接页面，你将找到包含epub、mobi、azw3格式的下载链接，点击下载即可。

## 支持我们

如果你有电子书资源想要分享，或者发现了链接失效或有其他问题，请不要犹豫，立刻提出问题或贡献你的资源。我们欢迎任何形式的贡献，让这个宝库变得更加丰富和有用。

## 许可证

该项目基于开源许可证（例如，MIT许可证）发布。请查看 [LICENSE](LICENSE) 文件以获取详细信息。

![Happy Reading](https://media.giphy.com/media/l2SpQRuiLWz8K/giphy.gif)

让我们一起享受阅读的乐趣吧！如果你喜欢这个项目，请不要忘记给它点个星星⭐️以表示支持。感谢你的参与和支持！
            """
        readme_file.write(markdown_content)
        # 在总目录README.md中创建带锚点链接的工作表列表
        readme_file.write('\n\n\n# 索引目录\n\n') 
        # 每 8 个标签分为一行
        line = []
        for tag_name, count in download_counts.items():
            line.append(f'- [{tag_name}({count})](md/{tag_name}.md) ')
            if len(line) == 8:  # 每 8 个标签分为一行
                readme_file.write(' | '.join(line) + '\n')
                line = []  # 清空当前行

        # 写入剩余的标签
        if line:
            readme_file.write(' | '.join(line) + '\n')

# 使用示例
md_directory = 'ebooks/md'  # 替换为你的 Markdown 文件目录
readme_path = 'ebooks/README.md'  # README 文件的路径

download_counts = count_downloads_in_md_files(md_directory)
download_counts_desc = dict(sorted(download_counts.items(), key=lambda item: item[1], reverse=True))
write_counts_to_readme(download_counts_desc, readme_path)

print(f"下载统计已写入 '{readme_path}' 文件。")
