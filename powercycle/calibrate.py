import os
import subprocess
import datetime
import pyoo
from db_interaction import *
import time as t

def calibrate_sheet(path):
    
    # call the bash script "startLO" which opens the libreoffice instance
    soffice = subprocess.Popen('startLO')
    # sleep for 7 seconds, wait for libreoffice to start completely
    t.sleep(7)
    
    lines = []
    
    desktop = pyoo.Desktop('localhost', 2002)
    doc = desktop.open_spreadsheet("../docs/templates/Calibrate_blank.ods")

    sheet = doc.sheets[0]
    
    # open the calibration text file to proccess
    with open(path, "r") as ins:
        for line in ins:
            line = line.rstrip('\n')
            lines.append(line)

    # the code below processes the raw sensor data and creates a new list
    # that starts after the first double. 
    lines = list(map(int, lines))
    
    # this loop locates the first double in the original list and creates
    # a new list with the values after the double
    for idx, val in enumerate(lines):
        if(idx > 0):
            double = lines[idx]/lines[idx-1]
            if double > 1.8:
               newlines =  lines[idx + 1 : idx + 796]
               break
    
    # insert the new list into the calibrate spreadsheet
    sheet[1:796,0].values = newlines
    
    # retieve the the delta theta values from the spreadsheet
    delta_theta = sheet[1:16,10].values
    
    # update the delta _theta text file with the new delta theta values
    with open("../docs/templates/delta_theta.txt", "w") as out:
        for item in delta_theta:
            out.write("%s\n" % item)
    
    # create file, insert into db, and save
    path = "../docs/calibration/"
    date = datetime.now()
    f_date = date.strftime('%Y-%m-%d %H.%M.%S.%f')
    filename = "calibrate" + f_date + ".ods"
    file_path = path + filename
    doc.save(file_path)
    calibrate_insert(filename, file_path, date)
    doc.close()
    
    # clean up
    lines.clear()
    newlines.clear()
    soffice.kill()

    print("File Saved")
    
    # returns expected value to GUI
    return 1
