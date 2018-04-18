from ALLOWED_USERS import ALLOWED_USERS
import os
import sys
import cv2
import numpy as np


def show_face(gray_hd, gray_ld):
    if sys.platform == "linux":
        return
    horizontal_stack = np.hstack((gray_hd, gray_ld))
    cv2.imshow('HD', horizontal_stack)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        pass


def predict_person(gray_hd, faces_hd, gray_ld, faces_ld, model):
    x, y, w, h, x_ld, y_ld, w_ld, h_ld = [None for _ in range(8)]
    if len(faces_hd) > 0:
        x, y, w, h = faces_hd[0]
    if len(faces_ld) > 0:
        x_ld, y_ld, w_ld, h_ld = faces_ld[0]
    
    if x is None:
        x, y, w, h = x_ld, y_ld, w_ld, h_ld
    elif x_ld is None:
        x_ld, y_ld, w_ld, h_ld = x, y, w, h
     
    gray_hd = gray_hd[y: y+h, x: x+w]
    gray_ld = gray_ld[y_ld: y_ld+h_ld, x_ld: x_ld+w_ld]

    # Scale
    gray_hd = cv2.resize(gray_hd, dsize=(92, 112), interpolation=cv2.INTER_CUBIC)
    gray_ld = cv2.resize(gray_ld, dsize=(92, 112), interpolation=cv2.INTER_CUBIC)

    show_face(gray_hd, gray_ld)

    hd_pred_y, conf_hd = model.predict(gray_hd)
    ld_pred_y, conf_ld = model.predict(gray_ld)

    if hd_pred_y != ld_pred_y:
        raise FacePredictException("Predictions are not compatible")
    
    return (hd_pred_y, ((conf_hd * 1.2) + (conf_ld * 0.8)) / 2)


def make_desicion(gray_hd, faces_hd, gray_ld, faces_ld, model):
    try:
       lbl,  confidence = predict_person(gray_hd, faces_hd, gray_ld, faces_ld, model)
       print(lbl, confidence)
       if confidence >= 100 and lbl in ALLOWED_USERS:
           os.system("python2.7 gpio_controller.py 0")
    except FacePredictException:
        pass


class FacePredictException(Exception):
    pass