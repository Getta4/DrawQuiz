from typing import Sequence
import os 
from google.cloud import vision

import tkinter as tk
import time

#変数の設定
objects = []
obj_score = []

#キャンバスの設定
window = tk.Tk()
window.title("DrawQuiz!")
cv = tk.Canvas(window,width=800,height=500)
cv.pack()

#正誤判定の動作(from Codelabs https://codelabs.developers.google.com/codelabs/cloud-vision-api-python?hl=ja#3 )
def analyze_image_from_uri(
    image_uri: str,
    feature_types: Sequence,
) -> vision.AnnotateImageResponse:
    client = vision.ImageAnnotatorClient()

    image = vision.Image()

    #ファイルの読み込み
    with open(image_uri,'rb') as image_file:
        content = image_file.read()
    image.content = content

    features = [vision.Feature(type_=feature_type) for feature_type in feature_types]
    request = vision.AnnotateImageRequest(image=image,features=features)

    response = client.annotate_image(request=request)

    return response

#ラベルを取得
def get_labels(response: vision.AnnotateImageResponse):
    for label in response.label_annotations:
        objects.append(label.description.lower())
        obj_score.append(int(round(label.score,2)*100))
'''
image_uri = ""
features = [vision.Feature.Type.LABEL_DETECTION]
response = analyze_image_from_uri(image_uri, features)
'''

window.mainloop()