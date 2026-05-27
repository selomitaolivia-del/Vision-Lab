import cv2

def histogram(img):

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )

    return cv2.calcHist(
        [gray],
        [0],
        None,
        [256],
        [0, 256]
    )