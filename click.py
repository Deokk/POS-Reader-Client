import cv2 as cv  # OpenCV import
import mouse
import time
from PIL import ImageGrab

table = 0
point = []


# 마우스 이벤트 콜백함수 정의


def mouse_callback(event, y, x, flags, param):
    global max_count
    if mouse.is_pressed("left"):
        point.append([x, y, param[x][y], False])
        print(x, y)
        max_count = max_count + 1
        time.sleep(0.1)


def call_img():
    img = ImageGrab.grab()
    return img


def click_img(table_count):
    max_count = 0
    img = call_img()
    table = table_count
    cv.namedWindow('image_click')  # 마우스 이벤트 영역 윈도우 생성
    cv.setMouseCallback('image_click', mouse_callback, param=img)

    while True:
        cv.imshow('image_click', img)
        if max_count == table:
            max_count = 0
            break
        k = cv.waitKey(1) & 0xFF
    cv.destroyAllWindows()

    return point
