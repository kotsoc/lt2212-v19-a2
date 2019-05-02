import os, sys
import argparse
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# simdoc.py -- Don't forget to put a reasonable amount code comments
# in so that we better understand what you're doing when we grade!

### One list to hold the data and one for class names
classNameList = []
dataList= []

## Helper function to read how many lines the matrix take in order to parse correcty with pandas
def readDataFrameLines(filaname, linenumber):
    with open(filaname, "r") as f:
        lines = f.readlines()
        if linenumber < len(lines)-1:
            ##Document class is always the next line after the lines to read
            classNameList.append(lines[linenumber+1].replace("\n", ""))
            return int(lines[linenumber])
        else:
            return -1

# add whatever additional imports you may need here

parser = argparse.ArgumentParser(description="Compute some similarity statistics.")
parser.add_argument("vectorfile", type=str,
                    help="The name of the input  file for the matrix data.")

args = parser.parse_args()

print("Reading matrix from {}.\n".format(args.vectorfile))

linestoRead =readDataFrameLines(args.vectorfile,0)
skip = 2
while(linestoRead > 0):
    ## Reading the ammount of lines that we wrote on the file and holding the Dataframes in a list
    dataList.append(pd.read_csv(args.vectorfile, index_col=0, skiprows = skip, nrows=linestoRead))
    skip += linestoRead+3
    linestoRead = readDataFrameLines(args.vectorfile,skip-2)

avgSelfCosSimList = []
avgCrossCosSimList = []

## Calculating Cos Similarities for each class with itself
for k in range(len(classNameList)):
    cos_sim = cosine_similarity(dataList[k].values)
    avgSim = 0.0
    sum = 0
    for i in range(len(cos_sim)):
       # temp = 0.0
        for j in range(len(cos_sim[i])):
            avgSim += cos_sim[i][j]
            sum+=1
    avgSelfCosSimList.append(avgSim/sum)

## Calculating Cross-classs Cos Similarities for each class
for k in range(len(classNameList)-1, 0, -1):
    cos_sim = cosine_similarity(dataList[k].values, dataList[k-1].values)
    avgSim = 0.0
    sum = 0
    for i in range(len(cos_sim)):
        for j in range(len(cos_sim[i])):
            avgSim += cos_sim[i][j]
            sum+=1
    avgCrossCosSimList.append(avgSim/sum)

for k in range(len(classNameList)):
    print("the average similarity of every document vector in class {} with itself is: {}".format(classNameList[k],avgSelfCosSimList[k]))
print("the cross similarity of every document vector in class {} with the class {} is: {}".format(classNameList[0],classNameList[1], avgCrossCosSimList[0]))