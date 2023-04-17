import os
import zipfile


def create_zip_file(path, name):

    # 创建并打开一个新的zip文件
    with zipfile.ZipFile(f"{name}.zip", 'w') as zip_file:
        # 遍历文件夹中的所有文件
        for root, _, files in os.walk(path):
            for file in files:
                # 获取文件相对路径
                rel_path = os.path.relpath(os.path.join(root, file), path)
                # 向zip文件中添加文件
                zip_file.write(os.path.join(root, file), rel_path)

    # 返回压缩文件的路径
    return os.path.abspath(f"{name}.zip")
