import cv2
import time
import pickle
import face_recognition
import numpy as np
from datetime import datetime
from PIL import Image
import os

def mark_attendance(name):
    now = datetime.now()
    date_ = now.strftime('%d-%B-%Y')
    try:
        with open('Attendance.csv', 'r+') as f:
            myDataList = f.readlines()
            nameList = {}
            for line in myDataList:
                entry = line.split(',')
                entry[2] = entry[2].replace("\n", "")
                entry[2] = entry[2].replace(" ", "")
                nameList[entry[0]] = entry[2]

            if (name, date_) not in nameList.items() and name != "Unknown_Face":
                now = datetime.now()
                time = now.strftime('%I:%M:%S:%p')
                date = now.strftime('%d-%B-%Y')
                f.writelines(f'{name}, {time}, {date}\n')
    except:
        with open('Attendance.csv', 'w+') as f:
            myDataList = f.readlines()
            nameList = {}
            for line in myDataList:
                entry = line.split(',')
                entry[2] = entry[2].replace("\n", "")
                entry[2] = entry[2].replace(" ", "")
                nameList[entry[0]] = entry[2]

            if (name, date_) not in nameList.items() and name != "Unknown_Face":
                now = datetime.now()
                time = now.strftime('%I:%M:%S:%p')
                date = now.strftime('%d-%B-%Y')
                f.writelines(f'{name}, {time}, {date}\n')


def main_app(name):
    start_time = time.time()
    with open("./data/encoded/" + name + "_encoded", "rb") as fp:  # Unpickling
        encoded_face_train = pickle.load(fp)
        # take pictures from webcam
    cap = cv2.VideoCapture(0)
    pred = 0
    while True:
        success, img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        faces_in_frame = face_recognition.face_locations(imgS)
        encoded_faces = face_recognition.face_encodings(imgS, faces_in_frame)
        for encode_face, faceloc in zip(encoded_faces, faces_in_frame):
            matches = face_recognition.compare_faces(encoded_face_train, encode_face)
            faceDist = face_recognition.face_distance(encoded_face_train, encode_face)
            matchIndex = np.argmin(faceDist)

            if matches[matchIndex]:
                pred = pred + 1
                mark_attendance(name)

            else:
                pred = pred - 1
                name = "Unknown_Face"
            y1, x2, y2, x1 = faceloc
            # since we scaled down by 4 times
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 5), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

        curr_time = int(time.time())
        time_elapsed = curr_time - int(start_time)
        cv2.imshow('webcam', img)

        if cv2.waitKey(1) & 0xFF == ord('q') or time_elapsed == 20:
            if pred > 0:
                cap.release()
                cv2.destroyAllWindows()
                dim = (124, 124)
                img = cv2.imread(
                    f"C:/Users/viral/PycharmProjects/Face_Recognition/FaceRecognition_GUI_2/data/{name}/0{name}.jpg",
                    cv2.IMREAD_UNCHANGED)
                resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
                cv2.imwrite(f".\\data\\{name}\\valid{name}.jpg", resized)
                Image1 = Image.open(f".\\2.png")

                # make a copy the image so that the
                # original image does not get affected
                Image1copy = Image1.copy()
                Image2 = Image.open(f".\\data\\{name}\\valid{name}.jpg")
                Image2copy = Image2.copy()

                # paste image giving dimensions
                Image1copy.paste(Image2copy, (195, 114))

                # save the image
                Image1copy.save("end.png")
                frame = cv2.imread("end.png", 1)

                cv2.imshow("Result", frame)
                cv2.waitKey(5000)
            else:
                print("Invalid User")
            break

    cap.release()
    cv2.destroyAllWindows()
