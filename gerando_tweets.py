import re
import sys
import string
import numpy as np
from keras.models import Sequential
from keras.callbacks import ModelCheckpoint
from keras.layers import Dense, Dropout, LSTM
from keras.layers.embeddings import Embedding
from keras.models import model_from_yaml


# Loading body of text
rawtext = open('ciro_all_body.txt','r').read().split('\n')
rawtext = ' '.join(rawtext)
rawtext = [word.strip(string.punctuation) for word in rawtext.split()]
rawtext = ' '.join(rawtext)
rawtext = rawtext.replace('-', ' ')
rawtext = ' '.join(rawtext.split())
rawtext = rawtext.lower()

all_words = rawtext.split()
unique_words = sorted(list(set(all_words)))
n_vocab = len(unique_words)
print("Total Vocab:", n_vocab)
word_to_int = dict((w, i) for i, w in enumerate(unique_words))
int_to_word = dict((i, w) for i, w in enumerate(unique_words))


seq_length = 6

# Carregando YAML model
yaml_file = open('word_model.yaml', 'r')
loaded_model_yaml = yaml_file.read()
yaml_file.close()
loaded_model = model_from_yaml(loaded_model_yaml)

# carregando os pesos do modelo
loaded_model.load_weights("word_rnn-best.hdf5")
print("Loaded model from disk")


# Funções para gerar os tweets
def sample(preds, temperature = 1.0):
    # helper function to sample an index from a probability array
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)


def generate_tweet(seed = '',tweet_words = 30, diversity = 1.0):
    
    # transforming tweet words into numbers
    tweet = [word for word in seed.split()]
    padding = ['0']*(seq_length-len(tweet))
    tweet = padding + tweet
    seed_num = [word_to_int[word] for word in tweet]
    
    for i in range(tweet_words):
        x = np.reshape(seed_num, (1, len(seed_num), 1))
        x = x/float(n_vocab)
        
        preds = loaded_model.predict(x, verbose=0)[0]
        index = sample(preds, diversity)
        tweet.append(int_to_word[index])
        seed_num.append(index)
        seed_num = seed_num[1:len(seed_num)]
    tweet = tweet[len(padding):]
    tweet_str = ' '.join(tweet)
    return tweet_str


def generate_list_tweets(seed = '', n_tweets = 100, diversity = None, words = 30):
    tweet_list = [] 
    
    for i in range(n_tweets):
        if diversity:
            div = diversity
        else:
            div = np.random.choice([0.2,0.5,1.0,1.5,2.0])
        tweet = generate_tweet(seed,tweet_words=words,diversity=div)
        print(div)
        print(tweet)
 

start = 'não sou candidato a guru de'
generate_list_tweets(start,n_tweets=20, diversity= 0.2, words=30)