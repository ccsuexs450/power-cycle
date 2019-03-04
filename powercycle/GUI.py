import tkinter as tk
from tkinter import *
import sys
import os

class GUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack()
        self.geometry("800x800")

        menu = Menu(self)
        self.config(menu=menu)
        subMenu = Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=subMenu)
        subMenu.add_command(label="Exit", command=self.quit)

        self.frames = {}
        for F in (Home, Calibrate):
            page = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show("Home")

    def show(self, page):
        frame = self.frames[page]
        frame.tkraise()

class Home(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        title = tk.Label(self, text="Bicycle Application", font=("Courier", 44), fg="black",)
        title.grid(row=1, column=1)
        calibrateButton = tk.Button(self, text="Calibrate", height=2, width=10, command=lambda: controller.show("Calibrate"))
        calibrateButton.grid(row=2, column=1, padx=2, pady=2)
        runButton = tk.Button(self, text="Run", height=4, width=20, command=lambda: controller.show("Calibrate"))
        runButton.grid(row=3, column=1, padx=2, pady=2)

        col_count, row_count = self.grid_size()
        for col in range(col_count):
            self.grid_columnconfigure(col, minsize=10)
        for row in range(row_count):
            self.grid_rowconfigure(row, minsize=10)

class Calibrate(tk.Frame):
    def __init__(self, parent, controller):
        def runScript():
            os.system('python Script.py')
        tk.Frame.__init__(self, parent)
        title = tk.Label(self, text="Calibration", font=("Courier", 44), fg="black")
        title.grid(row=1, column=15)
        calibrateButton = tk.Button(self, text="Run Calibration", height=4, width=24, command=runScript)
        calibrateButton.grid(row=2, column=15, padx=2, pady=2)
        homeButton = tk.Button(self, text="Home", height=3, width=18, command=lambda: controller.show("Home"))
        homeButton.grid(row=3, column=15, padx=2, pady=2)

        col_count, row_count = self.grid_size()
        for col in range(col_count):
            self.grid_columnconfigure(col, minsize=10)
        for row in range(row_count):
            self.grid_rowconfigure(row, minsize=10)

if __name__=="__main__":
    gui = GUI()
    gui.mainloop()