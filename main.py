import datetime
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

def markAttendance(name):
    with open(os.path.join(current_dir,'Attendance.csv'), 'r+') as f:
        myDataList = f.readlines()
        #creates a list of names from the file, to be used to compare against new names
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        #makes sure name is not already in the attendance document, and writes to the file
        if name not in nameList:
            now = datetime.datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')
            



#primary function calls
loadImages()
encodeList = findEncodings(images)

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
        matches = fr.compare_faces(encodeList, encodeFace)
        faceDis = fr.face_distance(encodeList, encodeFace)

        #obtains the face index with the least face distance(highest accuracy)
        #additional idea: if there is no match, we should change the text to say "unknown" or something
        matchIndex = np.argmin(faceDis)
        if matches[matchIndex]:
            name = studentNames[matchIndex].upper()
            name = name + " " + "{:.5f}".format(faceDis[matchIndex])
            markAttendance(name)
            y1,x2,y2,x1 = faceLoc
            y1,x2,y2,x1 = y1*8,x2*8,y2*8,x1*8

            #Draws facial rectangle
            cv.rectangle(imgL, (x1,y1), (x2,y2), (0,255,0), 2)
            #Draws filled in rectangle at bottom of rectangle for text
            cv.rectangle(imgL, (x1, y2-35), (x2,y2), (0,255,0), cv.FILLED)
            #Draws text
            cv.putText(imgL, name, (x1+6, y2-6), cv.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2)
        else:
            name = "UNKNOWN"
            y1,x2,y2,x1 = faceLoc
            y1,x2,y2,x1 = y1*8,x2*8,y2*8,x1*8

            #Draws facial rectangle
            cv.rectangle(imgL, (x1,y1), (x2,y2), (0,255,0), 2)
            #Draws filled in rectangle at bottom of rectangle for text
            cv.rectangle(imgL, (x1, y2-35), (x2,y2), (0,255,0), cv.FILLED)
            #Draws text
            cv.putText(imgL, name, (x1+6, y2-6), cv.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2)

    
    cv.imshow('Webcam', imgL)
    cv.waitKey(1)
    
