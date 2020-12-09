import cv2 as cv  # OpenCV import
import mouse
import time

table = 0
point = []
max_count = 0


# 마우스 이벤트 콜백함수 정의


def mouse_callback(event, y, x, flags, param):
    global max_count
    if mouse.is_pressed("left"):
        point.append([x, y, param[x][y], False])
        print(x, y)
        max_count = max_count + 1
        time.sleep(0.1)


def call_img(img_):
    return img_


def click_img(img_source):
    global max_count
    img = call_img(img_source)
    table = int(input("테이블 수를 입력하세요. : "))
    cv.namedWindow('image')  # 마우스 이벤트 영역 윈도우 생성
    cv.setMouseCallback('image', mouse_callback, param=img)
    while True:
        cv.imshow('image', img)
        if max_count == table:
            max_count = 0
            break
        k = cv.waitKey(1) & 0xFF
    cv.destroyAllWindows()

    image = img.copy()
    for point_ in point:
        cv.circle(image, (point_[1], point_[0]), 2, (0, 255, 255), thickness=-1)
    cv.imshow("image", image)

    return point
