import cv2
import os
from subprocess import Popen
import sys

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
video_capture = cv2.VideoCapture(0)
video_capture.read()
face_count = 0
playing = False
eye_count = 0
face_no_count = 0
eye_no_count = 0
while True:
    face_there = False
    eye_there = False
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    img2 = frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )
    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        img = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        face_there = True
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img2[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(255,0,0),2)
            eye_there= True
    if(face_there):
        face_count = face_count + 1
        if(face_count>10):
            if playing == False :
             pid = Popen(["rhythmbox","comingback.mp3"]).pid
             playing = True
            print("I see you!")
            face_count = 0
    else:
        face_no_count = face_no_count + 1
        if(face_no_count>10):
            print("Where did you go?")
            os.system("kill "+str(pid))
            playing = False
            face_no_count = 0
    if(eye_there):
        eye_count = eye_count + 1
        if(eye_count>10):
            print("Your eyes too!")
            eye_count = 0
    else:
        eye_no_count = eye_no_count + 1
        if(eye_no_count>10):
            print("Open your eyes!")
            eye_no_count = 0
    # Display the resulting frame
    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
