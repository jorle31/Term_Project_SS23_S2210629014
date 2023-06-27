"""
This module contains the SVM model for the fake news detector.
"""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC

def SVM_classifier(text: str) -> int:
    """Predicts whether a news article is reliable or not. 0 is reliable, 1 is not reliable.
    Takes the text of a news article as input and returns 0 or 1.
    
    :param text: The text to be classified.
    :return: The classification result.
    """
    data = pd.read_csv("src/logic/helper_functionality/news_check/reliability_model/fake_or_real_news.csv")
    print(data)
    data["fake"] = data["label"].apply(lambda x: 0 if x == "REAL" else 1)
    data = data.drop("label", axis = 1)
    X, y, = data["text"], data["fake"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)
    print(len(X_train))
    print(len(X_test))
    vectorizer = TfidfVectorizer(stop_words = "english", max_df = 0.7)
    X_train_vectorized = vectorizer.fit_transform(X_train)
    X_test_vectorized = vectorizer.transform(X_test)
    clf = LinearSVC()
    clf.fit(X_train_vectorized, y_train)
    print(clf.score(X_test_vectorized, y_test))
    vectorized_text = vectorizer.transform([text])
    result = clf.predict(vectorized_text)
    return result[0]