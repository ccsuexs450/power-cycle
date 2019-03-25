
import serial
import io
import time
from db_interaction import *

ser=serial.Serial("/dev/ttyACM0",9600)  #change ACM number as found from ls /de$
ser.baudrate=9600


values = []
time_values = []

def sensor_input():
    i = 0
    while i < 30:

        input = int(ser.readline().strip())
        values.append(str(input))
        i+=1

    return values


def textwrite():
    filename = time.strftime("%Y%m%d-%H%M%S")
    extension = ".txt"
    dir  = "../data/sensordata/"
    path = dir+filename+extension
    
    outfile = open(path, "w")
    for line in values:
        outfile.write(str(line))
        outfile.write("\n")
    outfile.close()
    user_email = "emailfromGUI" # these are place holders
    textfile_insert(user_email, filename, path, filename)


sensor_input()

print(values)

textwrite()

print('File created')


