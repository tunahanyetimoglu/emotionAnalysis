import re
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

from keras.models import Sequential, load_model
from keras.layers import Dense, LSTM, Embedding, Dropout
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences 

data = pd.read_csv("text_emotion.csv")

data = data.sample(frac=1).reset_index(drop=True)
clear_data = []

    
data = data[['sentiment', 'content']]
print(data.shape)
#data['sentiment'].value_counts().sort_index().plot.bar()
#data['content'].str.len().plot.hist() 
data['content'].apply(lambda x: x.lower())
data['content'] = data['content'].apply(lambda x: re.sub('[^a-zA-z0-9\s]', '', x))
data['content'].head()

tokenizer = Tokenizer(num_words=5000, split=" ")
tokenizer.fit_on_texts(data['content'].values)

X = tokenizer.texts_to_sequences(data['content'].values)
X = pad_sequences(X) # padding our text vector so they all have the same length
X[:5] 

model = Sequential()
model.add(Embedding(5000, 256, input_length=X.shape[1]))
model.add(Dropout(0.3))
model.add(LSTM(256, return_sequences=True, dropout=0.3, recurrent_dropout=0.2))
model.add(LSTM(256, dropout=0.3, recurrent_dropout=0.2))
model.add(Dense(13, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.summary()

y = pd.get_dummies(data['sentiment']).values
[print(data['sentiment'][i], y[i]) for i in range(0,12)]     

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0) 

batch_size = 32
epochs = 8
model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, verbose=2) 

model.save('sentiment_analysis.h5')

predictions = model.predict(X_test)
[print(data['text'][i], predictions[i], y_test[i]) for i in range(0, 5)] 