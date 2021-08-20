import pandas as pd
import numpy as np
import re
import string
from textblob import TextBlob, Word

def remove_duplicates_and_export(file):
    df = pd.read_csv(file, encoding="UTF-8",delimiter=",")
    df = df.drop_duplicates()
    df.to_csv('commentData.csv', encoding = "UTF-8",index=False)

def process_text(text):
    text = text.lower()
    text = re.sub("@[^ ]+", "", text)#Removes any addresses such as @ABC
    text = re.sub("https:\/\/t\.co\/[^ ]+$", "" ,text) #Removes links that show up as text.
    text = re.sub("^rt", "", text)
    text = text.replace('&amp; ', '')
    text = text.split(" ")
    text = [word.strip(string.punctuation) for word in text]
    text = [word for word in text if len(word) > 1]
    text = " ".join(text)
    sent = TextBlob(text)
    text = " ". join([w.lemmatize() for w in sent.words])

    return text

def process_dataset(df):
    df['Question'] = df.apply(lambda row : 1 if '?' in row['Text'] else 0, axis = 1)
    df['Exclamation'] = df.apply(lambda row : 1 if '!' in row['Text'] else 0, axis = 1)
    df['Upper Case'] = df.apply(lambda row : count_upper(row['Text']),axis = 1)
    return df

def count_upper(str): #Counts the % of consecutive upper-case characters in a string. Ex. count_upper('ABcDEFg') == 5/7 and returns a label accordingly.
    cont_upper = 0
    is_upper = False
    total = len(str)
    for c in str:
        if c.isupper() and is_upper:
            cont_upper += 1
        elif c.isupper():
            is_upper = True
        else:
            is_upper = False
            
    pct = cont_upper/total
    if pct > 0.05:
        return 1
    elif pct > 0.1:
        return 2
    else:
        return 0

