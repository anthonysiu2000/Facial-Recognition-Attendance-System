from tkinter import *
from tkinter import font
import sqlite3

from numpy import empty
from main import main



#tkinter._test()

#This class will be created to initialize the GUI and the whole Frame.
#Additional frames for each page will also be created, and will be manuevered around as according to this class
class GUI(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.title_font = font.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        #We will store multiple frames, the one on top of which will be presented.
        #If we wish for a frame of the gui to be visible, we bring it to the top

        #Main Frame that will hold all other frames, overlapping each other
        whole = Frame(self)
        whole.pack(side="top", fill="both", expand=True)
        whole.grid_rowconfigure(0, weight=1)
        whole.grid_columnconfigure(0, weight=1)

        #initializes each subframe into a dictionary, and places them into the main gui
        self.frames = {}
        for F in (Main, Students, Courses, CourseAttendance):
            page_name = F.__name__
            frame = F(whole=whole, controller=self)
            self.frames[page_name] = frame

            # put all of the frames in the same location
            frame.grid(row=0, column=0, sticky="nsew")

        #brings the starting frame to the top
        self.show_frame("Main")

    #function used by frame classes to bring up their frame to the top
    #by extracting the page name from the dictionary
    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        if page_name == "Courses":
            self.frames["CourseAttendance"].delLists()
        frame = self.frames[page_name]
        frame.tkraise()




#This is the main menu frame, containing functions to search the database by course or by student
class Main(Frame):
    
    def __init__(self, whole, controller):
        #Frame initialization
        Frame.__init__(self, whole, padx = 10, pady = 10)
        self.controller = controller
        self.columnconfigure(0, weight = 1)

        #Widgets
        Label(self, text="Main Page", font=controller.title_font).grid(row = 1, sticky = "we")
        buttonS = Button(self, text="Students", command=lambda: controller.show_frame("Students"))
        buttonS.grid(row = 2,sticky = (W,E))
        buttonC = Button(self, text="Courses", command=lambda: controller.show_frame("Courses"))
        buttonC.grid(row = 3,sticky = (W,E))

class Students(Frame):
    
    def __init__(self, whole, controller):
        #Frame initialization
        Frame.__init__(self, whole, padx = 10, pady = 10)
        self.controller = controller
        self.columnconfigure(0, weight = 1)
        

        #Widgets
        self.studentList = StringVar()
        Label(self, text="Students", font=controller.title_font).grid(row = 1, sticky = "we", columnspan=3)
        Listbox(self, height = 10, listvariable = self.studentList).grid(columnspan=2, row = 2, rowspan=5, sticky = "we")
        self.refreshStudents()
        
        entry = Entry(self, textvariable = StringVar())
        entry.grid(column = 2, row = 3, padx = 5)

        buttonA = Button(self, text="Add Student")
        buttonA.grid(column = 2, row = 4, padx = 5)
        
        buttonC = Button(self, text="Check Current Student's Enrollments")
        buttonC.grid(column = 2, row = 5, padx = 5)

        buttonB = Button(self, text="Back",
                           command=lambda: controller.show_frame("Main"))
        buttonB.grid(column = 2, row = 6, padx = 5)

    def refreshStudents(self):
        conn = sqlite3.connect('attendance_tracker.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        c.execute("SELECT * FROM Students")
        students = []
        for r in c.fetchall():
            students.append(r["ruid"] + " " + r["student_name"])
        conn.commit()
        conn.close()
        self.studentList.set(students)

class Courses(Frame):
    
    def __init__(self, whole, controller):
        
        #Frame initialization
        Frame.__init__(self, whole, padx = 10, pady = 10)
        self.controller = controller
        self.columnconfigure(0, weight = 1)
        

        #Widgets
        self.courseList = StringVar()
        Label(self, text="Courses", font=controller.title_font).grid(row = 1, sticky = "we", columnspan=3)
        coursebox = Listbox(self, height = 10, listvariable = self.courseList)
        coursebox.grid(columnspan=2, row = 2, rowspan=5, sticky = "we")

        self.refreshCourses()
        
        entry = Entry(self, textvariable = StringVar())
        entry.grid(column = 2, row = 2, padx = 5)

        buttonA = Button(self, text="Add Course")
        buttonA.grid(column = 2, row = 3, padx = 5)
        
        buttonC = Button(self, text="Start Tracking for Current Course",
                           command=lambda: self.stream(coursebox.curselection()[0]))
        buttonC.grid(column = 2, row = 4, padx = 5)

        buttonC = Button(self, text="Check Current Course's Attendance",
                           command=lambda: self.goToCourseAttendance(coursebox.curselection()[0]))
        buttonC.grid(column = 2, row = 5, padx = 5)

        buttonB = Button(self, text="Back",
                           command=lambda: controller.show_frame("Main"))
        buttonB.grid(column = 2, row = 6, padx = 5)
    

    def stream(self, index):
        conn = sqlite3.connect('attendance_tracker.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        c.execute("SELECT * FROM Courses")
        courses = []
        for r in c.fetchall():
            courses.append((r["course_id"],r["section"]))

        self.controller.frames["CourseAttendance"].refreshDates(courses[index][0], courses[index][1])
        
        main(courses[index][0], courses[index][1])

        conn.commit()
        conn.close()



    def refreshCourses(self):
        conn = sqlite3.connect('attendance_tracker.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        c.execute("SELECT * FROM Courses")
        courses = []
        for r in c.fetchall():
            courses.append(r["course_id"] + " S" + str(r["section"]) + " "+ r["course_name"])
        conn.commit()
        conn.close()
        self.courseList.set(courses)
    
    def goToCourseAttendance(self, index):
        conn = sqlite3.connect('attendance_tracker.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        c.execute("SELECT * FROM Courses")
        courses = []
        for r in c.fetchall():
            courses.append((r["course_id"],r["section"]))
        self.controller.frames["CourseAttendance"].refreshDates(courses[index][0], courses[index][1])
        self.controller.show_frame("CourseAttendance")
        conn.commit()
        conn.close()


class CourseAttendance(Frame):
    
    def __init__(self, whole, controller):
        
        #Frame initialization
        Frame.__init__(self, whole, padx = 10, pady = 10)
        self.controller = controller
        self.columnconfigure(0, weight = 1)
        

        #Widgets
        self.dateList = StringVar()
        self.presentList = StringVar()
        self.absentList = StringVar()
        Label(self, text="Course Attendance", font=controller.title_font).grid(row = 1, sticky = "we", columnspan=2)
        datebox = Listbox(self, height = 10, listvariable = self.dateList)
        datebox.grid(row = 2, rowspan=7, sticky = "wse")
        datebox.bind("<<ListboxSelect>>", lambda e: self.getAttendances(datebox.curselection()))

        Label(self, text="Present Students").grid(column = 1, row = 2, sticky = "we")
        Listbox(self, height = 4, listvariable = self.presentList).grid(column = 1, row = 3, rowspan=2, sticky = "wse")
        Label(self, text="Absent Students").grid(column = 1, row = 5, sticky = "we")
        Listbox(self, height = 4, listvariable = self.absentList).grid(column = 1, row = 6, rowspan=2, sticky = "wse")


        buttonB = Button(self, text="Back",
                           command=lambda: controller.show_frame("Courses"))
        buttonB.grid(column = 2, row = 8, padx = 5)
        
    def refreshDates(self, courseID, courseSection):
        conn = sqlite3.connect('attendance_tracker.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        c.execute("SELECT DISTINCT day FROM Lectures WHERE course_id=\"" + courseID + "\" AND section=" + str(courseSection))
        self.dates = []
        for r in c.fetchall():
            self.dates.append(r["day"])
        conn.commit()
        conn.close()
        self.courseID = courseID
        self.courseSection = courseSection
        self.dateList.set(self.dates)

    def getAttendances(self, currentS):
        if not currentS:
            return

        conn = sqlite3.connect('attendance_tracker.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        c.execute("SELECT * FROM Lectures WHERE course_id=\"" + self.courseID + "\" AND section=" + str(self.courseSection) + " AND day=\"" + str(self.dates[currentS[0]]) + "\"")
        ids = []
        for r in c.fetchall():
            ids.append(r["ruid"])
        self.presentList.set(ids)
        c.execute("SELECT ruid FROM Enrollments WHERE course_id=\"" + self.courseID + "\" AND section=" + str(self.courseSection) + " AND ruid NOT IN ("
            "SELECT ruid FROM Lectures WHERE course_id=\"" + self.courseID + "\" AND section=" + str(self.courseSection) + " AND day=\"" + str(self.dates[currentS[0]]) + "\")")
        absentids = []
        for r in c.fetchall():
            absentids.append(r["ruid"])
        self.absentList.set(absentids)
        
        conn.commit()
        conn.close()
    
    def delLists(self):
        self.presentList.set([])
        self.absentList.set([])

#starts up the gui by initializing the top level class
if __name__ == "__main__":
    app = GUI()
    app.mainloop()
"""

# employee db for testing
conn = sqlite3.connect('attendance_tracker.db')
# set up row object for column name access
conn.row_factory = sqlite3.Row
c = conn.cursor()
# commit the transaction
conn.commit()
# close connection
conn.close()
"""