from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

import collections
import random
import time
import math
import numpy as np

def dataSimu():
    frequency = 0.5
    noise = random.normalvariate(0., 1.)
    new = []
    for i in range(5):
        new.append((2 * i + 1) * 10.*math.sin(time.time()*frequency*(2 * i + 1)*math.pi) + noise)
    return new

class DynamicPlotter():

    def __init__(self, chNum = 5, sampleinterval=0.1, timewindow=10., size=(1200,700)):
        # Data stuff
        self. numOfCh  = chNum
        self._interval = int(sampleinterval*1000)
        self._bufsize = int(timewindow/sampleinterval)
        self.databufferList = []
        self.databuffer = collections.deque([0.0]*self._bufsize, self._bufsize)
        self.x = np.linspace(timewindow, 0.0, self._bufsize)
        self.y = np.zeros(self._bufsize, dtype=np.float)
        # PyQtGraph stuff
        self.app = QtGui.QApplication([])
        self.plt = pg.plot(title='Dynamic Plotting with PyQtGraph')
        self.plt.resize(*size)
        self.plt.showGrid(x=True, y=True)
        self.plt.setLabel('left', 'amplitude', 'V')
        self.plt.setLabel('bottom', 'time', 's')
        # adding legend
        self.plt.addLegend()
        self.curves = []
        self.clrList= ['r', 'g', 'b', 'c', 'm', 'w']
        self.nameList = ['PD1', 'PD2', 'PD3', 'PD4', 'PD5']
        for i in range(self.numOfCh):
            self.curves.append(self.plt.plot(self.x, self.y, lw = 2, pen=self.clrList[i], name = self.nameList[i]))
            self.databufferList.append(self.databuffer)
        
        # QTimer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateplot)
        self.timer.start(self._interval)

    def getdata(self, datas):
        for i in range(self.numOfCh):
            curve = self.curves[i]
            self.databufferList[i].append(datas[i])

    def updateplot(self):
        
        for i in range(self.numOfCh):
            curve = self.curves[i]
            self.y = self.databufferList[i]
            curve.setData(self.x, self.y)
        self.app.processEvents()

    def run(self):
        self.app.exec_()

if __name__ == '__main__':

    m = DynamicPlotter(sampleinterval=0.5, timewindow=30.)
    m.run()

