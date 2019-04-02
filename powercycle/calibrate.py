import pyoo
import subprocess 
import os
from db_interaction import *

#soffice = subprocess.Popen(' '.join([
   # 'soffice',
   # '--accept="host=localhost,port=2002;urp;"',
   # '--norestore',
   # '--nologo',
  #  '--nodefault',
 #   '--headless'
#]))
#output = soffice.communicate()
#
#cmd = """soffice --accept="socket,host=localhost,port=2002;urp;" --norestore --nologo --nodefault --headless"""
#os.system(cmd) 

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
print("File Saved")
doc.close()

kill_cmd = "pkill soffice"
#subprocess.Popen(kill_cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)

