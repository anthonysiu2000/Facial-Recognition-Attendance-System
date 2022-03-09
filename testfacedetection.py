import datetime
import sqlite3
import pickle
import cv2 as cv
import numpy as np
import face_recognition as fr
import os



#obtains the folder/database with attendance images
current_dir = os.path.dirname(__file__)
path = os.path.join(current_dir, "./lfwtest")

#sets up storage for images and students, respectively
studentNames = []


baseImages = []
basePeople = []
testImages = []
abcd = []

#iterates through the ";fw" folder, appending each file to an array for storage
def loadImages():
    people = os.listdir(path)


    #loops to go through every folder in lfwteset, each folder representing an individual
    for i,person in enumerate(people):
        studentNames.append(person)
        imageSet = os.listdir(f'{path}/{person}')
        if (i% 10 == 0):
            print("loading person #" + str(i))
        #goes through every image of a particular individual, using the first entry as a base image to be compared to
        for j,img in enumerate(imageSet):
            curImg = cv.imread(f'{path}/{person}/{img}')
            curImg = cv.cvtColor(curImg, cv.COLOR_BGR2RGB)
            if (len(fr.face_encodings(curImg)) == 0):
                abcd.append(True)
                break
            encode = fr.face_encodings(curImg)[0]
            if j == 0:
                baseImages.append(encode)
                basePeople.append(person)
            else:
                testImages.append((encode, person))


#load images into arrays
loadImages()


with open(os.path.join(current_dir,'Accuracies.csv'), 'r+') as f:
    for encoding in testImages:
        
        #obtain array of matches
        matches = fr.compare_faces(baseImages, encoding[0])
        faceDis = fr.face_distance(baseImages, encoding[0])

        #obtains the face index with the least face distance(highest accuracy)
        matchIndex = np.argmin(faceDis)

        correct = False
        if matches[matchIndex]:
            if basePeople[matchIndex] == encoding[1]:
                correct = True
                f.writelines(f'{correct},{faceDis[matchIndex]}\n')
            else:
                f.writelines(f'{correct},{faceDis[matchIndex]}\n')
        else:
            f.writelines(f'{correct},{faceDis[matchIndex]}\n')

print("failures: " + str(len(abcd)))




