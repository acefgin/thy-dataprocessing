from sklearn.model_selection import train_test_split
import csv
import numpy as np


datasetFile = "testDataset.tsv"
dataSet = []
with open(datasetFile,'r') as dataset:
    rows = csv.reader(dataset, delimiter='\t')

    for i, row in enumerate(rows):
        label = row[0]

        label = [int(label[0])]

        data = [float(x) for x in row[1:] if x != '']

        dataSet.append(label + data)


dataSet_np = np.array(dataSet)

TRAIN_SET, TEST_SET = train_test_split(dataSet_np, test_size=0.3, random_state=42, shuffle=True)

print(np.shape(TRAIN_SET))
print(np.shape(TEST_SET))

np.savetxt("NaBIT_TRAIN.tsv", TRAIN_SET.round(3), delimiter="\t")
np.savetxt("NaBIT_TEST.tsv", TEST_SET.round(3), delimiter="\t")