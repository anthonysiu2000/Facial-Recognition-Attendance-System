import cv2 as cv
import numpy as np
import face_recognition as fr
import os

#obtains the folder/database with attendance images
current_dir = os.path.dirname(__file__)
path = os.path.join(current_dir, "./baseImages")

#sets up storage for images and students, respectively
images = []
studentNames = []

#iterates through the "baseImages" folder, appending each file to an array for storage
def loadImages():
    myList = os.listdir(path)
    for img in myList:
        curImg = cv.imread(f'{path}/{img}')
        images.append(curImg)
        studentNames.append(os.path.splitext(img)[0])

#function to iterate through the image list and get their 128 long encodings
def findEncodings(images):
    encodings = []
    for img in images:
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        encode = fr.face_encodings(img)[0]
        encodings.append(encode)
    return encodings



#primary function calls
loadImages()
encodeList = findEncodings(images)



#start a live video capture
cap = cv.VideoCapture(0)

while True:
    #obtain current frame
    success, img = cap.read()

    #decrease frame size in order to help with computation
    imgS = cv.resize(img, (0,0), None, 0.25, 0.25)
    imgS = cv.cvtColor(imgS, cv.COLOR_BGR2RGB)

    #encodes our video capture, with face locations found to assist with computation
    currFaceFrame = fr.face_locations(imgS)
    currEncodeFrame = fr.face_encodings(imgS, currFaceFrame)

    #Loop for each face found in the frame
    for encodeFace, faceLoc in zip(currEncodeFrame, currFaceFrame):
        #obtains the True/False state and the accuracy/face_distance for each face in the database, returned as a list
        matches = fr.compare_faces(encodeList, encodeFace)
        faceDis = fr.face_distance(encodeList, encodeFace)

        #obtains the face index with the least face distance(highest accuracy)
        #additional idea: if there is no match, we should change the text to say "unknown" or something
        matchIndex = np.argmin(faceDis)
        if matches[matchIndex]:
            name = studentNames[matchIndex].upper()
            y1,x2,y2,x1 = faceLoc
            y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
            cv.rectangle(img, (x1,y1), (x2,y2), (0,255,0), 2)
            cv.rectangle(img, (x1, y2-35), (x2,y2), (0,255,0), cv.FILLED)
            cv.putText(img, name, (x1+6, y2-6), cv.FONT_HERSHEY_COMPLEX, 1, (255,0,255), 2)

    
    cv.imshow('Webcam', img)
    cv.waitKey(1)
    
