import numpy as np
import os, csv, glob

from stepsFilter import *

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
                if len(y1) >= 9: smoothedSgl.append(y1)

            if idx == 12:

                y2 = row[7:]
                
                y2 = np.array([float(i) for i in y2 if i != ''])
                if len(y2) >= 9: smoothedSgl.append(y2)

            if idx == 13:

                y3 = row[7:]
                
                y3 = np.array([float(i) for i in y3 if i != ''])
                if len(y3) >= 9: smoothedSgl.append(y3)

            if idx == 14:

                y4 = row[7:]
                
                y4 = np.array([float(i) for i in y4 if i != ''])
                if len(y4) >= 9: smoothedSgl.append(y4)

            if idx == 15:

                y5 = row[7:]
                
                y5 = np.array([float(i) for i in y5 if i != ''])
                if len(y5) >= 9: smoothedSgl.append(y5)

            idx += 1

    if len(smoothedSgl) != 0:
        for i in range(5):
            _, diff, cp, stepWidth, avgRate= labelSteps(smoothedSgl[i])
            ChResult.append(diff >= thList [i])
    
    return ChResult, smoothedSgl


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
    #testIDLkUpFile = "testID_lookup.csv"
    #estIDTb = testIDLkUp(testIDLkUpFile)
    reportcsvFile = "testDataset.tsv"
	
    with open(reportcsvFile,'w', newline = '') as reportCsv:
        writer = csv.writer(reportCsv, delimiter='\t' )
        idx = 1

        for filename in filenames:
            testID = os.path.splitext(os.path.basename(filename))[0]
            print(str(idx) + ":" + testID)
            idx += 1
            '''testInfo = testIDTb[testID]
            inputGInfo = testInfo[1]
            inputCInfo = testInfo[2]'''

            ChResult, smoothedSgl = results_processing(csvfoler, filename)
            if len(smoothedSgl[0]) < 189:
                continue


            for i in range(5):
                
                data2write = np.insert(smoothedSgl[i][:189], 0, int(ChResult[i]))
                writer.writerow(data2write)
        

