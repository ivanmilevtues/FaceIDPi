#from matplotlib import pyplot
import sys
import os
import numpy as np
import re
import cv2
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from PIL import Image

slash = '\\'
if sys.platform == 'linux':
    slash = '/'

FACE_CASCADE = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')


def read_pgm(filename):
    """
    Uncomment lines 16, 17 to convert jpgs to pgm
    NOTE: When runned with the classifiers will be taken twice
    1st: picture.jpg -> converted to pgm and taken
    2nd: picture.pgm -> opened and taken
    """
    # if '.jpg' in filename:
    #     filename = convert_jpg_pgm(filename)
    img = cv2.imread(filename)
    img = cv2.resize(img, dsize=(92, 112), interpolation=cv2.INTER_CUBIC)
    return  cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def get_parsed_data(dir="data"):
    faces = []
    labels = []
    for directory, _, files in os.walk(dir, topdown=False):
        file_paths = []
        for name in files:
            file_paths.append(os.path.join(directory, name))
        for file in file_paths:
            if 'JPGS' in file:
                continue
            label = int(file.split(slash)[1].split('s')[1])
            faces.append(read_pgm(file))
            labels.append(label)
    return faces, labels


def create_model(X, y):
    # X_train, X_test, y_train, y_test = X, X, y, y
    y = np.array(y)
    # X = np.array(X)
    X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                        shuffle=True,
                                                        test_size=0.3,
                                                        stratify=y,
                                                        random_state=42)
    y_test_pred = []
    y_train_pred = []
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.train(X_train, y_train)
    for image in X_test:
        y_test_pred.append(face_recognizer.predict(image))
    
    for image in X_train:
        y_train_pred.append(face_recognizer.predict(image))

    y_test_pred = np.array([c for c, _ in y_test_pred])
    y_train_pred = np.array([c for c, _ in y_train_pred])
    
    print(accuracy_score(y_test, y_test_pred),
          classification_report(y_test, y_test_pred))
        #   precision_score(y_test, y_test_pred),
        #   recall_score(y_test, y_test_pred))

    print(accuracy_score(y_train, y_train_pred),
          classification_report(y_train, y_train_pred))
        #   precision_score(y_train, y_train_pred),
        #   recall_score(y_train, y_train_pred))
    return face_recognizer


def convert_jpg_pgm(filename):
    img = Image.open(filename)
    filename = filename.split('.')[0] + '.pgm'
    print(filename)
    try:
        img = img.save(filename)
    except IOError:
        print("Convertion error")
    return filename


def main():
    faces, labels = get_parsed_data()
    model = create_model(faces, labels)
    del faces
    del labels
    model.write("model.cv2")

if __name__ == "__main__":
    main()
    # face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    # face_recognizer.train(faces, np.array(labels))
    # label_predict = face_recognizer.predict(faces[23])
