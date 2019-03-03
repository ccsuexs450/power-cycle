
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)
GPIO.add_event_detect(17, GPIO.FALLING)

values = []
time_values = []

def raw_input():
    i = 0;
    while i < 10:
        if GPIO.event_detected(17):
            values.append(time.time())
            i+=1
    return values

def edge_measure():
    for index, item in enumerate(values, start=0):
        time_values.append(values[index +1] - values[index])
        if index == 8:
            break
    return time_values

def textwrite():
    outfile = open("myOutFile.txt", "w")
    for line in time_values:
        outfile.write(str(line))
        outfile.write("\n")
    outfile.close()

raw_input()

print('Sensor time values: ',values)

edge_measure()

print(time_values)

textwrite()

print('File created')


