import numpy as np
import os, csv, glob

import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

def zNormArr(arr):
    baseline = np.mean(arr[30:60])
    sensorStd = np.std(arr[:30]) 
    return (arr - baseline) / sensorStd, sensorStd

def results_processing(folderPath, filename):

    plt.style.use('seaborn-bright')

    plt.rc('axes', linewidth=2)
    font = {'weight' : 'bold',
    'size'   : 21}
    plt.rc('font', **font)

    x = []
    signalList = []
    y1 = []
    y2 = []
    y3 = []
    y4 = []
    y5 = []
    OverallResult = ""

    with open(os.path.join(folderPath, filename),'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        idx = 0

        for row in plots:
            if idx == 1:
                OverallResult = row[4]
            if idx == 8:
                x = row[7:]
                x = [float(i)/1000/60 - 5 for i in x]
            if idx == 11:

                y1 = row[7:]
                y1 = np.array([float(i) for i in y1])
                if len(y1) >= 9: signalList.append(zNormArr(y1))
            if idx == 12:

                y2 = row[7:]
                y2 = np.array([float(i) for i in y2])
                if len(y2) >= 9: signalList.append(zNormArr(y2))
            if idx == 13:

                y3 = row[7:]
                y3 = np.array([float(i) for i in y3])
                if len(y3) >= 9: signalList.append(zNormArr(y3))
            if idx == 14:

                y4 = row[7:]
                y4 = np.array([float(i) for i in y4])
                if len(y4) >= 9: signalList.append(zNormArr(y4))
            if idx == 15:

                y5 = row[7:]
                y5 = np.array([float(i) for i in y5])
                if len(y5) >= 9: signalList.append(zNormArr(y5))

            idx += 1

    plt.figure(num=None, figsize=(24, 6), dpi=40)
    ax = plt.subplot(111)
    ax.plot(x, signalList[0], color = 'r', linewidth=2, label='PC')
    ax.plot(x, signalList[1], color = '#35ff35', linewidth=2, label='N1')
    ax.plot(x, signalList[2], color = '#3535ff', linewidth=2, label='N2')
    ax.plot(x, signalList[3], color = '#35ffff', linewidth=2, label='M1')
    ax.plot(x, signalList[4], color = '#ff35ff', linewidth=2, label='M2')
    plt.xlabel('Time (mins)', fontsize = 19, fontweight = 'bold')
    plt.ylabel('Signal (mvs)', fontsize = 19, fontweight = 'bold')
    plt.title('{}_{}'.format(os.path.splitext(os.path.split(filename)[1])[0], OverallResult), fontsize = 20, fontweight = 'bold')
    box = ax.get_position()
    ax.set_position([box.x0*0.35, box.y0, box.width * 1.2, box.height])
    ax.grid(linestyle = '-.')
    ax.legend(loc='lower right',  ncol=5)
    """"
    # Print diffs data in plot
    diffs_text = 'Diffs(mvs) = PC:{}, N1:{}, N2:{}, M1:{}, M2:{}'.format\
    (featList[0][0], featList[1][0], featList[2][0], featList[3][0], featList[4][0])
    Tqs_text = 'Tqs(mins) = PC:{}, N1:{}, N2:{}, M1:{}, M2:{}'.format\
    (featList[0][1], featList[1][1], featList[2][1], featList[3][1], featList[4][1])
    plt.text(-2.5, 440, diffs_text)
    plt.text(-2.5, 400, Tqs_text)
    """

    #ax.legend(loc='upper left')
    #plt.axis([-5,30,0,1])
    ax.xaxis.set_major_locator(MultipleLocator(2))
    ax.xaxis.set_major_formatter('{x:.0f}')
    ax.xaxis.set_minor_locator(MultipleLocator(1))

    #ax.yaxis.set_major_locator(MultipleLocator(40))
    #ax.yaxis.set_major_formatter('{x:.0f}')
    #ax.yaxis.set_minor_locator(MultipleLocator(20))


    #plt.tight_layout()
    plt.savefig(os.path.join(folderPath, '{}-{}.png'.format(os.path.splitext(os.path.split(filename)[1])[0], OverallResult)))


if __name__=='__main__':
    csvfoler = os.path.join(os.path.dirname(__file__), 'test_csv')
    filenames = sorted(glob.glob(os.path.join(csvfoler, '*.csv')))
    for filename in filenames:
        results_processing(csvfoler, filename)