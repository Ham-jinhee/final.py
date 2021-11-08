import sys
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QTableWidgetItem, QMessageBox, QApplication
from PyQt5.QtCore import QThread, pyqtSlot
from PyQt5 import QtCore
from PyQt5 import uic
import re

import socketio, time

ui_form = uic.loadUiType("RyuTalk_python.ui")[0]


class SocketClient(QThread):
  add_chat = QtCore.pyqtSignal(str)
  sio = socketio.Client()

  def __init__(self, parent=None):
    super().__init__()
    self.main = parent
    self.is_run = False
    self.ip = 1111
    self.localhost = 'localhost'

  def set_host(self, ip, port):
    self.ip = ip
    self.port = port

  def run(self):
    host = 'http://%s:%s' % (self.ip, self.port)

    self.connect(host)
    self.is_run = not self.is_run

  def connect(self, host):
    SocketClient.sio.on('receive', self.receive)
    SocketClient.sio.connect(host)
    self.add_chat.emit('채팅 서버와 접속 완료했습니다.')

  def send(self, msg, nmsg):
    SocketClient.sio.emit('send', nmsg)
    self.add_chat.emit('[나]:%s' % (msg))

  def receive(self, msg):
    self.add_chat.emit('%s' % (msg))


class ChatWindow(QMainWindow, ui_form):
  def __init__(self):
    super().__init__()
    self.setupUi(self)

    self.btn_send.clicked.connect(self.send_message)
    self.btn_connect.clicked.connect(self.socket_connection)
    self.sc = SocketClient(self)

    self.sc.add_chat.connect(self.add_chat)
    self.btn_make_room.clicked.connect(self.make_room)
    self.zzzz.clicked.connect(self.PageMinus2)

  def socket_connection(self):
    ip = self.input_ip.text()
    port = self.input_port.text()

    if (not ip) or (not port):
      self.add_chat('ip 또는 port 번호가 비었습니다.')
      return

    self.sc.set_host(ip, port)

    if not self.sc.is_run:
      self.sc.start()

  def send_message(self):

    if not self.sc.is_run:
      self.add_chat('서버와 연결 상태가 끊겨 있어 메시지를 전송할 수 없습니다.')
      return

    nick = self.input_nick.text()
    nmsg = "[" + nick +"] : "+ self.input_message.text()
    msg = self.input_message.text()
    try:
      self.sc.send(msg, nmsg)
      self.input_message.clear()
    except Exception as e:
      print(e)

  @pyqtSlot(str)
  def add_chat(self, msg):
    self.chats.appendPlainText(msg)

  def make_room(self):
    self.room = self.new_room_name.text()
    print("여기까진 됐겠지")
    print(self.room)
    if len(re.findall('\w', self.room)) < len(self.room):
      # self.room_check.setText('올바른 방이름을 적어주세요(공백/특수문자 제외)')
      self.new_room_name.clear()
      print("올바른 방이름")

    elif len(self.room) == 0:
      # self.room_check.setText('올바른 방이름을 적어주세요(공백/특수문자 제외)')
      self.new_room_name.clear()
      print("방이름을 적어라")

    elif len(re.findall('\s', self.room)) > 0:
      # self.room_check.setText('올바른 방이름을 적어주세요(공백/특수문자 제외)')
      self.new_room_name.clear()
      print("방이름 적으셈")

    else:
      self.SocketClient.send(f'#makeroom,{self.room},{self.user_id}'.encode())
      self.new_room_name.clear()
      print("방이 만들어졌나")

      # self.room_user_list.addItem(self.user_id)
      # self.stackedWidget.setCurrentWidget(self.room_page)

  def PageMinus2(self):
    currentpage = myWindow.stackedWidget.currentIndex()
    myWindow.stackedWidget.setCurrentIndex(currentpage - 2)


if __name__ == "__main__":
  app = QApplication(sys.argv)
  myWindow = ChatWindow()
  myWindow.setWindowTitle('류톡 채팅 프로그램')
  myWindow.show()
  app.exec_()