from typing import Sequence
import os 
from google.cloud import vision

import tkinter as tk
import time

from PIL import Image
import io

#変数の設定
objects = []
obj_score = []

#正誤判定の動作(from Codelabs https://codelabs.developers.google.com/codelabs/cloud-vision-api-python?hl=ja#3 )
def analyze_image_from_content(
    image_content: bytes,
    feature_types: Sequence,
) -> vision.AnnotateImageResponse:
    client = vision.ImageAnnotatorClient()

    image = vision.Image(content=image_content)

    features = [vision.Feature(type_=feature_type) for feature_type in feature_types]
    request = vision.AnnotateImageRequest(image=image,features=features)

    response = client.annotate_image(request=request)

    return response

#ラベルを取得
def get_labels(response: vision.AnnotateImageResponse):
    for label in response.label_annotations:
        objects.append(label.description.lower())
        obj_score.append(int(round(label.score,2)*100))

#描画関数
def draw(event):
    x1 = event.x - 3
    y1 = event.y - 3
    x2 = event.x + 3
    y2 = event.y + 3
    cv.create_oval(x1, y1, x2, y2, fill="black", outline="black")


def save_canvas():
#キャンバスの内容を取得
    ps = cv.postscript(colormode='color')
    img = Image.open(io.BytesIO(ps.encode('utf-8')))
    
    png_bytes_io = io.BytesIO()
    img.save(png_bytes_io, format='png')
    png_bytes = png_bytes_io.getvalue()

    features = [vision.Feature.Type.LABEL_DETECTION]
    response = analyze_image_from_content(png_bytes, features)
    get_labels(response)
    print(objects)
    print(obj_score)

#キャンバスの設定
window = tk.Tk()
window.title("DrawQuiz!")
cv = tk.Canvas(window,width=800,height=500)
cv.pack()

button = tk.Button(window, text="Save and Analyze", command=save_canvas)
button.pack()

cv.bind("<B1-Motion>", draw)

window.mainloop()