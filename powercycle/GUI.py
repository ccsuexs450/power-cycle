import tkinter as tk
from tkinter import *
from db_interaction import *
import os


class GUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.shared = {"email": tk.StringVar(), "form_self": tk.Variable(), "results_self": tk.Variable()}
        container = tk.Frame(self)
        container.pack()
        self.geometry("1200x800")
        self.title("Bicycle Application")

        menu = Menu(self)
        self.config(menu=menu)

        # create home menu
        menu.add_cascade(label="Home", command=lambda: self.show("Home"))

        # create search menu
        search_menu = Menu(menu, tearoff=0)
        menu.add_cascade(label="Search", menu=search_menu)
        search_menu.add_command(label="Search by user name", command=lambda: self.show("SearchName"))
        search_menu.add_command(label="Search by file type", command=lambda: self.show("SearchFile"))

        # create file menu
        file_menu = Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.quit)

        self.frames = {}
        for F in (Home, Calibrate, EnterEmail, Form, Run, SearchFile, SearchName, ResultsPage):
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
        title.grid(row=0, column=1, padx=30, pady=30)

        calibrate_button = tk.Button(self, text="Calibrate", height=2, width=10,
                                     bg="deep sky blue", command=lambda: controller.show("Calibrate"))
        calibrate_button.grid(row=1, column=1, padx=15, pady=15)
        run_button = tk.Button(self, text="Run", height=4, width=20,
                               bg="sea green", command=lambda: controller.show("EnterEmail"))
        run_button.grid(row=2, column=1, padx=2, pady=2)

        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)


# create calibration page
class Calibrate(tk.Frame):
    def __init__(self, parent, controller):
        def run_script():
            os.system('python Script.py')
        tk.Frame.__init__(self, parent)
        title = tk.Label(self, text="Calibration", font=("Courier", 44), fg="black")
        title.grid(row=1, column=1)
        calibrate_button = tk.Button(self, text="Run Calibration", height=4, width=24, bg="sea green", command=run_script)
        calibrate_button.grid(row=2, column=1, padx=2, pady=2)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)


# create lookup by email page
class EnterEmail(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller=controller
        title = tk.Label(self, text="Enter Email:", font=("Courier", 28), fg="black")
        title.grid(row=19, column=40)
        e = tk.Entry(self, textvariable=self.controller.shared["email"])
        e.grid(row=20, column=40, sticky="nsew")

        def submit():
            email(self.controller.shared["form_self"])
            search = email_search(e.get())
            if search == None:
                controller.show("Form")
            else:
                controller.show("Run")
        find_button = tk.Button(self, text="Find", height=2, width=8, bg="deep sky blue", command=submit)
        find_button.grid(row=25, column=40, padx=2, pady=2)
        col_count, row_count = self.grid_size()
        for col in range(col_count):
            self.grid_columnconfigure(col, minsize=10)
        for row in range(row_count):
            self.grid_rowconfigure(row, minsize=10)


# create form page
class Form(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.controller.shared["form_self"] = self
        s = tk.StringVar()
        Label(self, text="First Name", font=("Courier", 14)).grid(row=2, column=1, pady=2)
        Label(self, text="Last Name", font=("Courier", 14)).grid(row=3, column=1, pady=2)
        Label(self, text="Age", font=("Courier", 14)).grid(row=4, column=1, pady=2)
        Label(self, text="Height", font=("Courier", 14)).grid(row=5, column=1, pady=2)
        Label(self, text="Weight", font=("Courier", 14)).grid(row=6, column=1, pady=2)
        Label(self, text="Sex", font=("Courier", 14)).grid(row=7, column=1, pady=2)
        Label(self, text="Category", font=("Courier", 14)).grid(row=9, column=1, pady=2)
        entry1 = Entry(self)
        entry2 = Entry(self)
        entry3 = Entry(self)
        entry4 = Entry(self)
        entry5 = Entry(self)
        entry6 = tk.Radiobutton(self, text="Male", variable=s, value="Male")
        entry7 = tk.Radiobutton(self, text="Female", variable=s, value="Female")
        entry8 = Entry(self)
        entry1.grid(row=2, column=2, pady=2)
        entry2.grid(row=3, column=2, pady=2)
        entry3.grid(row=4, column=2, pady=2)
        entry4.grid(row=5, column=2, pady=2)
        entry5.grid(row=6, column=2, pady=2)
        entry6.grid(row=7, column=2, pady=2)
        entry7.grid(row=8, column=2, pady=2)
        entry8.grid(row=9, column=2, pady=2)

        def submit(email, fname, lname, age, height, weight, gender, category):
            user_insert(email, fname, lname, age, height, weight, gender, category)
            controller.show("Run")

        submit_button = tk.Button(self, text="Submit", height=2, width=12, bg="deep sky blue", command=lambda: submit(self.controller.shared["email"].get(), entry1.get(), entry2.get(), entry3.get(), entry4.get(), entry5.get(), s.get(), entry8.get()))
        submit_button.grid(row=10, column=2)

        self.grid_rowconfigure(0, weight=1, minsize=150)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(11, weight=1)
        self.grid_columnconfigure(3, weight=1)


# create search by file type page
class SearchFile(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller=controller
        var1 = tk.StringVar()
        var2 = tk.StringVar()
        var3 = tk.StringVar()
        title1 = tk.Label(self, text="Search by file type:", font=("Courier", 28), fg="black")
        title1.grid(row=19, column=40)
        e1 = tk.Entry(self, textvariable=var1 )
        e1.grid(row=20, column=40, sticky="nsew")
        title2 = tk.Label(self, text="Date range:", font=("Courier", 28), fg="black")
        title2.grid(row=24, column=40)
        title3 = tk.Label(self, text="From:", font=("Courier", 16), fg="black")
        title3.grid(row=25, column=40)
        e2 = tk.Entry(self, textvariable=var2)
        e2.grid(row=26, column=40, sticky="nsew")
        title4 = tk.Label(self, text="To:", font=("Courier", 16), fg="black")
        title4.grid(row=29, column=40)
        e3 = tk.Entry(self, textvariable=var3)
        e3.grid(row=30, column=40, sticky="nsew")

        def find():
            search_file = file_search(e1.get(), e2.get(), e3.get())
            if var1.get() == "":
                print("please enter a file name")
            else:
                results(self.controller.shared["results_self"], search_file)
                controller.show("ResultsPage")

        find_button = tk.Button(self, text="Find", height=2, width=8, bg="deep sky blue", command=find)
        find_button.grid(row=33, column=40, padx=2, pady=2)
        col_count, row_count = self.grid_size()
        for col in range(col_count):
            self.grid_columnconfigure(col, minsize=10)
        for row in range(row_count):
            self.grid_rowconfigure(row, minsize=10)


# create search by user name page
class SearchName(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller=controller
        var1 = tk.StringVar()
        var2 = tk.StringVar()
        var3 = tk.StringVar()
        var4 = tk.StringVar()
        title1 = tk.Label(self, text="Search by user name:", font=("Courier", 28), fg="black")
        title1.grid(row=19, column=40)
        title2 = tk.Label(self, text="First Name:", font=("Courier", 16), fg="black")
        title2.grid(row=20, column=40)
        e1 = tk.Entry(self, textvariable=var1)
        e1.grid(row=21, column=40, sticky="nsew")
        title3 = tk.Label(self, text="Last Name:", font=("Courier", 16), fg="black")
        title3.grid(row=22, column=40)
        e2 = tk.Entry(self, textvariable=var2 )
        e2.grid(row=23, column=40, sticky="nsew")
        title4 = tk.Label(self, text="Date range:", font=("Courier", 28), fg="black")
        title4.grid(row=27, column=40)
        title5 = tk.Label(self, text="From:", font=("Courier", 16), fg="black")
        title5.grid(row=28, column=40)
        e3 = tk.Entry(self, textvariable=var3)
        e3.grid(row=29, column=40, sticky="nsew")
        title6 = tk.Label(self, text="To:", font=("Courier", 16), fg="black")
        title6.grid(row=30, column=40)
        e4 = tk.Entry(self, textvariable=var4)
        e4.grid(row=31, column=40, sticky="nsew")

        def find():
            search_user = user_search(e1.get(), e2.get(), e3.get(), e4.get())
            records_search_user = user_records_search(e1.get(), e2.get())
            if var1.get() == "":
                print("please enter the first name")
            elif var2.get() == "":
                print("please enter last name")
            elif var3.get() == "" or var4.get() == "":
                results(self.controller.shared["results_self"], records_search_user)
                controller.show("ResultsPage")
            else:
                results(self.controller.shared["results_self"], search_user)
                controller.show("ResultsPage")

        find_button = tk.Button(self, text="Find", height=2, width=8, bg="deep sky blue", command=find)
        find_button.grid(row=34, column=40, padx=2, pady=2)
        col_count, row_count = self.grid_size()
        for col in range(col_count):
            self.grid_columnconfigure(col, minsize=10)
        for row in range(row_count):
            self.grid_rowconfigure(row, minsize=10)


# create results page
class ResultsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.controller.shared["results_self"] = self
        fname = tk.Label(self, text="FirstName", font=("Courier", 16), fg="black")
        fname.grid(row=0, column=1, padx=20)
        lname = tk.Label(self, text="LastName", font=("Courier", 16), fg="black")
        lname.grid(row=0, column=2, padx=20)
        email = tk.Label(self, text="Email", font=("Courier", 16), fg="black")
        email.grid(row=0, column=3, padx=20)
        name = tk.Label(self, text="Name", font=("Courier", 16), fg="black")
        name.grid(row=0, column=4, padx=20)
        path = tk.Label(self, text="Path", font=("Courier", 16), fg="black")
        path.grid(row=0, column=5, padx=20)
        date = tk.Label(self, text="Date", font=("Courier", 16), fg="black")
        date.grid(row=0, column=6, padx=20)


# create run page
class Run(tk.Frame):
    def __init__(self, parent, controller):
        def run_script():
            os.system('python Script.py')
        tk.Frame.__init__(self, parent)
        title = tk.Label(self, text="Run Bicycle", font=("Courier", 44), fg="black")
        title.grid(row=1, column=1)
        run_button = tk.Button(self, text="Run", height=4, width=24, bg="sea green", command=run_script)
        run_button.grid(row=2, column=1, padx=2, pady=2)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)


def widgets(self):
    list = self.winfo_children()
    for item in list:
        if item.winfo_children():
            list.extend(item.winfo_children())
    return list


def email(self):
    email = self.controller.shared["email"].get()
    self.title = tk.Label(self, text="Email: " + email, font=("Courier", 28), fg="black")
    self.title.grid(row=1, columnspan=4)


def results(self, list):
    widget_list = widgets(self)
    for item in widget_list[6:]:
        item.grid_forget()
    count = 0
    for x, i in enumerate(list):
        count = count + 1
        for y, j in enumerate(i[0:]):
            result = tk.Label(self, text=j, fg="black", padx=10)
            result.grid(row=x+1, column=y+1)
    vars = []
    for i, j in enumerate(range(count)):
        var = IntVar()
        Checkbutton(self, text="Send to Email?", variable=var).grid(row=i+1, column=7)
        vars.append(var)

    def submit():
        for i, j in enumerate(range(count)):
            if vars[i].get() == 1:
                print("Checked")
    button = tk.Button(self, text="Submit", height=2, width=8, bg="deep sky blue", command=submit)
    button.grid(row=x+2, column=4, padx=2, pady=2)
    self.grid_rowconfigure(count+1, weight=1)
    self.grid_columnconfigure(0, weight=1)
    self.grid_columnconfigure(6, weight=1)


if __name__ == "__main__":
    gui = GUI()
    gui.mainloop()
