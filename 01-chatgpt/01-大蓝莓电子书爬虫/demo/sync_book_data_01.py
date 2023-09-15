#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import aiohttp
import openpyxl
from bs4 import BeautifulSoup


async def fetch_url(session, url):
    try:
        async with session.get(url) as response:
            return await response.text()
    except Exception as e:
        print(f"请求URL时发生错误: {url}, 错误信息: {str(e)}")
        return None


async def process_urls(start, end, workbook):
    base_url = "https://www.dalanmei.com/download-book-"

    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(start, end + 1):
            url = f"{base_url}{i}.html"
            tasks.append(fetch_url(session, url))

        responses = await asyncio.gather(*tasks)

        # 获取或创建工作表
        worksheet = workbook.active
        if start > 1:
            worksheet = workbook.create_sheet(title=f"Sheet_{start}_{end}")

        # 添加Excel表头
        worksheet.append(
            ["ID", "URL", "文件名", "MOBI下载链接", "EPUB下载链接", "AZW3下载链接"])

        # 处理响应数据
        for i, response_text in enumerate(responses):
            if response_text:
                soup = BeautifulSoup(response_text, "html.parser")
                h2_element = soup.find("h2")
                file_name = h2_element.text.strip()

                download_url_div = soup.find("div", id="download_url")
                #  mobi_link = download_url_div.find("a", text="MOBI格式下载")["href"]
                #  epub_link = download_url_div.find("a", text="EPUB格式下载")["href"]
                #  azw3_link = download_url_div.find("a", text="AZW3格式下载")["href"]
                #
                # 查找MOBI下载链接
                mobi_link_element = download_url_div.find("a",
                                                          string="MOBI格式下载")
                if mobi_link_element:
                    mobi_link = mobi_link_element.get("href")
                else:
                    mobi_link = "链接未找到"

                # 查找EPUB下载链接
                epub_link_element = download_url_div.find("a",
                                                          string="EPUB格式下载")
                if epub_link_element:
                    epub_link = epub_link_element.get("href")
                else:
                    epub_link = "链接未找到"

                # 查找AZW3下载链接
                azw3_link_element = download_url_div.find("a",
                                                          string="AZW3格式下载")
                if azw3_link_element:
                    azw3_link = azw3_link_element.get("href")
                else:
                    azw3_link = "链接未找到"

                # 文件名格式为id+文件名
                file_name_with_id = f"{start + i}_{file_name}"

                # 添加数据到Excel工作表
                worksheet.append([
                    start + i, f"{base_url}{start + i}.html",
                    file_name_with_id, mobi_link, epub_link, azw3_link
                ])
            else:
                print(f"URL {base_url}{start + i}.html 未能获取响应内容")


async def main():
    # 创建一个Excel工作簿
    workbook = openpyxl.Workbook()

    # 划分任务范围
    batch_size = 1000
    num_batches = 14

    for batch in range(num_batches):
        start = batch * batch_size + 1
        end = start + batch_size - 1
        await process_urls(start, end, workbook)

    # 保存Excel文件
    workbook.save("book_data_sync_01.xlsx")


if __name__ == "__main__":
    import time

    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    print(f"总耗时：{end_time - start_time} 秒")
