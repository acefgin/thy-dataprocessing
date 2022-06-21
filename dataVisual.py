import numpy as np
import os, csv, glob
import pandas as pd


def dataVisual(folderPath, filename):
    csvfile = os.path.join(folderPath, filename)
    df = pd.read_csv(csvfile)
    print(df['Tq-1'])

if __name__=='__main__':
    cwd = os.path.dirname(__file__)
    name = "dataWizard_output.csv"
    print(name)
    dataVisual(cwd, name)

