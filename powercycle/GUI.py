import tkinter as tk
from tkinter import *
import os

class GUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack()
        self.geometry("1200x800")
        self.title("Bicycle Application")

        menu = Menu(self)
        self.config(menu=menu)

        # create home menu
        menu.add_cascade(label="Home", command=lambda: self.show("Home"))

        # create file menu
        file_menu = Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.quit)

        self.frames = {}
        for F in (Home, Calibrate, EnterEmail, Form, Run):
            page = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show("Home")

    # define show function
    def show(self, page):
        frame = self.frames[page]
        frame.tkraise()


# create home page
class Home(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        title = tk.Label(self, text="Welcome to Performance Cycling System !", font=("Courier", 32), fg="black",)
        title.grid(row=1, column=1)

        calibrate_button = tk.Button(self, text="Calibrate", height=2, width=10,
                                     bg="deep sky blue", command=lambda: controller.show("Calibrate"))
        calibrate_button.grid(row=5, column=1, padx=2, pady=2)
        run_button = tk.Button(self, text="Run", height=4, width=20,
                               bg="sea green", command=lambda: controller.show("EnterEmail"))
        run_button.grid(row=6, column=1, padx=2, pady=2)

        col_count, row_count = self.grid_size()
        for col in range(col_count):
            self.grid_columnconfigure(col, minsize=10)
        for row in range(row_count):
            self.grid_rowconfigure(row, minsize=10)


# create calibration page
class Calibrate(tk.Frame):
    def __init__(self, parent, controller):
        def run_script():
            os.system('pyton Script.py')
        tk.Frame.__init__(self, parent)
        title = tk.Label(self, text="Calibration", font=("Courier", 44), fg="black")
        title.grid(row=1, column=30)
        calibrate_button = tk.Button(self, text="Run Calibration", height=4, width=24, bg="sea green", command=run_script)
        calibrate_button.grid(row=2, column=30, padx=2, pady=2)

        col_count, row_count = self.grid_size()
        for col in range(col_count):
            self.grid_columnconfigure(col, minsize=10)
        for row in range(row_count):
            self.grid_rowconfigure(row, minsize=10)


# create lookup by email page
class EnterEmail(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        title = tk.Label(self, text="Enter Email:", font=("Courier", 28), fg="black")
        title.grid(row=19, column=40)
        e = Entry(self)
        e.grid(row=20, column=40, sticky="nsew")
        def submit():
            controller.show("Form")
        find_button = tk.Button(self, text="Find", height=2, width=8, bg="deep sky blue", command=submit)
        find_button.grid(row=25, column=40, padx=2, pady=2)
        col_count, row_count = self.grid_size()
        for col in range(col_count):
            self.grid_columnconfigure(col, minsize=10)
        for row in range(row_count):
            self.grid_rowconfigure(row, minsize=10)

class Form(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        s = tk.StringVar()
        Label(self, text="First Name", font=("Courier", 14)).grid(row=140, column = 380)
        Label(self, text="Last Name", font=("Courier", 14)).grid(row=160, column = 380)
        Label(self, text="Age", font=("Courier", 14)).grid(row=180, column = 380)
        Label(self, text="Height", font=("Courier", 14)).grid(row=200, column = 380)
        Label(self, text="Weight", font=("Courier", 14)).grid(row=220, column = 380)
        Label(self, text="Sex", font=("Courier", 14)).grid(row=240, column = 380)
        Label(self, text="Category", font=("Courier", 14)).grid(row=270, column = 380)
        entry1 = Entry(self)
        entry2 = Entry(self)
        entry3 = Entry(self)
        entry4 = Entry(self)
        entry5 = Entry(self)
        entry6 = tk.Radiobutton(self, text="Male", padx=20, variable=s, value="Male")
        entry7 = tk.Radiobutton(self, text="Female", padx=20, variable=s, value="Female")
        entry8 = Entry(self)
        entry1.grid(row=140, column=381)
        entry2.grid(row=160, column=381)
        entry3.grid(row=180, column=381)
        entry4.grid(row=200, column=381)
        entry5.grid(row=220, column=381)
        entry6.grid(row=240, column=381)
        entry7.grid(row=250, column=381)
        entry8.grid(row=270, column=381)

        def submit(email, fname, lname, age, height, weight, gender, category):
            print(email + " " + fname + " " + lname + " " + age + " " + height + " " + weight + " " + gender + " " + category)
            controller.show("Run")

        submit_button = tk.Button(self, text="Submit", height=2, width=12, command=lambda: submit("Email", entry1.get(), entry2.get(), entry3.get(), entry4.get(), entry5.get(), s.get(), entry8.get()))
        submit_button.grid(row=290, column=381)

        col_count, row_count = self.grid_size()
        for col in range(col_count):
            self.grid_columnconfigure(col, minsize=1)
        for row in range(row_count):
            self.grid_rowconfigure(row, minsize=1)

class Run(tk.Frame):
    def __init__(self, parent, controller):
        def run_script():
            os.system('python Script.py')
        tk.Frame.__init__(self, parent)
        title = tk.Label(self, text="Run Bicycle", font=("Courier", 44), fg="black")
        title.grid(row=1, column=30)
        run_button = tk.Button(self, text="Run", height=4, width=24, bg="sea green", command=run_script)
        run_button.grid(row=2, column=30, padx=2, pady=2)

        col_count, row_count = self.grid_size()
        for col in range(col_count):
            self.grid_columnconfigure(col, minsize=10)
        for row in range(row_count):
            self.grid_rowconfigure(row, minsize=10)

if __name__ == "__main__":
    gui = GUI()
    gui.mainloop()