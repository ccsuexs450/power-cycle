import os, signal
import subprocess
import time
import pyoo
from db_interaction import *

def power_sheet(lines, email):

    soffice = subprocess.Popen('startLO')

    time.sleep(3)

    lines = []
    dt    = []

    desktop = pyoo.Desktop('localhost', 2002)
    doc = desktop.open_spreadsheet("../docs/templates/Power_blank.ods")
    
    sum   = doc.sheets[0]
    power = doc.sheets[1]
    delta = doc.sheets[2]

    #with open("../data/sensordata/power.txt", "r") as ins:
    #    for line in ins:
    #        line = line.rstrip('\n')
    #        lines.append(line)

    print(lines[0:10])
 
    #power[1:496,0].values = lines
    power[1:30,0].values = lines


    with open("../docs/templates/delta_theta.txt", "r") as ins:
        for line in ins:
            line = line.rstrip('\n')
            dt.append(line)

    delta[1:16,1].values = dt
    
    # user search 
    profile = user_profile_search(email)
    print(profile)
    
    sum[1:9,7].values = profile
    
    path = "../docs/power/"
    date = time.strftime("%Y%m%d-%H%M%S")
    filename = email[0:5] + date + ".ods"
    file_path = path + filename
    doc.save(file_path)
    power_insert(email, filename, file_path, date)
    doc.close()

    soffice.kill()

    print("File Saved")

power_sheet("htazi@gmail.com")
