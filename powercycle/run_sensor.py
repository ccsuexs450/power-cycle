
import serial
import io
from datetime import datetime
from db_interaction import *
from calibrate import *
from power import *

values = []

def serial_conn():
    
    # opens serial connection to arduino
    ser=serial.Serial("/dev/ttyACM0",9600)  #change ACM number as found from ls /de$
    ser.baudrate=9600

    return ser


def calibrate_input(): #placeholder until sensor is working. Reads test input from file.
    
    # this below loop is only for testing when the sensor is not plugged in
    with open("../data/sensordata/calibrateTest.txt", "r") as ins:
        for line in ins:
            line = line.rstrip('\n')
            values.append(line)

# comment the loop below for testing    
   # try:
    #    ser = serial_conn()
   # except (serial.SerialException, FileNotFoundError) as e:
    #    print("Serial connection failed. Check sensor connections")
    #    raise

    # retrieve 900 data points from the sensor
#    i = 0
#    while i < 900:
#
#        input = int(ser.readline().strip())
#        values.append(str(input))
#        i+=1

    # retieve the text file path this is returned to the GUI
    path = textwrite("Calibration")
   
    print("Files Created")
    return path

# read sensor values from arduino and create a text file
def power_input(user_email):

    try:
        ser = serial_conn()
    except (serial.SerialException, FileNotFoundError) as e:
        print("Serial connection failed. Check sensor connections")
        raise
    i = 0
    while i < 495:

        input = int(ser.readline().strip())
        values.append(str(input))
        i+=1
    # retrieve text path and return to GUI
    path =  textwrite(user_email)
   
    print("Files Created")
 
    return path

# this function creates text files 
def textwrite(user_email):
   
    emailStr = str(user_email)
    date = datetime.now()
    f_date = date.strftime('%Y-%m-%d %H.%M.%S.%f')
    extension = ".txt"
    filename = emailStr[0:5] + f_date + extension
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

# this is test function used in development
def test_run(user_email):

   path = "../data/sensordata/power.txt"

   return path



