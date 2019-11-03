import logging
import os

from PIL import Image

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def image_resize(src_filename, dst_width, dst_height):
    """
    将原始图片的宽高比例调整到跟目标图的宽高比例一致，所以需要：
    1. 切图，缩小原始图片的宽度或者高度
    2. 将切图后的新图片生成缩略图
    :param src_filename: 原始图片的名字
    :param dst_width: 目标图片的宽度
    :param dst_height: 目标图片的高度
    """
    # 目标图片（缩略图）的命名
    fname, fextension = os.path.splitext(src_filename)
    thumbnail_filename = fname + '-{}x{}'.format(dst_width, dst_height) + fextension

    # 打开原始图片
    src_image = Image.open(src_filename)
    # 原始图片的宽度和高度
    src_width, src_height = src_image.size
    # 原始图片的宽高比例，保留2位小数
    src_ratio = float('%.2f' % (src_width / src_height))
    # 目标图片的宽高比例，保留2位小数
    dst_ratio = float('%.2f' % (dst_width / dst_height))

    # 如果原始图片的宽高比例大，则将原始图片的宽度缩小
    if src_ratio >= dst_ratio:
        # 切图后的新高度
        if src_height < dst_height:
            logging.warning('目标图片的高度({0} px)超过原始图片的高度({1} px)，最终图片的高度为 {1} px'.format(dst_height, src_height))
        new_src_height = src_height
        # 切图后的新宽度
        new_src_width = int(new_src_height * dst_ratio)  # 向下取整
        if new_src_width > src_width:  # 比如原始图片(1280*480)和目标图片(800*300)的比例完全一致时，此时new_src_width=1281，可能四周会有一条黑线
            logging.warning('切图的宽度({0} px)超过原始图片的宽度({1} px)，最终图片的宽度为 {1} px'.format(new_src_width, src_width))
            new_src_width = src_width
        blank = int((src_width - new_src_width) / 2)  # 左右两边的空白。向下取整
        # 左右两边留出同样的宽度，计算出新的 box: The crop rectangle, as a (left, upper, right, lower)-tuple
        box = (blank, 0, blank + new_src_width, new_src_height)
    # 如果原始图片的宽高比例小，则将原始图片的高度缩小
    else:
        # 切图后的新宽度
        if src_width < dst_width:
            logging.warning('目标图片的宽度({0} px)超过原始图片的宽度({1} px)，最终图片的宽度为 {1} px'.format(dst_width, src_width))
        new_src_width = src_width
        # 切图后的新高度
        new_src_height = int(new_src_width / dst_ratio)  # 向下取整
        if new_src_height > src_height:
            logging.warning('切图的高度({0} px)超过原始图片的高度({1} px)，最终图片的高度为 {1} px'.format(new_src_height, src_height))
            new_src_height = src_height
        blank = int((src_height - new_src_height) / 2)  # 上下两边的空白。向下取整
        # 上下两边留出同样的高度，计算出新的 box: The crop rectangle, as a (left, upper, right, lower)-tuple
        box = (0, blank, new_src_width, blank + new_src_height)

    # 切图
    new_src_image = src_image.crop(box)
    # 生成目标缩略图
    new_src_image.thumbnail((dst_width, dst_height))
    # 保存到磁盘上
    new_src_image.save(thumbnail_filename)

    logging.info('目标图片已生成: {}'.format(thumbnail_filename))


if __name__ == '__main__':
    # image_resize('D:\\MyCode\\resize-images\\flask-vuejs.png', 60, 60)
    # image_resize('D:\\MyCode\\resize-images\\flask-vuejs.png', 480, 270)
    # image_resize('D:\\MyCode\\resize-images\\flask-vuejs.png', 800, 300)
    # image_resize('D:\\MyCode\\resize-images\\flask-vuejs.png', 960, 360)
    # image_resize('D:\\MyCode\\resize-images\\flask-vuejs.png', 1280, 480)
    path = 'D:\\MyCode\\resize-images\\uploads'
    images = os.listdir(path)
    for image in images:
        absolute_image_path = os.path.join(path, image)
        image_resize(absolute_image_path, 480, 270)
