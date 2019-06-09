import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np
import data_helpers as dh

from keras import backend as K
from keras.models import Sequential, load_model
from keras.layers import Dense, LSTM, Embedding, Dropout
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils import plot_model


emotion = {
                'empty' : 'neutral',
                'sadness' : 'sadness',
                'enthusiasm' : 'fun',
                'neutral' : 'neutral',
                'worry' : 'fear',
                'surprise' : 'fear',
                'love' : 'fun',
                'fun' : 'fun',
                'hate' : 'sadness',
                'happiness' : 'happiness',
                'relief' : 'happiness',
}

data = pd.read_csv("../data/clean_tweet.csv")
data = data.dropna()
data = data.sample(frac=1).reset_index(drop=True)
data = data[['sentiment', 'content']]
data = data.sample(frac=1).reset_index(drop=True)
data.sentiment = data.sentiment.map(emotion)
#print(data.sentiment.value_counts())

max_words = 11000
lstm_out_1 = 768
lstm_out_2 = 256
embed_dim = 2048

tokenizer = Tokenizer(num_words=max_words)
tokenizer.fit_on_texts(data['content'].values)

#print("Toplam ", len(tokenizer.word_index), " adet farklı kelime bulunmaktadır")
#print("Toplam ", tokenizer.num_words, " adet kelime işleme alınacaktır")
#X = tokenizer.texts_to_sequences(data['content'].values)
#X = pad_sequences(X)
#print(pd.get_dummies(data['sentiment']).columns.tolist())
#y = pd.get_dummies(data['sentiment']).values

def clean_tweets(tweets):
  c_tweet = []
  for tweet in tweets:
    clean_tweet = dh.clean_tweet(tweet)
    c_tweet.append(clean_tweet)
  return c_tweet

def token_tweets(cl_tweets):
  sequences = tokenizer.texts_to_sequences(cl_tweets)
  X = pad_sequences(sequences)
  zeros = np.zeros((X.shape[0],23-X.shape[1]))
  X = np.hstack((zeros,X))
  return X

def dataset_clean():
  data = pd.read_csv("../data/text_emotion.csv")
  data = data[['sentiment', 'content']]
  data = data.ix[data['sentiment'] != 'anger']
  data = data.ix[data['sentiment'] != 'boredom']
  data = data.reset_index(drop=True)
  print(data.shape)

  data['sentiment'].value_counts().sort_index().plot.bar()
  data['content'].str.len().plot.hist() 

  for i in range(39711):
    data['content'] = dh.clean_tweet(data['content'][i])
  data.to_csv("../data/clean_tweet.csv")

def model_create():
  model = Sequential()
  model.add(Embedding(max_words, embed_dim, input_length=23))
  model.add(LSTM(lstm_out_1, return_sequences=True))
  model.add(Dropout(0.2))
  model.add(LSTM(lstm_out_2))
  model.add(Dropout(0.2))
  model.add(Dense(5, activation='softmax'))
  model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
  model.summary()
  return model

def model_train_save(model):
  plot_model(model, to_file='model_plot.png', show_shapes=True, show_layer_names=True, rankdir='LR')
  batch_size = 64
  epochs = 2
  model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, verbose=1, validation_data=(X_test, y_test)) 
  model.save('../data/sentiment_analysis_model.h5')

#model = model_create()
#model_train_save(model)

def result(data):
    model = load_model('../data/sentiment_analysis_model.h5')
    predictions = model.predict_classes(data)
    K.clear_session()
    return predictions

       