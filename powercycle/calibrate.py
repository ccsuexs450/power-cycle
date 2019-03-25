import pyoo
import subprocess 
import os

#soffice = subprocess.Popen(' '.join([
   # 'soffice',
   # '--accept="host=localhost,port=2002;urp;"',
   # '--norestore',
   # '--nologo',
  #  '--nodefault',
 #   '--headless'
#]))
#output = soffice.communicate()


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

for i in lines[0:10]:
    j =str(i+1)
    sheet[j,0].value = lines[i]

doc.save('calibrateTest.ods')
print("File Saved")
doc.close()

kill_cmd = "pkill soffice.bin"
#subprocess.Popen(kill_cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)

