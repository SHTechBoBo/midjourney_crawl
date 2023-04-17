import random
import requests
import time


class Requester:
    def __init__(self, cookie: str = None, referer: str = None, proxy: str = None, sleep_time: tuple = (1, 3)):
        # 初始化请求器对象，设置cookie、referer、代理和等待时间
        self.header = {}
        if cookie:
            self.header["Cookie"] = cookie
        if referer:
            self.header["Referer"] = referer
        self.proxy = proxy
        self.sleep_time = sleep_time

    def get_header(self):
        # 生成并返回带有User-Agent的请求头
        user_agent = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/" \
                     f"{random.randint(80, 90)}.0.{random.randint(4100, 4200)}.{random.randint(100, 150)} Safari/537.36"
        self.header["User-Agent"] = user_agent
        return self.header

    def get_request(self, url, max_retries=3):
        # 在循环外定义一个变量用于记录错误信息
        error_messages = []

        # 使用 for 循环实现请求重试机制
        for retry_num in range(max_retries):
            # 在发送请求前等待一段随机时间，以避免过于频繁的请求
            time.sleep(random.uniform(self.sleep_time[0], self.sleep_time[1]))

            # 获取请求头信息
            header = self.get_header()

            try:
                # 使用代理（如果有）发送请求，并检查响应状态码
                response = requests.get(url=url, proxies=self.proxy, headers=header) if self.proxy else \
                    requests.get(url=url, headers=header)

                if response.status_code == 200:
                    return response
                else:
                    # 如果状态码不是200，将请求失败信息添加到错误信息列表
                    error_messages.append(f"Status Code: {response.status_code}")
            except requests.RequestException as error:
                # 捕获并处理请求异常，将错误信息添加到错误信息列表
                error_messages.append(f"Error: {error}")

            # 输出重试次数
            print(f"Retrying {url}... ({retry_num + 1}/{max_retries})")

        # 当达到最大尝试次数后，输出所有的错误信息并抛出异常
        print("\n".join(set(error_messages)))
        raise Exception(f"Request Failed after {max_retries} retries: {url}")
