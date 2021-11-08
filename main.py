import tensorflow.keras
import numpy as np
import cv2
import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5 import uic
import matplotlib.pyplot as plt
import re

form_class = uic.loadUiType("RyuTalk_python_cam.ui")[0] # ui연결

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.room_motion.clicked.connect(self.cam)


    def cam(self):

        model = tensorflow.keras.models.load_model('keras_model.h5')

        cap = cv2.VideoCapture(0)

        size = (224, 224)

        classes = ['Scissors', 'Rock', 'Paper']

        while cap.isOpened():
            ret, img = cap.read()
            if not ret:
                break

            h, w, _ = img.shape
            cx = h / 2
            img = img[:, 200:200+img.shape[0]]
            img = cv2.flip(img, 1)

            img_input = cv2.resize(img, size)
            img_input = cv2.cvtColor(img_input, cv2.COLOR_BGR2RGB)
            img_input = (img_input.astype(np.float32) / 127.0) - 1
            img_input = np.expand_dims(img_input, axis=0)

            prediction = model.predict(img_input)
            idx = np.argmax(prediction)
            text = classes[idx]
            self.room_chat.setText(text)

            # cv2.putText(img, text=classes[idx], org=(10, 30), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.8, color=(255, 255, 255), thickness=2)

            cv2.imshow('result', img)
            if cv2.waitKey(1) == ord('q'):
                break

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()