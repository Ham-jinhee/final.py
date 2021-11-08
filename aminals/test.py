import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from PyQt5 import QtCore, QtWidgets
import pyautogui as pg  # pyautogui 모듈 불러오기
from PIL import Image, ImageOps
import tensorflow as tf
import numpy as np


page1= uic.loadUiType("aaa.ui")[0]

class animal(QMainWindow,page1) :
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.file_upload.clicked.connect(self.loadImage) #파일 업로드 버튼
        self.user.clicked.connect(self.check) #유저확인 버튼
        # self.model.setShortcut('Ctrl+L')  # 모델불러오기 단축키
        # self.model.triggered.connect(self.loadModel)  #모델 불러오키 버튼

    def check(self):
        result = 0
        a = pg.confirm(text='정답이 맞습니까?', title='동물 구별 프로그램', buttons=['OK', 'NG'])
        print(a)
        if (a == 'OK'):
            result = "Yes"
        else:
            result = "No"
        print(result)

    def loadModel(self):
        try:
            모델파일, _ = QFileDialog.getOpenFileName(self, '모델 추가', '')
            if 모델파일:
                self.인식모델 = tf.keras.models.load_model(모델파일, compile=False)
                self.label.setText('모델추가 완료!')
            self.이미지업로드.setEnabled(True)
        except:
            self.label.setText("모델 파일이 아닙니다!")

    def loadImage(self):
        # Create the array of the right shape to feed into the keras model
        # The 'length' or number of images you can put into the array is
        # determined by the first position in the shape tuple, in this case 1.
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

        이미지이름, _ = QFileDialog.getOpenFileName(self, '이미지 추가', './')
        # Replace this with the path to your image
        이미지파일 = QPixmap(이미지이름).scaled(200, 200, aspectRatioMode=Qt.KeepAspectRatio)
        self.이미지.setPixmap(이미지파일)
        self.이미지.adjustSize()
        if 이미지파일:
            image = Image.open(이미지이름)
            # resize the image to a 224x224 with the same strategy as in TM2:
            # resizing the image to be at least 224x224 and then cropping from the center
            size = (224, 224)
            image = ImageOps.fit(image, size, Image.ANTIALIAS)

            # turn the image into a numpy array
            image_array = np.asarray(image)
            # Normalize the image
            normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
            # Load the image into the array
            data[0] = normalized_image_array

            # run the inference
            prediction = self.인식모델.predict(data)
            print(prediction)
            l = list(prediction[0])
            if l.index(max(l)) == 0:
                print("사람")
                self.animal.setHidden(False)
                self.animal.setText('사람')
            elif l.index(max(l)) == 1:
                print("고양이")
                self.animal.setHidden(False)
                self.animal.setText('고양이')
            elif l.index(max(l)) == 2:
                print("강아지")
                self.animal.setHidden(False)
                self.animal.setText('강아지')
            elif l.index(max(l)) == 3:
                print("토끼")
                self.animal.setHidden(False)
                self.animal.setText('토끼')
            else:
                print("응 아니야~")
                self.animal.setHidden(False)
                self.animal.setText('아무것도 아니야')

start = QApplication(sys.argv)
mywindow = animal()
mywindow.show()
start.exec()


def settectlavel_2(self):
    pix = self.photo.Pixmap()
    if pix != None:
        self.label_2.setText("입니다.")
        self.label_2.setStyleSheet("""QLabel {font: 85 italic 12pt "Arial Black"; color: rgb(0, 0, 0);}""")
    else:
        self.t_2.setText(" ")
        self.t_2.setStyleSheet("""QLabel {font: 85 italic 12pt "Arial Black"; color: rgb(0, 0, 0);}""")

