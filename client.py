import socket
import cv2
import numpy as np


class socket_communicator:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, tcp_ip: str, tcp_port: int):
        self.s.connect((tcp_ip, tcp_port))

    def send_img(self, img):
        company_id = "1"
        job_number = "1"
        self.s.sendall(company_id.encode())
        self.s.sendall(job_number.encode())
        img_np = np.array(img)
        img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        binary_cv = cv2.imencode('.PNG', img_np)[1].tobytes()
        img_size = len(binary_cv).to_bytes(4,byteorder="little")
        self.s.sendall(img_size)
        self.s.sendall(binary_cv)
