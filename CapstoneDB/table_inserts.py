import pickle
import sqlite3
import os

# employee db for testing
conn = sqlite3.connect('attendance_tracker.db')

c = conn.cursor()

# parse text file
#obtains the folder/database with attendance images
current_dir = os.path.dirname(__file__)
path = os.path.join(current_dir, "./CapstoneDB")

student_data = open(os.path.join(current_dir, 'students.txt'), 'r')
course_data = open(os.path.join(current_dir, 'courses.txt'), 'r')
lecture_data = open(os.path.join(current_dir, 'lectures.txt'), 'r')
enrollment_data = open(os.path.join(current_dir, 'enrollments.txt'), 'r')


student_list = []
course_list = []
lecture_list = []
enrollment_list = []

# courses
count = 0
for line in course_data.readlines():
    if count == 0:
        count += 1
        continue
    data = line.strip()
    data = data.split()
    # id          name        section
    course_id = data[0]
    course_name = ""
    for i in range(1, len(data) - 1):
        course_name += data[i]
    section = data[len(data) - 1]
    section = int(section)
    # add to list
    course_list.append((course_id, course_name, section))
    count += 1

# insert courses
c.executemany("INSERT INTO Courses values (?, ?, ?)", course_list)

# students
count = 0
for line in student_data.readlines():
    if count == 0:
        count += 1
        continue
    data = line.strip()
    data = data.split()
    # ruid first_name last_name
    ruid = data[0]
    name = data[1] + " " + data[2]
    example_encodings = list(range(0, 128))
    example_encodings[0] = 5.123
    # pickle to serialize so that sqlite3 can accept it
    example_encodings = pickle.dumps(example_encodings)
    student_list.append((ruid, name, example_encodings))
    count += 1

# insert students
c.executemany("INSERT INTO Students values (?, ?, ?)", student_list)


# enrollments
count = 0
for line in enrollment_data.readlines():
    if count == 0:
        count += 1
        continue
    data = line.strip()
    data = data.split()
    # ruid course_id section
    ruid = data[0]
    course_id = data[1]
    section = data[2]
    section = int(section)
    enrollment_list.append((ruid, course_id, section))
    count += 1

# insert enrollments
c.executemany("INSERT INTO Enrollments values (?, ?, ?)", enrollment_list)


# lecture attendance data
count = 0
for line in lecture_data.readlines():
    if count == 0:
        count += 1
        continue
    data = line.strip()
    data = data.split()
    # ruid courseid section date
    ruid = data[0]
    course_id = data[1]
    section = data[2]
    section = int(section)
    day = data[3]
    lecture_list.append((day, ruid, course_id, section))
    count += 1

# insert lecture attendance
c.executemany("INSERT INTO Lectures values (?, ?, ?, ?)", lecture_list)

# commit the transaction
conn.commit()

# close connection
conn.close()