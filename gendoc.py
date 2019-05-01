import os, sys
import glob
import argparse
import numpy as np
import pandas as pd
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfTransformer
from assign1 import calc_vector

# gendoc.py -- Don't forget to put a reasonable amount code comments
# in so that we better understand what you're doing when we grade!

# add whatever additional imports you may need here

parser = argparse.ArgumentParser(description="Generate term-document matrix.")
parser.add_argument("-T", "--tfidf", action="store_true", help="Apply tf-idf to the matrix.")
parser.add_argument("-S", "--svd", metavar="N", dest="svddims", type=int,
                    default=None,
                    help="Use TruncatedSVD to truncate to N dimensions")
parser.add_argument("-B", "--base-vocab", metavar="M", dest="basedims",
                    type=int, default=None,
                    help="Use the top M dims from the raw counts before further processing")
parser.add_argument("foldername", type=str,
                    help="The base folder name containing the two topic subfolders.")
parser.add_argument("outputfile", type=str,
                    help="The name of the output file for the matrix data.")

args = parser.parse_args()

## Parsing the top folder we expect  sub-folders inside it
folders = os.listdir(args.foldername)
print(folders)

## List to hold text vectors
vectorMap = {}
tfidList = []
print("Loading data from directory {}.".format(args.foldername))

if not args.basedims:
    topN = 0
else:
    print("Using only top {} terms by raw count.".format(args.basedims))
    topN = args.basedims

for dir in folders:
  dirPath = args.foldername+'/'+dir
  if os.path.isdir(dirPath):
    files = [dirPath+'/'+f for f in os.listdir(dirPath) if os.path.isfile(dirPath+'/'+f)]
    ## Create the vector for each file
    for file in files:
      ##Keeping just the name to avoid duplicates
      justName = file.split("/")
      vectorMap[justName[5]]= calc_vector(file, topN)
    
if args.tfidf:
    transformer  = TfidfTransformer()
    print("Applying tf-idf to raw counts.")
    for vec in vectorList:
        bow_maxtrix = TfidfTransformer.fit_transform(vec)
        tfidList.append(TfidfTransformer.transform(bow_maxtrix))
## Parsing the freq vectors to a dataframe

if args.svddims:
    print("Truncating matrix to {} dimensions via singular value decomposition.".format(args.svddims))

# THERE ARE SOME ERROR CONDITIONS YOU MAY HAVE TO HANDLE WITH CONTRADICTORY
# PARAMETERS.

print("Writing matrix to {}.".format(args.outputfile))
dataFr = pd.DataFrame.from_dict(vectorMap)
dataFr = dataFr.fillna(0)
print(dataFr)
with open(format(args.outputfile), "w") as f:
    f.write(dataFr.to_string())


