from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pandas as pd
import numpy as np
import MeCab
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.externals import joblib


class WordDividor:
    INDEX_CATEGORY = 0
    INDEX_ROOT_FORM = 6
    TARGET_CATEGORIES = ["名詞", " 動詞",  "形容詞", "副詞", "連体詞", "感動詞"]

    def __init__(self, dictionary="mecabrc"):
        self.dictionary = dictionary
        self.tagger = MeCab.Tagger(self.dictionary)

    def extract_words(self, text):
        if not text:
            return []

        words = []

        node = self.tagger.parseToNode(text)
        while node:
            features = node.feature.split(',')

            if features[self.INDEX_CATEGORY] in self.TARGET_CATEGORIES:
                if features[self.INDEX_ROOT_FORM] == "*":
                    words.append(node.surface)
                else:
                    # prefer root form
                    words.append(features[self.INDEX_ROOT_FORM])

            node = node.next

        return words

if __name__ == '__main__':

  df_business = pd.read_csv('./datasets/business.csv', index_col=0)
  df_carrier_edu = pd.read_csv('./datasets/carrier_education.csv', index_col=0)
  df_finance_market = pd.read_csv('./datasets/finance_market.csv', index_col=0)
  df_politics_economics = pd.read_csv('./datasets/politics_economics.csv', index_col=0)
  df_society_sports = pd.read_csv('./datasets/society_sports.csv', index_col=0)
  df_technology = pd.read_csv('./datasets/technology.csv', index_col=0)
  df_innovation = pd.read_csv('./datasets/innovation.csv', index_col=0)
  df_others = pd.read_csv('./datasets/others.csv', index_col=0)

  df = pd.concat([df_business, df_carrier_edu, df_finance_market, df_innovation, df_others, df_politics_economics, df_society_sports, df_technology])

  df = df.reset_index(drop=True)

  df = df.drop_duplicates(['title', 'source'])

  df['data'] = df['title'] + ' ' + df['source']

  text_data = df['data']
  text_target = df['theme']

  X_train, X_test, y_train, y_test = train_test_split(text_data, text_target, test_size=0.20, random_state=0)

  X_train.to_csv('./datasets/x_train.csv', mode="w")

  wd = WordDividor()
  cv = CountVectorizer(min_df=2, analyzer=wd.extract_words)

  vect = cv.fit(X_train)
  X_train = vect.transform(X_train)

  param_grid = {'C': [0.001, 0.01, 0.1, 1, 10, 100, 1000]}
  grid = GridSearchCV(LogisticRegression(), param_grid, cv=5)
  grid.fit(X_train, y_train)
  print(grid.best_score_)
  print(grid.best_params_)

  X_test = vect.transform(X_test)
  print(grid.score(X_test, y_test))

  joblib.dump(grid, 'text_logreg.pkl')

  sample = ['無所属・小川淳也氏、立憲会派入り表明', '大坂なおみの優勝にブーイング　２０歳の新女王が涙の謝罪「こんな終わり方ですみません」']
  sample = vect.transform(sample)
  print(grid.predict(sample))
