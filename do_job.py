import time
from PIL import ImageGrab

thread_ongoing = False


def capturing_sequence(server_socket):
    while thread_ongoing:
        print("ongoing")
        self.showMinimized()
        time.sleep(0.3)
        img = ImageGrab.grab()
        server_socket.send_img(img)
        self.showNormal()
