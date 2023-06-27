"""
This module contains the SVM model for the fake news detector.
"""
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier

def random_forest_classifier(text: str) -> int:
    # Loading the Dataset
    data = pd.read_csv("src/logic/helper_functionality/news_check/reliability_model/fake_or_real_news.csv")
    print(data)

    # Preprocessing the Labels
    data["fake"] = data["label"].apply(lambda x: 0 if x == "REAL" else 1)

    # Dropping the Label Column
    data = data.drop("label", axis=1)

    # Splitting the Data into Training and Test Sets
    X, y = data["text"], data["fake"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Vectorizing the Text Data
    vectorizer = TfidfVectorizer(stop_words="english", max_df=0.7)
    X_train_vectorized = vectorizer.fit_transform(X_train)
    X_test_vectorized = vectorizer.transform(X_test)

    # Training a Random Forest Classifier
    clf = RandomForestClassifier()
    clf.fit(X_train_vectorized, y_train)

    # Evaluating the Classifier
    print(clf.score(X_test_vectorized, y_test))

    # Making Predictions on New Text
    vectorized_text = vectorizer.transform([text])
    result = clf.predict(vectorized_text)
    print(result)
    return result