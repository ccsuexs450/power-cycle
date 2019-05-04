 
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from scipy.interpolate import spline
from scipy.interpolate import UnivariateSpline
from scipy import stats
from db_interaction import *


def draw_graph(datax, datay1, datay2, email):
    
    fig, ax1 = plt.subplots()
      
    x_sm  = np.array(datax)
    y1_sm = np.array(datay1)
    
    p = np.poly1d(np.polyfit(x_sm, y1_sm, 3))
    t = np.linspace(x_sm.min(), x_sm.max(), 100)
    
    color = 'k'
    ax1.set_xlim([50, x_sm.max()+20])
    ax1.set_ylim([0, y1_sm.max() + 200])
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
    ax2.set_xlim([50, x_sm.max() + 20])
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
