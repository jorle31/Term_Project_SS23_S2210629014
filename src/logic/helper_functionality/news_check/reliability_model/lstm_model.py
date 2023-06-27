"""
This module contains the SVM model for the fake news detector.
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
    # Assuming you have loaded and preprocessed your data
    data = pd.read_csv("src/logic/helper_functionality/news_check/reliability_model/fake_or_real_news.csv")
    X = data["text"].values
    y = data["label"].values

    # Splitting the Data into Training and Test Sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Tokenizing and Preprocessing Text Data
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(X_train)
    X_train_sequences = tokenizer.texts_to_sequences(X_train)
    X_test_sequences = tokenizer.texts_to_sequences(X_test)

    vocab_size = len(tokenizer.word_index) + 1

    # Truncate or pad sequences to a fixed length
    max_len = 100  # Define your desired sequence length here
    X_train_padded = pad_sequences(X_train_sequences, maxlen=max_len)
    X_test_padded = pad_sequences(X_test_sequences, maxlen=max_len)

    # Encoding Labels
    label_encoder = LabelEncoder()
    y_train_encoded = label_encoder.fit_transform(y_train)
    y_test_encoded = label_encoder.transform(y_test)

    # Creating the LSTM Model
    model = Sequential()
    model.add(Embedding(vocab_size, 100, input_length=max_len))
    model.add(LSTM(128))
    model.add(Dropout(0.2))
    model.add(Dense(1, activation='sigmoid'))

    learning_rate = 0.001
    optimizer = Adam(learning_rate=learning_rate)
    model.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=['accuracy'])

    # Training the LSTM Model
    model.fit(X_train_padded, y_train_encoded, validation_data=(X_test_padded, y_test_encoded), epochs=10, batch_size=64)

    # Evaluating the LSTM Model
    y_pred_probabilities = model.predict(X_test_padded)
    y_pred_classes = (y_pred_probabilities > 0.5).astype(int)

    # Convert encoded labels back to original form
    y_test_original = label_encoder.inverse_transform(y_test_encoded)
    y_pred_original = label_encoder.inverse_transform(y_pred_classes.ravel())

    # Calculate accuracy
    accuracy = accuracy_score(y_test_original, y_pred_original)
    print(f'Accuracy: {accuracy}')

    # Preprocess the new text
    new_text_sequences = tokenizer.texts_to_sequences([text])
    new_text_padded = pad_sequences(new_text_sequences, maxlen=max_len)

    # Make predictions on the new text
    predicted_probabilities = model.predict(new_text_padded)
    predicted_classes = (predicted_probabilities > 0.5).astype(int)

    # Convert the predicted label back to original form
    predicted_label = label_encoder.inverse_transform(predicted_classes.ravel()) 

    print("Predicted Label:", predicted_label)
    return predicted_label[0]