import pyoo
import os
import subprocess
from db_interaction import *
from time import sleep

soffice = subprocess.Popen([
    'lxterminal',
    '-e',
    '/usr/bin/soffice',
    '--accept=host=localhost,port=2002;urp;',
    '--norestore',
    '--nologo',
    '--nodefault',
    '--headless'])

lines = []

desktop = pyoo.Desktop('localhost', 2002)
doc = desktop.open_spreadsheet("../docs/calibration/Calibrate_blank.ods")

sheet = doc.sheets[0]

with open("../data/sensordata/calibrate.txt", "r") as ins:
    for line in ins:
        line = line.rstrip('\n')
        lines.append(line)

print(lines[0:10])
 
#for i in range(0,795):
#    j = i + 1
#    sheet[j,0].value = lines[i]

sheet[1:796,0].values = lines

path = "../docs/calibration/"
date = "date_time" # place holder
filename = "calibrate_now_date_time.ods"  # place holder
file_path = path + filename
doc.save(file_path)
calibrate_insert(filename, file_path, date)
doc.close()


#soffice.kill()

print("File Saved")

