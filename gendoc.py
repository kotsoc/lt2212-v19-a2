import os, sys
import glob
import argparse
import numpy as np
import pandas as pd
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfTransformer
from assign1 import calc_vector
from sklearn.feature_extraction.text import CountVectorizer

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
### Dict that hold all filenames belongig to the class
classVectors={}
featureNames={}

print("Loading data from directory {}.".format(args.foldername))

if args.basedims:
    print("Using only top {} terms by raw count.".format(args.basedims))

################### VECTORIZER ##############
vectorizer = CountVectorizer(input='filename', lowercase=True, stop_words='english', max_features=args.basedims)

### Getting the name of all files
for dir in folders:
  dirPath = args.foldername+'/'+dir
  if os.path.isdir(dirPath):
    filepaths = [dirPath+'/'+f for f in os.listdir(dirPath) if os.path.isfile(dirPath+'/'+f)]
    word_vec = vectorizer.fit_transform(filepaths)
    featureNames[dir] = vectorizer.get_feature_names()
    classVectors[dir] = word_vec
    ## Was using my own vectorizer initially from assign 1, but using sklearns vectorizer made things go smoother so i changed to it
    #justName = file.split("/")
    #vectorMap[justName[5]]= calc_vector(file, topN)

################# TDIF ##############
if args.tfidf:
    transformer  = TfidfTransformer()
    print("Applying tf-idf to raw counts.")
    for dir in folders:
        classVectors[dir] = TfidfTransformer().fit_transform(classVectors[dir])

################# Dataframe from Vectorizer ##############
dataFrameDict = {}
for dir in folders:
    dataFrameFromVectorizer = pd.DataFrame.from_records(classVectors[dir].A, columns=featureNames[dir])
    dataFrameDict[dir] = dataFrameFromVectorizer


if args.svddims:
    if((not args.basedims) or args.svddims < args.basedims ):
        print("Truncating matrix to {} dimensions via singular value decomposition.".format(args.svddims))
        truncSVD = TruncatedSVD(n_components=args.svddims)
        for dir in folders:
            classVectors[dir] = truncSVD.fit_transform(classVectors[dir])
            dataFrameDict[dir] = pd.DataFrame.from_records(classVectors[dir])
    else:
        print("SVD dimensions should be fewer than the initial dimensions of WordMatrix. Skipping operation")

#print(dataFrameFromVectorizer)

print("Writing matrix to {}.".format(args.outputfile))

with open(format(args.outputfile), "w") as f:
    for dir in folders:
        ##lines that each class takes
        lines = '{}'.format(len(dataFrameDict[dir].axes[0]))
        print(lines)
        ### Writing Lines, Class name and then Dataframe as csv 
        f.writelines([lines,'\n',dir,'\n'])
        f.write(dataFrameDict[dir].to_csv())



