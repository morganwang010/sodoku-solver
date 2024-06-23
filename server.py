from urllib import response
from flask import Flask, request, redirect, url_for,jsonify,send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import cv2
from SudokuExtractor import extract_sudoku
from SudokuSolver import solve
from NumberExtractor import extract_number, display_sudoku
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import uuid

app = Flask(__name__)
CORS(app)
@app.route('/solve', methods=['POST'])
def solve_sodoku():
    filePath = "imgs"
    file =  request.args.get('jpg')
    path = filePath + "/" + file

    image_ori = cv2.imread(path, 0)
    ratio = image_ori.shape[0] / 540
    w = round(image_ori.shape[1] / ratio)
    image_resize = cv2.resize(image_ori, (w, 540))

    image = extract_sudoku(path)
    image_show = cv2.resize(image, (540, 540))

    result = extract_number(image)
    # display_sudoku(result)
    result = solve(result)
    response = result
    if result is not None:
        print("Solution is:")
        # display_sudoku(result)
    else:
        print("No Solution!")
    
    return str(response), 200
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def solve_sodoku(fileName):
    filePath = "uploads/"
    path = filePath + str(fileName)

    image_ori = cv2.imread(path, 0)
    ratio = image_ori.shape[0] / 540
    w = round(image_ori.shape[1] / ratio)
    image_resize = cv2.resize(image_ori, (w, 540))

    image = extract_sudoku(path)
    image_show = cv2.resize(image, (540, 540))

    result = extract_number(image)
    # display_sudoku(result)
    result = solve(result)
   
    if result is not None:
        print("Solution is:")
        # display_sudoku(result)
    else:
        print("No Solution!")
    fileResult = save_result_img(result,fileName)
    return str(fileResult)

def save_result_img(data,fileName):
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
    fileNames = str(uuid.uuid4()) + '.png'
    image.save("uploads/" + fileNames)
    return fileNames

    # 如果需要显示图片，可以使用以下代码
    # image.show()
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_image():
    # Check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    
    # If user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Ensure the upload folder exists
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        file.save(file_path)
        result = solve_sodoku(filename)
        imgurl = "http://127.0.0.1:5000/uploads/" + str(result)
        # print(filename)

        return jsonify({'message': 'File uploaded successfully', 'filename': imgurl}), 200
    else:
        return jsonify({'error': 'File type not allowed'}), 400
@app.route('/uploads/<image_name>')
def display_image(image_name):
    image_path = os.path.join('uploads', image_name)
    print(image_name)
    return send_from_directory('uploads', image_name, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)