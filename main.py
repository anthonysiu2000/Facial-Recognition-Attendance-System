import cv2 as cv
import numpy as np
import face_recognition as fr
import os

#obtains the folder/database with attendance images
current_dir = os.path.dirname(__file__)
path = os.path.join(current_dir, "./testImages/obama.jpg")

#load image
img = cv.imread(path)
studentName = "Obama"

#get the 128 long encodings
img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
encode = fr.face_encodings(img)[0]
encodings = []
encodings.append(encode)

#start a live video capture
cap = cv.VideoCapture(0)

while True:
    #obtain current frame
    success, imgL = cap.read()

    #larger resolution for screen
    imgL = cv.resize(imgL, (0,0), None, 2, 2)

    #decrease frame size in order to help with computation
    imgS = cv.resize(imgL, (0,0), None, 0.125, 0.125)
    imgS = cv.cvtColor(imgS, cv.COLOR_BGR2RGB)

    #encodes our video capture, with face locations found to assist with computation
    frameLocation = fr.face_locations(imgS)
    frameEncoding = fr.face_encodings(imgS, frameLocation)

    #Loop for each face found in the frame
    for encodeFace, faceLoc in zip(frameEncoding, frameLocation):
        #obtains the True/False state and the accuracy/face_distance for the current face, returned as a list
        matches = fr.compare_faces(encodings, encodeFace)
        faceDis = fr.face_distance(encodings, encodeFace)

        if matches[0]:
            y1,x2,y2,x1 = faceLoc
            y1,x2,y2,x1 = y1*8,x2*8,y2*8,x1*8

            #Draws facial rectangle
            cv.rectangle(imgL, (x1,y1), (x2,y2), (0,255,0), 2)
            #Draws text
            cv.putText(imgL, studentName, (x1+6, y2-6), cv.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)

    
    cv.imshow('Webcam', imgL)
    cv.waitKey(1)
    
