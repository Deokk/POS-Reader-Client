import sys
from PyQt5.QtCore import QCoreApplication, pyqtSlot
from PyQt5.QtWidgets import *

import client
import threading
import do_job


def print_debug(line):
    if True:
        print(line)


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'MarketPOSReader'
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, 300, 200)

        self.table_widget = Table(self)
        self.setCentralWidget(self.table_widget)

        self.show()


class Table(QWidget):
    s = None
    company_id = None
    company_name = None
    company_address = None
    company_table_address = None
    company_table_count = None
    t = None
    thread_ongoing = False

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(300, 200)

        self.tabs.addTab(self.tab1, "POS-Reader")
        self.tabs.addTab(self.tab2, "Settings")

        self.capture_button = QPushButton('POS 캡쳐 및 전송')
        self.connect_server_button = QPushButton('서버 연결')
        self.cancel_button = QPushButton('종료')
        self.capture_button.clicked.connect(self.start_capture)
        self.cancel_button.clicked.connect(QCoreApplication.instance().quit)
        self.connect_server_button.clicked.connect(self.connect_server)

        self.tab1.layout = QVBoxLayout(self)
        self.tab1.layout.addWidget(self.capture_button)
        self.tab1.layout.addWidget(self.connect_server_button)
        self.tab1.layout.addWidget(self.cancel_button)
        self.tab1.setLayout(self.tab1.layout)

        self.name_input = QPushButton('매장명 변경')
        self.table_input = QPushButton('테이블 변경')
        self.region_input = QPushButton('매장주소 변경')
        self.number_input = QPushButton('최대수용인원 변경')
        self.name_input.clicked.connect(self.name_dialog)
        self.table_input.clicked.connect(self.table_dialog)
        self.region_input.clicked.connect(self.region_dialog)
        self.number_input.clicked.connect(self.number_dialog)

        self.tab2.layout = QVBoxLayout(self)
        self.tab2.layout.addWidget(self.name_input)
        self.tab2.layout.addWidget(self.table_input)
        self.tab2.layout.addWidget(self.region_input)
        self.tab2.layout.addWidget(self.number_input)
        self.tab2.setLayout(self.tab2.layout)

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        self.read_info()

    def start_capture(self):
        if self.capture_button.text() == 'POS 캡쳐 및 전송':
            self.capture_button.setText('캡쳐 중지')
            self.capturing_thread = threading.Thread(target=do_job.capturing_sequence, args=(self.server_socket,))
            self.capturing_thread.start()

        elif self.capture_button.text() == '캡쳐 중지':
            self.capture_button.setText('POS 캡쳐 및 전송')
            do_job.thread_ongoing = False

    def connect_server(self):
        try:
            self.server_socket = client.socket_communicator('localhost', 5001)
            print('server connected')
        except:
            print('connection failure')

    def name_dialog(self):
        text, ok = QInputDialog.getText(self, '매장명 변경', '매장명:')

        if ok:
            self.le.setText(str(text))

    def table_dialog(self):
        text, ok = QInputDialog.getText(self, '테이블 변경', '테이블:')

        if ok:
            self.le.setText(str(text))

    def region_dialog(self):
        text, ok = QInputDialog.getText(self, '매장주소 변경', '매장주소:')

        if ok:
            self.le.setText(str(text))

    def number_dialog(self):
        text, ok = QInputDialog.getText(self, '수용인원 변경', '매장주소:')

        if ok:
            self.le.setText(str(text))

    def read_info(self):
        try:
            f = open('company.txt', 'r', encoding='utf-8')
            info = f.read().split('\n')
            self.company_id = info[0]
            self.company_name = info[1]
            self.company_address = info[2]
            self.company_table_address = info[3]
            self.company_table_count = info[4]
        except FileExistsError or FileNotFoundError:
            print('Creation Needed')  # 여기서 팝업 창 띄울 것
        except IndexError:
            print('File not correct')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
