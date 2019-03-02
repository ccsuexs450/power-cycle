
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)
GPIO.add_event_detect(17, GPIO.FALLING)

values = []

i = 0;
while i < 10:
    if GPIO.event_detected(17):
        values.append(time.time())
        i+=1

print('Sensor time values: ',values)

time_values = []

for index, item in enumerate(values, start=0):
    time_values.append(values[index +1] - values[index])
    if index == 8:
        break


print(time_values)


