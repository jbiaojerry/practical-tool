import os
import pandas as pd
import shutil

# 指定原始epub文件所在路径
epub_directory = 'epub'
# Excel文件路径
excel_file = '03-dalanmei_books_by_tags.xlsx'
# 指定存放结果的目标目录
target_directory = 'organized_epub'

# 删除指定目录下所有 "._" 文件
for root, dirs, files in os.walk(epub_directory):
    for filename in files:
        if filename.startswith("._"):
            file_path = os.path.join(root, filename)
            os.remove(file_path)

print("已删除所有 '._' 文件")

# 创建目标目录（如果不存在）
os.makedirs(target_directory, exist_ok=True)

# 读取Excel文件
excel_data = pd.read_excel(excel_file, sheet_name=None)  # 读取所有sheet

# 创建字典来跟踪已重命名的文件
renamed_files = {}

# 遍历epub目录下的文件
for root, dirs, files in os.walk(epub_directory):
    for filename in files:
        if filename.endswith('.epub'):
            # 解析文件名，获取数字编号
            file_parts = filename.split('-')
            if len(file_parts) > 0:
                try:
                    numeric_id = int(file_parts[0])
                    sheet_name = None
                    # 遍历所有sheet查找匹配的记录
                    for sheet, df in excel_data.items():
                        if 'ID' in df.columns and '书名' in df.columns:
                            record = df[df['ID'] == numeric_id]
                            if not record.empty:
                                sheet_name = sheet
                                break
                    if sheet_name:
                        book_name = record.iloc[0]['书名']
                        # 创建目录
                        new_directory = os.path.join(target_directory, sheet_name)
                        os.makedirs(new_directory, exist_ok=True)
                        # 构建新的文件名
                        new_filename = f'{numeric_id}-{book_name}.epub'
                        
                        # 处理文件名重复的情况
                        if new_filename in renamed_files:
                            renamed_files[new_filename] += 1
                            base_filename, extension = os.path.splitext(new_filename)
                            new_filename = f'{base_filename}-{renamed_files[new_filename]}{extension}'
                        else:
                            renamed_files[new_filename] = 0
                        
                        # 移动文件到目标目录
                        source_path = os.path.join(root, filename)
                        destination_path = os.path.join(new_directory, new_filename)
                        shutil.move(source_path, destination_path)
                        print(f'已将文件 {filename} 移动到目录 {new_directory}，并重命名为 {new_filename}')
                    else:
                        print(f'未找到ID为 {numeric_id} 的记录')
                except ValueError:
                    print(f'文件名 {filename} 不符合命名规范')
