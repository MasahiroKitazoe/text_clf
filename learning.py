from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pandas as pd
import numpy as np
import requests

iris = datasets.load_iris()
X = pd.DataFrame(iris.data, columns=["sepal_length", "sepal_width", "petal_length", "petal_width"])
y = iris.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=0)

clf = LogisticRegression()
clf.fit(X_train, y_train)

from sklearn.externals import joblib
joblib.dump(clf, 'iris_logreg.pkl')
joblib.dump(["sepal_length", "sepal_width", "petal_length", "petal_width"], 'iris_logreg_cols.pkl')



