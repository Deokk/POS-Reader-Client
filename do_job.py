import time
from PIL import ImageGrab

thread_ongoing = False


def capturing_sequence(server_socket):
    while thread_ongoing:
        print("ongoing")
        img = ImageGrab.grab()
        server_socket.send_img(img)
