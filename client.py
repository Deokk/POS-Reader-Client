import socket
import cv2
import numpy as np
import time
from PIL import ImageGrab
import MarketPOSReader


class socket_communicator:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    company_id = None
    thread_ongoing = False

    def __init__(self, tcp_ip: str, tcp_port: int):
        self.s.connect((tcp_ip, tcp_port))

    def capturing_sequence(self, server_socket):
        while self.thread_ongoing:
            print("image ongoing")
            img = ImageGrab.grab()
            server_socket.send_img(img)

    def send_img(self, img):
        try:
            job_number = "1"
            self.s.sendall(self.company_id.encode())
            time.sleep(1)
            self.s.sendall(job_number.encode())
            img_np = np.array(img)
            img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
            binary_cv = cv2.imencode('.PNG', img_np)[1].tobytes()
            img_size = len(binary_cv).to_bytes(4, byteorder="little")
            self.s.sendall(img_size)
            time.sleep(1)
            self.s.sendall(binary_cv)
        except ConnectionError:
            print('Connection needed')  # 팝업창 필요 : 서버와의 연결을 확인해주세요
            MarketPOSReader.Table.server_msg_dialog()
            self.s.close()
            self.thread_ongoing = False
        except OSError:
            print('Connection needed')  # 팝업창 필요 : 서버와의 연결을 확인해주세요
            MarketPOSReader.Table.server_msg_dialog()
            self.s.close()
            self.thread_ongoing = False

    def change_setting(self, setting_number: int, text: str or tuple):
        try:
            self.s.sendall(self.company_id.encode())
            time.sleep(1)
            job_number = "2"
            self.s.sendall(job_number.encode())
            time.sleep(1)
            self.s.sendall(str(setting_number).encode())

            if setting_number == 1:
                point, color = text
                self.s.sendall(str(len(str(point))).encode())
                time.sleep(1)
                self.s.sendall(str(point).encode())
                time.sleep(1)
                self.s.sendall(str(len(str(color))).encode())
                time.sleep(1)
                self.s.sendall(str(color).encode())
            else:
                self.s.sendall(str(len(text.encode())).encode())
                time.sleep(1)
                self.s.sendall(text.encode())
        except ConnectionError:
            print('Connection needed')  # 팝업창 필요 : 서버와의 연결을 확인해주세요
            MarketPOSReader.Table.server_msg_dialog()
            self.s.close()
            self.thread_ongoing = False
        except OSError:
            print('Connection needed')  # 팝업창 필요 : 서버와의 연결을 확인해주세요
            MarketPOSReader.Table.server_msg_dialog()
            self.s.close()
            self.thread_ongoing = False

    def create_new_market(self):
        try:
            job_number = "0"
            self.s.sendall(job_number.encode())
            # new_id = int((self.s.recv(4)).decode())
            new_id = 3
            print('Creation Needed')  # 여기서 팝업 창 띄울 것 : 세팅을 진행해주세요 with new_id
            # string으로 전부 받아와서 진행
            MarketPOSReader.Table.number_dialog()
            MarketPOSReader.Table.region_dialog()
            MarketPOSReader.Table.name_dialog()

        except ConnectionError:
            print('Connection needed')  # 팝업창 필요 : 서버와의 연결을 확인해주세요
            MarketPOSReader.Table.server_msg_dialog()
            self.s.close()
            self.thread_ongoing = False
        except OSError:
            print('Connection needed')  # 팝업창 필요 : 서버와의 연결을 확인해주세요
            MarketPOSReader.Table.server_msg_dialog()
            self.s.close()
            self.thread_ongoing = False
