import streamlit as st
import MidjourneyCrawl
import Utility
import time
import re

# 创建一个表单
with st.form("download_form"):
    key_input = st.text_input("Enter the keyword:", value="Tiamat")
    num_input = st.number_input("Enter the number of images:", min_value=1, max_value=500, value=1)
    # 将提交按钮放在表单内部
    submit_button = st.form_submit_button("Get Images")

# 当提交按钮被按下时
if submit_button:
    # 如果输入不为空
    if key_input:
        # 如果输入仅包含英文字符、数字和标点符号
        if re.match(r'^[a-zA-Z0-9\s!"#$%&\'()*+,\-./:;<=>?@\[\\\]^_`{|}~]*$', key_input):

            # 显示开始爬取的信息
            st.success(f"Start Crawl!")
            # 记录开始时间
            start_time = time.time()

            # 调用爬虫函数下载图片
            file_path = MidjourneyCrawl.get_key_images(key_input, num_input)
            # 压缩文件夹并返回文件路径
            zip_file_path = Utility.create_zip_file(file_path, key_input)

            # 记录结束时间
            end_time = time.time()
            # 计算耗时
            elapsed_time = end_time - start_time

            # 读取压缩文件内容并创建下载按钮
            with open(zip_file_path, "rb") as file:
                file_content = file.read()
                st.download_button(
                    label="Download ZIP",
                    data=file_content,
                    file_name=f"{key_input}.zip",
                    mime="application/zip"
                )

            # 显示下载成功及耗时信息
            st.success(f"Download Successfully! {elapsed_time:.2f} Seconds")
        else:
            # 如果输入包含非法字符，则显示错误信息
            st.error("Only English characters, numbers, and punctuation are allowed!")
    else:
        # 如果输入为空，则显示错误信息
        st.error("Invalid Input!")

# 要运行此文件，请在终端中输入：streamlit run app.py
