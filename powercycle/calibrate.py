import os
import subprocess
import pyoo
from db_interaction import *

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
doc = desktop.open_spreadsheet("../docs/templates/Calibrate_blank.ods")

sheet = doc.sheets[0]

with open("../data/sensordata/calibrate.txt", "r") as ins:
    for line in ins:
        line = line.rstrip('\n')
        lines.append(line)

print(lines[0:10])
 
sheet[1:796,0].values = lines

path = "../docs/calibration/"
date = "date_time" # place holder
filename = "calibrate_now_date_time.ods"  # place holder
file_path = path + filename
doc.save(file_path)
calibrate_insert(filename, file_path, date)
doc.close()

soffice.kill()

print("File Saved")

