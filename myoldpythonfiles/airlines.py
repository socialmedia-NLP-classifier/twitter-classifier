#******************************************************************************
# airlines.py
#******************************************************************************
# Name: Kukai Nakahata
#******************************************************************************
# Collaborators/outside sources used 
#(IMPORTANT! Write "NONE" if none were used):
#
#NONE
#
# Reminder: you are to write your own code.
#******************************************************************************
# Overall notes (not to replace inline comments):
# the predictions get better after few runs and reaches a limit of 84% accuracy, 
# with other weird tweeks to the coefficient calculation, it can bring predictions up to 88% accuracy
import pandas as pd
import math
from math import trunc

# you can ignore this, this is here because my computer had the wrong directory, so the following code will check if the directory is correct
# if the directory is not the cuurent working file, then the file path gets updated
import os
scriptpath, filename = os.path.realpath(__file__), "" 
for i in range(1,len(scriptpath)+1):
    if scriptpath[-i] == "\\":
        scriptpath = scriptpath[0:-i]
        break
if os.getcwd() != scriptpath: filename = scriptpath + "\\"

def open_better_dic_txt(): # open the better deictioary, creates one if it doesnt exist
        try:
                file1, file2, file3 = open(filename+"better_pos_dictionary_abcd.txt", "r"), open(filename+"better_neut_dictionary_abcd.txt", "r"), open(filename+"better_neg_dictionary_abcd.txt", "r")
        except:
                tempfile1, tempfile2, tempfile3 = open(filename+"better_pos_dictionary_abcd.txt", "w"), open(filename+"better_neut_dictionary_abcd.txt", "w"), open(filename+"better_neg_dictionary_abcd.txt", "w")
                tempfile1.close()
                tempfile2.close()
                tempfile3.close()
                file1, file2, file3 = open(filename+"better_pos_dictionary_abcd.txt", "r"), open(filename+"better_neut_dictionary_abcd.txt", "r"), open(filename+"better_neg_dictionary_abcd.txt", "r")
        get_dic(file1, pos_coeffs) 
        get_dic(file2, neut_coeffs)   
        get_dic(file3, neg_coeffs)        

def get_dic(filetxt, rel_dic): # gets a string of the words and weights and adds them to a dictionary
        for i in filetxt:
                j = i.split()
                rel_dic[j[0]] = float(j[1])
        filetxt.close()

def find_coeff(a,b,c, total,w, rel_dic, coeff, scale): # uses the equation to shift the coefficents by a certain value, the equation is mainly based on the accuracy and the total number of tweets it got wrong
        val = a/(total + b + c)
        if w in rel_dic and abs(val-rel_dic[w]) > 0.1:
                rel_dic[w] += scale*(trunc((math.log10(coeff)+1)*(val-rel_dic[w])*100)/100) #shift the value by a small number
        else:
                rel_dic[w] = 0.3 # this is the default value

def write_to_file(filename, rel_dic):
        for key, value in rel_dic.items():
                if value < 0.0001:
                        value = 0.001
                value = str(value)
                filename.write(key+" "+value[0:6]+"\n")

def remove_symbol(a): #input: array, output: array without special character and all lowercase
        char_to_remove = ["!","@","%","^","&","*","(",")","'",".",",","?","+","-","_","\"","/",";",":","#","$","’","=","”","“"]
        additional_char = ["0","1","2","3","4","5","6","7","8","9"]
        char_to_remove +=additional_char
        for w in range(len(a)): # words in the noise_list gets filtered out
                if a[w] in noise_list:
                        a[w] = ""
        for k in range(len(a)):# goes through each word and each letter and remove special symbols
                new_word, word_size = "", len(a[k])
                for j in range(word_size): #j-th letter
                        if a[k][j] in char_to_remove: pass
                        else: new_word+=a[k][j]
                if len(new_word) == 1: new_word = "" # if the word is a single character, make it an empty string(it gets filtered after)
                else: new_word = new_word.lower() #change all to lowercase
                if new_word != a[k]: a[k] = new_word
        a = list(filter(None, a))
        return a    

def remove_some_endings(a): # input: an array with words, converts or remove some endings in the words
        for i in range(len(a)):
                word = a[i]
                if len(word)>4:  # removes ing, ed, ly, es and other common endings
                        ending, ending1 = word[-3:], word[-2:]
                        if ending == "ies": a[i] = word[0:-3]+"y"
                        elif ending == "ing":
                                for v in vowels:
                                        if v in word[0:-3]:
                                                if word[-4] == "z": a[i] = word[0:-3]+"e"
                                                else: a[i] = word[0:-3]
                                                break
                        elif ending in ["ful","ish","ive","ous","ize","ism","ist"]: a[i] = word[0:-3]
                        elif ending1 == "ed" and word[-3] != "e":  a[i] = word[0:-2]
                        elif ending1 in ["ly","es","al","or","er","en","ic" ]: a[i] = word[0:-2]
                        elif (word[-2:] != "ss") and (word[-3] not in vowels): a[i] = word[0:-3]            
        return a #returns a new array of words with special endings filtered out
                                
def predict_sentiment(tweet): # this function returns the predicted sentiments
        uniquewords, dic = {}, [pos_coeffs, neut_coeffs, neg_coeffs]
        sent_value, sent_num, sentiments = [0,0,0], [0,0,0], ["positive", "neutral", "negative"]# the numerical values that represents sentiments are in same position respect to sentiments
        for new_word in tweet: # looks at the number of words with sentiment and adds sentiment value
                coeff = 1
                for j in range(len(dic)):
                        if new_word in dic[j]:
                                try: uniquewords[new_word] += 1 # looks if the tweet have repeated words with sentiments like "bad bad bad"
                                except: uniquewords[new_word] = 1
                                if uniquewords[new_word] > 1: 
                                        coeff = (1.5**uniquewords[new_word])
                                sent_value[j] += coeff*float(dic[j][new_word]) 
                                sent_num[j] += 1
                                break
                   
        max_num, mid_num= max(sent_num), 0
        for index, number in enumerate(sent_num): #find the maximum number and the index of the middle value
                if number == max_num: max_index = index
                if max_num > number >= mid_num: mid_num = number

        if len(tweet)> 21: # after filtering words like "i", "me", "the" and special character, if the tweet is long, its mostly bound to be a negative tweet
                return [sentiments[2], sent_value, sent_num]
        if sent_value == [0,0,0]:   # by default if there's no sentiment that can be predicted, it returns negative
                return [sentiments[2], sent_value, sent_num]   
        for i in range(3): # for each sentiment, I mutliply the value by the overall number of positive, neutral or negative sentimental words.
                sent_value[i] = sent_value[i]*sent_num[i]
                if i == max_index:
                        sent_value[i] = sent_value[i]*(sent_num[i]+2)
                        if max_num- mid_num >= 5: sent_value[i] = sent_value[i]*(sent_num[i]+1)
        if max(sent_value) == sent_value[0]: return [sentiments[0], sent_value, sent_num] # returns the sentiment with the highest value
        if max(sent_value) == sent_value[2]: return [sentiments[2], sent_value, sent_num]
        return [sentiments[1], sent_value, sent_num]

# set up variables
pos_coeffs, neut_coeffs, neg_coeffs, temp_dic = {},{},{},{}
noise_list = ["virginamerica", "to", "in", "your", "have", "and", "it", "flight", "for", "that", "the", "on", "is", "my", "of", "me", "you", "with", "be", "at", "not", "was", "unit"]
vowels = ["a","e","i","o","u","y"]
tweets_df = pd.read_csv(filename + "tweet.csv")
tweet_entry, sentiment_entry = tweets_df["text"], tweets_df["airline_sentiment"]
pos_count, neg_count, neut_count, count, correct_sentiment = 0, 0, 0, 0, 0
pos_prediction, neg_prediction, neut_prediction = 1,1,1

open_better_dic_txt()
for i in range(len(tweet_entry)): # go through each tweet and predict sentiments, then count the ones it got correct
        tweet = remove_some_endings(remove_symbol(tweet_entry[i].split()))
        sent = predict_sentiment(tweet)
        if sentiment_entry[i] == "positive": pos_count += 1 # counts the number of positive, negative, or neutral tweet
        elif sentiment_entry[i] == "negative": neg_count +=1
        else:  neut_count+=1
        if sentiment_entry[i] == sent[0]: # chek if the prediction is right
                correct_sentiment+=1
                if sent[0] == "positive": pos_prediction +=1
                elif sent[0] == "negative": neg_prediction+=1
                else: neut_prediction+=1
        """ # this is for looking at the tweet and sentiment that it predicted wrong
        else:
                if count < 500 and sentiment_entry[i] != "negative" and sent[2].count(0) != 2:
                        print(i, sentiment_entry[i], sent, end="")
                        count+=1
        """   
        for j in tweet:# this loop will look at each unique word and count the number of times it showed up in positive, negative, or neutral tweets
                while True: 
                        try:
                                if sentiment_entry[i] == "positive": temp_dic[j][0] +=1
                                elif sentiment_entry[i] == "negative":  temp_dic[j][2] +=1
                                else:  temp_dic[j][1] +=1
                                break              
                        except: temp_dic[j] = [0,0,0]

print("overall accururacy:", correct_sentiment/i) # the break down of the predictions
print("positive: correct:", pos_prediction, "out of",pos_count,"accuracy:",pos_prediction/pos_count)
print("neutral: correct:",neut_prediction, "out of",neut_count,"accuracy:",neut_prediction/neut_count)
print("negative: correct:",neg_prediction, "out of",neg_count,"accuracy:",neg_prediction/neg_count)
temp_list3 = [pos_prediction/pos_count, neut_prediction/neut_count, neg_prediction/neg_count]

if min(temp_list3) == temp_list3[0]: val_pos = 1.6 # these add weights to the predictions that are underperforming compared to the other predictions
elif max(temp_list3) == temp_list3[0]: val_pos = 1
else: val_pos =1.4
if min(temp_list3) == temp_list3[1]: val_neut = 1.6
elif max(temp_list3) == temp_list3[1]: val_neut = 1
else: val_neut =1.4
if min(temp_list3) == temp_list3[2]:  val_neg = 1.6
elif max(temp_list3) == temp_list3[2]: val_neg = 1
else: val_neg =1.4

for i in temp_dic: # look at each unique word and puts it in the most correct dictionary with coefficients
        arr = temp_dic[i]
        total = arr[0] + arr[1] + arr[2]
        if total >= 1 and i not in noise_list:
                if abs(arr[0] - arr[2])/max(arr[0], arr[2],1) < 0.10: # modify the coefficients based on the performance of the prediction
                        find_coeff(arr[1], arr[0], arr[2], total,i,  neut_coeffs,((neut_count-neut_prediction)/neut_count)/(neut_prediction/neut_count), 1)
                elif arr[0] > (arr[1] + arr[2]):
                        find_coeff(arr[0], arr[1], arr[2], total,i,pos_coeffs,((pos_count-pos_prediction)/pos_count)/(pos_prediction/pos_count), val_pos)
                elif arr[1] > (arr[0] + arr[2]):
                        find_coeff(arr[1], arr[0], arr[2], total,i,  neut_coeffs,((neut_count-neut_prediction)/neut_count)/(neut_prediction/neut_count), val_neut)
                elif arr[2] > 2*(arr[0] + arr[1]):
                        find_coeff(arr[2], arr[0], arr[1], total,i, neg_coeffs, ((neg_count-neg_prediction)/neg_count)/(neg_prediction/neg_count), val_neg)
                        
# open file and write the new coefficients and updated words
file1, file2, file3 = open(filename+"better_pos_dictionary_abcd.txt", "w"), open(filename+"better_neut_dictionary_abcd.txt", "w"), open(filename+"better_neg_dictionary_abcd.txt", "w")
write_to_file(file1, pos_coeffs)
write_to_file(file2, neut_coeffs)
write_to_file(file3, neg_coeffs)
file1.close()
file2.close()
file3.close()