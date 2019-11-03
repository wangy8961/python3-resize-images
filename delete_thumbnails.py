import logging
import os
import re

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def main():
    """删除指定目录下的所有缩略图"""
    path = 'D:\\MyCode\\resize-images\\uploads'
    images = os.listdir(path)  # list

    pattern = re.compile(r'.*-(\d)+?x(\d)+?\..*')
    count = 0  # 统计需要删除的图片数
    for image in images:
        result = re.search(pattern, image)
        if result is not None:
            absolute_image_path = os.path.join(path, image)
            os.remove(absolute_image_path)
            count += 1
    logging.info('已删除缩略图 [{}] 张'.format(count))


if __name__ == '__main__':
    main()
