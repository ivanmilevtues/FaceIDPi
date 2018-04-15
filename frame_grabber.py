import numpy as np
import cv2
import os


def main_loop():
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5)

        if len(faces) > 0:
            x, y, w, h = faces[0]
            gray = gray[y: y+h, x: x+w]
        else:
            for x, y, w, h in faces:
                # gray = gray[x: x+w, y: y+h]
                cv2.rectangle(gray, (x, y), (x + w, y + h), (255, 0, 0), 2)

        cv2.imshow('Camera1', gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def add_face_to_data():
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5)

        if len(faces) > 0:
            x, y, w, h = faces[0]
            gray = gray[y: y+h, x: x+w]
            save_img(gray)
            break


def save_img(img, dir='data'):
    dir_num = 0
    for directory, _, files in os.walk(dir, topdown=False):
        file_paths = []
        for name in files:
            file_paths.append(os.path.join(directory, name))
        for file in file_paths:
            curr_dir_num = int(file.split('\\')[1].split('s')[1])
            dir_num = curr_dir_num if curr_dir_num > dir_num else dir_num
    
    dir_num += 1
    dir_name = dir + '\\s' + str(dir_num)
    print(dir_name)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    cv2.imwrite(filename=(dir_name + '\\1.pgm'), img=img)

    
if __name__ == '__main__':
    add_face_to_data()
