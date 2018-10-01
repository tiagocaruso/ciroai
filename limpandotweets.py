import numpy as np
import pandas as pd
import csv

# importando o arquivo com os tweets 
tweets = pd.DataFrame.from_csv('cirogomes_tweets.csv').reset_index()

# Limpando os tweets
def TweetClean1(x): 
    dots = "(...)"
    clean_x = x
    if dots in clean_x:
        clean_x = x.split(dots)[1]         
    if '(..)' in clean_x:
        clean_x = clean_x.replace('(..)','')  
    if 'http' in clean_x:
        clean_x = clean_x.split('http')[0]  
    if '#JornalOGlobo' in clean_x:
        clean_x = clean_x.replace('#JornalOGlobo','')
    return clean_x


tweets['textClean'] = tweets['text'].apply(TweetClean1)
tweets['textLength'] = tweets['textClean'].apply(lambda x: len(x))
tweets = tweets[tweets.textLength >= 50].copy() # Selectionando os tweets com mais de 50 letras 
print(len(tweets))


# Trasnformando em uma longa string
big_string = ''
for i, row in tweets.iterrows():
    new_text = row['textClean']
    big_string = big_string + new_text + '\n'
print(len(big_string))

# Salvando em arquivo txt
file = open("ciro_all_tweets_body.txt",'w') 
file.write(big_string) 
file.close() 
