import sys
import time

from PyQt5.QtCore import QCoreApplication, pyqtSlot
from PyQt5.QtWidgets import *

import client
import threading
import click


def print_debug(line):
    if True:
        print(line)


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'MarketPOSReader'
        self.setWindowTitle(self.title)
        self.setGeometry(800, 400, 300, 200)

        self.table_widget = Table(self)
        self.setCentralWidget(self.table_widget)

        self.show()


class Table(QWidget):
    server_socket = None
    capturing_thread = None
    thread_ongoing = False

    company_id = None
    company_name = None
    company_address = None
    company_table_address = None
    company_table_count = None

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(300, 200)

        self.tabs.addTab(self.tab1, "Settings")
        self.tabs.addTab(self.tab2, "POS-Reader")

        self.name_input = QPushButton('매장명 변경')
        self.table_input = QPushButton('테이블 변경')
        self.region_input = QPushButton('매장주소 변경')
        self.number_input = QPushButton('최대수용인원 변경')

        notification = ""

        try:
            f = open('company.txt', 'r', encoding='utf-8')
            info = f.read().split('\n')
            self.company_id = info[0]
            self.company_name = info[1]
            self.company_address = info[2]
            self.company_table_address = info[3]
            self.company_table_count = info[4]
            notification = "매장 정보 설정이 완료되었습니다.\nPOS-Reader 탭에서 정보 전송을 진행해주세요."

        except FileExistsError and FileNotFoundError:
            self.new_market()

        except IndexError:
            notification = "매장 정보 설정이 미완료 되었습니다.\n정보를 갱신하고 POS-Reader 탭으로 이동해주세요."

        self.name_input.clicked.connect(self.name_dialog)
        self.table_input.clicked.connect(self.table_dialog)
        self.region_input.clicked.connect(self.region_dialog)
        self.number_input.clicked.connect(self.number_dialog)
        self.notification_label = QLabel(notification, self)

        self.tab1.layout = QVBoxLayout(self)
        self.tab1.layout.addWidget(self.name_input)
        self.tab1.layout.addWidget(self.table_input)
        self.tab1.layout.addWidget(self.region_input)
        self.tab1.layout.addWidget(self.number_input)
        self.tab1.layout.addWidget(self.notification_label)
        self.tab1.setLayout(self.tab1.layout)

        self.capture_button = QPushButton('POS 캡쳐 및 전송')
        self.connect_server_button = QPushButton('서버 연결')
        self.cancel_button = QPushButton('종료')
        self.capture_button.clicked.connect(self.start_capture)
        self.cancel_button.clicked.connect(QCoreApplication.instance().quit)
        self.connect_server_button.clicked.connect(self.connect_server)

        self.tab2.layout = QVBoxLayout(self)
        self.tab2.layout.addWidget(self.capture_button)
        self.tab2.layout.addWidget(self.connect_server_button)
        self.tab2.layout.addWidget(self.cancel_button)
        self.tab2.setLayout(self.tab2.layout)

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        self.read_info()

    def start_capture(self):
        if self.server_socket is not None:
            if self.capture_button.text() == 'POS 캡쳐 및 전송':
                self.window().hide()
                time.sleep(0.5)
                self.window().show()
                self.capture_button.setText('캡쳐 중지')
                client.socket_communicator.thread_ongoing = True
                self.capturing_thread = threading.Thread(target=self.server_socket.capturing_sequence,
                                                         args=(self.server_socket,))
                self.capturing_thread.start()

            elif self.capture_button.text() == '캡쳐 중지':
                self.capture_button.setText('POS 캡쳐 및 전송')
                client.socket_communicator.thread_ongoing = False
        else:
            self.server_msg_dialog()

    def connect_server(self):
        try:
            self.server_socket = client.socket_communicator('localhost', 5001)
            self.server_socket.company_id = self.company_id
            print('server connected')
        except:
            print('connection failure')
            self.server_msg_dialog()

    def server_msg_dialog(self):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText("서버 연결을 실패했습니다.")
        msg_box.setWindowTitle("서버 연결 실패")
        msg_box.setStandardButtons(QMessageBox.Ok)
        return_value = msg_box.exec()
        if return_value == QMessageBox.Ok:
            print('OK clicked')

    def name_dialog(self):
        if self.server_socket is not None:
            text, ok = QInputDialog.getText(self, '매장명 변경', '매장명:')

            if ok:
                self.server_socket.change_setting(0, text)
        else:
            print('server connection needed')
            self.server_msg_dialog()

    def table_dialog(self):
        if self.server_socket is not None:
            self.window().hide()
            time.sleep(0.5)
            point, color = click.click_img(6)
            self.window().show()
            self.server_socket.change_setting(1, (point, color))
        else:
            print('server connection needed')
            self.server_msg_dialog()

    def region_dialog(self):
        if self.server_socket is not None:
            text, ok = QInputDialog.getText(self, '매장주소 변경', '매장주소:')

            if ok:
                self.server_socket.change_setting(2, text)
        else:
            print('server connection needed')
            self.server_msg_dialog()

    def number_dialog(self):
        if self.server_socket is not None:
            text, ok = QInputDialog.getText(self, '수용인원 변경', '수용인원:')

            if ok:
                self.server_socket.change_setting(3, text)
        else:
            print('server connection needed')
            self.server_msg_dialog()

    def read_info(self):
        try:
            f = open('company.txt', 'r', encoding='utf-8')
            info = f.read().split('\n')
            self.company_id = info[0]
            self.company_name = info[1]
            self.company_address = info[2]
            self.company_table_address = info[3]
            self.company_table_count = info[4]

        except FileExistsError and FileNotFoundError:
            self.new_market()
        except IndexError:
            print('File not correct')

    def new_market(self):
        self.connect_server()
        new_id = self.server_socket.create_new_market()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
