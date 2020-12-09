import sys
import time
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtWidgets import *
from PIL import ImageGrab
import client
import threading


def print_debug(line):
    if True:
        print(line)


class MarketPOSReader(QWidget):
    s = None
    company_id = None
    t = None
    thread_ongoing = False

    def __init__(self):
        super().__init__()

        self.market_ID = 'test'
        self.id = 'id'
        self.pw = 'pw'
        self.capture_button = QPushButton('POS 캡쳐 및 전송')
        self.setting_button = QPushButton('매장 정보 설정')
        self.cancel_button = QPushButton('종료', self)
        self.connect_server_button = QPushButton('서버 연결')
        self.initUI()
        self.read_info()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def start_capture(self):
        if self.capture_button.text() == 'POS 캡쳐 및 전송':
            self.capture_button.setText('캡쳐 중지')
            self.thread_ongoing = True
            # self.showMinimized()
            # time.sleep(0.3)
            # img = ImageGrab.grab()
            # self.s.send_img(img)
            # self.showNormal()
            self.t = threading.Thread(target=self.capturing_sequence)
            self.t.start()

        elif self.capture_button.text() == '캡쳐 중지':
            self.capture_button.setText('POS 캡쳐 및 전송')
            self.thread_ongoing = False

    def capturing_sequence(self):
        while self.thread_ongoing:
            print_debug("sequence ongoing")
            time.sleep(5)
            img = ImageGrab.grab()
            self.s.send_img(img)

    def connect_server(self):
        try:
            self.s = client.socket_communicator('localhost', 5001)
            print('server connected')
        except:
            print('connection failure')

    def read_info(self):
        try:
            f = open('company.txt', 'r', encoding='utf-8')
            info = f.readline()
            self.company_id = info
            print_debug(f.readline())  # 주소
        except FileExistsError or FileNotFoundError:
            print('Creation Needed')
        except IndexError:
            print('Information file Error')

    def initUI(self):
        self.center()
        self.capture_button.clicked.connect(self.start_capture)
        self.cancel_button.clicked.connect(QCoreApplication.instance().quit)
        self.connect_server_button.clicked.connect(self.connect_server)

        sub_box = QHBoxLayout()
        sub_box.addStretch(1)
        sub_box.addWidget(self.setting_button)
        sub_box.addWidget(self.cancel_button)
        sub_box.addStretch(1)

        main_box = QHBoxLayout()
        main_box.addStretch(2)
        main_box.addWidget(self.capture_button)
        main_box.addStretch(2)

        main_box.addStretch(3)
        main_box.addWidget(self.connect_server_button)
        main_box.addStretch(3)

        v_box = QVBoxLayout()
        v_box.addStretch(1)
        v_box.addLayout(main_box)
        v_box.addStretch(1)
        v_box.addLayout(sub_box)
        v_box.addStretch(1)

        self.setLayout(v_box)
        self.setWindowTitle('MarketPOSReader')
        self.setGeometry(300, 300, 300, 200)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MarketPOSReader()
    sys.exit(app.exec_())
