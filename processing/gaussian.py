import cv2

def gaussian(img):

    return cv2.GaussianBlur(
        img,
        (15, 15),
        0
    )