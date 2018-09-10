import urllib.request, urllib.error
from bs4 import BeautifulSoup
import pandas as pd

urls = ['https://www.nikkei.com/business/', 'https://www.nikkei.com/business/archive/', 'https://www.nikkei.com/economy/', 'https://www.nikkei.com/economy/archive/']

classes = {'ビジネス': 0,'金融・マーケット': 2,'経済・政治': 5,'社会': 6}

for url in urls:
  html = urllib.request.urlopen(url)
  soup = BeautifulSoup(html, "html.parser")

  titles = []
  sources = []

  page_contents = soup.find(id="CONTENTS_MAIN")

  titles_list = soup.select('h3[class*="title"]')

  for title in titles_list:
    titles.append(title.find_next('a').string)

  page_name = soup.find(class_="l-miH11_title").find_next('span').string
  i = 0
  indexes = []
  themes = []
  for _ in range(len(titles)):
    sources.append('日本経済新聞')
    themes.append(classes[page_name])
    i += 1
    indexes.append(i)

  df = pd.DataFrame({'index': indexes,
                     'title': titles,
                     'source': sources,
                     'theme': themes})
  df = df.set_index('index')

  file_names = {'ビジネス': 'business', '経済・政治': 'politics_economics','スポーツ': 'society_sports', '社会': 'society_sports'}

  csv_name = './datasets/{}.csv'.format(file_names[page_name])
  df_origin = pd.read_csv(csv_name, index_col=0)

  df_new = pd.concat([df_origin, df])
  df_new = df_new.drop_duplicates(['title', 'source'])
  df_new = df_new.reset_index(drop=True)
  df_new.to_csv(csv_name, mode="w")

