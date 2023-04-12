import streamlit as st
import midjourney

# 在 Streamlit 应用程序中创建输入字段和按钮
user_input = st.text_input("请输入您想要的关键字：")
image_count_input = st.text_input("请输入您想要爬取的图片数量：")
submit_button = st.button("获取图片")

# 检查用户是否单击了提交按钮，然后运行主要功能
if submit_button:
    if user_input and image_count_input.isdigit():
        image_count = int(image_count_input)
        path = midjourney.category_search(user_input, image_count)  # 将图片数量传递给 category_search 函数
        st.success("图片已成功下载！保存在{}".format(path))
    else:
        st.error("请输入有效的关键字和图片数量！")

# 要运行此文件，请在终端中输入：streamlit run app.py
