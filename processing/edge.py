import cv2

def edge(img):

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )

    return cv2.Canny(
        gray,
        100,
        200
    )