import numpy as np
import os, csv, glob

import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

from zNormed import *

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
                x = [float(i)/1000/60 - 5 for i in x if i != '']
            if idx == 11:

                y1 = row[7:]
                y1 = np.array([float(i) for i in y1 if i != ''])
                yNormed, PD1Scalar = zNormArr(y1)
                signalList.append(yNormed)
            if idx == 12:

                y2 = row[7:]
                y2 = np.array([float(i) for i in y2 if i != ''])
                yNormed, PD2Scalar = zNormArr(y2)
                signalList.append(yNormed)
            if idx == 13:

                y3 = row[7:]
                y3 = np.array([float(i) for i in y3 if i != ''])
                yNormed, PD3Scalar = zNormArr(y3)
                signalList.append(yNormed)
            if idx == 14:

                y4 = row[7:]
                y4 = np.array([float(i) for i in y4 if i != ''])
                yNormed, PD4Scalar = zNormArr(y4)
                signalList.append(yNormed)
            if idx == 15:

                y5 = row[7:]
                y5 = np.array([float(i) for i in y5 if i != ''])
                yNormed, PD5Scalar = zNormArr(y5)
                signalList.append(yNormed)
            
            idx += 1
    avgScalar = (PD1Scalar + PD2Scalar + PD3Scalar + PD4Scalar + PD5Scalar) / 5
    print("\u03C3 1: {}, \u03C3 2: {}, \u03C3 3: {}, \u03C3 4:  {}, \u03C3 5:{}" \
        .format(PD1Scalar, PD2Scalar, PD3Scalar, PD4Scalar, PD5Scalar))
    for i in range(len(signalList)):
        signalList[i] = signalList[i] * avgScalar

    plt.figure(num=None, figsize=(24, 12), dpi=60)
    ax = plt.subplot(311)
    ax.plot(x, signalList[0], color = 'r', linewidth=2, label='PC')
    ax.plot(x, signalList[1], color = '#35ff35', linewidth=2, label='N1')
    ax.plot(x, signalList[2], color = '#3535ff', linewidth=2, label='N2')
    ax.plot(x, signalList[3], color = '#35ffff', linewidth=2, label='M1')
    ax.plot(x, signalList[4], color = '#ff35ff', linewidth=2, label='M2')
    plt.xlabel('Time (mins)', fontsize = 19, fontweight = 'bold')
    plt.ylabel('Normalized Signal', fontsize = 19, fontweight = 'bold')
    plt.title('{}_{}'.format(os.path.splitext(os.path.split(filename)[1])[0], OverallResult), fontsize = 20, fontweight = 'bold')
    box = ax.get_position()
    ax.set_position([box.x0*0.35, box.y0, box.width * 1.2, box.height])
    ax.grid(linestyle = '-.')
    ax.legend(loc='upper right',  ncol=5)

    bx = plt.subplot(312)
    bx.plot(x[:-1], np.diff(signalList[0]), color = 'r', linewidth=2, label='PC')
    bx.plot(x[:-1], np.diff(signalList[1]), color = '#35ff35', linewidth=2, label='N1')
    bx.plot(x[:-1], np.diff(signalList[2]), color = '#3535ff', linewidth=2, label='N2')
    bx.plot(x[:-1], np.diff(signalList[3]), color = '#35ffff', linewidth=2, label='M1')
    bx.plot(x[:-1], np.diff(signalList[4]), color = '#ff35ff', linewidth=2, label='M2')
    plt.xlabel('Time (mins)', fontsize = 19, fontweight = 'bold')
    plt.ylabel('Diff', fontsize = 19, fontweight = 'bold')
    #plt.title('{}_{}'.format(os.path.splitext(os.path.split(filename)[1])[0], OverallResult), fontsize = 20, fontweight = 'bold')
    box = bx.get_position()
    bx.set_position([box.x0*0.35, box.y0, box.width * 1.2, box.height])
    bx.grid(linestyle = '-.')
    bx.legend(loc='upper right',  ncol=5)

    cx = plt.subplot(313)
    cx.plot(x[:-2], np.diff(np.diff(signalList[0])), color = 'r', linewidth=2, label='PC')
    cx.plot(x[:-2], np.diff(np.diff(signalList[1])), color = '#35ff35', linewidth=2, label='N1')
    cx.plot(x[:-2], np.diff(np.diff(signalList[2])), color = '#3535ff', linewidth=2, label='N2')
    cx.plot(x[:-2], np.diff(np.diff(signalList[3])), color = '#35ffff', linewidth=2, label='M1')
    cx.plot(x[:-2], np.diff(np.diff(signalList[4])), color = '#ff35ff', linewidth=2, label='M2')
    plt.xlabel('Time (mins)', fontsize = 19, fontweight = 'bold')
    plt.ylabel('Diff^2', fontsize = 19, fontweight = 'bold')
    #plt.title('{}_{}'.format(os.path.splitext(os.path.split(filename)[1])[0], OverallResult), fontsize = 20, fontweight = 'bold')
    box = cx.get_position()
    cx.set_position([box.x0*0.35, box.y0, box.width * 1.2, box.height])
    cx.grid(linestyle = '-.')
    cx.legend(loc='upper right',  ncol=5)

    cx.set_ylim([-1.5, 1.5])

    #plt.tight_layout()
    plt.savefig(os.path.join(folderPath, '{}-{}_diff.png'.format(os.path.splitext(os.path.split(filename)[1])[0], OverallResult)))

if __name__=='__main__':
    csvfoler = os.path.join(os.path.dirname(__file__), 'test_csv')
    filenames = sorted(glob.glob(os.path.join(csvfoler, '*.csv')))
    for filename in filenames:
        print(os.path.splitext(os.path.basename(filename))[0])
        results_processing(csvfoler, filename)