from tkinter import *
from tkinter import font
import sqlite3
import pickle
from turtle import width



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
        Listbox(self, height = 10, listvariable = self.courseList).grid(columnspan=2, row = 2, rowspan=5, sticky = "we")
        self.refreshCourses()
        
        entry = Entry(self, textvariable = StringVar())
        entry.grid(column = 2, row = 2, padx = 5)

        buttonA = Button(self, text="Add Course")
        buttonA.grid(column = 2, row = 3, padx = 5)
        
        buttonC = Button(self, text="Start Tracking for Current Course")
        buttonC.grid(column = 2, row = 4, padx = 5)

        buttonC = Button(self, text="Check Current Course's Attendance",
                           command=lambda: controller.show_frame("CourseAttendance"))
        buttonC.grid(column = 2, row = 5, padx = 5)

        buttonB = Button(self, text="Back",
                           command=lambda: controller.show_frame("Main"))
        buttonB.grid(column = 2, row = 6, padx = 5)
        
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

class CourseAttendance(Frame):
    
    def __init__(self, whole, controller):
        
        #Frame initialization
        Frame.__init__(self, whole, padx = 10, pady = 10)
        self.controller = controller
        self.columnconfigure(0, weight = 1)
        

        #Widgets
        self.dateList = StringVar()
        Label(self, text="Course Attendance", font=controller.title_font).grid(row = 1, sticky = "we", columnspan=2)
        Listbox(self, height = 10, listvariable = self.dateList).grid(row = 2, rowspan=7, sticky = "we")
        self.refreshDates()
        
        
        Label(self, text="Present Students").grid(column = 1, row = 2, sticky = "we")
        Listbox(self, height = 4).grid(column = 1, row = 3, rowspan=2, sticky = "we")
        Label(self, text="Absent Students").grid(column = 1, row = 5, sticky = "we")
        Listbox(self, height = 4).grid(column = 1, row = 6, rowspan=2, sticky = "we")


        buttonB = Button(self, text="Back",
                           command=lambda: controller.show_frame("Courses"))
        buttonB.grid(column = 2, row = 8, padx = 5)
        
    def refreshDates(self):
        conn = sqlite3.connect('attendance_tracker.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        c.execute("SELECT * FROM Courses")
        courses = []
        for r in c.fetchall():
            courses.append(r["course_id"] + " S" + str(r["section"]) + " "+ r["course_name"])
        conn.commit()
        conn.close()
        self.dateList.set(courses)

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