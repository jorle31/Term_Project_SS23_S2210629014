"""
This module contains the LSTM model for the fake news detector.
"""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from keras.models import Sequential
from keras.layers import LSTM, Dense, Embedding
from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences
from keras.optimizers import Adam
from keras.layers import Dropout

def LSTM_classifier(text: str) -> int:
    """Predicts whether a news article is reliable or not. 0 is reliable, 1 is not reliable.
    Takes the text of a news article as input and returns 0 or 1.
    
    :param text: The text to be classified.
    :return: The classification result.
    """
    data = pd.read_csv("src/logic/helper_functionality/news_check/reliability_model/fake_or_real_news.csv")
    X = data["text"].values
    y = data["label"].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(X_train)
    X_train_sequences = tokenizer.texts_to_sequences(X_train)
    X_test_sequences = tokenizer.texts_to_sequences(X_test)
    vocab_size = len(tokenizer.word_index) + 1
    max_len = 100
    X_train_padded = pad_sequences(X_train_sequences, maxlen = max_len)
    X_test_padded = pad_sequences(X_test_sequences, maxlen = max_len)
    label_encoder = LabelEncoder()
    y_train_encoded = label_encoder.fit_transform(y_train)
    y_test_encoded = label_encoder.transform(y_test)
    model = Sequential()
    model.add(Embedding(vocab_size, 100, input_length = max_len))
    model.add(LSTM(128))
    model.add(Dropout(0.2))
    model.add(Dense(1, activation = 'sigmoid'))
    learning_rate = 0.001
    optimizer = Adam(learning_rate = learning_rate)
    model.compile(loss = 'binary_crossentropy', optimizer = optimizer, metrics = ['accuracy'])
    model.fit(X_train_padded, y_train_encoded, validation_data = (X_test_padded, y_test_encoded), epochs = 10, batch_size = 64)
    y_pred_probabilities = model.predict(X_test_padded)
    y_pred_classes = (y_pred_probabilities > 0.5).astype(int)
    y_test_original = label_encoder.inverse_transform(y_test_encoded)
    y_pred_original = label_encoder.inverse_transform(y_pred_classes.ravel())
    accuracy = accuracy_score(y_test_original, y_pred_original)
    print(f'Accuracy: {accuracy}')
    new_text_sequences = tokenizer.texts_to_sequences([text])
    new_text_padded = pad_sequences(new_text_sequences, maxlen = max_len)
    predicted_probabilities = model.predict(new_text_padded)
    predicted_classes = (predicted_probabilities > 0.5).astype(int)
    predicted_label = label_encoder.inverse_transform(predicted_classes.ravel()) 
    print("Predicted Label:", predicted_label)
    return predicted_label[0]