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

#sets up storage for images and students, respectively
images = []
studentNames = []
ruIDs = []

#Access the database
conn = sqlite3.connect('attendance_tracker.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()


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

#-----------------------------------------------------------------------------------------------------------------------------------------
#Change this function later on so Attendance.csv is reset every time we select a different lecture, or move away from attendance.csv entirely and 
#use sql instructions that avoid duplicate entries
#Also when adding an attendance, we should find a way to select the course id and string .
#-----------------------------------------------------------------------------------------------------------------------------------------
def markAttendance(name):
    with open(os.path.join(current_dir,'Attendance.csv'), 'r+') as f:
        myDataList = f.readlines()
        #creates a list of names from the file, to be used to compare against new names
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        #makes sure name is not already in the attendance document, and writes to the file
        now = datetime.datetime.now()
        dtString = now.strftime('%m/%d')
        if name not in nameList:
            f.writelines(f'\n{name},{dtString}')

            #marks presence in database
                    
            #Find a way to find the the student with an encoding matching our live face's encoding via sql select
            #Find the student's ruid, which we will append to lecture list
            ruid = ""            
            c.execute("SELECT * FROM Students WHERE student_name = (?)", (name.lower(),))
            for r in c.fetchall():
                ruid = r["ruid"]
            
            

            # lecture attendance data
            temp = (dtString, ruid, "14:332:448", 3)
            print(temp)
            # insert lecture attendance
            c.execute("INSERT INTO Lectures values (?, ?, ?, ?)", temp)
        
        
        



            
def addStudents(names, encodings, ruIDs, cursor):# students
    studentList = []
    for i in range(len(names)):
        studentList.append((ruIDs[i], names[i], pickle.dumps(encodings[i])))

    # insert students
    cursor.executemany("INSERT INTO Students values (?, ?, ?)", studentList)

    # for now, every student will be part of the same class section
    # enrollments
    enrollmentList = []
    for i in range(len(names)):
        enrollmentList.append((ruIDs[i], "14:332:448", 3))

    # insert enrollments
    c.executemany("INSERT INTO Enrollments values (?, ?, ?)", enrollmentList)

#primary function calls
loadImages()
encodeList = findEncodings(images)
for i in range(len(encodeList)):
    ruIDs.append(str(180000000+i))


#start a live video capture
cap = cv.VideoCapture(0)




#Hard-coded course ID for now. Change later to allow choice of course with GUI
courseID = "14:332:448"
section = 3
course_name = "Capstone"
temp = (courseID, course_name, section)
# insert courses
c.execute("INSERT INTO Courses values (?, ?, ?)", temp)

#Adding students and enrollment connections 
addStudents(studentNames, encodeList, ruIDs, c)



#Students should be added to the database outside of this script in students.txt
#They should not be added while attendance system is active


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
        matchIndex = np.argmin(faceDis)
        if matches[matchIndex]:
            name = studentNames[matchIndex].upper()
            markAttendance(name)
            name = name + " " + "{:.5f}".format(faceDis[matchIndex])
            y1,x2,y2,x1 = faceLoc
            y1,x2,y2,x1 = y1*8,x2*8,y2*8,x1*8

            #Draws facial rectangle
            cv.rectangle(imgL, (x1,y1), (x2,y2), (0,255,0), 2)
            #Draws filled in rectangle at bottom of rectangle for text
            cv.rectangle(imgL, (x1, y2-35), (x2,y2), (0,255,0), cv.FILLED)
            #Draws text
            cv.putText(imgL, name, (x1+6, y2-6), cv.FONT_HERSHEY_COMPLEX, 1, (0,0,0), 2)
        else:
            name = "UNKNOWN"
            y1,x2,y2,x1 = faceLoc
            y1,x2,y2,x1 = y1*8,x2*8,y2*8,x1*8

            #Draws facial rectangle
            cv.rectangle(imgL, (x1,y1), (x2,y2), (0,255,0), 2)
            #Draws filled in rectangle at bottom of rectangle for text
            cv.rectangle(imgL, (x1, y2-35), (x2,y2), (0,255,0), cv.FILLED)
            #Draws text
            cv.putText(imgL, name, (x1+6, y2-6), cv.FONT_HERSHEY_COMPLEX, 1, (0,0,0), 2)
    
    #attendance image
    attImg = np.zeros((800,800,3), np.uint8)
    with open(os.path.join(current_dir,'Attendance.csv'), 'r+') as f:
        myDataList = f.readlines()
        #creates a list of names from the file, to be used to compare against new names
        for i, line in enumerate(myDataList):
            entry = line.split(',')
            entryLine = entry[0] + " " + entry[1]
            cv.putText(attImg, entryLine, (10, 30 + 30 * i), cv.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2)

    #Upload an new entry into the database
    #When making a GUI, make sure to add an option to add a new course, with a sql command making it if the class is new
    #adding students via gui is unnecessary, but accessing might be good
    #Connecting students to enrollments should definetly be an option



    # commit the transaction
    conn.commit()


    
    cv.imshow('Webcam', imgL)
    cv.imshow('Attendance', attImg)
    if cv.waitKey(1) == ord('q'):
        break
    
# close connection
conn.close()
print("connection closed")

