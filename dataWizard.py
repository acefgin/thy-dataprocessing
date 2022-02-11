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

def results_processing(folderPath, filename, resultAnalysisWithNormedData = False):

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
                yNormed, PD1Scalar = zNormArr(y1)
                normedSgl.append(yNormed)
            if idx == 12:

                y2 = row[7:]
                
                y2 = np.array([float(i) for i in y2 if i != ''])
                if len(y2) >= 9: smoothedSgl.append(smooth(y2))
                yNormed, PD2Scalar = zNormArr(y2)
                normedSgl.append(yNormed)
            if idx == 13:

                y3 = row[7:]
                
                y3 = np.array([float(i) for i in y3 if i != ''])
                if len(y3) >= 9: smoothedSgl.append(smooth(y3))
                yNormed, PD3Scalar = zNormArr(y3)
                normedSgl.append(yNormed)
            if idx == 14:

                y4 = row[7:]
                
                y4 = np.array([float(i) for i in y4 if i != ''])
                if len(y4) >= 9: smoothedSgl.append(smooth(y4))
                yNormed, PD4Scalar = zNormArr(y4)
                normedSgl.append(yNormed)
            if idx == 15:

                y5 = row[7:]
                
                y5 = np.array([float(i) for i in y5 if i != ''])
                if len(y5) >= 9: smoothedSgl.append(smooth(y5))
                yNormed, PD5Scalar = zNormArr(y5)
                normedSgl.append(yNormed)
            
            idx += 1
    avgScalar = (PD1Scalar + PD2Scalar + PD3Scalar + PD4Scalar + PD5Scalar) / 5
    sScore = [PD1Scalar, PD2Scalar, PD3Scalar, PD4Scalar, PD5Scalar]
    print("test scalar: " + str(round(avgScalar, 2)))
    for i in range(len(normedSgl)):
        normedSgl[i] = normedSgl[i] * avgScalar
    
    rawDatafeatList = np.zeros((5,4))
    normedDatafeatList = np.zeros((5,4))

    if len(normedSgl) != 0:
        for i in range(5):
            _, diff, cp, stepWidth, avgRate= labelSteps(normedSgl[i])
            if resultAnalysisWithNormedData:
                ChResult.append(diff >= thList [i])
            if diff == 0 and len(normedSgl[i]) >= 50:
                diff = round(consecutiveSum(np.diff(normedSgl[i]), 50), 1)
            normedDatafeatList[i] = [diff, cp, stepWidth, avgRate]
    
    if len(smoothedSgl) != 0:
        for i in range(5):
            _, diff, cp, stepWidth, avgRate= labelSteps(smoothedSgl[i])
            if not resultAnalysisWithNormedData:
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

    return idInfo, ChResult, OverallResult, rawDatafeatList, normedDatafeatList, sScore, thList


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
            LkUp[row[0]] = [row[1], row[2]]
    return LkUp


if __name__=='__main__':
    csvfoler = os.path.join(os.path.dirname(__file__), 'dataPool')
    filenames = sorted(glob.glob(os.path.join(csvfoler, '*.csv')))
    testIDLkUpFile = "testID_lookup.csv"
    testIDTb = testIDLkUp(testIDLkUpFile)
    reportcsvFile = "dataWizard_output.csv"
    resultAnalysisWithNormedData = False
	
    with open(reportcsvFile,'w', newline = '') as reportCsv:
        writer = csv.writer(reportCsv)
        header = ["TestID#", "KitID", "InputRt", "SampleType", "Concentration", "OutputRt", \
        "ChRt-1", "VolDiff-1", "Tq-1", "StepWidth-1", "AvgRate-1", "SentivityScore-1", "Threshold-1", \
        "ChRt-2", "VolDiff-2", "Tq-2", "StepWidth-2", "AvgRate-2", "SentivityScore-2", "Threshold-2", \
        "ChRt-3", "VolDiff-3", "Tq-3", "StepWidth-3", "AvgRate-3", "SentivityScore-3", "Threshold-3", \
        "ChRt-4", "VolDiff-4", "Tq-4", "StepWidth-4", "AvgRate-4", "SentivityScore-4", "Threshold-4", \
        "ChRt-5", "VolDiff-5", "Tq-5", "StepWidth-5", "AvgRate-5", "SentivityScore-5", "Threshold-5",]
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
            inputInfo = testInfo[1]
            if "-" in inputInfo:
                inputInfoList = inputInfo.split(" - ")
            else:
                inputInfoList = [inputInfo, ""]
            sampleInfoString = ""
            sampleInfo = ["", ""]
            
            sampleInfoString = inputInfoList[1]
            print(any(map(str.isdigit,sampleInfoString)))
            if any(map(str.isdigit, sampleInfoString)):
                if sampleInfoString[-1] == "K":
                    if "." in sampleInfoString:
                        pattern = re.compile("([a-zA-Z]+)(\d+\.\d+[a-zA-Z])")
                    else:
                        pattern = re.compile("([a-zA-Z]+)(\d+[a-zA-Z])")
                else:
                    if "." in sampleInfoString:
                        pattern = re.compile("([a-zA-Z]+)(\d+\.\d+)")
                    else:
                        pattern = re.compile("([a-zA-Z]+)(\d+)")
                sampleInfo = pattern.match(sampleInfoString).groups()
            else:
                sampleInfo = [sampleInfoString, ""]

            idInfo, chResult, overallRlt, rawDatafeatList, normedDatafeatList, sScore, thList = results_processing(csvfoler, filename, resultAnalysisWithNormedData)

            if overallRlt == "Positive":
                if "Positive" in testInfo[1]:
                    TP += 1
                elif "Negative" in testInfo[1]:
                    FP += 1
                else:
                    unspecified += 1
            elif overallRlt == "Negative":
                if "Positive" in testInfo[1]:
                    FN += 1
                elif "Negative" in testInfo[1]:
                    TN += 1
                else:
                    unspecified += 1
            else:
                invalidNum += 1
                if not ("Positive" in testInfo[1] or "Negative" in testInfo[1]):
                    unspecified += 1

            testInfo = [testID, testInfo[0], inputInfoList[0], sampleInfo[0], sampleInfo[1], overallRlt]
            #writer.writerow(testInfo)
            #header = ["Well", "ChRt", "VolDiff", "Tq", "StepWidth", "AvgRate", "SentivityScore", "Threshold"]
            #writer.writerow(header)
            for i in range(5):
                
                data2Write = [chResult[i], str(rawDatafeatList[i][0]), str(normedDatafeatList[i][1]), str(rawDatafeatList[i][2]), \
					str(rawDatafeatList[i][3]), str(round(sScore[i], 1)), str(thList[i])]
                testInfo += data2Write
            writer.writerow(testInfo)

        writer.writerow('\n')
        if resultAnalysisWithNormedData:
            print("Result analysis with normalized data")
        else:
            print("Result analysis with raw data")
        msg2print = "Specificed test num: {}, invalid test num: {}".format(idx - unspecified - 1, invalidNum)
        print(msg2print)
        msg2print = "TN: {} , FP: {}".format(TN, FP)
        print(msg2print)
        msg2print = "FN: {} , TP: {}".format(FN, TP)
        print(msg2print)