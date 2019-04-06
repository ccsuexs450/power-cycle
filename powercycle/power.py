import os
import subprocess
import time
import pyoo
from db_interaction import *

soffice = subprocess.Popen([
    'lxterminal',
    '-e',
    'soffice',
    '--accept=host=localhost,port=2002;urp;',
    '--norestore',
    '--nologo',
    '--nodefault',
    '--headless'])

lines = []
dt    = []

desktop = pyoo.Desktop('localhost', 2002)
doc = desktop.open_spreadsheet("../docs/templates/Calibrate_blank.ods")

power = doc.sheets[1]
delta = doc.sheets[2]

with open("../data/sensordata/power.txt", "r") as ins:
    for line in ins:
        line = line.rstrip('\n')
        lines.append(line)

print(lines[0:10])
 
power[1:496,0].values = lines

with open("../docs/templates/delta_theta.txt", "r") as ins:
    for line in ins:
        line = line.rstrip('\n')
        dt.append(line)

delta[1:16,10].values = dt

path = "../docs/power/"
date = time.strftime("%Y%m%d-%H%M%S")
filename = "username" + date + ".ods"
file_path = path + filename
doc.save(file_path)
calibrate_insert(filename, file_path, date)
doc.close()

soffice.kill()

print("File Saved")
