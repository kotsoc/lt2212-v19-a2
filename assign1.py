import re

def calc_vector(name, topN):
    #parser = argparse.ArgumentParser()
    #parser.add_argument("--name", "-n", help="name of the file to be opened")
    #parser.add_argument("--top", type=int,  help="number of words to print")
    #parser.add_argument("--to-lower", help="lower-case all the words before counting frequencies", action="store_true")
    #args = parser.parse_args()

    to_lower = True
    text = open(name, encoding="utf-8")
    lines = text.read().split()
    words= []
    for line in lines:
        if to_lower:
            words += re.sub(r'[^A-Za-z0-9]','',line).lower().split(" ")
        else:
            words += line.split(" ")
    freq_dict = { }
    for word in words:
        if word in freq_dict:
            freq_dict[word] += 1
        else:
            freq_dict[word] = 1
    sorted_list = sorted(freq_dict, key=freq_dict.get, reverse =True)
    numToList = len(sorted_list)
    if topN == 0 or topN > numToList:
        topN = numToList
    for i in range(topN):
        print(sorted_list[i] + ': %d' %(freq_dict[sorted_list[i]]) )
    text.close()