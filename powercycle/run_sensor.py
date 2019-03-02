
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)
GPIO.add_event_detect(17, GPIO.FALLING)

values = []

i=0
while i < 10:
    if GPIO.event_detected(17):
        value = time.time()
        values.append(value)
        i+=1
        print(values)

