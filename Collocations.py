#Andrew Gasiorowski

import math
import re, sys
from collections import Counter

#this function goes through the corpus and creates uni/bi-grams
def make_grams(fileName):
    words = re.findall(r"(?:(?<=^)[A-Za-z.]+|(?<= )[A-Za-z.]+(?= )|(?<= )[A-Za-z.]+$)", open(fileName).read())
    uni_grams = dict(Counter(zip(words)))
    bi_grams = dict(Counter(zip(words,words[1:])))
    return uni_grams, bi_grams

#this function makes two dicts where the key is the unigram and the value is the number of occurences--
#initially set to zero
#w1 represents word occurences as word1   and w2 as word2..
#After we have both of these dicts we iterate through the bigram list and incrament the unigram value for
#each word as we encounter it.
#This is somewhat innefficient because we traverse the dict 3 times O(3N) however each dict is accesible #in constant time so this function is still operating in linear time.
#I believe there is a more efficient way to count word occurencecs using relativly simple math, but I wasn't able to figure it out.
def count_word_occurences(uni_grams, bi_grams):
    w1 = {}
    for key, value in uni_grams.items():
        w1[key[0]] = 0
    w2 = w1
    for key, value in bi_grams.items():
        w1[key[0]] = w1[key[0]] + 1
        w2[key[0]] = w2[key[0]] + 1    
    return w1, w2

#This function tabulates, for each word, a 2by2 table where (1,1) = oneone = word1 followed by word2
#(1,2) = onetwo = not word 1 followed by word 2, etc
#from this it calculates expected values before computing chi-squared and Pointwise Mutual Information
def calc_metrics(bi_grams, w1, w2):
    table = []
    w1_sum = sum(w1.values())
    w2_sum = sum(w2.values())
    bigram_sum = sum(bi_grams.values())
    for key, value in bi_grams.items():
        oneone = value
        onetwo = w2[key[1]] - value
        twoone = w1[key[0]] - value
        twotwo = bigram_sum - value - onetwo - twoone
#         onetwo = w1_sum - w1[key[0]] + w2[key[1]]
#         twoone = w1[key[0]] + w2_sum - w2[key[1]]
#         twotwo = w1_sum - w1[key[0]] + w2_sum - w2[key[1]]
        n = oneone + onetwo + twoone + twotwo
        eoneone = ((oneone + twoone)/n)*((oneone+onetwo)/n)*(n)
        eonetwo = ((onetwo + twotwo)/n)*((oneone + onetwo)/n)*(n)
        etwoone = ((oneone + twoone)/n)*((twoone + twotwo)/n)*(n)
        etwotwo = ((onetwo + twotwo)/n)*((twoone + twotwo)/n)*(n)
        s1 = ((oneone - eoneone)**2)/eoneone
        s2 = ((onetwo - eonetwo)**2)/eonetwo
        s3 = ((twoone - etwoone)**2)/etwoone
        s4 = ((twotwo - etwotwo)**2)/etwotwo
        xsquare = s1+s2+s3+s4
        #pmi = math.log((((value)/(bigram_sum))/((w1[key[0]]/w1_sum)*(w2[key[1]]/w2_sum))),2)
        pmi = math.log((((value)/(bigram_sum))/((w1[key[0]]/bigram_sum)*(w2[key[1]]/bigram_sum))),2)
        entry = (key, xsquare, pmi)
        table.append(entry)
    return table

#this function prints the output on the screen
def print_output(table, measure_type):
    numeric_measure = 1
    if measure_type == 'pmi':
        numeric_measure = 2
    metric_table.sort(reverse=True if numeric_measure == 2 else True, key=lambda tup: tup[numeric_measure])
    c = 0
    template = "{0:20}{1:20}{2:10}"
    for item in metric_table:
        if c < 25:
            line_tup = (item[0][0], item[0][1],str(round(item[numeric_measure],4)))
            #print(item[0],':',str(round(item[numeric_measure],4)))
            print(template.format(*line_tup))
            c = c + 1

#This block of code grabs file names from command line        
able = str(sys.argv).split(',')
regex = re.compile('[^a-zA-Z.]')
file_r = regex.sub('', able[1])
measure = regex.sub('', able[2])
measure = measure.lower()

#This block of calls functions to compute metrics
unigram, bigram = make_grams(file_r)
lhs_list, rhs_list = count_word_occurences(unigram, bigram)
metric_table = calc_metrics(bigram, lhs_list, rhs_list)
print_output(metric_table, measure)
