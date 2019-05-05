import os
import subprocess
import datetime
import pyoo
from db_interaction import *

def calibrate_sheet(lines):
    
    soffice = subprocess.Popen('startLO')
    time.sleep(7)
    
#    lines = []

    desktop = pyoo.Desktop('localhost', 2002)
    doc = desktop.open_spreadsheet("../docs/templates/Calibrate_blank.ods")

    sheet = doc.sheets[0]

#    with open("../data/sensordata/calibrate.txt", "r") as ins:
#        for line in ins:
#            line = line.rstrip('\n')
#            lines.append(line)

    print(lines[0:10])
 
    sheet[1:901,0].values = lines

    delta_theta = sheet[1:16,10].values

    with open("../docs/templates/delta_theta.txt", "w") as out:
        for item in delta_theta:
            out.write("%s\n" % item)

    path = "../docs/calibration/"
    date = str(datetime.datetime.now())
    filename = email[0:5] + date + ".ods"
    file_path = path + filename
    doc.save(file_path)
    calibrate_insert(filename, file_path, date)
    doc.close()

    soffice.kill()

    print("File Saved")

