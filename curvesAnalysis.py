from msilib import _Unspecified
from re import S
import re
import numpy as np
import os, csv, glob

import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
from zmq import THREAD_SCHED_POLICY_DFLT

from stdBounding import *
from slidingWin import *
from stepsFilter import *
from zNormed import *

def results_processing(folderPath, filename):

    x = []
    smoothedSgl = []
    y1 = []
    y2 = []
    y3 = []
    y4 = []
    y5 = []
    idInfo = []
    ChResult = []
    OverallResult = ""
    thList = [40, 40, 40, 60, 60]

    with open(os.path.join(folderPath, filename),'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        idx = 0

        for row in plots:
            if idx == 1:
                idInfo.append([row[0], row[2]])
            if idx == 8:
                x = row[7:]
                x = [float(i)/1000/60 - 5 for i in x if i != '']
            if idx == 11:

                y1 = row[7:]
                
                y1 = np.array([float(i) for i in y1 if i != ''])
                if len(y1) >= 9: smoothedSgl.append(smooth(y1))

            if idx == 12:

                y2 = row[7:]
                
                y2 = np.array([float(i) for i in y2 if i != ''])
                if len(y2) >= 9: smoothedSgl.append(smooth(y2))

            if idx == 13:

                y3 = row[7:]
                
                y3 = np.array([float(i) for i in y3 if i != ''])
                if len(y3) >= 9: smoothedSgl.append(smooth(y3))

            if idx == 14:

                y4 = row[7:]
                
                y4 = np.array([float(i) for i in y4 if i != ''])
                if len(y4) >= 9: smoothedSgl.append(smooth(y4))

            if idx == 15:

                y5 = row[7:]
                
                y5 = np.array([float(i) for i in y5 if i != ''])
                if len(y5) >= 9: smoothedSgl.append(smooth(y5))

            idx += 1
    
    rawDatafeatList = np.zeros((5,4))
    
    if len(smoothedSgl) != 0:
        for i in range(5):
            _, diff, cp, stepWidth, avgRate= labelSteps(smoothedSgl[i], startPt = 75, rateTh = 0.3, width_LB = 12, avgRate_LB = 0.84)

            ChResult.append(diff >= thList [i])
            if diff == 0 and len(smoothedSgl[i]) >= 50:
                diff = round(consecutiveSum(np.diff(smoothedSgl[i]), 50), 1)
            rawDatafeatList[i] = [diff, cp, stepWidth, avgRate]    
    
    if ChResult[0] and (ChResult[1] or ChResult[2] or ChResult[3] or ChResult[4]):
        OverallResult = "Positive"
    elif ChResult[0] and ((ChResult[1] == 0) and (ChResult[2] == 0) and (ChResult[3] == 0) and (ChResult[4] == 0)):
        OverallResult = "Negative"
    elif ChResult[0] ==0:
        OverallResult = "Invalid"

    return idInfo, ChResult, OverallResult, rawDatafeatList, thList, [75, 0.3, 12, 0.84]


def testIDLkUp(filename):
    
    LkUp = {}
    with open(filename,'r') as csvfile:
        items = csv.reader(csvfile, delimiter=',')
        idx = 0
        for row in items:
            if idx == 0:
                idx += 1
                continue
            #print(row)
            LkUp[row[0]] = [row[1], row[2], row[3], row[4], row[5]]
    return LkUp


if __name__=='__main__':
    csvfoler = os.path.join(os.path.dirname(__file__), 'dataPool')
    filenames = sorted(glob.glob(os.path.join(csvfoler, '*.csv')))
    testIDLkUpFile = "testID_lookup.csv"
    testIDTb = testIDLkUp(testIDLkUpFile)
    reportcsvFile = "curveAnalysis_output.csv"
	
    with open(reportcsvFile,'w', newline = '') as reportCsv:
        writer = csv.writer(reportCsv)
        header = ["TestID#", "KitID", "InputGp", "Input[C]", "OutputRt", "Exp. Result", \
        "ChRt-1", "VolDiff-1", "StepWidth-1", "AvgRate-1", "Threshold-1", \
        "ChRt-2", "VolDiff-2", "StepWidth-2", "AvgRate-2", "Threshold-2", \
        "ChRt-3", "VolDiff-3", "StepWidth-3", "AvgRate-3", "Threshold-3", \
        "ChRt-4", "VolDiff-4", "StepWidth-4", "AvgRate-4", "Threshold-4", \
        "ChRt-5", "VolDiff-5", "StepWidth-5", "AvgRate-5", "Threshold-5",]
        writer.writerow(header)
        idx = 1
        TP = 0
        TN = 0
        FP = 0
        FN = 0
        invalidNum = 0
        unspecified  = 0

        for filename in filenames:
            testID = os.path.splitext(os.path.basename(filename))[0]
            print(str(idx) + ":" + testID)
            idx += 1
            testInfo = testIDTb[testID]
            inputGInfo = testInfo[1]
            inputCInfo = testInfo[2]

            idInfo, chResult, overallRlt, rawDatafeatList, thList, [startPt, rateTh, width_LB, avgRate_LB] = results_processing(csvfoler, filename)

            if overallRlt == "Positive":
                if "Positive" in inputGInfo:
                    TP += 1
                elif "Negative" in inputGInfo:
                    FP += 1
                else:
                    unspecified += 1
            elif overallRlt == "Negative":
                if "Positive" in inputGInfo:
                    FN += 1
                elif "Negative" in inputGInfo:
                    TN += 1
                else:
                    unspecified += 1
            else:
                invalidNum += 1
                if not ("Positive" in testInfo[1] or "Negative" in testInfo[1]):
                    unspecified += 1

            testInfo = [testID, testInfo[0], inputGInfo, inputCInfo, overallRlt, testInfo[-1]]
            for i in range(5):
                
                data2Write = [chResult[i], str(rawDatafeatList[i][0]), str(rawDatafeatList[i][2]), \
					str(rawDatafeatList[i][3]), str(thList[i])]
                testInfo += data2Write
            writer.writerow(testInfo)

        writer.writerow('\n')

        print("Result analysis with raw data")
        print("ADF parameter-startPt: {}, rateTh: {}, widthLB: {}, avgRateLB: {}".format(startPt, rateTh, width_LB, avgRate_LB))
        msg2print = "Specificed test num: {}, invalid test num: {}".format(idx - unspecified - 1, invalidNum)
        print(msg2print)
        msg2print = "TN: {} , FP: {}".format(TN, FP)
        print(msg2print)
        msg2print = "FN: {} , TP: {}".format(FN, TP)
        print(msg2print)