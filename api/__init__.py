import flask

from . import classifier

model = classifier.SpamClassifier()
app = flask.Flask(__name__)
