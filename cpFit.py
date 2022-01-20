import matplotlib.pyplot as plt
import os, csv, glob
from scipy.optimize import curve_fit
import numpy as np

def cp_fit(time, yplot):

    def func(x, a, k, m, b):
        return a + (k - a) / (1 + np.exp(-b * (x - m)))

    timeLB = 2
    timeRB = 22

    Tq = 0
    Beta_m = 0
    r_squared = 0

    popt, pcov = curve_fit(func, time, yplot)
    residuals = yplot - func(time, *popt)
    ss_res = np.sum(residuals**2)

    ss_tot = np.sum((yplot-np.mean(yplot))**2)
    r_squared = 1 - (ss_res / ss_tot)

    Tq = popt[2] - 2/popt[3]
    Beta_m = (popt[1] - popt[0]) / 2 / (popt[2] - Tq)

    return (round(Tq,2), round(Beta_m, 2), round(r_squared, 2))
