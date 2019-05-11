import os, signal
import subprocess
from datetime import datetime
import time as t
import math
import pyoo
from db_interaction import *
from power_chart import *
lines = []

def power_sheet(path, email):

    
    soffice = subprocess.Popen('startLO')

    t.sleep(7)
    dt    = []

    desktop = pyoo.Desktop('localhost', 2002)
    doc = desktop.open_spreadsheet("../docs/templates/Power_template.ods")
    
    sum   = doc.sheets[0]
    power = doc.sheets[1]
    delta = doc.sheets[2]

    # comment this loop when sensor is plugged in
    with open("../data/sensordata/nickp2019-05-06 20.14.08.566792.txt", "r") as ins:
        for line in ins:
            line = line.rstrip('\n')
            lines.append(line)

        # get sensor values
#    with open(path, "r") as ins:
#        for line in ins:
#            line = line.rstrip('\n')
#            lines.append(line)


    print(lines[0:10])
    print(len(lines)) 
    power[1:496,0].values = lines
    
    lines.clear()
    with open("../docs/templates/delta_theta.txt", "r") as ins:
        for line in ins:
            line = line.rstrip('\n')
            dt.append(line)

    delta[1:16,1].values = dt

    # retrieve payload
    max_pow = round(power[20, 43].value)
    rpm_opt = round(power[20, 46].value)
    rpm_max = round(power[22, 46].value)
    
    # calculate fiber twitch
    twitch = (2.0833 * rpm_opt) - 198.458
    
    # graph data
    datax  = power[1:11,32].values
    datay1 = power[1:11,33].values
    datay2 = power[1:11,34].values
     
    graph_path = draw_graph(datax, datay1, datay2, email)

    # user search 
    profile = user_profile_search(email)
    print(profile)
    
    sum[1:10,7].values = profile
    
    path = "../docs/power/"
    date = datetime.now()
    f_date = date.strftime('%Y-%m-%d %H.%M.%S.%f')
    filename = email[0:5] + f_date + ".ods"
    file_path = path + filename
    doc.save(file_path)
    power_insert(email, filename, file_path, date)
    doc.close()
    
    payload = []

    payload.append(max_pow)
    payload.append(rpm_max)
    payload.append(rpm_opt)
    payload.append(twitch)
    payload.append(graph_path)

    soffice.kill()

    print("File Saved")
    
    return payload

#power_sheet(lines, "htazi@gmail.com")
