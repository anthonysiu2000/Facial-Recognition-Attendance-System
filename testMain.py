import cv2 as cv
import numpy as np
import face_recognition as fr
from os.path import dirname, join

#pip install cmake
#pip install dlib
#pip install face_recognition

current_dir = dirname(__file__)
file_path = join(current_dir, "./images/obama.jpg")
file_path2 = join(current_dir, "./images/obama2.jpg")

picObama = fr.load_image_file(file_path)
picObama = cv.cvtColor(picObama, cv.COLOR_BGR2RGB)
picObama2 = fr.load_image_file(file_path2)
picObama2 = cv.cvtColor(picObama2, cv.COLOR_BGR2RGB)

#face Loc is the first instance of a face, returning an array of 4 numbers corresponding to the four pixel corners of detected faces
faceLoc = fr.face_locations(picObama)[0]
# A 128 array of floats describing the HOG encoding of the face
encodeObama = fr.face_encodings(picObama)[0]
cv.rectangle(picObama, (faceLoc[3], faceLoc[0]), (faceLoc[1],faceLoc[2]), (255,0,0), 2)

faceLoc2 = fr.face_locations(picObama2)[0]
encodeObama2 = fr.face_encodings(picObama2)[0]
cv.rectangle(picObama2, (faceLoc2[3], faceLoc2[0]), (faceLoc2[1],faceLoc2[2]), (255,0,0), 2)

print(encodeObama)

cv.imshow('Obama', picObama)
cv.imshow('Obama test', picObama2)
cv.waitKey(0)
