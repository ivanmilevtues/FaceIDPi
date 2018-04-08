from matplotlib import pyplot
import os
import numpy as np
import re
import cv2


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


if __name__ == "__main__":
    faces, labels = get_parsed_data()
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.train(faces, np.array(labels))
    label_predict = face_recognizer.predict(faces[23])
    print(labels[23], label_predict)
