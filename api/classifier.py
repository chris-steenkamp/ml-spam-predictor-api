import os
import pickle
import random
import traceback


class SpamClassifier(object):
    def __init__(self, model_path="spam.model"):
        self.__model_path = model_path
        self.model = None
        self.cls = None

        self.load_model()

    @staticmethod
    def save_object(obj, filename):
        with open(filename, "wb") as f:
            pickle.dump(obj, f)

    def train_model(self, training_data="spam.csv"):
        from sklearn.feature_extraction.text import CountVectorizer
        from sklearn.naive_bayes import MultinomialNB
        from sklearn.model_selection import train_test_split
        import pandas as pd
        
        df = pd.read_csv(training_data, encoding="latin-1")
        df.drop(['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], axis=1, inplace=True)
        df['label'] = df['v1'].map({'ham': 0, 'spam': 1})
        x = df['v2']
        y = df['label']
        self.model = CountVectorizer()
        x = self.model.fit_transform(x)  # Fit the Data

        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)
        # Naive Bayes Classifier
        self.cls = MultinomialNB()
        self.cls.fit(x_train, y_train)
        self.cls.score(x_test, y_test)

    def load_model(self):
        try:
            model_path = f"{self.__model_path}.mdl"
            classifier_path = f"{self.__model_path}.cls"
            if os.path.exists(model_path) and os.path.exists(classifier_path):
                from sklearn.feature_extraction.text import CountVectorizer
                from sklearn.naive_bayes import MultinomialNB

                with open(model_path, "rb") as f:
                    self.model = pickle.load(f)

                with open(classifier_path, "rb") as f:
                    self.cls = pickle.load(f)
            else:
                self.train_model()
                SpamClassifier.save_object(self.cls, f"{self.__model_path}.cls")
                SpamClassifier.save_object(self.model, f"{self.__model_path}.mdl")
        except Exception as e:
            self.cls = None
            self.model = f"{e}\n{traceback.format_exc()}"


    def predict(self, data):
        if self.cls is not None:
            v = self.model.transform(data).toarray()
            return int(self.cls.predict(v))

        return self.model


class TestSpamClassifier(object):
    def __init__(self, model_path=".\\spam.model"):
        self.__model_path = model_path
        self.model = None
        self.cls = None

        self.load_model()

    def train_model(self, training_data="spam.csv"):
        self.model = "trained model"
        self.cls = "trained classifier"

    def load_model(self):
        self.train_model()

    def predict(self, data):
        return random.choice(["spam", "not spam"])
