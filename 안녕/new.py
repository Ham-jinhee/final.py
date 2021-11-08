import sys
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QTableWidgetItem, QMessageBox, QApplication
from PyQt5.QtCore import QThread, pyqtSlot
from PyQt5 import QtCore
from PyQt5 import uic
from socket import *
import threading

ui_form = uic.loadUiType("RyuTalk_python11111.ui")[0]

class ChatWindow(QMainWindow, ui_form) :

  def __init__(self):
    super().__init__()
    self.setupUi(self)
    # data.conn_soc = None  # 서버와 연결된 소켓
    port=5200

    clientsock=socket(AF_INET,SOCK_STREAM)
    clientsock.connect(('192.168.0.72',port)) # 나 자신에게 포트를 연결해라.
    self.chats.addItem('연결되었습니다.')
    print("서버연결")

    # self.btn_connect.clicked.connect(self.socket_connection)  # ip/port
    self.btn_send.clicked.connect(self.send_message) # 입력 버튼 클릭시 send_message 호출
    self.btn_join.clicked.connect(self.PagePlus1) # 회원가입 버튼
    self.btn_choice_room.clicked.connect(self.PagePlus1) # 채팅방 선택하기 버튼
    self.btn_out.clicked.connect(self.PageMinus1) # 채팅창 나가기
    self.btn_back.clicked.connect(self.PageMinus1) # 채팅방선택창 뒤로가기

  def PagePlus1(self):
    currentpage = myWindow.stackedWidget.currentIndex()
    myWindow.stackedWidget.setCurrentIndex(currentpage + 1)

  def PagePlus2(self):
    currentpage = myWindow.stackedWidget.currentIndex()
    myWindow.stackedWidget.setCurrentIndex(currentpage + 2)

  def PagePlus3(self):
    currentpage = myWindow.stackedWidget.currentIndex()
    myWindow.stackedWidget.setCurrentIndex(currentpage + 3)

  def PageMinus1(self):
    currentpage = myWindow.stackedWidget.currentIndex()
    myWindow.stackedWidget.setCurrentIndex(currentpage - 1)

  def PageMinus2(self):
    currentpage = myWindow.stackedWidget.currentIndex()
    myWindow.stackedWidget.setCurrentIndex(currentpage - 2)

  # def socket_connection(self): # 소켓 연결
  #   print("ㅎㅎㅎ")
  #   port=4200
  #
  #   clientsock=socket(AF_INET,SOCK_STREAM)
  #   clientsock.connect(('localhost',port))
  #   self.chats.addItem('연결되었습니다.')
  #   print("왜")

  def send_message(self):
    global clientsock
    msg = self.input_message.text()  # 입력 메시지 가져오기
    self.chats.addItem('[나]:%s' % (msg))
    self.input_message.setText('')  # 입력창 지우기
    print(msg)

    # clientsock.send(msg.encode('utf-8'))# encode는 문자열을 byte로 변환해주는 메소드
    self.clientsock.send(f'{self.room}${self.user_id} : {self.input_message.text()}'.encode())
    print("여긴가")


    # data.send(msg.encode('utf-8'))  # 인자값으로 클라이언트 소켓을 받아야 합니다. 소켓 데이터값.
    # print("여긴가")
    # sender = threading.Thread(target=send, args=(clientSock,))
    # print("너니")
    # sender.start()
    # print("여기까진 안오겠지")
    # clientSock.send(msg.encode('utf-8'))

  def receive(self):
    global clientsock
    while True:
      recvData = clientsock.recv(1024)
      print('상대방: ', recvData.decode('utf-8'))


if __name__ == "__main__":
  app = QApplication(sys.argv)
  myWindow = ChatWindow()
  myWindow.setWindowTitle('RyuTalk 채팅')
  myWindow.show()
  app.exec_()