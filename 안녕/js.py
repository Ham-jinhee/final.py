import sys
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QTableWidgetItem, QMessageBox, QApplication
from PyQt5.QtCore import QThread, pyqtSlot
from PyQt5 import QtCore
from PyQt5 import uic

ui_form = uic.loadUiType("RyuTalk_python.ui")[0]


class SocketClient(QThread):
    add_chat = QtCore.pyqtSignal(str)

    def init(self, parent=None):
        super().init()
        self.main = parent
        self.is_run = False

    def run(self):
        self.is_run = not self.is_run
        print('data receive listen')
        self.add_chat.emit('채팅 서버와 접속 완료했습니다.')

    def send(self, msg):
        self.add_chat.emit(msg)

class ChatWindow(QMainWindow, ui_form):
    def init(self):
        super().init()
        self.setupUi(self)

        self.btn_send.clicked.connect(self.send_message)
        self.btn_connect.clicked.connect(self.socket_connection)
        self.sc = SocketClient(self)

        self.sc.add_chat.connect(self.add_chat)

    def socket_connection(self):
        ip = self.input_ip.toPlainText()
        port = self.input_port.toPlainText()

        print(ip, port)

        if not self.sc.is_run:
            self.sc.start(1)

    def send_message(self):
        if not self.sc.is_run:
            self.add_chat('서버와 연결 상태가 끊겨 있어 메시지를 전송할 수 없습니다.')
            return

        msg = self.input_message.toPlainText()
        self.add_chat('[나] %s' % (msg))
        self.input_message.setPlainText('')

    @pyqtSlot(str)
    def addchat(self, msg):
        self.chats.appendPlainText(msg)


if __name__ == "__main__":
  app = QApplication(sys.argv)
  myWindow = ChatWindow()
  myWindow.setWindowTitle('류톡 채팅 프로그램')
  myWindow.show()
  app.exec_()