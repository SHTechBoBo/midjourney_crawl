import streamlit as st
import midjourney

# 在 Streamlit 应用程序中创建输入字段和按钮
user_input = st.text_input("请输入您想要的关键字：")
num_input = st.number_input("请输入您想要爬取的图片数量：", min_value=1, value=10)
submit_button = st.button("获取图片")

# 检查用户是否单击了提交按钮，然后运行主要功能
if submit_button:
    if user_input:
        zip_file_path = midjourney.category_search(user_input, num_input)  # 获取压缩文件的路径

        # 读取文件内容并创建下载按钮
        with open(zip_file_path, "rb") as f:
            file_content = f.read()
            st.download_button(
                label="点击下载压缩文件",
                data=file_content,
                file_name=f"{user_input}_images.zip",
                mime="application/zip"
            )
        st.success("图片已成功下载！")
    else:
        st.error("请输入有效的关键字！")

# 要运行此文件，请在终端中输入：streamlit run app.py
