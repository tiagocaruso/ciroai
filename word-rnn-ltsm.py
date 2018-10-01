import re
import sys
import string
import numpy as np
from keras.utils import np_utils
from keras.models import Sequential
from keras.callbacks import ModelCheckpoint
from keras.layers import Dense, Dropout, LSTM
from keras.layers.embeddings import Embedding
from keras.models import model_from_yaml

# Importando o corpo do texto
rawtext = open('ciro_all_body.txt','r').read().split('\n')
rawtext = ' '.join(rawtext)
rawtext = [word.strip(string.punctuation) for word in rawtext.split()]
rawtext = ' '.join(rawtext)
rawtext = rawtext.replace('-', ' ')
rawtext = ' '.join(rawtext.split())
rawtext = rawtext.lower()
print(len(rawtext))

# Criando dicionários que vão de palavras para inteiros e vice-versa
all_words = rawtext.split()
unique_words = sorted(list(set(all_words)))
n_vocab = len(unique_words)
print("Total Vocab:", n_vocab)
word_to_int = dict((w, i) for i, w in enumerate(unique_words))
int_to_word = dict((i, w) for i, w in enumerate(unique_words))

# Trasnformando a string em uma lista
raw_text = rawtext.split()
n_words = len(raw_text)
print(n_words)

# Criando a base de dados onde o modelo será treinado
seq_length = 6 # Esse parâmetro indica a quantidade de palavras que serão usadas para prever a próxima palavra
dataX = []
dataY = []
for i in range(0, n_words - seq_length):
    seq_in  = raw_text[i: i+seq_length]
    seq_out = raw_text[i+seq_length]
    dataX.append([word_to_int[word] for word in seq_in])
    dataY.append(word_to_int[seq_out])
n_patterns = len(dataX)
print('Total patterns:', n_patterns)

# Mudando o formato de dataX para o tamoanho[obs, passos , caracteristicas] and mudando a escala para  0-1
# Represent dataY as one hot encoding
X_train = np.reshape(dataX, (n_patterns, seq_length, 1))/float(n_vocab)
Y_train = np_utils.to_categorical(dataY)

# Criando o modelo em Keras
model = Sequential()
model.add(LSTM(256, input_shape=(X_train.shape[1], X_train.shape[2])))
model.add(Dropout(0.2))
model.add(Dense(Y_train.shape[1], activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam')
print(model.summary())

# Recuperando o modelo salvo, salvando o modelo e criando checkpoints
filepath="word_rnn-best.hdf5"
model.load_weights(filepath) # So rode essa linha se os pesos já foram estimados ao menos uma vez
model.compile(loss='categorical_crossentropy', optimizer='adam')
checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
callbacks_list = [checkpoint]

# Treinando o modelo. Ao menos 80 epochs. Isso vai levar algumas horas, funciona bem melhor se você tiver gpus
model.fit(X_train, Y_train, epochs=80, batch_size=32, callbacks=callbacks_list)

# Salvando o modelo em Yaml
model_yaml = model.to_yaml()
with open("word_model.yaml", "w") as yaml_file:
    yaml_file.write(model_yaml)