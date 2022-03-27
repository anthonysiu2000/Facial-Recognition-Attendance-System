import datetime
import sqlite3
import pickle
import cv2 as cv
import numpy as np
import face_recognition as fr
import os



#obtains the folder/database with attendance images
current_dir = os.path.dirname(__file__)
path = os.path.join(current_dir, "./baseImages")

conn = sqlite3.connect('attendance_tracker.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

images = []
studentNames = []
ruIDs = []

#iterates through the "baseImages" folder, appending each file to an array for storage
def loadImages():
    myList = os.listdir(path)
    for img in myList:
        curImg = cv.imread(f'{path}/{img}')
        images.append(curImg)
        studentNames.append(os.path.splitext(img)[0].lower())

#function to iterate through the image list and get their 128 long encodings
def findEncodings(images):
    encodings = []
    for img in images:
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        encode = fr.face_encodings(img)[0]
        encodings.append(encode)
    return encodings

loadImages()
encodeList = findEncodings(images)
for i in range(len(encodeList)):
    ruIDs.append(str(170000000+i))

names = studentNames
studentList = []
for i in range(len(names)):
    studentList.append((ruIDs[i], names[i], pickle.dumps(encodeList[i])))

# insert students
c.executemany("INSERT INTO Students values (?, ?, ?)", studentList)

# for now, every student will be part of the same class section
# enrollments
enrollmentList = []
for i in range(len(names)):
    enrollmentList.append((ruIDs[i], "14:332:448", 3))

# insert enrollments
c.executemany("INSERT INTO Enrollments values (?, ?, ?)", enrollmentList)

# commit the transaction
conn.commit()

# close connection
conn.close()