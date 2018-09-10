import urllib.request, urllib.error
from bs4 import BeautifulSoup
import pandas as pd

urls = ['https://www.businessinsider.jp/politics/', 'https://www.businessinsider.jp/business/', 'https://www.businessinsider.jp/careers/']

classes = [5, 0, 1]

category_id = 0

for url in urls:
  html = urllib.request.urlopen(url)
  soup = BeautifulSoup(html, "html.parser")

  titles = []
  sources = []

  hot_topic = soup.find(class_="p-hotSummaryCard-title").find_next('a').string
  titles.append(hot_topic)

  large_topics = soup.find_all(class_="p-largeSummaryCard-title")
  for large_topic in large_topics:
    large_topic_title = large_topic.find_next('a').string
    titles.append(large_topic_title)

  topics = soup.find_all(class_="p-cardList-cardTitle")
  for topic in topics:
    topic_title = topic.find_next('a').string
    titles.append(topic_title)

  i = 0
  indexes = []
  themes = []
  for _ in range(len(titles)):
    sources.append('Business Insider Japan')
    themes.append(classes[category_id])
    i += 1
    indexes.append(i)

  df = pd.DataFrame({'index': indexes,
                     'title': titles,
                     'source': sources,
                     'theme': themes})
  df = df.set_index('index')

  file_names = {0: 'politics_economics', 1: 'business', 2: 'carrier_education'}

  csv_name = './datasets/{}.csv'.format(file_names[category_id])
  df_origin = pd.read_csv(csv_name, index_col=0)

  df_new = pd.concat([df_origin, df])
  df_new = df_new.drop_duplicates(['title', 'source'])
  df_new = df_new.reset_index(drop=True)
  df_new.to_csv(csv_name, mode="w")

  category_id += 1
