import numpy as np
import cv2

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
