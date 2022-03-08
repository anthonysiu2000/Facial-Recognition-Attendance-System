import sqlite3
import pickle

# employee db for testing
conn = sqlite3.connect('attendance_tracker.db')
# set up row object for column name access
conn.row_factory = sqlite3.Row

c = conn.cursor()


# check tables by doing selects
print("---------------------------STUDENTS------------------------------")
c.execute("SELECT * FROM Students")
for r in c.fetchall():
    print(r["ruid"])
    print(r["student_name"])
    # deserialize the 128 float array of encodings
    encodings = pickle.loads(r["encodings"])
    print(encodings[1:10])

print("---------------------------COURSES------------------------------")
c.execute("SELECT * FROM Courses")
for r in c.fetchall():
    for e in r:
        print(e)


print("---------------------------ENROLLMENTS------------------------------")
c.execute("SELECT * FROM Enrollments")
for r in c.fetchall():
    for e in r:
        print(e)

print("---------------------------ATTENDANCES------------------------------")
c.execute("SELECT * FROM Lectures")
for r in c.fetchall():
    for e in r:
        print(e)

# commit the transaction
conn.commit()

# close connection
conn.close()