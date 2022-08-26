import matplotlib.pyplot as plt
import os, csv, glob
import numpy as np
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

from slidingWin import *
from stepsFilter import *

def csvPlotter(folderPath, filename):

	print(os.path.splitext(os.path.basename(filename))[0])
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

	rlt = []
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
				x = [float(i)/1000/60 - 5 for i in x]
			if idx == 11:
				ChResult.append(row[5])
				y1 = row[7:]
				rlt.append(row[6])
				y1 = np.array([float(i) for i in y1])
				if len(y1) >= 9: signalList.append(smooth(y1))
			if idx == 12:
				ChResult.append(row[5])
				y2 = row[7:]
				rlt.append(row[6])
				y2 = np.array([float(i) for i in y2])
				if len(y2) >= 9: signalList.append(smooth(y2))
			if idx == 13:
				ChResult.append(row[5])
				y3 = row[7:]
				rlt.append(row[6])
				y3 = np.array([float(i) for i in y3])
				if len(y3) >= 9: signalList.append(smooth(y3))
			if idx == 14:
				ChResult.append(row[5])
				y4 = row[7:]
				rlt.append(row[6])
				y4 = np.array([float(i) for i in y4])
				if len(y4) >= 9: signalList.append(smooth(y4))
			if idx == 15:
				ChResult.append(row[5])
				y5 = row[7:]
				rlt.append(row[6])
				y5 = np.array([float(i) for i in y5])
				if len(y5) >= 9: signalList.append(smooth(y5))

			idx += 1

	featList = np.zeros((5,4))

	if len(signalList) != 0:

		for i in range(5):
			_, diff, cp, stepWidth, avgRate= labelSteps(signalList[i])
			if diff == 0 and len(signalList[i]) >= 50:
				diff = round(consecutiveSum(np.diff(signalList[i]), 50), 1)
			featList[i] = [diff, cp, stepWidth, avgRate]

	plt.figure(num=None, figsize=(24, 6), dpi=40)
	ax = plt.subplot(111)
	ax.plot(x, y1, color = 'r', linewidth=2, label='PC')
	ax.plot(x, y2, color = '#35ff35', linewidth=2, label='N1')
	ax.plot(x, y3, color = '#3535ff', linewidth=2, label='N2')
	ax.plot(x, y4, color = '#35ffff', linewidth=2, label='M1')
	ax.plot(x, y5, color = '#ff35ff', linewidth=2, label='M2')
	plt.xlabel('Time (mins)', fontsize = 19, fontweight = 'bold')
	plt.ylabel('Signal (mvs)', fontsize = 19, fontweight = 'bold')
	plt.title('{}_{}'.format(os.path.splitext(os.path.split(filename)[1])[0], OverallResult), fontsize = 20, fontweight = 'bold')
	box = ax.get_position()
	ax.set_position([box.x0*0.35, box.y0, box.width * 1.2, box.height])
	ax.grid(linestyle = '-.')
	ax.legend(loc='upper right',  ncol=5)
	# Print diffs data in plot
	diffs_text = 'Diffs(mvs) = PC:{}, N1:{}, N2:{}, M1:{}, M2:{}'.format\
	(featList[0][0], featList[1][0], featList[2][0], featList[3][0], featList[4][0])
	AvgRate_text = 'AvgRate(mvs/10s) = PC:{}, N1:{}, N2:{}, M1:{}, M2:{}'.format\
	(featList[0][3], featList[1][3], featList[2][3], featList[3][3], featList[4][3])
	plt.text(-2.5, 440, diffs_text)
	plt.text(-2.5, 400, AvgRate_text)

	#ax.legend(loc='upper left')
	plt.axis([-5,30,40,480])
	ax.xaxis.set_major_locator(MultipleLocator(2))
	ax.xaxis.set_major_formatter('{x:.0f}')
	ax.xaxis.set_minor_locator(MultipleLocator(1))

	ax.yaxis.set_major_locator(MultipleLocator(40))
	ax.yaxis.set_major_formatter('{x:.0f}')
	ax.yaxis.set_minor_locator(MultipleLocator(20))

	plt.savefig(os.path.join(folderPath, '{}_{}.png'.format(os.path.splitext(os.path.split(filename)[1])[0], OverallResult)))

	return idInfo, OverallResult, featList

if __name__=='__main__':
	deviceNum = input("Input NABITA number(000-999): ")
	prefix = 'NABITA{}'.format(deviceNum)

	csvfoler = os.path.join(os.path.dirname(__file__), 'slgtestCsv')
	filenames = sorted(glob.glob(os.path.join(csvfoler, '*{}*.csv'.format(prefix))))
	for filename in filenames:
		csvPlotter(csvfoler, filename)
