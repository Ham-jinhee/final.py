# import cv2
# import matplotlib.pyplot as plt
#
#
# vfile = cv2.VideoCapture(0) # 웹캠연결 0 은 노트북캠

# if vfile.isOpened():
#     while True:
#         vret, img = vfile.read()
#         if vret:
#             cv2.imshow('webcam',img) # 이미지 불러오기
#             if cv2.waitKey(1) != -1: # 어떤키가 눌러지지 않는 이상 계속 지속
#                 cv2.imwrite('webcam_snap.jpg',img) # 이미지 저장
#                 break
#         else:
#             print("프레임이 정상적이지 않음")
#             break
# else:
#     print("오류 발생")
#
# vfile.release()
# cv2.destroyWindow()

# import numpy as np
# import cv2
#
# cap = cv2.VideoCapture(0)  # 노트북 웹캠을 카메라로 사용
# cap.set(3, 640)  # 너비
# cap.set(4, 480)  # 높이
#
# ret, frame = cap.read()  # 사진 촬영
# frame = cv2.flip(frame, 1)  # 좌우 대칭
#
# cv2.imwrite('self camera test.jpg', frame)  # 사진 저장
#
# cap.release()
# cv2.destroyAllWindows()

# 웹캠으로 사진찍기 (video_cam_take_pic.py)

# form_class = uic.loadUiType("RyuTalk_python_cam.ui")[0] # ui연결

# class MyWindow(QMainWindow, form_class):
#     def __init__(self):
#         super().__init__()
#         self.setupUi(self)
#
#         self.room_motion.clicked.connect(self.cam)
#
#
#     def cam(self):
#         # 캠찍어서 이미지 저장하기
#         vfile = cv2.VideoCapture(0)  # 웹캠연결 0 은 노트북캠
#
#         classes = ['OK', 'Heart']
#
#         if vfile.isOpened():
#             while True:
#                 vret, img = vfile.read()
#                 if vret:
#                     cv2.imshow('webcam',img) # 이미지 불러오기
#                     img = cv2.flip(img, 1)  # 좌우 대칭
#                     if cv2.waitKey(1) != -1: # 어떤키가 눌러지지 않는 이상 계속 지속
#                         cv2.imwrite('webcam_snap11.jpg',img) # 이미지 저장
#                         break
#                 else:
#                     print("프레임이 정상적이지 않음")
#                     break
#         else:
#             print("오류 발생")
#
#         vfile.release()
#
#         # 이미지 불러오기
#         path = './webcam_snap11.jpg'
#
#         model = tensorflow.keras.models.load_model('keras_model.h5')  # 모델 고정
#
#         if path :
#             image = Image.open('./webcam_snap11.jpg')
#             # resize the image to a 224x224 with the same strategy as in TM2:
#             # resizing the image to be at least 224x224 and then cropping from the center
#             size = (224, 224)
#             image = ImageOps.fit(image, size, Image.ANTIALIAS)
#
#             # turn the image into a numpy array
#             image_array = np.asarray(image)
#             # Normalize the image
#             normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
#             # Load the image into the array
#             data[0] = normalized_image_array
#
#         prediction = self.인식모델.predict(data)
#
#         l = list(prediction[0])
#         if l.index(max(l)) == 0:
#             print("OK")
#             # self.animal.setHidden(False)
#             self.OK_chat = "OK"
#             self.room_chat.setText(OK_chat)
#
#         elif l.index(max(l)) == 1:
#             print("heart")
#             # self.animal.setHidden(False)
#             self.heart_chat = "사랑해"
#             self.room_chat.setText(heart_chat)
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     myWindow = MyWindow()
#     myWindow.show()
#     app.exec_()

# # 캠찍어서 이미지 저장하기
# vfile = cv2.VideoCapture(0)  # 웹캠연결 0 은 노트북캠
#
# classes = ['OK', 'Heart']
#
# if vfile.isOpened():
#     while True:
#         vret, img = vfile.read()
#         if vret:
#             cv2.imshow('webcam',img) # 이미지 불러오기
#             img = cv2.flip(img, 1)  # 좌우 대칭
#             if cv2.waitKey(1) != -1: # 어떤키가 눌러지지 않는 이상 계속 지속
#                 cv2.imwrite('webcam_snap11.jpg',img) # 이미지 저장
#                 break
#         else:
#             print("프레임이 정상적이지 않음")
#             break
# else:
#     print("오류 발생")
#
# vfile.release()

# 이미지 불러오기
# path = './webcam_snap11.jpg'
# model = tensorflow.keras.models.load_model('keras_model.h5')  # 모델 고정

# if path :
#     image = Image.open('./webcam_snap11.jpg')
#     # resize the image to a 224x224 with the same strategy as in TM2:
#     # resizing the image to be at least 224x224 and then cropping from the center
#     size = (224, 224)
#     image = ImageOps.fit(image, size, Image.ANTIALIAS)
#
#     # turn the image into a numpy array
#     image_array = np.asarray(image)
#     # Normalize the image
#     normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
#     # Load the image into the array
#     data[0] = normalized_image_array
#
# prediction = self.인식모델.predict(data)
#
# l = list(prediction[0])
# if l.index(max(l)) == 0:
#     print("OK")
#     # self.animal.setHidden(False)
#     self.OK_chat = "OK"
#     self.room_chat.setText(OK_chat)
#
# elif l.index(max(l)) == 1:
#     print("heart")
#     # self.animal.setHidden(False)
#     self.heart_chat = "사랑해"
#     self.room_chat.setText(heart_chat)


import cv2
import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5 import uic
import matplotlib.pyplot as plt
import tensorflow
import numpy as np
import re

form_class = uic.loadUiType("RyuTalk_python_cam.ui")[0] # ui연결

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.room_motion.clicked.connect(self.cam)

    def cam(self):
        global cap, img
        model = tensorflow.keras.models.load_model('keras_model22.h5')
        cap = cv2.VideoCapture(0)
        size = (224, 224)
        classes = ['Hi', 'OK', 'No']
        while cap.isOpened():
            ret, img = cap.read()
            if not ret:
                break
            h, w, _ = img.shape
            cx = h / 2
            img = img[:, 200:200 + img.shape[0]]
            img = cv2.flip(img, 1)

            img_input = cv2.resize(img, size)
            img_input = cv2.cvtColor(img_input, cv2.COLOR_BGR2RGB)
            img_input = (img_input.astype(np.float32) / 127.0) - 1
            img_input = np.expand_dims(img_input, axis=0)

            prediction = model.predict(img_input)
            idx = np.argmax(prediction)
            text = classes[idx]
            self.room_chat.setText(text)
            cv2.imshow('result', img)
            if cv2.waitKey(1) == ord('q'):
                break

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()