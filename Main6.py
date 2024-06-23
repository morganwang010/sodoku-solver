import os
import cv2
from SudokuExtractor6 import extract_sudoku
from SudokuSolver6 import solve6
from NumberExtractor6 import extract_number6, display_sudoku6
import numpy as np
from PIL import Image, ImageDraw, ImageFont
def save_result_img(data):
    # 配置图片的宽度和高度
    cell_size = 50  # 每个单元格的大小
    rows = len(data)
    cols = len(data[0])
    width = cols * cell_size
    height = rows * cell_size

    # 创建一个空白图片，背景为白色
    image = Image.new('RGB', (width, height), 'white')

    # 创建一个绘图对象
    draw = ImageDraw.Draw(image)

    # 设置字体（你可以选择系统中的其他字体）
    font = ImageFont.truetype("arial.ttf", 20)

    # 遍历数组并将每个元素绘制到图片上
    for i, row in enumerate(data):
        for j, value in enumerate(row):
            # 计算文本的放置位置
            text = str(value)
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            text_x = j * cell_size + (cell_size - text_width) / 2
            text_y = i * cell_size + (cell_size - text_height) / 2
            
            # 绘制单元格边框
            draw.rectangle([j * cell_size, i * cell_size, (j + 1) * cell_size, (i + 1) * cell_size], outline='black')
            
            # 将文本绘制到图片上
            draw.text((text_x, text_y), text, fill='black', font=font)

    # 保存图片
    image.save('array_image.png')

    # 如果需要显示图片，可以使用以下代码
    # image.show()


# 读图
filePath = ".\\imgs\\"
files = os.listdir(filePath)
for file in files:
    path = filePath + file

    image_ori = cv2.imread(path, 0)
    ratio = image_ori.shape[0] / 300
    w = round(image_ori.shape[1] / ratio)
    image_resize = cv2.resize(image_ori, (w, 300))

    image = extract_sudoku(path)
    image_show = cv2.resize(image, (300, 300))

    result = extract_number6(image)
    # display_sudoku6(result)
    result1 = solve6(result)
    # save_result_img(result)
    if result1 is not None:
        print("Solution is:")
        display_sudoku6(result)
    else:
        print("No Solution!")

    image_stack = np.hstack((image_resize, image_show))

    cv2.imshow("image", image_stack)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
