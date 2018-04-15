from matplotlib import pyplot
import os
import numpy as np
import re
import cv2
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report


def read_pgm(filename, byteorder='>'):
    """Return image data from a raw PGM file as numpy array.
    Format specification: http://netpbm.sourceforge.net/doc/pgm.html
    """
    with open(filename, 'rb') as f:
        buffer = f.read()
    try:
        header, width, height, maxval = re.search(
            b"(^P5\s(?:\s*#.*[\r\n])*"
            b"(\d+)\s(?:\s*#.*[\r\n])*"
            b"(\d+)\s(?:\s*#.*[\r\n])*"
            b"(\d+)\s(?:\s*#.*[\r\n]\s)*)", buffer).groups()
    except AttributeError:
        raise ValueError("Not a raw PGM file: '%s'" % filename)
    return np.frombuffer(buffer,
                            dtype='u1' if int(
                                maxval) < 256 else byteorder+'u2',
                            count=int(width)*int(height),
                            offset=len(header)
                            ).reshape((int(height), int(width)))


def get_parsed_data(dir="data"):
    faces = []
    labels = []
    for directory, _, files in os.walk(dir, topdown=False):
        file_paths = []
        for name in files:
            file_paths.append(os.path.join(directory, name))
        for file in file_paths:
            label = int(file.split('\\')[1].split('s')[1])
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

if __name__ == "__main__":
    faces, labels = get_parsed_data()
    create_model(faces, labels)
    # face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    # face_recognizer.train(faces, np.array(labels))
    # label_predict = face_recognizer.predict(faces[23])
