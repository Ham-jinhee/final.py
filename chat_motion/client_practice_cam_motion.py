import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5 import uic
import socket
import threading
from threading import Thread
import tensorflow.keras
import re
import cv2
import numpy as np
from os import listdir
from os.path import isfile, join
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

form_class = uic.loadUiType("RyuTalk_python_cam_02.ui")[0]


class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.user_pw = []
        self.user_ids = []
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.setupUi(self)
        self.Host = '10.10.21.118'
        self.Port = 7200
        self.client_socket.connect((self.Host, self.Port))
        self.check_cnt = 0
        self.user_id = ''
        self.room = ''
        self.stackedWidget.setCurrentWidget(self.login_page)
        self.login_btn.clicked.connect(self.login)
        self.signup_btn.clicked.connect(self.signup)
        self.make_room_btn.clicked.connect(self.make_room)
        self.refresh_btn.clicked.connect(self.refresh)
        self.room_list.itemDoubleClicked.connect(self.room_join)
        self.room_send_btn.clicked.connect(self.write)
        self.room_exit_btn.clicked.connect(self.exit_room)
        self.room_online.itemDoubleClicked.connect(self.room_invite)
        self.room_motion.clicked.connect(self.cam) # 모션채팅 연결
        self.face.clicked.connect(self.facejoin)
        self.face_btn.clicked.connect(self.facelogin)

    def facelogin(self):

        data_path = 'faces/'
        onlyfiles = [f for f in listdir(data_path) if isfile(join(data_path, f))]

        Training_Data, Labels = [], []

        for i, files in enumerate(onlyfiles):
            image_path = data_path + onlyfiles[i]
            images = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            Training_Data.append(np.asarray(images, dtype=np.uint8))
            Labels.append(i)

        Labels = np.asarray(Labels, dtype=np.int32)

        self.model = cv2.face.LBPHFaceRecognizer_create()

        self.model.train(np.asarray(Training_Data), np.asarray(Labels))

        print("Model Training Complete!!!!!")

        face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        def face_detector(img, size=0.5):
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_classifier.detectMultiScale(gray, 1.3, 5)

            if faces is ():
                return img, []

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 2)
                roi = img[y:y + h, x:x + w]
                roi = cv2.resize(roi, (200, 200))

            return img, roi

        cap = cv2.VideoCapture(0)
        while True:

            ret, frame = cap.read()

            image, face = face_detector(frame)

            try:
                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                result = self.model.predict(face)

                if result[1] < 500:
                    confidence = int(100 * (1 - (result[1]) / 300))
                    display_string = str(confidence) + '% Confidence it is user'
                cv2.putText(image, display_string, (100, 120), cv2.FONT_HERSHEY_COMPLEX, 1, (250, 120, 255), 2)

                if confidence > 84:
                    cv2.putText(image, "Unlocked", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                    cv2.imshow('Face Cropper', image)

                    self.stackedWidget.setCurrentWidget(self.signup_page)

                else:
                    cv2.putText(image, "Locked", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
                    cv2.imshow('Face Cropper', image)

            except:
                cv2.putText(image, "Face Not Found", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                cv2.imshow('Face Cropper', image)
                pass

            if cv2.waitKey(1) == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def facejoin(self):

        face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        def face_extractor(img):

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_classifier.detectMultiScale(gray, 1.3, 5)

            if faces is ():
                return None

            for (x, y, w, h) in faces:
                cropped_face = img[y:y + h, x:x + w]

            return cropped_face

        cap = cv2.VideoCapture(0)
        count = 0

        while True:
            ret, frame = cap.read()
            if face_extractor(frame) is not None:
                count += 1
                face = cv2.resize(face_extractor(frame), (200, 200))
                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

                file_name_path = 'faces/user' + str(count) + '.jpg'
                cv2.imwrite(file_name_path, face)

                # cv2.putText(face,str(count),(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                cv2.imshow('Face Cropper', face)
            else:
                print("Face not Found")
                pass

            if cv2.waitKey(1) == 13 or count == 300:
                break

        cap.release()
        cv2.destroyAllWindows()
        self.stackedWidget.setCurrentWidget(self.login_page)
        print('Colleting Samples Complete!!!')

    def room_invite(self):
        invite_id = self.room_online.currentItem().text()
        self.reply = QMessageBox.question(self, 'Invite', '{} 유저를 {} 방으로 초대하시겠습니까?'
                                          .format(invite_id, self.room),
                                          QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if self.reply == QMessageBox.Yes:
            self.client_socket.send(f'#invite,{self.room},{invite_id}'.encode())
        else:
            pass

    def login(self):
        user_id = self.id_line.text()
        user_pw = self.pw_line.text()
        self.client_socket.send(f'#my_id_pw,{user_id},{user_pw}'.encode())
        message = self.client_socket.recv(1024).decode()
        if message == '2':
            QtWidgets.QMessageBox.about(self, "QMessageBox", "회원정보가 일치하지 않습니다.")
            self.id_line.clear()
            self.pw_line.clear()
        else:
            read_thread = Thread(target=self.reading, daemon=True)
            read_thread.start()
            self.user_id = user_id
            print('before refresh')
            self.refresh()
            print('after refresh')
            self.stackedWidget.setCurrentWidget(self.room_list_page)

    def signup(self):
        self.stackedWidget.setCurrentWidget(self.signup_page)
        self.signup_ok_btn.clicked.connect(self.signup_check)

    def id_check(self):
        self.check_cnt += 1
        if self.id.text() in self.user_ids:
            QtWidgets.QMessageBox.about(self, "QMessageBox", "이미 존재하는 아이디입니다.")
            self.id.clear()
        elif self.id.text() not in self.user_ids:
            QtWidgets.QMessageBox.about(self, "QMessageBox", "사용 가능한 아이디입니다.")

    def signup_check(self):
        id_temp = self.id.text()
        pw_temp = self.pw.text()
        pw_check = self.pw_check.text()
        if pw_temp != pw_check:
            QtWidgets.QMessageBox.about(self, "QMessageBox", "비밀번호 다시 확인해주세요")
            self.pw.clear()
            self.pw_check.clear()

        else:
            self.client_socket.send(f'#signup,{id_temp},{pw_temp}'.encode())
            message = self.client_socket.recv(1024).decode()
            if message == '2':
                QtWidgets.QMessageBox.about(self, "QMessageBox", "이미 존재하는 회원정보입니다.")
            else:
                QtWidgets.QMessageBox.about(self, "QMessageBox", "회원가입 되었습니다.")
                self.stackedWidget.setCurrentWidget(self.login_page)

    def exit_room(self):
        self.stackedWidget.setCurrentWidget(self.room_list_page)
        self.main_chat.clear()
        self.client_socket.send(f'#exit,{self.room},{self.user_id}'.encode())

    def make_room(self):
        self.room = self.room_name_line.text()
        if len(re.findall('\w', self.room)) < len(self.room):
            self.room_check.setText('올바른 방이름을 적어주세요(공백/특수문자 제외)')
            self.room_name_line.clear()

        elif len(self.room) == 0:
            self.room_check.setText('올바른 방이름을 적어주세요(공백/특수문자 제외)')
            self.room_name_line.clear()

        elif len(re.findall('\s', self.room)) > 0:
            self.room_check.setText('올바른 방이름을 적어주세요(공백/특수문자 제외)')
            self.room_name_line.clear()

        else:
            self.client_socket.send(f'#makeroom,{self.room},{self.user_id}'.encode())
            self.room_name_line.clear()
            self.room_user_list.addItem(self.user_id)
            self.stackedWidget.setCurrentWidget(self.room_page)

    def room_join(self):
        self.room = self.room_list.currentItem().text()
        self.client_socket.send(f'#roomjoin,{self.room},{self.user_id}'.encode())
        self.stackedWidget.setCurrentWidget(self.room_page)

    def invite_join(self, invite_room):
        self.client_socket.send(f'#roomjoin,{invite_room},{self.user_id}'.encode())
        self.stackedWidget.setCurrentWidget(self.room_page)
        self.refresh()

    def write(self):
        self.client_socket.send(f'{self.room}${self.user_id} : {self.room_chat.text()}'.encode())
        self.room_chat.clear()

    def recv_oac(self, message):
        try:
            self.room_list.clear()
            self.online_users_list.clear()
            self.room_online.clear()
            onlineusers = message.split(';')[0]
            chattingrooms = message.split(';')[1]
            onlineusers = onlineusers.split(',')[1:-1]
            chattingrooms = chattingrooms.split(',')[:-1]
            print('onlineusers : ', onlineusers)
            print('chattingrooms : ', chattingrooms)
            for i in onlineusers:
                self.online_users_list.addItem(i)
                self.room_online.addItem(i)
            for i in chattingrooms:
                if i != 'temp_room':
                    self.room_list.addItem(i)
        except Exception as e:
            print(e)
            pass

    def refresh(self):
        print('refresh 1')
        self.client_socket.send('#refresh'.encode())
        print('refresh 2')
        message = self.client_socket.recv(1024).decode()
        print(message)
        print('refresh 3')
        self.recv_oac(message)
        print('refresh 4')

    def reading(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                print('message:', message)
                if '#onlineusers' in message:
                    self.recv_oac(message)

                elif '#joinuser' in message:
                    self.room_user_list.clear()
                    add_user = message.split(';')[1]
                    add_user2 = add_user.split(',')[:-1]
                    join_message = message.split(';')[0].split(',')[1]
                    print('add_user :', add_user)
                    for i in add_user2:
                        self.room_user_list.addItem(i)
                    self.main_chat.addItem(join_message)
                    self.client_socket.send('#refresh'.encode())

                elif '#exituser' in message:
                    exit_message = message.split(';')[0].split(',')[1]
                    now_users = message.split(';')[1].split(',')
                    print(now_users)
                    self.main_chat.addItem(exit_message)
                    self.room_user_list.clear()
                    for i in now_users:
                        self.room_user_list.addItem(i)
                elif '#inviteuser' in message:
                    room_name = message.split(',')[1]
                    self.reply = QMessageBox.question(self, 'Invite', '{} 방에서 초대하였습니다.'
                                                      .format(room_name),
                                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

                    if self.reply == QMessageBox.Yes:
                        print(room_name)
                        self.invite_join(room_name)
                    else:
                        pass

                else:
                    print('else')
                    self.main_chat.addItem(message)
            except Exception as e:
                print(e)
                pass

    def cam(self):
        global cap, img
        model = tensorflow.keras.models.load_model('keras_model.h5')
        cap = cv2.VideoCapture(0)
        size = (224, 224)
        classes = ['하이', '오케이', 'NoNo']
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
