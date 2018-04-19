import numpy as np
import cv2
import os
from face_recognition import make_desicion, show_face
from time import time, sleep
from process_data import main


def main_loop():
    os.system("python2.7 gpio_controller.py 1")
    model = cv2.face.LBPHFaceRecognizer_create()
    model.read("model.cv2")
    cam_hd = cv2.VideoCapture(0)
    cam_ld = cv2.VideoCapture(1)
    face_cascade = cv2.CascadeClassifier(
        './haarcascade_frontalface_default.xml')
    try:
        while True:
            gray_hd, gray_ld, faces_hd, faces_ld = cap_get_faces(cam_hd, cam_ld,
                                                                 face_cascade)

            show_face(gray_hd, gray_ld, faces_hd, faces_ld)
            if len(faces_hd) > 0 or len(faces_ld) > 0:
                make_desicion(gray_hd, faces_hd, gray_ld, faces_ld, model)
            result_stat = int(os.system('python2.7 gpio_controller.py 1'))
            print("Result status", result_stat)
            if result_stat == 1:
                cam_hd.release()
                cam_ld.release()
                add_face_to_data()
    finally:
        os.system("python2.7 gpio_controller.py -1")
        cam_hd.release()
        cam_ld.release()


def add_face_to_data():
    cam_hd = cv2.VideoCapture(0)
    cam_ld = cv2.VideoCapture(1)
    face_cascade = cv2.CascadeClassifier(
        './haarcascade_frontalface_default.xml')
    
    dir_name = get_dir()
    i, k = 0, 0
    while True:
        gray_hd, gray_ld, faces_hd, faces_ld = cap_get_faces(cam_hd, cam_ld,
                                                             face_cascade)
        show_face(gray_hd, gray_ld, faces_hd, faces_ld)
        if len(faces_hd) > 0:
            x, y, w, h = faces_hd[0]
            save_img(gray_hd[y: y+h, x: x+w], dir_name)
            i += 1
        if len(faces_ld) > 0:
            x, y, w, h = faces_ld[0]
            save_img(gray_ld[y: y+h, x: x+w], dir_name, cam='ld')
            k += 1

        if i >= 9 and k >= 9:
            break
        sleep(1)

    cam_hd.release()
    cam_ld.release()

    main()
    main_loop()


def get_dir(dir='data'):
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
    return dir_name


def save_img(img, dir_name, cam='hd'):
    print(dir_name)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    cv2.imwrite(filename=(dir_name + '\\' + str(int(time())) + cam + '.pgm'),
                img=img)


def cap_get_faces(cam_hd, cam_ld, face_cascade):
    ret, frame_hd = cam_hd.read()
    ret, frame_ld = cam_ld.read()

    gray_hd = cv2.cvtColor(frame_hd, cv2.COLOR_BGR2GRAY)
    gray_ld = cv2.cvtColor(frame_ld, cv2.COLOR_BGR2GRAY)

    faces_hd = face_cascade.detectMultiScale(
        gray_hd, scaleFactor=1.1, minNeighbors=5)

    faces_ld = face_cascade.detectMultiScale(
        gray_ld, scaleFactor=1.1, minNeighbors=5)
    return (gray_hd, gray_ld, faces_hd, faces_ld)
    

if __name__ == '__main__':
    main_loop()