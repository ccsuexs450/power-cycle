import time
import numpy as np
import matplotlib.pyplot as plt
# from scipy.interpolate import spline
# from scipy.interpolate import UnivariateSpline
from db_interaction import *


def draw_graph(datax, datay1, datay2, email):
    fig, ax1 = plt.subplots()

    x_sm = np.array(datax)
    y1_sm = np.array(datay1)

    p = np.poly1d(np.polyfit(x_sm, y1_sm, 3))
    t = np.linspace(0, 1, 200)
    # x_smooth = np.linspace(x_sm.min(), x_sm.max(), 100)
    # y_smooth = spline(datax, datay1, x_smooth)

    color = 'k'
    ax1.set_xlim([50, 190])
    ax1.set_ylim([0, 1400])
    ax1.set_xlabel('Pedaling Rate(rpm)')
    ax1.set_ylabel('Power(watts)', color=color)
    # ax1.plot(x_smooth, y_smooth, color=color)
    ax1.plot(x_sm, y1_sm, 'o', t, p(t), color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    x_sm = np.array(datax)
    y2_sm = np.array(datay2)

    p = np.poly1d(np.polyfit(x_sm, y2_sm, 3))
    t = np.linspace(0, 1, 200)
    # x_smooth = np.linspace(x_sm.min(), x_sm.max(), 200)
    # y2_smooth = spline(datax, datay2, x_smooth)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    ax2.set_xlim([50, 190])
    ax2.set_ylim([0, 140])
    color = 'tab:red'
    ax2.set_ylabel('Torque(Nm)', color=color)  # we already handled the x-label with ax1
    # ax2.plot(x_smooth, y2_smooth, color=color)
    ax2.plot(x_sm, y2_sm, 'o', t, p(t), color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    #    plt.show()

    path = "../docs/graph/"
    date = time.strftime("%Y%m%d-%H%M%S")
    filename = email[0:5] + date + ".png"
    file_path = path + filename
    plt.savefig(file_path)
    graph_insert(email, filename, file_path, date)
