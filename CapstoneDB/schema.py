import sqlite3

# employee db for testing
conn = sqlite3.connect('attendance_tracker.db')

c = conn.cursor()

# must create in order - courses, students, enrollment, lectures

# courses
#'''
c.execute("""
    CREATE TABLE Courses(
        course_id text,
        course_name text,
        section integer,
        primary key(course_id, section)
    )
""")
#'''

# students
c.execute("""
    CREATE TABLE Students(
        ruid text primary key,
        student_name text,
        encodings blob
    )
""")

# enrollments
c.execute("""
    CREATE TABLE Enrollments(
        ruid text,
        course_id text,
        section integer,
        primary key(ruid, course_id, section),
        foreign key(ruid) references Students,
        foreign key(course_id, section) references Courses
    )
""")


# lectures (only exists when a student has attended a particular lecture)
c.execute("""
    CREATE TABLE Lectures(
        day text,
        ruid text,
        course_id text,
        section integer,
        primary key(day, ruid, course_id, section),
        foreign key(ruid) references Students,
        foreign key(course_id, section) references Courses
    )
""")

# commit the transaction
conn.commit()

# close connection
conn.close()

print("finished schema")