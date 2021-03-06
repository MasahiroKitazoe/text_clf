from sklearn.externals import joblib
from flask import Flask, jsonify, request
import pandas as pd
from flask_httpauth import HTTPBasicAuth
from text_clf import WordDividor
from sklearn.feature_extraction.text import CountVectorizer

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "NewsPicksTeamA": "iamgroot33z"
}

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

@app.route('/classify/<string:clf_file>', methods=['POST'])
def predict(clf_file):
    X_train = pd.read_csv('./datasets/x_train.csv', header=None)
    X_train = X_train.iloc[:, 1]
    wd = WordDividor()
    cv = CountVectorizer(analyzer=wd.extract_words)
    vect = cv.fit(X_train)
    X_train = vect.transform(X_train)

    clf = joblib.load("{}.pkl".format(clf_file))
    data = request.json
    data = pd.Series([data['text']])
    bow = vect.transform(data)
    prediction = clf.predict(bow)
    return str(prediction)

@app.route('/', methods=['GET'])
def hello():
    return 'Hello World!! I Love You!!'

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port=80)
