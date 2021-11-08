import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5 import uic
import socket
from threading import Thread
import tensorflow.keras
import re
import cv2
import numpy as np
from os import listdir
from os.path import isdir
from os.path import isfile, join
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

form_class = uic.loadUiType("RyuTalk_1104.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self) #유아이 셋팅
        self.stackedWidget.setCurrentWidget(self.login_page)  # 첫화면 -로그인페이지
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 소켓 생성
        self.Host = '10.10.21.118' # 서버 아이피
        self.Port = 7500  #서버 포트번호
        self.client_socket.connect((self.Host, self.Port)) #서버 연결
        self.user_id = ''  # 접속중인 아이디
        self.room = '' #접속중인 채팅방이름
        self.login_btn.clicked.connect(self.login) #로그인페이지- 로그인 버튼
        self.face_btn.clicked.connect(self.facelogin)  # 로그인 페이지 - face_login 버튼
        self.signup_btn.clicked.connect(self.signup)  # 로그인페이지-회원가입 버튼
        self.btn_id_check.clicked.connect(self.id_check) #회원가입 페이지- 아이디 중복체크
        self.signup_ok_btn.clicked.connect(self.signup_check)  # 회원가입 페이지- 회원가입 완료 버튼
        self.face.clicked.connect(self.facejoin)  # 회원가입 페이지- face 버튼
        self.make_room_btn.clicked.connect(self.make_room) #대기창- 채팅방 만들기 버튼
        self.refresh_btn.clicked.connect(self.refresh) #대기창- 새로고침 버튼
        self.room_list.itemDoubleClicked.connect(self.room_join) #채팅방입장 - 채팅방목록에서 더블클릭
        self.make_pw_room_btn.clicked.connect(self.go_pw_room) #비밀방 만드는 페이지 넘어가는 버튼
        self.make_room_btn_2.clicked.connect(self.make_pw_room) #비밀채팅방 생성버튼
        self.make_room_btn_cancel.clicked.connect(self.cancel) #비밀채팅방 취소-대기방페이지로 돌아가기
        self.join_room_btn.clicked.connect(self.join_room) #비밀채팅방- 입장 버튼
        self.join_room_btn_cancel.clicked.connect(self.cancel) #비밀채팅방 -입장 취소 버튼
        self.room_exit_btn.clicked.connect(self.exit_room) #채팅방 나가기 버튼
        self.room_online.itemDoubleClicked.connect(self.room_invite) #유저초대 - 접속중인 유저목록에서 더블클릭
        self.room_send_btn.clicked.connect(self.write)  # 입력 버튼
        self.room_motion.clicked.connect(self.cam) # 모션채팅 버튼

    #1로그인
    def login(self):
        user_id = self.id_line.text()
        user_pw = self.pw_line.text()
        self.client_socket.send(f'#my_id_pw,{user_id},{user_pw}'.encode()) # 소켓에 정보 전송
        message = self.client_socket.recv(1024).decode()
        if message == '2':
            QtWidgets.QMessageBox.about(self, "QMessageBox", "회원정보가 일치하지 않습니다.")
            self.id_line.clear()
            self.pw_line.clear()
        else:
            read_thread = Thread(target=self.reading, daemon=True)
            read_thread.start()
            self.user_id = user_id
            self.stackedWidget.setCurrentWidget(self.room_list_page)
            self.refresh()

    # 2
    def facelogin(self):
        self.trains()
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
                min_score = 999  # 가장 낮은 점수로 예측된 사람의 점수
                min_score_name = ""  # 가장 높은 점수로 예측된 사람의 이름
                # 검출된 사진을 흑백으로 변환
                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                # 위에서 학습한 모델로 예측시도
                for key, model in self.models.items():
                    result = model.predict(face)
                    if min_score > result[1]:
                        min_score = result[1]
                        min_score_name = key
                        print(min_score)
                # min_score 신뢰도이고 0에 가까울수록 자신과 같다는 뜻이다.
                if min_score < 500:
                    # 백분율로 표시
                    confidence = int(100 * (1 - (min_score) / 300))
                    # 유사도 화면에 표시
                    display_string = str(confidence) + '% Confidence it is ' + min_score_name
                cv2.putText(image, display_string, (100, 120), cv2.FONT_HERSHEY_COMPLEX, 1, (250, 120, 255), 2)
                # 60 보다 크면 동일 인물로 간주해 UnLocked!
                if confidence > 80:
                    cv2.putText(image, "Unlocked : " + min_score_name, (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1,
                                (0, 255, 0),
                                2)
                    cv2.imshow('Face Cropper', image)
                    login_info = min_score_name.split(',')
                    id_temp = login_info[0]
                    pw_temp = login_info[1]
                    self.id_line.setText(id_temp)
                    self.pw_line.setText(pw_temp)

                    if cv2.waitKey(1) == 13:
                        self.login()
                        print("오키")

                        break
                else:
                    # 60 미만이면 타인.. Locked!!!
                    cv2.putText(image, "Locked", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
                    cv2.imshow('Face Cropper', image)

            except:
                # 얼굴 검출 안됨
                cv2.putText(image, "Face Not Found", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                cv2.imshow('Face Cropper', image)
                pass

            if cv2.waitKey(1) == 13:
                break

        cap.release()
        cv2.destroyWindow('Face Cropper')
        print("오키1")
        # self.login()
    #3
    def signup(self):
        self.stackedWidget.setCurrentWidget(self.signup_page)

    # 4
    def id_check(self):
        id_temp = self.id.text()
        self.client_socket.send(f'#idcheck,{id_temp}'.encode())
        message = self.client_socket.recv(1024).decode()
        if message == '2':
            QtWidgets.QMessageBox.about(self, "QMessageBox", "이미 존재하는 아이디입니다.")
            self.id.clear()
        else:
            QtWidgets.QMessageBox.about(self, "QMessageBox", "사용 가능한 아이디입니다.")
    #5
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
    #6
    def facejoin(self):  ##### 1.사진저장########## +가입한 회원 모델학습

        face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        name = self.id.text()
        password = self.pw.text()

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
        # 폴더만들기
        path = 'faces/' + name + ',' + password
        try:
            if not os.path.exists(path):
                os.makedirs(path)
        except OSError:
            print('Error: Creating directory. ' + path)

        while True:
            ret, frame = cap.read()
            if face_extractor(frame) is not None:
                count += 1
                face = cv2.resize(face_extractor(frame), (200, 200))
                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                file_name_path = 'faces/' + name + ',' + password + '/' + str(count) + '.jpg'
                cv2.imwrite(file_name_path, face)
                cv2.imshow('Face Cropper', face)

            else:
                print("Face not Found")
                path = 'C:/Users/jeongseon/PycharmProjects/pythonProject1/faces/' + name + ',' + password + '/' + str(
                    count) + '.jpg'
                os.remove(path)
                pass
            count += 1

            # 얼굴 사진 300장을 다 얻으면 종료
            if cv2.waitKey(1) == 13 or count == 300:
                break
        cap.release()
        cv2.destroyWindow('Face Cropper')

        self.trains()
        self.signup_check()
        self.stackedWidget.setCurrentWidget(self.login_page)
        print('Colleting Samples Complete!!!')
    #7
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
    #8
    def refresh(self):
        self.client_socket.send('#refresh'.encode())
        message = self.client_socket.recv(1024).decode()
        print(message)
        self.recv_oac(message)
    #9
    def room_join(self):
        self.room = self.room_list.currentItem().text()
        if '\U0001F512' in self.room:
            self.stackedWidget.setCurrentWidget(self.pw_input_page)
        else:
            self.client_socket.send(f'#roomjoin,{self.room},{self.user_id}'.encode())
            self.stackedWidget.setCurrentWidget(self.room_page)
    #10
    def go_pw_room(self):
        self.stackedWidget.setCurrentWidget(self.pw_make_page)
    #11
    def make_pw_room(self):
        self.room_name_check = self.room_name_line_2.text()
        self.room_pw_check = self.room_pw_line.text()
        room_name = "\U0001F512{}".format(self.room_name_check)
        self.client_socket.send(
            f'#makepwroom,{room_name},{self.user_id},{self.room_pw_check}'.encode())
        self.room_user_list.addItem(self.user_id)
        self.room_name_line.clear()
        self.room_pw_line.clear()
        self.stackedWidget.setCurrentWidget(self.room_page)

    #12
    def cancel(self):
        self.stackedWidget.setCurrentWidget(self.room_list_page)
    #13
    def join_room(self):
        self.room_pw = self.lineedit_pw.text()
        self.client_socket.send(f'#pwroomjoin,{self.room},{self.user_id},{self.room_pw}'.encode())
        self.lineedit_pw.clear()
        self.stackedWidget.setCurrentWidget(self.room_page)
    #14
    def exit_room(self):
        self.stackedWidget.setCurrentWidget(self.room_list_page)
        self.main_chat.clear()
        self.client_socket.send(f'#exit,{self.room},{self.user_id}'.encode())
    #15
    def room_invite(self):
        invite_id = self.room_online.currentItem().text()
        self.reply = QMessageBox.question(self, 'Invite', '{} 유저를 {} 방으로 초대하시겠습니까?'
                                          .format(invite_id, self.room),
                                          QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if self.reply == QMessageBox.Yes:
            self.client_socket.send(f'#invite,{self.room},{invite_id}'.encode())
        else:
            pass
    #16
    def write(self):
        self.client_socket.send(f'{self.room}${self.user_id} : {self.room_chat.text()}'.encode())
        self.room_chat.clear()

    #17
    def cam(self):
        global cap, img
        model = tensorflow.keras.models.load_model('keras_model.h5')
        cap = cv2.VideoCapture(0)
        size = (224, 224)
        classes = ['하이', '오케이', '노노']
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
            if cv2.waitKey(1) == 13:
                break
        cap.release()
        cv2.destroyAllWindows()
    #18
    def train(self,name):  # 회원가입시 모델학습
        data_path = 'faces/' + name + '/'
        # 파일만 리스트로 만듬
        face_pics = [f for f in listdir(data_path) if isfile(join(data_path, f))]
        Training_Data, Labels = [], []
        for i, files in enumerate(face_pics):
            image_path = data_path + face_pics[i]
            images = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            # 이미지가 아니면 패스
            if images is None:
                continue
            Training_Data.append(np.asarray(images, dtype=np.uint8))
            Labels.append(i)
        if len(Labels) == 0:
            print("There is no data to train.")
            return None
        Labels = np.asarray(Labels, dtype=np.int32)
        # 모델 생성
        model = cv2.face.LBPHFaceRecognizer_create()
        # 학습
        model.train(np.asarray(Training_Data), np.asarray(Labels))
        print(name + " : Model Training Complete!!!!!")
        # 학습 모델 리턴
        return model
    #19
    def trains(self):  # 로그인시 전체모델 학습
        # faces 폴더의 하위 폴더를 학습
        data_path = 'faces/'
        # 폴더만 색출
        model_dirs = [f for f in listdir(data_path) if isdir(join(data_path, f))]
        # 학습 모델 저장할 딕셔너리
        self.models = {}
        # 각 폴더에 있는 얼굴들 학습
        for model in model_dirs:
            print('model :' + model)
            # 학습 시작
            result = self.train(model)
            # 학습이 안되었다면 패스!
            if result is None:
                continue
            # 학습되었으면 저장
            print('model2 :' + model)
            self.models[model] = result
        # 학습된 모델 딕셔너리 리턴
        return self.models

    #20
    def invite_join(self, invite_room):
        self.client_socket.send(f'#roomjoin,{invite_room},{self.user_id}'.encode())
        self.stackedWidget.setCurrentWidget(self.room_page)
        # self.refresh()

   #21
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
    #22
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()