import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
import pyautogui as pg  # pyautogui 모듈 불러오기
from PIL import Image, ImageOps
import tensorflow as tf
import numpy as np
import sqlite3 # sql 모듈 불러오기
import datetime
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

page1 =uic.loadUiType('1.ui')[0]

class Detect(QMainWindow,page1) :
    def __init__(self):
        super().__init__()
        self.setupUi(self)


        self.file_upload.setEnabled(False)
        self.file_upload.clicked.connect(self.loadImage) #파일 업로드 버튼
        self.user.clicked.connect(self.check) #유저확인 버튼

        self.인식모델 = None

        #메뉴바 만들기
        menu=self.menuBar()
        menu.setNativeMenuBar(False)
        filemenu = menu.addMenu("File")

        modelmenu=QAction('모델 불러오기',self)
        modelmenu.setShortcut('Ctrl+L')  # 모델불러오기 단축키
        modelmenu.triggered.connect(self.loadModel)  #모델 불러오키 버튼
        filemenu.addAction(modelmenu)

    def check(self):
        conn = sqlite3.connect("Distinguishing_animals.db", isolation_level=None)  # db연동
        cur = conn.cursor()  # connection으로부터 cursor생성
        a = pg.confirm(text='정답이 맞습니까?', title='동물 구별 프로그램', buttons=['OK', 'NG'])
        name = self.animal.text()
        nowdate = datetime.datetime.now()

        if (a == 'OK'):
            result = "Yes"
            now = ('{}'.format(nowdate), '{}'.format(name), '{}'.format(이미지이름), '{}'.format(result))
            act = "INSERT INTO Animal_discrimination_results(Datetime, Animal, Address ,Accuracy)VALUES(?,?,?,?)"
            cur.execute(act, now)
            print("DB저장 완료")
            # im = Image.open(이미지이름)
            # im.save('./OK/{}.png'.format(nowdate))
            # print("OK저장")
        else:
            result = "No"
            now = ('{}'.format(nowdate), '{}'.format(name), '{}'.format(이미지이름), '{}'.format(result))
            act = "INSERT INTO Animal_discrimination_results(Datetime, Animal, Address ,Accuracy)VALUES(?,?,?,?)"
            cur.execute(act, now)
            im = Image.open(이미지이름)
            # print("DB저장 완료")
            # im.save('./NG/{}.png'.format(nowdate))
            # print("NG저장")

        print(result)

    def loadModel(self):
        try:
            모델파일, _ =QFileDialog.getOpenFileName(self,'모델 추가','')
            if 모델파일:
                self.인식모델=tf.keras.models.load_model(모델파일,compile=False)
                self.label.setText('모델추가 완료!')
            self.file_upload.setEnabled(True)
        except:
            self.label.setText("모델 파일이 아닙니다!")

    def loadImage(self):
        # Create the array of the right shape to feed into the keras model
        # The 'length' or number of images you can put into the array is
        # determined by the first position in the shape tuple, in this case 1.
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        global 이미지이름
        global 이미지파일
        이미지이름, _ = QFileDialog.getOpenFileName(self, '이미지 추가', './')
        # Replace this with the path to your image
        이미지파일 = QPixmap(이미지이름).scaled(300,330,aspectRatioMode=Qt.KeepAspectRatio)
        self.photo.setPixmap(이미지파일)
        self.photo.adjustSize()

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
            elif l.index(max(l))==4:
                print("곰")
                self.animal.setHidden(False)
                self.animal.setText('곰')
            elif l.index(max(l))==5:
                print("코끼리")
                self.animal.setHidden(False)
                self.animal.setText('코끼리')
            elif l.index(max(l))==6:
                print("사자")
                self.animal.setHidden(False)
                self.animal.setText('사자')
            elif l.index(max(l))==7:
                print("상어")
                self.animal.setHidden(False)
                self.animal.setText('상어')
            elif l.index(max(l))==8:
                print("물고기")
                self.animal.setHidden(False)
                self.animal.setText('물고기')
            elif l.index(max(l))==9:
                print("고릴라")
                self.animal.setHidden(False)
                self.animal.setText('고릴라')

            else:
                print("응 아니야~")
                self.animal.setHidden(False)
                self.animal.setText('아무것도 아니야')


start = QApplication(sys.argv)
mywindow = Detect()
mywindow.show()
start.exec_()
