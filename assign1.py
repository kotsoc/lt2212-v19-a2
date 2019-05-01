import re

## Will reuse the code from assignment 1 for counting the word frequencies
def calc_vector(name, topN):
    #######################
    ## ArgParse is not needed since we are using this as a helped function
    #parser = argparse.ArgumentParser()
    #parser.add_argument("--name", "-n", help="name of the file to be opened")
    #parser.add_argument("--top", type=int,  help="number of words to print")
    #parser.add_argument("--to-lower", help="lower-case all the words before counting frequencies", action="store_true")
    #args = parser.parse_args()
    #######################
    to_lower = True
    text = open(name, encoding="utf-8")
    lines = text.read().split()
    words= []
    for line in lines:
        if to_lower:
            words += re.sub(r'[^A-Za-z0-9]+','',line).lower().split()
        else:
            words += line.split(" ")
    freq_dict = { }
    for word in words:
        if word in freq_dict:
            freq_dict[word] += 1
        else:
            freq_dict[word] = 1
    text.close()
    sorted_list = sorted(freq_dict, key=freq_dict.get, reverse =True)
    numToList = len(sorted_list)
    if topN > 0 and topN < numToList:
        topNFreqDict = {}
        for i in range(topN):
            topNFreqDict[sorted_list[i]] = freq_dict[sorted_list[i]]
        print(len(topNFreqDict))
        return topNFreqDict
    else:
        return freq_dict