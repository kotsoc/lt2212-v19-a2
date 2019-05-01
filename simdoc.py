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
    print(linestoRead)
    print(skip)
print(classNameList)