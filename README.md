"# Facial-Recognition-Attendance-System" 


This primary objective of this project was to develop an online application in order to create an automated attendance system for classrooms, businesses, etc.

The tools necessary to build this project were primarily the use of Python and several associated packages. 
This included "sqlite", a package to allows us to create a disk-based database without the need for a server, and allowing for SQL queries.
This also included "face_recognition", the primary source of our facial recognition, which transforms the 2d image of a face into a particular encoding for reducing memory content.



Steps for starting project:

Before each run, ensure that there is no file in the main folder titled attendance_tracker.db, and ensure that the Attendance.csv file is empty, save for the subject title

1. Run schema.py to create the SQLite database. This should create attendance_tracker.db in the main folder.
2. Add images of students/individuals that we wish to perform facial recognition on into the folder labeled baseImages. There should only be one face per image.
3. Run addStudentsEnrollments.py in order to add these images into the database.
4. Run gui.py

Steps for Functionality testing:

1. Click on Students to add students based on id and name.
2. Click on Courses to add new courses, check the attendance for a particular course, or most importantly, start facial tracking for a particular course'
3. When performing the facial recognition, there will be a view of the attendance for the current class. Whenever a face is recognized in the video recording (which should use your builtin webcam), the person who the face belongs to should be recorded in that sideview, including a relavent timestamp
