import glob
import math

from PIL import Image

INCOMING_IMAGES_DIR = "incoming_images/"  # 输入图片的目录
OUTPUT_IMAGES_DIR = "output_images/"  # 输出图片的目录
MAX_COLUMN_COUNT = 30  # 每行图片数量限制


def sprite_sheet_generator():
    # 获取指定目录下的所有PNG文件
    paths = glob.glob(INCOMING_IMAGES_DIR + "*.png")
    if len(paths) > 0:
        # 图片总数
        amount = len(paths)
        # 获取单张输入图片信息
        with Image.open(paths[0]) as img:
            img_width = img.width  # 输入图片的宽度
            img_height = img.height  # 输入图片的高度

        # 打印基本信息
        print("当前输入图片尺寸为 {0}x{1}, 总计 {2} 张图片".format(img_width, img_height, amount))
        # 请求用户输入并验证有效性
        while True:
            column_count = input("请输入每行图片数量：")
            if column_count.isdigit():
                column_count = int(column_count)
                if column_count > MAX_COLUMN_COUNT:
                    print("每行图片数量超过限制：{}".format(MAX_COLUMN_COUNT))
                else:
                    break
            else:
                print("请输入一个有效的整数.")

        # 规定列数不超过总数
        if column_count > amount:
            column_count = amount
        # 计算行数
        row_count = math.ceil(amount / column_count)
        # 计算 sprite sheet 的宽度与高度
        max_width = column_count * img.width
        max_height = row_count * img.height

        # 创建图片
        sprite_sheet = Image.new("RGBA", (max_width, max_height))

        # 循环并粘贴到 sprite sheet 上
        width, height = 0, 0  # 粘贴图片的位置
        for path in paths:
            with Image.open(path) as img:
                # 将图片粘贴到指定位置
                sprite_sheet.paste(img, (width, height))
                width += img.width
                # 宽度到达最大宽度后,开始粘贴到下一排
                if width >= max_width:
                    width %= max_width  # 宽度重新开始
                    height += img.height  # 计算下一排开始的高度
        sprite_sheet.save(OUTPUT_IMAGES_DIR + 'sprite-sheet.png')
        print("已完成, 生成目录：" + OUTPUT_IMAGES_DIR)
        # 等待输入再退出,让程序在打包后双击运行时看到上面的完成信息
        input("输入回车退出程序...")
    else:
        print('no images in', INCOMING_IMAGES_DIR, 'directory.')


""" 
程序打包：pyinstaller --onefile spritesheet-maker.py
打包完成后需要创建 INCOMING_IMAGES_DIR 与 OUTPUT_IMAGES_DIR 目录
"""
if __name__ == '__main__':
    sprite_sheet_generator()
