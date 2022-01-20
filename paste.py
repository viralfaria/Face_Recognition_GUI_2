from PIL import Image, ImageDraw, ImageFilter
import cv2
import os

path = "C:/Users/viral/PycharmProjects/Face_Recognition/Images"
cam = cv2.VideoCapture(0)
img_counter = 0
cv2.namedWindow("unknown_face")
while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("unknown_face", frame)

    key = cv2.waitKey(1)
    try:
        img_name = "{}.jpg".format("unknown_image")
        cv2.imwrite(os.path.join(path, img_name), frame)
        print("{} written!".format(img_name))
        img_counter = img_counter + 1
    except:
        pass

    if key == ord("q") or key == 27 or img_counter == 1:
        break
cam.release()

cv2.destroyAllWindows()
