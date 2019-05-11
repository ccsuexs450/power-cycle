 
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from scipy.interpolate import spline
from scipy.interpolate import UnivariateSpline
from scipy import stats
from db_interaction import *


def draw_graph(datax, datay1, datay2, email):
    
    fig, ax1 = plt.subplots()
    
      
#    x_sm_size= np.array(datax)
#    y1_sm_size = np.array(datay1)

    x_sm = np.array(datax)
    y1_sm = np.array(datay1)
     
  #  x_sm_raw = np.array(datax)
  #  y1_sm_raw = np.array(datay1)
  #  mean = np.mean(y1_sm_raw, axis=0)
  #  sd = np.std(y1_sm_raw, axis=0)
  #  print(mean)
  #  print(sd)
  #  indices = [0,1,2,3,4,5,6,7,8.9]
  #  datay1 = list(datay1)
  #  remove_list = []
  #  index_list  = []
    #y1_sm = [x for ind, x in y1_sm_raw if not (x > mean + sd*.80)]
  #  y1_sm_x_sm = [(x, y) for x, y in zip(y1_sm_raw, x_sm_size) if not (x>mean+sd*.8)] 
  #  for idx, val in enumerate(datay1):
  #      if val > mean + sd*0.8:
  #          remove_list.append(val)
  #          index_list.append(idx)
    
  #  print(remove_list)
  #  a = set(datay1)
  #  b = set(remove_list)
  #  c = a - b
  #  y1_sm = list(c)
   
  #  print(y1_sm_x_sm)
   
  #  y1_sm, x_sm = zip(y1_sm_x_sm)      
   
    p = np.poly1d(np.polyfit(x_sm, y1_sm, 2))
    t = np.linspace(x_sm.min(), x_sm.max(), 100)
    
    color = 'k'
    ax1.set_xlim([50, x_sm.max() + 10])
    ax1.set_ylim([0, y1_sm.max() + 100])
    ax1.set_xlabel('Pedaling Rate(rpm)')
    ax1.set_ylabel('Power(watts)', color=color)
    ax1.plot(t, p(t),color=color, linewidth = 3)
    ax1.tick_params(axis='y', labelcolor=color)
    
    x2len = len(datax)
    y2len = len(datay2)

    x2_sm = np.array(datax[1:x2len -1])
    y2_sm = np.array(datay2[1:y2len-1])
    z = np.polyfit(x2_sm, y2_sm, 1)
    p = np.poly1d(z)
    
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    ax2.set_xlim([50, x_sm.max() + 10])
    ax2.set_ylim([0, y2_sm.max() + 10])
    color = 'tab:red'
    ax2.set_ylabel('Torque(Nm)', color=color)  # we already handled the x-label with ax1
    ax2.plot(x2_sm, p(x2_sm), '-',  color=color, linewidth = 3)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
  
    path = "../docs/graph/"
    date = datetime.now()
    f_date = date.strftime('%Y-%m-%d %H.%M.%S.%f')
    filename = email[0:5] +f_date + ".png"
    file_path = path + filename
    plt.savefig(file_path)
    graph_insert(email, filename, file_path, date)
    
    return file_path
