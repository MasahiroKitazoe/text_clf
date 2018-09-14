import urllib.request, urllib.error
from bs4 import BeautifulSoup
import pandas as pd
import time

def get_sponsor_name(lists, sources):
  for element in lists:
    source = element.find_next(class_="sponsor-name").string
    sources.append(source)
    return sources

urls = ['https://newspicks.com/theme-news/technology/', 'https://newspicks.com/theme-news/business/', 'https://newspicks.com/theme-news/economic/', 'https://newspicks.com/theme-news/market/', 'https://newspicks.com/theme-news/education/', 'https://newspicks.com/theme-news/sports/', 'https://newspicks.com/theme-news/innovation/']

for url in urls:

  html = urllib.request.urlopen(url)
  soup = BeautifulSoup(html, "html.parser")

  titles = []
  sources = []

  page_name = soup.find(class_="page-name").string
  right_box = soup.find_all(class_="right-box")
  if not page_name in ['イノベーション', 'ジョブオファー']:
    for element in right_box:
      title = element.find_next('div').string
      titles.append(title)
    for element in right_box:
      source = element.find_next(class_='meta').find_next('div').string
      sources.append(source)

  news_cards = soup.find_all(class_="news-card")
  news_cards_len = len(news_cards)
  for element in news_cards:
    title_link = element.find_next('a')
    title = title_link.find_next(class_="title").string
    titles.append(title)

  publisher_containers = soup.find_all(class_="publisher-container")
  containers_len = len(publisher_containers)
  for element in publisher_containers:
    source = element.find_next('span').string
    sources.append(source)

  if news_cards_len != containers_len:
    sources = get_sponsor_name(soup.find_all(class_="sponsored-container"), sources)

  classes = {'ビジネス': 0, 'キャリア・教育': 1, '金融・マーケット': 2, 'イノベーション': 3, 'ジョブオファー': 4, '政治・経済': 5, '社会・スポーツ': 6, 'テクノロジー': 7}

  i = 0
  indexes = []
  themes = []
  for _ in range(len(titles)):
    themes.append(classes[page_name])
    i += 1
    indexes.append(i)

  df = pd.DataFrame({'index': indexes,
                     'title': titles,
                     'source': sources,
                     'theme': themes})
  df = df.set_index('index')

  file_names = {'テクノロジー': 'technology', 'ビジネス': 'business', '政治・経済': 'politics_economics', '金融・マーケット': 'finance_market', 'キャリア・教育': 'carrier_education', '社会・スポーツ': 'society_sports', 'イノベーション': 'innovation', 'ジョブオファー': 'others'}

  csv_name = './datasets/{}.csv'.format(file_names[page_name])
  df_origin = pd.read_csv(csv_name, index_col=0)

  df_new = pd.concat([df_origin, df])
  df_new = df_new.drop_duplicates(['title', 'source'])
  df_new = df_new.reset_index(drop=True)
  df_new.to_csv(csv_name, mode="w")

  print("カテゴリー「{}」終わり".format(page_name))
  time.sleep(1)
