import numpy as np
import cv2
import os
from face_recognition import make_desicion, show_face


def main_loop():
    os.system("python2.7 gpio_controller.py 1")
    model = cv2.face.LBPHFaceRecognizer_create()
    model.read("model.cv2")
    cam_hd = cv2.VideoCapture(0)
    cam_ld = cv2.VideoCapture(1)
    face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
    try:
        while True:
            ret, frame_hd = cam_hd.read()
            ret, frame_ld = cam_ld.read()

            gray_hd = cv2.cvtColor(frame_hd, cv2.COLOR_BGR2GRAY)
            gray_ld = cv2.cvtColor(frame_ld, cv2.COLOR_BGR2GRAY)

            faces_hd = face_cascade.detectMultiScale(
                gray_hd, scaleFactor=1.1, minNeighbors=5)

            faces_ld = face_cascade.detectMultiScale(
                gray_ld, scaleFactor=1.1, minNeighbors=5)
            show_face(gray_hd, gray_ld, faces_hd, faces_ld)
            if len(faces_hd) > 0 or len(faces_ld) > 0:
                make_desicion(gray_hd, faces_hd, gray_ld, faces_ld, model)
    finally:
        os.system("python2.7 gpio_controller.py -1")
        cam_hd.release()
        cam_ld.release()


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
    main_loop()
