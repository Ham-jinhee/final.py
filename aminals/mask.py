import sys

import tensorflow.keras
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import numpy as np
import tensorflow as tf
from PIL import Image, ImageOps

class 마스크경고(QMainWindow):
    def __init__(self):
        super().__init__()
        self.UI초기화()

    def UI초기화(self):
        self.대표이미지 = QLabel(self)
        self.대표이미지.setPixmap(QPixmap('').scaled(35,44))
        self.대표이미지.move(20,65)
        self.대표이미지.resize(35,44)

        self.가게이름 = QLabel('라이캣의 무인가게 마스크경고',self)
        self.가게이름.setFont(QFont("Decorative", 15))
        self.가게이름.adjustSize()
        self.가게이름.move(80, 70)

        self.이미지 = QLabel(self)
        self.이미지.move(200,100)

        self.가이드 = QLabel('상단바 File을 눌러 모델 추가 후 이미지를 삽입하여 인식합니다.',self)
        self.가이드.move(40, 500)
        self.가이드.adjustSize()

        self.마스크경고 = QLabel('마스크를 써주세요',self)
        self.마스크경고.move(200,550)
        self.마스크경고.adjustSize()
        self.마스크경고.setHidden(True) # 보이지 않게 하기

        self.이미지업로드 = QPushButton('파일업로드',self)
        self.이미지업로드.move(170, 430)
        self.이미지업로드.resize(240, 40) # 크기조정
        self.이미지업로드.setEnabled(False) # 모델이 정상적으로 업로드 되었을 경우에만 버튼 활성화
        self.이미지업로드.clicked.connect(self.loadImage)

        self.인식모델 = None

        메뉴바 = self.menuBar() # 여기서만 한 번 사용되기 때문에 self를 사용하지 않음
        메뉴바.setNativeMenuBar(False)
        파일메뉴 = 메뉴바.addMenu('File')

        모델불러오기메뉴 = QAction('모델불러오기',self)
        모델불러오기메뉴.setShortcut('Ctrl+L')
        모델불러오기메뉴.triggered.connect(self.loadModel)
        파일메뉴.addAction(모델불러오기메뉴)

        self.setWindowTitle('동물구별 프로그램')
        self.setGeometry(300,300,600,600)
        self.show()

    def loadModel(self):
        try:
            모델파일, _ = QFileDialog.getOpenFileName(self,'모델추가', '')
            if 모델파일:
                self.인식모델 = tf.keras.Model.load_model(모델파일)
                self.가이드.setText('모델추가완료')
            self.이미지업로드.setEnabled(True)
        except:
            self.가이드.setText('모델이 아닙니다')

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

프로그램무한반복 = QApplication(sys.argv)
실행인스턴스 = 마스크경고()
프로그램무한반복.exec_()
