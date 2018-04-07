import sys
import os
import shutil
import pickle
import numpy as np
import pandas as pd
from sklearn.externals import joblib
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import SelectFromModel
from sklearn.feature_extraction.text import TfidfVectorizer
import sys
sys.path.append('./classifier')
import string
import re
import json

import nltk
from nltk.stem.porter import *
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer as VS
from textstat.textstat import *
#---------------------------------------------------------------------------
import time
import traceback

from flask import Flask, request, jsonify
import pandas as pd
from sklearn.externals import joblib

import classifier 
from classifier import tokenize, preprocess


app = Flask(__name__)


model_columns = None

print "Loading trained classifier... "
model = joblib.load('./classifier/final_model.pkl')

print "Loading other information..."
tf_vectorizer = joblib.load('./classifier/final_tfidf.pkl')
idf_vector = joblib.load('./classifier/final_idf.pkl')
pos_vectorizer = joblib.load('./classifier/final_pos.pkl')


@app.route('/predict', methods=['POST'])
def predict():
    if model:
        try:
            samples = [request.get_json()['text']]
            sample_predictions = classifier.get_predictions(samples, model, tf_vectorizer, idf_vector, pos_vectorizer)
            predictions = [classifier.class_to_name(sample_predictions[i]) for i in range(len(sample_predictions))]
            return jsonify({'predictions': predictions})

        except Exception, e:
            return jsonify({'error': str(e), 'trace': traceback.format_exc()})
    else:
        return 'You need to load your model first'


if __name__ == '__main__':
    try:
        port = int(sys.argv[1])
    except Exception, e:
        port = 80

    app.run(host='0.0.0.0', port=port, debug=True)
