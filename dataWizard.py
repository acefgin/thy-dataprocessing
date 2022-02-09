import numpy as np
import os, csv, glob

import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

from stdBounding import *
from slidingWin import *
from stepsFilter import *
from zNormed import *

def results_processing(folderPath, filename):

    plt.style.use('seaborn-bright')

    plt.rc('axes', linewidth=2)
    font = {'weight' : 'bold',
    'size'   : 21}
    plt.rc('font', **font)

    x = []
    normedSgl = []
    smoothedSgl = []
    y1 = []
    y2 = []
    y3 = []
    y4 = []
    y5 = []
    idInfo = []
    ChResult = []
    OverallResult = ""

    with open(os.path.join(folderPath, filename),'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        idx = 0

        for row in plots:
            if idx == 1:
                idInfo.append([row[0], row[2]])
                OverallResult = row[4]
            if idx == 8:
                x = row[7:]
                x = [float(i)/1000/60 - 5 for i in x if i != '']
            if idx == 11:

                y1 = row[7:]
                ChResult.append(row[5])
                y1 = np.array([float(i) for i in y1 if i != ''])
                if len(y1) >= 9: smoothedSgl.append(smooth(y1))
                yNormed, PD1Scalar = zNormArr(y1)
                normedSgl.append(yNormed)
            if idx == 12:

                y2 = row[7:]
                ChResult.append(row[5])
                y2 = np.array([float(i) for i in y2 if i != ''])
                if len(y2) >= 9: smoothedSgl.append(smooth(y2))
                yNormed, PD2Scalar = zNormArr(y2)
                normedSgl.append(yNormed)
            if idx == 13:

                y3 = row[7:]
                ChResult.append(row[5])
                y3 = np.array([float(i) for i in y3 if i != ''])
                if len(y3) >= 9: smoothedSgl.append(smooth(y3))
                yNormed, PD3Scalar = zNormArr(y3)
                normedSgl.append(yNormed)
            if idx == 14:

                y4 = row[7:]
                ChResult.append(row[5])
                y4 = np.array([float(i) for i in y4 if i != ''])
                if len(y4) >= 9: smoothedSgl.append(smooth(y4))
                yNormed, PD4Scalar = zNormArr(y4)
                normedSgl.append(yNormed)
            if idx == 15:

                y5 = row[7:]
                ChResult.append(row[5])
                y5 = np.array([float(i) for i in y5 if i != ''])
                if len(y5) >= 9: smoothedSgl.append(smooth(y5))
                yNormed, PD5Scalar = zNormArr(y5)
                normedSgl.append(yNormed)
            
            idx += 1
    avgScalar = (PD1Scalar + PD2Scalar + PD3Scalar + PD4Scalar + PD5Scalar) / 5
    print("test scalar: " + str(round(avgScalar, 2)))
    for i in range(len(signalList)):
        signalList[i] = signalList[i] * avgScalar
    
    featList = np.zeros((5,4))
    #print(np.shape(signalList))

    if len(signalList) != 0:
        for i in range(5):
            _, diff, cp, stepWidth, avgRate= labelSteps(signalList[i])
            if diff == 0 and len(signalList[i]) >= 50:
                diff = round(consecutiveSum(np.diff(signalList[i]), 50), 1)
            featList[i] = [diff, cp, stepWidth, avgRate]
    return idInfo, OverallResult, featList

if __name__=='__main__':
    csvfoler = os.path.join(os.path.dirname(__file__), 'test_csv')
    filenames = sorted(glob.glob(os.path.join(csvfoler, '*.csv')))
    for filename in filenames:
        print(filename)
        results_processing(csvfoler, filename)
    
    cwd = os.path.dirname(__file__)

    reportcsvFile = "dataWizard_output"
	header = ["SampleID", "Barcode", "Result", "Well", "VolDiff", "Tq", "StepWidth", "AvgRate"]
	with open(reportcsvFile,'w', newline = '') as reportCsv:
		writer = csv.writer(reportCsv)
		writer.writerow(header)

		for filename in filenames:

			idInfo, overallRlt, featList = results_processing(csvfoler, filename)
			for i in range(5):
				
				data2Write = [idInfo[0][0], idInfo[0][1], overallRlt, str(i+1), str(featList[i][0]), \
					str(featList[i][1]), str(featList[i][2]), str(featList[i][3])]
				writer.writerow(data2Write)

		writer.writerow('\n')