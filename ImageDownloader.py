import os
import re
from Requester import Requester


class ImageDownloader:
    def __init__(self, url: str, name: str, path: str, requester: Requester):
        self.url = url
        # 从URL中提取文件扩展名并添加到名称
        self.name = f"{name}.{re.findall(r'[^.]*$', url)[0]}"
        # 检查路径是否存在，如果不存在则创建
        if not os.path.exists(path):
            os.makedirs(path)
        # 将文件名添加到路径中
        self.path = os.path.join(path, self.name)
        self.requester = requester

    def download(self):
        # 使用requester对象获取URL响应
        response = self.requester.get_request(url=self.url)
        # 将图像内容写入文件
        with open(self.path, "wb") as out_file:
            out_file.write(response.content)
        # 打印成功消息
        print(f"{self.name} Download Success (Path: {os.path.abspath(self.path)})")
