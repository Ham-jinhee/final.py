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
import sqlite3 # sql 모듈 불러오기
# import os
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

page1= uic.loadUiType("animal.ui")[0]

class animal(QMainWindow,page1) :
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.file_upload.clicked.connect(self.loadImage) #파일 업로드 버튼
        self.user.clicked.connect(self.check) #유저확인 버튼
        self.model.setShortcut('Ctrl+L')  # 모델불러오기 단축키
        self.model.triggered.connect(self.loadModel)  #모델 불러오키 버튼

    def check(self):
        result = 0
        a = pg.confirm(text='정답이 맞습니까?', title='동물 구별 프로그램', buttons=['OK', 'NG'])
        print(a)
        if (a == 'OK'):
            result = "Yes"
        else:
            result = "No"
        print(result)

    # def UI초기화(self):
    #     self.대표이미지 = QLabel(self)
    #     self.대표이미지.setPixmap(QPixmap('mong.png').scaled(35,44))
    #     self.대표이미지.move(20,65)
    #     self.대표이미지.resize(35,44)
    #     self.가게이름 = QLabel("동물구분",self)
    #     self.가게이름.setFont(QFont("Decorative",15))
    #     self.가게이름.adjustSize()
    #     self.가게이름.move(80,70)
    #
    #     self.이미지 = QLabel(self)
    #     self.이미지.move(200,100)
    #
    #     self.가이드 = QLabel("상단바 file을 눌러 모델 추가 후 이미지를 삽입하여 인식합니다.",self)
    #     self.가이드.move(40,500)
    #     self.가이드.adjustSize()
    #
    #     self.animal = QLabel('기린이 아닙니다!!',self)
    #     self.animal.move(200,550)
    #     self.animal.adjustSize()
    #     self.animal.setHidden(True)
    #
    #     self.이미지업로드 = QPushButton('파일 업로드',self)
    #     self.이미지업로드.move(170,430)
    #     self.이미지업로드.resize(240,40)
    #     self.이미지업로드.clicked.connect(self.loadImage)
    #
    #     self.인식모델 = None
    #
    #     메뉴바 = self.menuBar()
    #     메뉴바.setNativeMenuBar(False)
    #     파일메뉴=메뉴바.addMenu('File')
    #
    #     모델불러오기메뉴 = QAction('모델 불러오기',self)
    #     모델불러오기메뉴.setShortcut('Ctrl+L') #단축키
    #     모델불러오기메뉴.triggered.connect(self.loadModel)
    #     파일메뉴.addAction(모델불러오기메뉴)

    #     self.setWindowTitle(('(주)동물구분인공지능프로그램'))
    #     self.setGeometry(300,300,600,600)
    #     self.show()

    def loadModel(self):
        try:
            모델파일, _ =QFileDialog.getOpenFileName(self,'모델 추가','')
            if 모델파일:
                self.인식모델=tf.keras.models.load_model(모델파일,compile=False)
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
        이미지파일 = QPixmap(이미지이름).scaled(200,200,aspectRatioMode=Qt.KeepAspectRatio)
        self.이미지.setPixmap(이미지파일)
        self.이미지.adjustSize()
        if 이미지파일 :
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
            if l.index(max(l)) ==0:
                print("사람")
                self.animal.setHidden(False)
                self.animal.setText('사람')
            elif l.index(max(l))==1:
                print("고양이")
                self.animal.setHidden(False)
                self.animal.setText('고양이')
            elif l.index(max(l))==2:
                print("강아지")
                self.animal.setHidden(False)
                self.animal.setText('강아지')
            elif l.index(max(l))==3:
                print("토끼")
                self.animal.setHidden(False)
                self.animal.setText('토끼')
            else:
                print("응 아니야~")
                self.animal.setHidden(False)
                self.animal.setText('아무것도 아니야')

            # conn = sqlite3.connect("Distinguishing_animals.db", isolation_level=None)  # db연동
            # cur = conn.cursor()  # connection으로부터 cursor생성
            # cur.execute("INSERT INTO Animal_discrimination_results(Datetime, Animal, accuracy, Result)VALUES(?,?,?,?)")

start = QApplication(sys.argv)
mywindow = animal()
mywindow.show()
start.exec()


# # Load the model
# model = load_model('keras_model.h5')
#
# # Create the array of the right shape to feed into the keras model
# # The 'length' or number of images you can put into the array is
# # determined by the first position in the shape tuple, in this case 1.
# data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
# # Replace this with the path to your image
# image = Image.open('dog.jpg')
# #resize the image to a 224x224 with the same strategy as in TM2:
# #resizing the image to be at least 224x224 and then cropping from the center
# size = (224, 224)
# image = ImageOps.fit(image, size, Image.ANTIALIAS)
#
# #turn the image into a numpy array
# image_array = np.asarray(image)
# # Normalize the image
# normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
# # Load the image into the array
# data[0] = normalized_image_array
#
# # run the inference
# prediction = model.predict(data)
# print(prediction)
