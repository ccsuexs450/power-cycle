
import serial
import io
import time
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

    textwrite("calibrator")
    calibrate_sheet(values, user_email)

    print("Files Created")
    

def power_input(user_email):

    ser = serial_conn()

    i = 0
    while i < 29:

        input = int(ser.readline().strip())
        values.append(str(input))
        i+=1

    textwrite(user_email)
    power_sheet(values, user_email)

    print("Files Created")


def textwrite(user_email):
    emailStr = str(user_email)
    filename = emailStr[0:5] + time.strftime("%Y%m%d-%H%M%S")
    extension = ".txt"
    dir  = "../data/sensordata/"
    path = dir+filename+extension
    
    outfile = open(path, "w")
    for line in values:
        outfile.write(str(line))
        outfile.write("\n")
    outfile.close()
    textfile_insert(user_email, filename, path, filename)

#power_input("htazi@gmail.com")


