import os, csv, glob
import time, datetime

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

from slidingWin import *
from stepsFilter import *

def csvPlotter(folderPath, filename):

	plt.style.use('seaborn-bright')

	plt.rc('axes', linewidth=2)
	font = {'weight' : 'bold',
	'size'   : 21}
	plt.rc('font', **font)

	x = []
	y1 = []
	y2 = []
	y3 = []
	y4 = []
	y5 = []

	rlt = []
	OverallResult = []
	ChResult = []

	with open(os.path.join(folderPath, filename),'r') as csvfile:
		plots = csv.reader(csvfile, delimiter=',')
		idx = 0

		for row in plots:
			if idx == 1:
				OverallResult.append(row[4])
			if idx == 8:
				x = row[7:]
				x = [float(i)/1000/60 - 5 for i in x]
			if idx == 11:
				ChResult.append(row[5])
				y1 = row[7:]
				rlt.append(row[6])
				y1 = np.array([float(i) for i in y1])
				if len(y1) >= 9: y1 = smooth(y1)
			if idx == 12:
				ChResult.append(row[5])
				y2 = row[7:]
				rlt.append(row[6])
				y2 = np.array([float(i) for i in y2])
				if len(y2) >= 9: y2 = smooth(y2)
			if idx == 13:
				ChResult.append(row[5])
				y3 = row[7:]
				rlt.append(row[6])
				y3 = np.array([float(i) for i in y3])
				if len(y3) >= 9: y3 = smooth(y3)
			if idx == 14:
				ChResult.append(row[5])
				y4 = row[7:]
				rlt.append(row[6])
				y4 = np.array([float(i) for i in y4])
				if len(y4) >= 9: y4 = smooth(y4)
			if idx == 15:
				ChResult.append(row[5])
				y5 = row[7:]
				rlt.append(row[6])
				y5 = np.array([float(i) for i in y5])
				if len(y5) >= 9: y5 = smooth(y5)

			idx += 1

	y1_steps, y1_Diff, y1_cp = labelSteps(y1)
	if y1_Diff == 0:
		if len(y1) >= 50:
			y1_Diff = round(consecutiveSum(np.diff(y1), 50), 1)
	y2_steps, y2_Diff, y2_cp = labelSteps(y2)
	if y2_Diff == 0:
		if len(y2) >= 50:
			y2_Diff = round(consecutiveSum(np.diff(y2), 50), 1)
	y3_steps, y3_Diff, y3_cp = labelSteps(y3)
	if y3_Diff == 0:
		if len(y3) >= 50:
			y3_Diff = round(consecutiveSum(np.diff(y3), 50), 1)
	y4_steps, y4_Diff, y4_cp = labelSteps(y4)
	if y4_Diff == 0:
		if len(y4) >= 50:
			y4_Diff = round(consecutiveSum(np.diff(y4), 50), 1)
	y5_steps, y5_Diff, y5_cp = labelSteps(y5)
	if y5_Diff == 0:
		if len(y5) >= 50:
			y5_Diff = round(consecutiveSum(np.diff(y5), 50), 1)

	plt.figure(num=None, figsize=(24, 6), dpi=40)
	ax = plt.subplot(111)
	ax.plot(x, y1[4:-5], color = 'r', linewidth=2, label='PC')
	ax.plot(x, y2[4:-5], color = '#35ff35', linewidth=2, label='N1')
	ax.plot(x, y3[4:-5], color = '#3535ff', linewidth=2, label='N2')
	ax.plot(x, y4[4:-5], color = '#35ffff', linewidth=2, label='M1')
	ax.plot(x, y5[4:-5], color = '#ff35ff', linewidth=2, label='M2')
	plt.xlabel('Time (mins)', fontsize = 19, fontweight = 'bold')
	plt.ylabel('Signal (mvs)', fontsize = 19, fontweight = 'bold')
	plt.title('{}_{}'.format(os.path.splitext(os.path.split(filename)[1])[0], OverallResult[0]), fontsize = 20, fontweight = 'bold')
	box = ax.get_position()
	ax.set_position([box.x0*0.35, box.y0, box.width * 1.2, box.height])
	ax.grid(linestyle = '-.')
	ax.legend(loc='lower right',  ncol=5)
	# Print diffs data in plot
	diffs_text = 'Diffs(mvs) = PC:{}, N1:{}, N2:{}, M1:{}, M2:{}'.format\
	(y1_Diff, y2_Diff, y3_Diff, y4_Diff, y5_Diff)
	Tqs_text = 'Tqs(mins) = PC:{}, N1:{}, N2:{}, M1:{}, M2:{}'.format\
	(y1_cp, y2_cp, y3_cp, y4_cp, y5_cp)
	plt.text(-2.5, 440, diffs_text)
	plt.text(-2.5, 400, Tqs_text)

	#ax.legend(loc='upper left')
	plt.axis([-5,30,40,480])
	ax.xaxis.set_major_locator(MultipleLocator(2))
	ax.xaxis.set_major_formatter('{x:.0f}')
	ax.xaxis.set_minor_locator(MultipleLocator(1))

	ax.yaxis.set_major_locator(MultipleLocator(40))
	ax.yaxis.set_major_formatter('{x:.0f}')
	ax.yaxis.set_minor_locator(MultipleLocator(20))

	"""
	#Print Tp, Beta, R^2 in plot
	Tqs = []
	Betas = []
	R2s = []
	idx = 0
	fluoReads = [y1, y2, y3, y4, y5]
	for fluoRead in fluoReads:
		if ChResult[idx] != "Amplified":
			idx += 1
			Tqs.append(0)
			Betas.append(0)
			R2s.append(0)
			continue
		Tq, Beta, R2 = cp_fit(x, fluoRead)
		Tqs.append(Tq)
		Betas.append(Beta)
		R2s.append(R2)
		idx += 1

	Tq_text = 'Tqs = PC:{}, N1:{}, N2:{}, M1:{}, M2:{}'.format\
	(Tqs[0], Tqs[1], Tqs[2], Tqs[3], Tqs[4])

	plt.text(-2.5, 280, Tq_text)

	Beta_text = 'Betas = PC:{}, N1:{}, N2:{}, M1:{}, M2:{}'.format\
	(Betas[0], Betas[1], Betas[2], Betas[3], Betas[4])

	plt.text(-2.5, 310, Beta_text)

	R2_text = 'R2s = PC:{}, N1:{}, N2:{}, M1:{}, M2:{}'.format\
	(R2s[0], R2s[1], R2s[2], R2s[3], R2s[4])

	plt.text(-2.5, 340, R2_text)

	"""

	#plt.tight_layout()
	plt.savefig(os.path.join(folderPath, '{}_{}.png'.format(os.path.splitext(os.path.split(filename)[1])[0], OverallResult[0])))

def fileSplitter(multitestPath, slgtestPath, filename, devicePrefix, savePath):
    headers = []
    dateTimes = []
    lysisData = []
    detectData = []

    with open(os.path.join(multitestPath, filename),'r') as multiTests:
        rows = csv.reader(multiTests, delimiter=',')
        status = 0
        invalidSet = set()

        for row in rows:

            if len(row) == 0:
                status += 1
            elif row[0] == 'SampleId':
                headers.append(row)
                continue
            elif status == 0:
                if row[4] == 'Unspecified':
                    invalidSet.add(row[1])
                    continue
                dateTimes.append(row)
            elif status == 1:
                if row[1] in invalidSet:
                    continue
                lysisData.append(row)
            elif status == 2:
                if row[1] in invalidSet:
                    continue
                detectData.append(row)
        print(len(headers))
        print(len(dateTimes))
        print(len(lysisData))
        print(len(detectData))
        for testNum in range(len(dateTimes)):
            #fileName = dateTimes[testNum][]
            '''
            dateTime = dateTimes[testNum][3]
            timestamp = time.mktime(datetime.datetime.strptime\            (dateTime, "%m/%d/%Y %H:%M:%S").timetuple())
            date_time = datetime.datetime.fromtimestamp(timestamp)
            newDateTime = date_time.strftime("%Y%m%d%H%M%S")
            '''

            newFile = os.path.join(savePath, '{}_{}-{}.csv'.format(devicePrefix, dateTimes[testNum][1], dateTimes[testNum][0]))
            if os.path.isfile(newFile):
            	continue
            with open(newFile,'w', newline = '') as slgTest:
                writer = csv.writer(slgTest)
                writer.writerow(headers[0])
                writer.writerow(dateTimes[testNum])
                writer.writerow('\n')
                writer.writerow(headers[1])
                for i in range(2):
                    writer.writerow(lysisData[2 * testNum + i])
                writer.writerow('\n')
                writer.writerow(headers[2])
                for i in range(8):
                    writer.writerow(detectData[8 * testNum + i])

if __name__=='__main__':

	cwd = os.path.dirname(__file__)
	multitestPath = os.path.join(cwd, 'multitestCsv')
	slgtestPath = os.path.join(cwd, 'slgtestCsv')

	deviceNum = input("Input NABITA number(000-999): ")
	dateTime = input("Input date time (YYYYmmddHHMMSS): ")
	devicePrefix = 'NABITA{}'.format(deviceNum)
	datetimePrefix = '{}'.format(dateTime)

	resultFolder = '{}_{}'.format(devicePrefix, datetimePrefix)
	savePath = os.path.join(slgtestPath, resultFolder)
	if not os.path.isdir(savePath):
		os.mkdir(savePath)

	filename = '{}.csv'.format(resultFolder)
	fileSplitter(multitestPath, slgtestPath, filename, devicePrefix, savePath)

	filenames = sorted(glob.glob(os.path.join(savePath, '*.csv')))
	for filename in filenames:
		csvPlotter(savePath, filename)
