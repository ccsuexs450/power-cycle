import tkinter as tk
from tkinter import *
from tkinter import ttk
#from power_chart import *
from db_interaction import *
from results_test import *
#from run_sensor import *
from datetime import *
import os
from PIL import Image, ImageTk
from email_function import *
from validate_email import validate_email
import socket
from automatic_email_bash import *
import time

class GUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.shared = {"email": tk.StringVar(), "form_self": tk.Variable(), "results_self": tk.Variable(),
                       "calibration_results_self": tk.Variable(), "results_page_self": tk.Variable(),
                       "max_power": tk.StringVar(), "rpm": tk.StringVar(), "rpm_opt": tk.StringVar(),
                       "twitch": tk.StringVar(), "path": tk.StringVar(), "path_txt_test": tk.StringVar(),
                       "process_self": tk.Variable(), "password": tk.StringVar(), "email_boolean": tk.Variable()}

        toolbar = Frame(self, bg="gray87")
        house = Image.open("../icons/Home.png")
        house = house.resize((30, 35))
        image = ImageTk.PhotoImage(house)
        button = tk.Button(toolbar, text="Home", image=image, height=25, width=50, command=lambda: self.show("Home"))
        button.pack(side=LEFT)
        button.image=image
        toolbar.pack(side=TOP, fill=X)

        container = tk.Frame(self)
        container.pack()

        self.geometry("1200x800")
        self.title("Bicycle Application")

        menu = Menu(self)
        self.config(menu=menu)

        # create file menu
        file_menu = Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Home", command=lambda: self.show("Home"))
        file_menu.add_command(label="Calibrate", command=lambda: self.show("Calibrate"))
        file_menu.add_command(label="Run", command=lambda: self.show("Run"))
        file_menu.add_command(label="Exit", command=self.quit)

        # create search menu
        search_menu = Menu(menu, tearoff=0)
        menu.add_cascade(label="Search", menu=search_menu)
        search_menu.add_command(label="Search by user name", command=lambda: self.show("SearchName"))
        search_menu.add_command(label="Search by file type", command=lambda: self.show("SearchFile"))

        self.frames = {}
        for F in (Home, Calibrate, EnterEmail, Form, Run, SearchFile, SearchName, ResultsPage, CalibrationResultsPage,
                  FinalResultsPage, ProcessingPage):
            page = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show("Home")
        if (os.path.isfile("store.txt")):
            popup = tk.Tk()
            label1 = tk.Label(popup, text="Enter sending email password")
            label1.grid(row=2, column=0, pady=10)
            password = tk.Entry(popup, width=35, show="*")
            password.grid(row=3, column=0)
            button = ttk.Button(popup, text="Submit", command=lambda: send(popup))
            button.grid(row=4, column=0, pady=5)

            def send(popup):
                if sendBatch(password.get()) == 0:
                    error['bg'] = "red"
                    error['text'] = "Password not valid"
                else:
                    popup.destroy()

            error = tk.Label(popup)
            error.grid(row=6, column=0)

    # define show function
    def show(self, page):
        frame = self.frames[page]
        frame.tkraise()


# create home page
class Home(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        title = tk.Label(self, text="Cycling Performance System", font=("Open Sans", 32))
        title.grid(row=0, column=1, columnspan=3, padx=30, pady=30)
        run_button = tk.Button(self, text="Run", height=6, width=30, bg="turquoise", relief="flat", command=lambda: controller.show("EnterEmail"))
        run_button.grid(row=1, column=1, columnspan=3, padx=2, pady=2)
        file_search = tk.Button(self, text="Search Data By File", height=4, width=20, bg="green yellow", relief="flat", command=lambda: controller.show("SearchFile"))
        file_search.grid(row=3, column=1, pady=2)
        name_search = tk.Button(self, text="Search Data By Name", height=4, width=20, bg="orange", relief="flat", command=lambda: controller.show("SearchName"))
        name_search.grid(row=3, column=2, pady=2)
        calibrate_button = tk.Button(self, text="Calibrate", height=4, width=20, bg="MediumPurple1", relief="flat", command=lambda: controller.show("Calibrate"))
        calibrate_button.grid(row=3, column=3, pady=2)

        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(2, minsize=100)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(4, weight=1)


# create final results page
class FinalResultsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.controller.shared["results_page_self"] = self


# create calibration page
class Calibrate(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def run_script():
            os.system('python Script.py')
        title = tk.Label(self, text="Calibration", font=("Open Sans", 44), fg="black")
        title.grid(row=1, column=1)
        calibrate_button = tk.Button(self, text="Run Calibration", height=4, width=24, bg="turquoise", relief="flat", command=run_script)
        calibrate_button.grid(row=2, column=1, padx=2, pady=2)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)


# create lookup by email page
class EnterEmail(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        title = tk.Label(self, text="Enter Email:", font=("Open Sans", 28), fg="black")
        title.grid(row=1, column=1)
        e = tk.Entry(self, textvariable=self.controller.shared["email"])
        e.grid(row=2, column=1, pady=10, sticky="nsew")

        def submit():
            email = e.get()
            try:
                socket.create_connection(("www.google.com", 80))
                connection = True
            except OSError:
                connection = False
            if len(email) == 0:
                message("Entry cannot be blank")
            else:
                search = email_search(email)
                if search == None:
                    if connection == True:
                        if validate(email) == 0:
                            message("Invalid email address")
                            return
                    form(self.controller.shared["form_self"], True)
                    controller.show("Form")
                else:
                    form(self.controller.shared["form_self"], False)
                    controller.show("Form")

        find_button = tk.Button(self, text="Find", height=2, width=8, bg="turquoise", relief="flat", command=submit)
        find_button.grid(row=3, column=1, padx=2, pady=2)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)


# create form page
class Form(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.controller.shared["form_self"] = self

    def validate_int(self, value):
        if str.isdigit(value) or value == "":
            return True
        else:
            return False

    def validate_float(self, value):
        if value != "":
            try:
                float(value)
                return True
            except ValueError:
                return False
        else:
            return True


# create search by file type page
class SearchFile(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        var1 = tk.StringVar()
        var2 = tk.StringVar()
        var3 = tk.StringVar()
        title1 = tk.Label(self, text="Search by file type:", font=("Open Sans", 28), fg="black")
        title1.grid(row=1, column=1)
        e1 = tk.Entry(self, textvariable=var1)
        e1.grid(row=2, column=1, sticky="nsew")
        title2 = tk.Label(self, text="Date range: (YYYY-MM-DD)", font=("Open Sans", 28), fg="black")
        title2.grid(row=4, column=1)
        title3 = tk.Label(self, text="From:", font=("Open Sans", 16), fg="black")
        title3.grid(row=5, column=1)
        e2 = tk.Entry(self, textvariable=var2)
        e2.grid(row=6, column=1, sticky="nsew")
        title4 = tk.Label(self, text="To:", font=("Open Sans", 16), fg="black")
        title4.grid(row=7, column=1)
        e3 = tk.Entry(self, textvariable=var3)
        e3.grid(row=8, column=1, sticky="nsew")

        def find():
            try:
                if len(e2.get()) != 0:
                    datetime.strptime(e2.get(), "%Y-%m-%d")
                    date1 = e2.get()
                    if len(e3.get()) == 0:
                        date2 = str(date.today())
                if len(e3.get()) != 0:
                    datetime.strptime(e3.get(), "%Y-%m-%d")
                    date2 = e3.get()
                    if len(e2.get()) == 0:
                            date1 = "2019-01-01"
                if len(e2.get()) == 0 and len(e3.get()) == 0:
                    date1 = e2.get()
                    date2 = e3.get()
            except:
                message("Wrong date format. Correct format is YYYY-MM-DD")
            else:
                search_text_file = text_file_search(date1, date2)
                search_power_file = power_file_search(date1, date2)
                search_calibration_file = calibration_file_search(date1, date2)
                search_graph_file = graph_file_search(date1, date2)
                search_text_file_records = text_file_records_search()
                search_power_file_records = power_file_records_search()
                search_calibration_file_records = calibration_file_records_search()
                search_graph_file_records = graph_file_records_search()

                if var1.get() == "":
                    message("Please enter a file type")
                elif var1.get() == "text":
                    if var2.get() == "" and var3.get() == "":
                        results(self.controller.shared["results_self"], search_text_file_records)
                        controller.show("ResultsPage")
                    else:
                        results(self.controller.shared["results_self"], search_text_file)
                        controller.show("ResultsPage")
                elif var1.get() == "power":
                    if var2.get() == "" or var3.get() == "":
                        results(self.controller.shared["results_self"], search_power_file_records)
                        controller.show("ResultsPage")
                    else:
                        results(self.controller.shared["results_self"], search_power_file)
                        controller.show("ResultsPage")
                elif var1.get() == "calibration":
                    if var2.get() == "" or var3.get() == "":
                        calibration_results(self.controller.shared["calibration_results_self"], search_calibration_file_records)
                        controller.show("CalibrationResultsPage")
                    else:
                        calibration_results(self.controller.shared["calibration_results_self"], search_calibration_file)
                        controller.show("CalibrationResultsPage")
                elif var1.get() == "graph":
                    if var2.get() == "" or var3.get() == "":
                        results(self.controller.shared["results_self"], search_graph_file_records)
                        controller.show("ResultsPage")
                    else:
                        results(self.controller.shared["results_self"], search_graph_file)
                        controller.show("ResultsPage")
                else:
                    print(" the file type you have entered is not found!!!")

        find_button = tk.Button(self, text="Find", height=2, width=8, bg="turquoise", relief="flat", command=find)
        find_button.grid(row=9, column=1, padx=10, pady=10)

        self.grid_rowconfigure(0, weight=1, minsize=150)
        self.grid_rowconfigure(3, minsize=50)
        self.grid_rowconfigure(10, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)


# create search by user name page
class SearchName(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller=controller
        var1 = tk.StringVar()
        var2 = tk.StringVar()
        var3 = tk.StringVar()
        var4 = tk.StringVar()
        title1 = tk.Label(self, text="Search by user name:", font=("Open Sans", 28), fg="black")
        title1.grid(row=1, column=1)
        title2 = tk.Label(self, text="First Name:", font=("Open Sans", 16), fg="black")
        title2.grid(row=2, column=1)
        e1 = tk.Entry(self, textvariable=var1)
        e1.grid(row=3, column=1, sticky="nsew")
        title3 = tk.Label(self, text="Last Name:", font=("Open Sans", 16), fg="black")
        title3.grid(row=4, column=1)
        e2 = tk.Entry(self, textvariable=var2 )
        e2.grid(row=5, column=1, sticky="nsew")
        title4 = tk.Label(self, text="Date range: (YYYY-MM-DD)", font=("Open Sans", 28), fg="black")
        title4.grid(row=7, column=1)
        title5 = tk.Label(self, text="From:", font=("Open Sans", 16), fg="black")
        title5.grid(row=8, column=1)
        e3 = tk.Entry(self, textvariable=var3)
        e3.grid(row=9, column=1, sticky="nsew")
        title6 = tk.Label(self, text="To:", font=("Open Sans", 16), fg="black")
        title6.grid(row=10, column=1)
        e4 = tk.Entry(self, textvariable=var4)
        e4.grid(row=11, column=1, sticky="nsew")

        def find():
            try:
                if len(e3.get()) != 0:
                    datetime.strptime(e3.get(), "%Y-%m-%d")
                    date1 = e3.get()
                    if len(e4.get()) == 0:
                        date2 = str(date.today())
                if len(e4.get()) != 0:
                    datetime.strptime(e4.get(), "%Y-%m-%d")
                    date2 = e4.get()
                    if len(e3.get()) == 0:
                        date1 = "2019-01-01"
                if len(e3.get()) == 0 and len(e4.get()) == 0:
                    date1 = e3.get()
                    date2 = e4.get()
            except:
                message("Wrong date format. Correct format is YYYY-MM-DD")
            else:
                search_user = user_search(e1.get(), e2.get(), date1, date2)
                records_search_user = user_records_search(e1.get(), e2.get())
                if var1.get() == "":
                    message("Please enter first name")
                elif var2.get() == "":
                    message("Please enter last name")
                elif var3.get() == "" and var4.get() == "":
                    results(self.controller.shared["results_self"], records_search_user)
                    controller.show("ResultsPage")
                else:
                    results(self.controller.shared["results_self"], search_user)
                    controller.show("ResultsPage")

        find_button = tk.Button(self, text="Find", height=2, width=8, bg="turquoise", relief="flat", command=find)
        find_button.grid(row=12, column=1, padx=10, pady=10)

        self.grid_rowconfigure(0, weight=1, minsize=150)
        self.grid_rowconfigure(6, minsize=50)
        self.grid_rowconfigure(13, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)


# create results page
class ResultsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.controller.shared["results_self"] = self
        fname = tk.Label(self, text="FirstName", font=("Open Sans", 16), fg="black")
        fname.grid(row=0, column=1, padx=20)
        lname = tk.Label(self, text="LastName", font=("Open Sans", 16), fg="black")
        lname.grid(row=0, column=2, padx=20)
        email = tk.Label(self, text="Email", font=("Open Sans", 16), fg="black")
        email.grid(row=0, column=3, padx=20)
        name = tk.Label(self, text="Name", font=("Open Sans", 16), fg="black")
        name.grid(row=0, column=4, padx=20)
        path = tk.Label(self, text="Path", font=("Open Sans", 16), fg="black")
        path.grid(row=0, column=5, padx=20)
        date = tk.Label(self, text="Date", font=("Open Sans", 16), fg="black")
        date.grid(row=0, column=6, padx=20)


# create calibration results page
class CalibrationResultsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.controller.shared["calibration_results_self"] = self
        name = tk.Label(self, text="Name", font=("Open Sans", 16), fg="black")
        name.grid(row=0, column=1, padx=20)
        path = tk.Label(self, text="Path", font=("Open Sans", 16), fg="black")
        path.grid(row=0, column=2, padx=20)
        date = tk.Label(self, text="Date", font=("Open Sans", 16), fg="black")
        date.grid(row=0, column=3, padx=20)


# create processing page
class ProcessingPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.controller.shared["process_self"] = self

        explanation = '''data collection finished. It's in the path bellow, click continue to process,
        it may take a minute or so to process, please be patient '''

        title = tk.Label(self, text=explanation, font=("Courier", 18), fg="black", )
        title.grid(row=0, column=1,padx=30, pady=30)
        path_test = str(self.controller.shared["path_txt_test"].get())
        user_email = str(self.controller.shared["email"].get())
        self.title = tk.Label(self, text="Path: " + path_test, font=("Courier", 16), fg="blue")
        self.title.grid(row=1, column=1, pady=5)

        def cont():
            user_email = str(self.controller.shared["email"].get())
            print(user_email)
            # comment the below function call for testing
           # values = power_sheet(path_test,user_email)
            # comment the below function call for full functionality
            values = resultsT(path_test, user_email)
            self.controller.shared["max_power"].set(values[0])
            self.controller.shared["rpm"].set(values[1])
            self.controller.shared["rpm_opt"].set(values[2])
            self.controller.shared["twitch"].set(values[3])
            self.controller.shared["path"].set(values[4])

            if values is not None:
                values = None
                controller.show("FinalResultsPage")
                results_page(self.controller.shared["results_page_self"])

        cont_button = tk.Button(self, text="Continue", height=4, width=24, bg="turquoise", relief="flat", command=cont)
        cont_button.grid(row=2, column=1, padx=2, pady=2)


# create run page
class Run(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        #self.controller.shared["path_txt_test"].set(power_input_test())

        def run():
            user_email = str(self.controller.shared["email"].get())
            # comment the below function call for testing
            #path = test_run(user_email)
            # comment the below function call for full functionality
            path = power_input_test(user_email)
            self.controller.shared["path_txt_test"].set(path)
            if path is not None:
                path = None
                print(path)
                controller.show("ProcessingPage")
                process(self.controller.shared["process_self"])

        title = tk.Label(self, text="Run Bicycle", font=("Open Sans", 44), fg="black")
        title.grid(row=1, column=1)
        run_button = tk.Button(self, text="Run", height=4, width=24, bg="turquoise", relief="flat", command=run)
        run_button.grid(row=2, column=1, padx=2, pady=2)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)


def form(self, new):
    widget_list = widgets(self)
    i = len(widget_list) - 1
    if len(widget_list)!= 0:
        while widget_list[i].winfo_ismapped():
            widget_list[i].grid_forget()
            i = i-1
    email = self.controller.shared["email"].get()
    int_check = (self.register(self.validate_int))
    float_check = (self.register(self.validate_float))
    self.title = tk.Label(self, text="Email: " + email, font=("Open Sans", 28), fg="black")
    self.title.grid(row=1, columnspan=5)
    s = tk.StringVar()
    Label(self, text="First Name", font=("Open Sans", 14)).grid(row=2, column=1, pady=2)
    Label(self, text="Last Name", font=("Open Sans", 14)).grid(row=3, column=1, pady=2)
    Label(self, text="Date(YYYY-MM-DD)", font=("Open Sans", 14)).grid(row=4, column=1, pady=2)
    Label(self, text="Height(feet, inches)", font=("Open Sans", 14)).grid(row=5, column=1, pady=2)
    Label(self, text="Weight(lbs)", font=("Open Sans", 14)).grid(row=6, column=1, pady=2)
    Label(self, text="Sex", font=("Open Sans", 14)).grid(row=7, column=1, pady=2)
    Label(self, text="Category", font=("Open Sans", 14)).grid(row=9, column=1, pady=2)
    entry1 = Entry(self)
    entry2 = Entry(self)
    entry3 = Entry(self)
    entry4 = Entry(self, validate='all', validatecommand=(int_check, '%P'), width=10)
    entry5 = Entry(self, validate='all', validatecommand=(int_check, '%P'), width=10)
    entry6 = Entry(self, validate='all', validatecommand=(float_check, '%P'))
    entry7 = tk.Radiobutton(self, text="Male", variable=s, value="Male")
    entry8 = tk.Radiobutton(self, text="Female", variable=s, value="Female")
    entry9 = Entry(self, validate='all', validatecommand=(int_check, '%P'))

    if not new:
        user_info = user_profile_search(email)
        entry1.insert(0, user_info[1])
        entry2.insert(0, user_info[2])
        entry3.insert(0, user_info[8])
        entry4.insert(0, int(user_info[4])//12)
        entry5.insert(0, int(user_info[4]) % 12)
        entry6.insert(0, user_info[5])
        if user_info[6] == "Male":
            entry7.invoke()
        else:
            entry8.invoke()
        entry9.insert(0, user_info[7])

    entry1.grid(row=2, column=2, columnspan=2, pady=2)
    entry2.grid(row=3, column=2, columnspan=2, pady=2)
    entry3.grid(row=4, column=2, columnspan=2, pady=2)
    entry4.grid(row=5, column=2, pady=2, padx=2)
    entry5.grid(row=5, column=3, pady=2, padx=2)
    entry6.grid(row=6, column=2, columnspan=2, pady=2)
    entry7.grid(row=7, column=2, columnspan=2, pady=2)
    entry8.grid(row=8, column=2, columnspan=2, pady=2)
    entry9.grid(row=9, column=2, columnspan=2, pady=2)

    def submit(email, fname, lname, date, feet, inches, weight, gender, category):
        if len(fname) == 0 or len(lname) == 0 or len(feet) == 0 or len(inches) == 0 or len(weight) == 0 or len(gender) == 0 or len(category) == 0:
            message("Form entries cannot be blank")
        else:
            try:
                birth = datetime.strptime(date, "%Y-%m-%d")
                today = datetime.now()
                year = 365.2422
                age = round(((today - birth).days / year), 1)
            except:
                message("Wrong date format. Correct format is YYYY-MM-DD")
            else:
                height = eval(feet) * 12 + eval(inches)
                if new:
                    user_insert(email, fname, lname, age, height, weight, gender, category, date)
                else:
                    user_update(email, fname, lname, age, height, weight, gender, category, date)
                self.controller.show("Run")

    submit_button = tk.Button(self, text="Submit", height=2, width=12, bg="turquoise", relief="flat", command=lambda: submit(self.controller.shared["email"].get(), entry1.get(), entry2.get(), entry3.get(), entry4.get(), entry5.get(), entry6.get(), s.get(), entry9.get()))
    submit_button.grid(row=10, column=1, columnspan=3, pady=20)

    self.grid_rowconfigure(0, weight=1, minsize=150)
    self.grid_columnconfigure(0, weight=1)
    self.grid_rowconfigure(11, weight=1)
    self.grid_columnconfigure(4, weight=1)


def process(self):
    widget_list = widgets(self)
    if len(widget_list) != 0:
        widget_list[0].grid_forget()
    explanation = '''data collection finished. It's in the path bellow, click continue to process,
        it may take a minute or so to process, please be patient '''

    self.title = tk.Label(self, text=explanation, font=("Courier", 18), fg="black", )
    self.title.grid(row=0, column=1,padx=30, pady=30)

    path_test = self.controller.shared["path_txt_test"].get()
    self.title = tk.Label(self, text="Path: " + path_test, font=("Courier", 16), fg="blue")
    self.title.grid(row=1, column=1, pady=5)


def results_page(self):
    widget_list = widgets(self)
    if len(widget_list) != 0:
        widget_list[0].grid_forget()
    email = self.controller.shared["email"].get()
    max_power = self.controller.shared["max_power"].get()
    rpm = self.controller.shared["rpm"].get()
    rpm_opt = self.controller.shared["rpm_opt"].get()
    twitch = self.controller.shared["twitch"].get()
    self.title = tk.Label(self, text="This is the performance results for the user with the email: " + email,
                          font=("Courier", 16), fg="black")
    self.title.grid(row=0, column=1, columnspan=10, rowspan=3, pady=20)
    self.title = tk.Label(self, text="Max Power: " + max_power, font=("Courier", 16), fg="blue")
    self.title.grid(row=4, column=2, pady=5)
    self.title = tk.Label(self, text="RPM : " + rpm, font=("Courier", 16), fg="red")
    self.title.grid(row=4, column=3, pady=5)
    self.title = tk.Label(self, text="RPM opt: " + rpm_opt, font=("Courier", 16), fg="blue")
    self.title.grid(row=5, column=2, pady=5)
    self.title = tk.Label(self, text="Twitch %: " + twitch, font=("Courier", 16), fg="red")
    self.title.grid(row=5, column=3, pady=5)

    path = str(self.controller.shared["path"].get())
    email_path = []
    email_path.append(path)
    load = Image.open(path)
    render = ImageTk.PhotoImage(load)
    img = Label(self, image=render)
    img.image = render
    img.grid(row=8, column=0, columnspan=10, rowspan=4, padx=20)

    var1 = IntVar()
    var2 = IntVar()
    Checkbutton(self, text="Change user ?", variable=var1).grid(row=13, column=4)
    Checkbutton(self, text="Run again ?", variable=var2).grid(row=13, column=3)

    try:
        socket.create_connection(("www.google.com", 80))
        connection = True
    except OSError:
        connection = False
    popup = tk.Tk()
    label1 = tk.Label(popup, text="Enter sending email password")
    label1.grid(row=2, column=0, pady=10)
    entry = tk.Entry(popup, width=35, show="*")
    entry.grid(row=3, column=0)
    error = tk.Label(popup)
    error.grid(row=6, column=0)

    def send(popup):
        password = entry.get()
        error['bg'] = "red"
        if connection == True:
            if sendEmail(email, password, email_path) == 0:
                error['text'] = "Password not valid"
                return
        else:
            sendEmail(email, password, path)
            message("There is no internet connection, files were safely stored\n Saved Email(s) & Attachment(s) will be sent next time the application is run")
        popup.destroy()

    button = ttk.Button(popup, text="Submit", command=lambda: send(popup))
    button.grid(row=4, column=0, pady=5)
    button = ttk.Button(popup, text="Continue without emailing", command=popup.destroy)
    button.grid(row=5, column=0, pady=5)


    def submit():
        if var1.get() == 1:
            self.controller.show("EnterEmail")
        if var2.get() == 1:
            self.controller.show("Run")

    submit_button = tk.Button(self, text="Submit", height=2, width=8, bg="turquoise", relief="flat", command=submit)
    submit_button.grid(row=13, column=2, padx=40)

    self.grid_rowconfigure(3, weight=1)
    self.grid_columnconfigure(0, weight=1)
    self.grid_columnconfigure(2, weight=1)


def results(self, list):
    widget_list = widgets(self)
    i = len(widget_list) - 1
    while widget_list[i].winfo_ismapped() and i > 5:
        widget_list[i].grid_forget()
        i = i - 1
    count = 0
    paths = []
    for x, i in enumerate(list):
        count = count + 1
        for y, j in enumerate(i[0:]):
            if y == 4:
                paths.append(j)
            result = tk.Label(self, text=j, fg="black", padx=10)
            result.grid(row=x+1, column=y+1)
    email_vars = []
    open_vars = []
    for i, j in enumerate(range(count)):
        var = IntVar()
        var1 = IntVar()
        Checkbutton(self, text="Send to Email?", variable=var).grid(row=i+1, column=7)
        Checkbutton(self, text="Open?", variable=var1).grid(row=i+1, column=8)
        email_vars.append(var)
        open_vars.append(var1)

    def submit():
        send = False
        email_paths = []
        for i, j in enumerate(range(count)):
            if email_vars[i].get() == 1:
                send = True
                email_paths.append(paths[i])
            if open_vars[i].get() == 1:
                os.startfile(paths[i])

        if send:
            try:
                socket.create_connection(("www.google.com", 80))
                connection = True
            except OSError:
                connection = False
            popup = tk.Tk()
            label1 = tk.Label(popup, text="Enter receiving email")
            label1.grid(row=0, column=0, pady=10)
            entry = tk.Entry(popup, width=35)
            entry.grid(row=1, column=0)
            label2 = tk.Label(popup, text="Enter sending email password")
            label2.grid(row=2, column=0, pady=10)
            passEntry = tk.Entry(popup, width=35, show="*")
            passEntry.grid(row=3, column=0)
            error = tk.Label(popup)
            error.grid(row=5, column=0)

            def send(popup):
                email = entry.get()
                password = passEntry.get()
                error['bg'] = "red"
                if connection == True:
                    if validate(email) == 0:
                        error['text'] = "Email not valid"
                        return
                    if sendEmail(email, password, email_paths) == 0:
                        error['text'] = "Password not valid"
                        return
                else:
                    sendEmail(email, password, email_paths)
                    message("There is no internet connection, files were safely stored\n Saved Email(s) & Attachment(s) will be sent next time the application is run")
                popup.destroy()
            button = ttk.Button(popup, text="Submit", command=lambda: send(popup))
            button.grid(row=4, column=0, pady=5)

    button = tk.Button(self, text="Submit", height=4, width=24, bg="turquoise", relief="flat", command=submit)
    button.grid(row=count+1, columnspan=10, padx=2, pady=20)

    self.grid_columnconfigure(0, weight=1)
    self.grid_columnconfigure(9, weight=1)


def calibration_results(self, list):
    widget_list = widgets(self)
    i = len(widget_list) - 1
    while widget_list[i].winfo_ismapped() and i > 2:
        widget_list[i].grid_forget()
        i = i - 1
    count = 0
    paths = []
    for x, i in enumerate(list):
        count = count + 1
        for y, j in enumerate(i[0:]):
            if y == 1:
                paths.append(j)
            result = tk.Label(self, text=j, fg="black", padx=10)
            result.grid(row=x+1, column=y+1)
    email_vars = []
    open_vars = []
    for i, j in enumerate(range(count)):
        var = IntVar()
        var1 = IntVar()
        Checkbutton(self, text="Send to Email?", variable=var).grid(row=i+1, column=4)
        Checkbutton(self, text="Open?", variable=var1).grid(row=i+1, column=5)
        email_vars.append(var)
        open_vars.append(var1)

    def submit():
        send = False
        email_paths = []
        for i, j in enumerate(range(count)):
            if email_vars[i].get() == 1:
                send = True
                email_paths.append(paths[i])
            if open_vars[i].get() == 1:
                os.startfile(paths[i])

        if send:
            try:
                socket.create_connection(("www.google.com", 80))
                connection = True
            except OSError:
                connection = False
            popup = tk.Tk()
            label1 = tk.Label(popup, text="Enter receiving email")
            label1.grid(row=0, column=0, pady=10)
            entry = tk.Entry(popup, width=30)
            entry.grid(row=1, column=0)
            label2 = tk.Label(popup, text="Enter sending email password")
            label2.grid(row=2, column=0, pady=10)
            passEntry = tk.Entry(popup, width=30, show="*")
            passEntry.grid(row=3, column=0)
            error = tk.Label(popup)
            error.grid(row=5, column=0)
            def send(popup):
                email = entry.get()
                password = passEntry.get()
                error['bg'] = "red"
                if connection == True:
                    if validate(email) == 0:
                        error['text'] = "Email not valid"
                        return
                    if sendEmail(email, password, email_paths) == 0:
                        error['text'] = "Password not valid"
                        return
                else:
                    sendEmail(email, password, email_paths)
                    message("There is no internet connection, files were safely stored\n Saved Email(s) & Attachment(s) will be sent next time the application is run")
                popup.destroy()
            button = ttk.Button(popup, text="Submit",  command=lambda: send(popup))
            button.grid(row=4, column=0, pady=5)

    button = tk.Button(self, text="Submit", height=4, width=24, bg="turquoise", relief="flat", command=submit)
    button.grid(row=count+1, columnspan=7, padx=2, pady=20)

    self.grid_columnconfigure(0, weight=1)
    self.grid_columnconfigure(6, weight=1)

def widgets(self):
    list = self.winfo_children()
    for item in list:
        if item.winfo_children():
            list.extend(item.winfo_children())
    return list

def message(text):
    popup = tk.Tk()
    label = tk.Label(popup, text=text)
    label.grid(row=0, column=1, pady=10)
    button = ttk.Button(popup, text="Ok", command=popup.destroy)
    button.grid(row=1, column=1)

    popup.grid_columnconfigure(0, weight=1, minsize=50)
    popup.grid_columnconfigure(2, weight=1, minsize=50)
    popup.grid_rowconfigure(2, minsize=30)

def validate(receiver_email):
    is_valid = validate_email(receiver_email, verify=True)
    if (is_valid == False):
        return 0
    else:
        return 1

if __name__ == "__main__":
    gui = GUI()
    gui.mainloop()

