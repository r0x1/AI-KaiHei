import cv2

from brawl_stars.object_detection import ObjectDetection

detect1 = ObjectDetection()

img1 = cv2.imread('C:\\workspace\\test_video\\temp_img\\RPReplay_Final1594510234_339.png')  # BGR

list1 = detect1.detect(img1)

print(list1)
