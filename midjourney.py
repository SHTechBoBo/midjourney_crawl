import json
import os
import time
import random
import tempfile
import shutil
import zipfile

import requests
from concurrent.futures import ThreadPoolExecutor
import re

keys = ["luxury product"]

api_url = "https://www.midjourney.com/api/app/vector-search/?amount=500&dedupe=true&jobStatus=completed&jobType" \
          "=upscale&orderBy=hot&prompt={}&refreshApi=0&searchType=vector&service=null&user_id_ranked_score=null&_ql" \
          "=todo&_qurl=https://www.midjourney.com/app/search/?search={}"

user_id = "cc149883-fa3c-4cd7-9256-4da6020fe309"
cookie = "imageSize=medium; imageLayout_2=hover; getImageAspect=2; fullWidth=false; showHoverIcons=true; " \
         "_ga=GA1.1.1458977405.1681269111; " \
         "__Host-next-auth.csrf-token=4989e5bcd6955914556ae8404f578dfe8c895e1b705ce75d9f1e30909c20f389" \
         "|b52373e1869f817a3671739d68aa08523089dc11c4851b77c99f2b25653bc699; " \
         "__Secure-next-auth.callback-url=https://www.midjourney.com/app/; _dd_s=rum=0&expire=1681271435923; " \
         "__Secure-next-auth.session-token=eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..kmlp9NiLe7ijGCYv" \
         ".fR2T8QhR7Ykyvf2yyvGcd9H8le7eEv2_gRe8bpRePKHNcSbym7VDqlVIowNWYoUPdqdbYJiClepbYqDSZ2Yr6EGANsDB__" \
         "YDOCv8OFaVDN_dF0aC_jF8Yf1RPbFX8M-0DNjj2jPuYd_Q0a-aY6rJ9VOJq02k6iR3nQSoOruXJSWREINSm2AtoC5tQ4kycmOqbxO" \
         "ZpQLUzLv9-n7ZC7INrXbZmLDc6zwhJSlH9SGnwsooTi_bg16EKMW6UnvbRSGUixEMdjpslTE3vg8ds5-JCPDAOhl2eqQNIBAKxZ1IAg" \
         "4BUa1cHo0Q7UY3pZOn4dbLYk9xgsXFuTRzBCyWfYs0DsDImA4bA5zoVJKxbYYiRc-N7c6tUXXaQIrB9nLC5Gdmdpqiargbzp2-1hh4-8" \
         "feHY3S4HN8Qu3onIbahShou9g2h4eqDspV-bEOdIe0Ge5HGhfd1RfU3KUrdt0Tj-3C451xzz1fICuFdBI9BS8LaYNKjfcFQTmPXaIjEqTc" \
         "x51JW9zwIOoDPH5wH0DuHAAQK5yPmJEP4HGQTIfhSKuQCVkjudACAVuQTJXGv4mW2m1Ih4dcnBvibys2gTGZMACtPSSr1keXjo49bJ14Si" \
         "cOuyDK1HHImX29a1B45HWUg3Jf6qBf6rIJIxjNfjDJJ3u8Eh3_IfXeWlum8LJDuRrRGVdB7_-6gx5oAKUtqGoYa5TzmD7vNDR09AMF6rfHdU" \
         "LUCPPLWxzuADNOJiFl3SUwKZ-yhSqYsOAfJVMhRZO9irAi3xlBJnH6jLhseRSRJBYs4-u0I3pRjhjCLJgaapnmyVTjX3ufU" \
         "-0FbpRPgDmfU8gkCa4rYTez58g_0hAU733JoQAew5pQB5xqISzyuT8IhQDVWvGuF8VGZfxii6xHdGyxyL3od7C_AO8IIbtKo_" \
         "-RfdydBn2ihfsVANQQjG7zc4LmidOhZGvY2BH2YzQBbRomQFvx2udLtOA9oiFwpm-qxG_P5YYZkcOqaqbXpfUGoTY_SJg-1YqAWqRCkoa" \
         "-lq6AFYBKuJYhW7fP-BC-IYO4L2gPN6cNvBBOAPHTE6Mclfpgi8l6-6GnPPjIbXFnIdBZYky9G" \
         "-vGu5ZatewY4U9n5N_39xDBJus4UmagsKkOU0Ziq95Rv2ju3dnfBx3IkuynbMp8yORboXfVBVbx" \
         "-h2uSlJZaEKit3laA2QLc7Q38DgxODIY9Tki0jKeVKRLmm17vjgVin5ZudlY8kGscwC3VVKXBX7kOnuJicvzehR2KHNFDFL91uUpTxsNA950" \
         "nmdWBL7D_axgpoQArWgy3nvgJee4jLWADou7n_5HuxaJuw1CzSgoSdJIUV987fy9KNoeDmg-4yiYy2UhnLppLzB3hJjUmJtukkiFiX6OqU" \
         "-Msbogc1R0-dPh7KAk6zYok2j8q8wzWtknog7iFaY0uturQJqyDRVW44xpK2I6rW8apsypOdsL4lMzGfrhCrxhiBBulNI6ix" \
         "-wgR3LIrkW_GKugAAkIJuJ5FU4dleDHA9OMv94i0FfdKZYsMXHLbRQG" \
         "-dYzEUzePBmd_WjAfC3lCfE3dyy4CTLrNpDHaQA0_1qoAnIjZuelLqBOyfqQDf-mBXTDPt1YK8KkcV0CmCqYi0hzg2R19h4DDBqf" \
         "--MUuRcDN8SD6UvILPXHHiY2j8vnF6EFttj1LYzda8BJLpBMfvt_9g7F_UvCq" \
         "-DgsEcDR6VLYwUrTRVlNzULr1_LRm5w_zs7xTUTtFmI5B_R-9n-U0l9kbLfM1oQ2qnJBkdrtg6Q398pdu1LiqV" \
         "-k7gqHmHqvdssYeCz9r9m1y_YEZ9pN_4G5_RhJQEe7HjUlTZ3sRxsThyiCyw3QXfxUcyreQnldA_7we8t5ukhlMfNeq3" \
         "ZuAtJrbmIeCDNZAx11tnOLpoRxw9PP1Z3aJH6xD4Vecw-oJIV_rVsg-Ma1mXforKxWleybcGL6lC0uWLKYe7LMXezBW8kvxikK" \
         "-EPIVrHPNJe20N6ufRQN8.eofMEsUhTTzxCCOOm2ZpkQ; _ga_Q0DQ5L7K0D=GS1.1.1681269111.1.1.1681270536.0.0.0 "

# proxies = {
#     'http': 'http://127.0.0.1:7890',
#     'https': 'http://127.0.0.1:7890',
# }


def get_header(keyword: str):
    user_agent = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" \
                 f"{random.randint(80, 90)}.0.{random.randint(4100, 4200)}.{random.randint(100, 150)} Safari/537.36 "
    return {"User-Agent": user_agent, "Referer": f"https://www.midjourney.com/app/?search={keyword}", "Cookie": cookie}


def get_request(keyword: str):
    url = api_url.format(keyword, keyword)
    time.sleep(random.uniform(2, 3)+random.random()*2)
    # response = requests.get(url=url, proxies=proxies, headers=get_header(keyword))
    response = requests.get(url=url, headers=get_header(keyword))
    if response.status_code == 200:
        print("Request Success: {}".format(url))
        return response
    raise Exception("Request Fail: {}".format(url))


def download_request(pic_url: str, keyword: str):
    time.sleep(random.uniform(1, 5)+random.random()*2)
    # response = requests.get(url=pic_url, proxies=proxies, headers=get_header(keyword))
    response = requests.get(url=pic_url, headers=get_header(keyword))
    if response.status_code == 200:
        print("Request Success: {}".format(pic_url))
        return response
    raise Exception("Request Fail: {}".format(pic_url))


def category_search(key: str, num: int):
    infos = get_request(key).json()

    # 创建一个临时文件夹
    with tempfile.TemporaryDirectory() as temp_dir:
        print(temp_dir)
        all_data = {}
        i = 1
        for info in infos:
            if i > num:
                break
            try:
                src = info['image_paths'][0]
                prompt = info['full_command']
                model = info['_job_type']
                all_data[f"{key}_{i}"] = {"src": src, "model": model, "prompt": prompt}
                i += 1
            except KeyError:
                continue

        # 在临时文件夹中创建一个 JSON 文件
        json_path = os.path.join(temp_dir, f"{key}.json")
        with open(json_path, "w", encoding="utf-8") as out_file:
            json.dump(all_data, out_file, indent=4, ensure_ascii=False)

        # 下载图片并将其保存到临时文件夹
        for name in all_data:
            response = download_request(all_data[name]['src'], key)
            img_path = os.path.join(temp_dir, f"{name}.png")
            with open(img_path, "wb") as out_file:
                out_file.write(response.content)
            print(f"{name}.png Success!")

            # 压缩临时文件夹中的文件
        zip_file_path = os.path.join(temp_dir, f"{key}.zip")
        with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
            for root, _, files in os.walk(temp_dir):
                for file in files:
                    if not file.endswith('.zip'):
                        zip_file.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), temp_dir))

        # 将 ZIP 文件移动到桌面
        desktop = os.path.expanduser("~/Desktop")
        desktop_zip_file_path = os.path.join(desktop, f"{key}.zip")
        shutil.move(zip_file_path, desktop_zip_file_path)
        print(f"ZIP file created at: {desktop_zip_file_path}")
        return desktop_zip_file_path


if __name__ == '__main__':
    for key in keys:
        category_search(key, 5)
