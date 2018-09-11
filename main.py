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
@auth.login_required
def predict(clf_file):
    X_train = pd.read_csv('./datasets/x_train.csv')
    wd = WordDividor()
    cv = CountVectorizer(min_df=2, analyzer=wd.extract_words)
    vect = cv.fit(X_train)

    clf = joblib.load("{}.pkl".format(clf_file))
    data = request.json
    bow = vect.transform(data)
    prediction = clf.predict(bow)
    return jsonify({'prediction':prediction.tolist()})


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0')
