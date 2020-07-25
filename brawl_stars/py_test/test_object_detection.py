import cv2

from brawl_stars.object_detection import ObjectDetection

detect1 = ObjectDetection()

img1 = cv2.imread('D:\\workspace\\test_video\\temp_img\\1594915755.195893.png')  # BGR

list1 = detect1.detect(img1)

print(list1)
