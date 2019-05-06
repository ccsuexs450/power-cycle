
import serial
import io
from datetime import datetime
from db_interaction import *
from calibrate import *
from power import *

values = []

def serial_conn():
    
    ser=serial.Serial("/dev/ttyACM0",9600)  #change ACM number as found from ls /de$
    ser.baudrate=9600

    return ser


def calibrate_input(): #placeholder until sensor is working. Reads test input from file.

    with open("../data/sensordata/calibrate.txt", "r") as ins:
        for line in ins:
            line = line.rstrip('\n')
            values.append(line)

# comment the loop below for testing    
   # try:
    ser = serial_conn()
   # except (serial.SerialException, FileNotFoundError) as e:
    #    print("Serial connection failed. Check sensor connections")
    #    raise

    
    i = 0
    while i < 900:

        input = int(ser.readline().strip())
        values.append(str(input))
        i+=1

    cal_values = values.copy()
    path = textwrite("Calibration")
#    calibrate_sheet(cal_values)
   # cal_values.clear()    

    print("Files Created")
    return path

def power_input(user_email):

   # try:
    ser = serial_conn()
   # except (serial.SerialException, FileNotFoundError) as e:
    #    print("Serial connection failed. Check sensor connections")
    #    raise
    i = 0
    while i < 495:

        input = int(ser.readline().strip())
        values.append(str(input))
        i+=1
    
    # uncomment and replace the return value with path for current implementation
    path =  textwrite(user_email)
    
    #power_sheet(values, user_email)

    print("Files Created")
   # return values
    return path

def textwrite(user_email):
    emailStr = str(user_email)
    date = datetime.now()
    f_date = date.strftime('%Y-%m-%d %H.%M.%S.%f')
    filename = emailStr[0:5] + f_date
    extension = ".txt"
    dir  = "../data/sensordata/"
    path = dir+filename+extension
    
    outfile = open(path, "w")
    for line in values:
        outfile.write(str(line))
        outfile.write("\n")
    outfile.close()
    textfile_insert(user_email, filename, path, date)
    values.clear()

    return path


def test_run(user_email):

   path = "../data/sensordata/power.txt"

   return path

#power_input("htazi@gmail.com")
#calibrate_input()
#test_run("htazi@gmail.com")

