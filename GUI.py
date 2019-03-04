from tkinter import *
import sys
import os

def runScript():
    os.system('python Script.py')
def calWindow():
    window1 = Toplevel()
    window1.configure(bg="dim gray")
    window1.geometry("800x800")

    menu = Menu(window)
    window1.config(menu=menu)

    subMenu = Menu(menu, tearoff=0)
    menu.add_cascade(label="File", menu=subMenu)
    subMenu.add_command(label="Exit", command=window1.quit)

    title = Label(window1, text="Calibration", font=("Courier", 44), fg="white", bg="dim gray")
    title.grid(row=0, columnspan=150)
    calibrateButton = Button(window1, text="Run Calibration", height=3, width=18, command=runScript)
    calibrateButton.grid(row=25, column=72, padx=2, pady=2)
    col_count, row_count = window1.grid_size()


    for col in range(col_count):
        window1.grid_columnconfigure(col, minsize=10)

    for row in range(row_count):
        window1.grid_rowconfigure(row, minsize=10)

window = Tk()
window.configure(bg="dim gray")
window.geometry("800x800")

menu = Menu(window)
window.config(menu=menu)

subMenu = Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Exit", command=window.quit)

title = Label(window, text="Bicycle Application", font=("Courier", 44), fg="white", bg="dim gray")
title.grid(row=0, columnspan=150)
insertButton = Button(window, text="Calibrate", height=2, width=10, command=calWindow)
insertButton.grid(row=20, column=72, padx=2, pady=2)
printButton = Button(window, text="Run", height=4, width=20, command=runScript)
printButton.grid(row=25, column=72, padx=2, pady=2)

col_count, row_count = window.grid_size()

for col in range(col_count):
    window.grid_columnconfigure(col, minsize=10)

for row in range(row_count):
    window.grid_rowconfigure(row, minsize=10)

window.mainloop()