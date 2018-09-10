import urllib.request, urllib.error
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.footballchannel.jp/category/hotnews/"
html = urllib.request.urlopen(url)
soup = BeautifulSoup(html, "html.parser")

titles = []
sources = []

contents_title = soup.find_all(class_="contents_title")
for content in contents_title:
  title = content.find_next('a').string
  titles.append(title)

i = 0
indexes = []
themes = []
for _ in range(len(titles)):
  sources.append('フットボールチャンネル')
  themes.append(6)
  i += 1
  indexes.append(i)

df = pd.DataFrame({'index': indexes,
                   'title': titles,
                   'source': sources,
                   'theme': themes})
df = df.set_index('index')

df_origin = pd.read_csv('./datasets/society_sports.csv', index_col=0)

df_new = pd.concat([df_origin, df])
df_new = df_new.drop_duplicates(['title', 'source'])
df_new = df_new.reset_index(drop=True)
df_new.to_csv('./datasets/society_sports.csv', mode="w")
