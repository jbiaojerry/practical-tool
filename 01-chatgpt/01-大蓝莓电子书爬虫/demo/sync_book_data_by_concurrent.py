#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import requests
import concurrent.futures
import openpyxl
from bs4 import BeautifulSoup


# 爬取单个URL的函数
def fetch_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"请求URL时发生错误: {url}, 错误信息: {str(e)}")
        return None


# 解析并保存数据的函数
def process_data(data, worksheet, start):
    if data:
        soup = BeautifulSoup(data, "html.parser")
        h2_element = soup.find("h2")
        file_name = h2_element.text.strip()

        download_url_div = soup.find("div", id="download_url")
        mobi_link_element = download_url_div.find("a", string="MOBI格式下载")
        epub_link_element = download_url_div.find("a", string="EPUB格式下载")
        azw3_link_element = download_url_div.find("a", string="AZW3格式下载")

        mobi_link = mobi_link_element.get(
            "href") if mobi_link_element else "链接未找到"
        epub_link = epub_link_element.get(
            "href") if epub_link_element else "链接未找到"
        azw3_link = azw3_link_element.get(
            "href") if azw3_link_element else "链接未找到"

        # 文件名格式为id+文件名
        file_name_with_id = f"{start}_{file_name}"

        # 添加数据到Excel工作表（仅当EPUB链接存在时）
        if epub_link != "链接未找到":
            worksheet.append([
                start, f"https://www.dalanmei.com/download-book-{start}.html",
                file_name_with_id, mobi_link, epub_link, azw3_link
            ])
    else:
        print(
            f"URL https://www.dalanmei.com/download-book-{start}.html 未能获取响应内容"
        )


def main():
    # 创建一个Excel工作簿
    workbook = openpyxl.Workbook()
    worksheet = workbook.active

    # 添加Excel表头
    worksheet.append(["ID", "URL", "文件名", "MOBI下载链接", "EPUB下载链接", "AZW3下载链接"])

    # 划分任务范围
    num_urls = 13385
    batch_size = 1000
    num_batches = (num_urls + batch_size - 1) // batch_size

    with concurrent.futures.ProcessPoolExecutor(
            max_workers=os.cpu_count()) as executor:
        futures = []

        for batch in range(num_batches):
            start = batch * batch_size + 1
            end = min(start + batch_size, num_urls + 1)

            urls = [
                f"https://www.dalanmei.com/download-book-{i}.html"
                for i in range(start, end)
            ]

            # 并行处理URL
            for url in urls:
                future = executor.submit(fetch_url, url)
                futures.append((future, start))

        # 处理完成的数据
        for future, start in futures:
            data = future.result()
            process_data(data, worksheet, start)

    # 保存Excel文件
    workbook.save("book_data_by_concurrent_01.xlsx")


if __name__ == "__main__":
    import time

    start_time = time.time()
    main()
    end_time = time.time()
    print(f"总耗时：{end_time - start_time} 秒")
