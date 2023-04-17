from Requester import Requester
from ImageDownloader import ImageDownloader
import os
import threading
import concurrent.futures

with open('cookie.txt', 'r', encoding='utf-8') as in_file:
    cookie = in_file.read()

proxies = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890',
}

Midjourney_Requester = Requester(cookie=cookie, referer="https://www.midjourney.com/app/feed/")
# Midjourney_Requester = Requester(cookie=cookie, referer="https://www.midjourney.com/app/feed/", proxy=proxies)


search_api = "https://www.midjourney.com/api/app/vector-search/?amount=500&dedupe=true&jobStatus=completed" \
             "&jobType=upscale&orderBy=hot&prompt={}&refreshApi=0&searchType=vector&service=null" \
             "&user_id_ranked_score=null&_ql=todo&_qurl=https://www.midjourney.com/app/search/?search={}"


# 定义一个函数，用于下载图片和保存相关信息
def download_image(folder_name, key, index, info, requester):
    try:
        # 根据关键字和索引创建图片名称
        image_name = f"{key}_{index}"

        # 使用 ImageDownloader 下载图片并保存到指定文件夹
        ImageDownloader(url=info['image_paths'][0], name=image_name,
                        path=folder_name, requester=requester).download()

        # 将图片相关信息保存到文本文件
        with open(os.path.join(folder_name, f"{image_name}.txt"), "w", encoding="utf-8") as out_file:
            out_file.write(f"model: {info['_job_type']}\n")
            out_file.write(f"prompt: {info['full_command']}\n")

    except KeyError:
        pass


def get_key_images(key: str, max_images: int = 10):
    global Midjourney_Requester

    # 获取请求数据
    infos = Midjourney_Requester.get_request(search_api.format(key, key)).json()

    # 创建一个文件夹
    folder_name = f"{key}"
    os.makedirs(folder_name, exist_ok=True)

    # 使用ThreadPoolExecutor创建一个线程池，限制同时运行的线程数量
    with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        # 提交任务给线程池
        tasks = [executor.submit(download_image, folder_name, key, index, info, Midjourney_Requester)
                 for index, info in enumerate(infos, start=1) if index <= max_images]

        # 等待所有任务完成
        for _ in concurrent.futures.as_completed(tasks):
            pass

    # 返回文件夹的绝对路径
    return os.path.abspath(folder_name)
