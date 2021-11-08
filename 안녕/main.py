import sys
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QTableWidgetItem, QMessageBox, QApplication
from PyQt5.QtCore import QThread, pyqtSlot
from PyQt5 import QtCore
from PyQt5 import uic

import socketio, time
from socket import *

ui_form = uic.loadUiType("RyuTalk_python.ui")[0]

class SocketClient(QThread):
  add_chat = QtCore.pyqtSignal(str)
  sio = socketio.Client()

  def __init__(self, parent=None):
    super().__init__()
    self.main = parent
    self.is_run = False
    # self.ip = 4200
    # self.localhost = '192.168.0.72'

  def set_host(self, ip, port):
    self.ip = ip
    self.port = port

  def run(self):
    host = 'http://%s:%s' % (self.ip, self.port)

    self.connect(host)
    self.is_run = not self.is_run

  def connect(self, host):
    print("연결시작1")
    SocketClient.sio.on('receive', self.receive)
    SocketClient.sio.connect(host)
    self.add_chat.emit('채팅 서버와 접속 완료했습니다.')
    print("연결완료1")

  def send(self, msg):
    SocketClient.sio.emit('send', msg)
    self.add_chat.emit('[나]:%s' % (msg))

  def receive(self, msg):
    self.add_chat.emit('[상대방] %s' % (msg))

class ChatWindow(QMainWindow, ui_form):
  def __init__(self):
    super().__init__()
    self.setupUi(self)

    self.btn_connect.clicked.connect(self.socket_connection)  # ip/port 연결
    self.btn_send.clicked.connect(self.send_message) # 입력 버튼 클릭시 send_message 호출
    self.sc = SocketClient(self)
    self.sc.add_chat.connect(self.add_chat)

    sc = SocketClient(self)  # 쓰레드 객체 생성 #
    sc.start(1)  # 쓰레드 객체 실행(run() 메서드 실행) #

  def socket_connection(self):
    print("연결시작2")
    ip = self.input_ip.text()
    print("IP")
    port = self.input_port.text()
    print("port")
    # ip = '192.168.0.72'
    # port = 4200
    print("여기까지 완료")

    self.sc = SocketClient(self)
    if (not ip) or (not port):
      self.add_chat('ip 또는 port 번호가 비었습니다.')
      return

    self.sc.set_host(ip, port)
    print("예쓰")
    if not self.sc.is_run:
      self.sc.start()

  def send_message(self):
    print(self.input_message.text())  # object_name이 input_message에서 입력값 가져오기
    if not self.sc.is_run: # 서버 연결상태가 아닐 경우 메세지 송출
      self.add_chat('서버와 연결 상태가 끊겨 있어 메시지를 전송할 수 없습니다.')
      return

    msg = self.input_message.text()  # 입력 메시지 가져오기
    #self.add_chat('[나] %s' % (msg))  # 화면에 출력
    self.sc.send('[나]:%s'%(msg))# 화면에 출력
    self.input_message.setText('')  # 입력창 지우기



  @pyqtSlot(str)
  def add_chat(self, msg):
    self.chats.appendPlainText(msg)

if __name__ == "__main__":
  app = QApplication(sys.argv)
  myWindow = ChatWindow()
  myWindow.setWindowTitle('류톡 채팅 프로그램')
  myWindow.show()
  app.exec_()