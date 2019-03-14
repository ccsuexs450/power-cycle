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
        for F in (Home, Calibrate, EnterEmail):
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
            os.system('Script.py')
        tk.Frame.__init__(self, parent)
        title = tk.Label(self, text="Calibration", font=("Courier", 44), fg="black")
        title.grid(row=1, column=30)
        calibrate_button = tk.Button(self, text="Run Calibration", height=4, width=24, bg="sea green",
                                     command=run_script)
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
        find_button = tk.Button(self, text="Find", height=2, width=8, bg="deep sky bitlue",
                                command=lambda: controller.show("Home"))
        find_button.grid(row=25, column=40, padx=2, pady=2)

        col_count, row_count = self.grid_size()
        for col in range(col_count):
            self.grid_columnconfigure(col, minsize=10)
        for row in range(row_count):
            self.grid_rowconfigure(row, minsize=10)


if __name__ == "__main__":
    gui = GUI()
    gui.mainloop()
