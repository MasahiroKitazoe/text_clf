import urllib.request, urllib.error
from bs4 import BeautifulSoup
import pandas as pd

url = input("スクレイピングしたいページURLを入力: ")
html = urllib.request.urlopen(url)
soup = BeautifulSoup(html, "html.parser")

right_box = soup.find_all(class_="right-box")

titles = []
for element in right_box:
  title = element.find_next('div').string
  titles.append(title)

sources = []
for element in right_box:
  source = element.find_next(class_='meta').find_next('div').string
  sources.append(source)

page_names = []
page_name = soup.find(class_="page-name").string
for _ in range(len(titles)):
  page_names.append(page_name)

df = pd.DataFrame({'title': titles,
                   'source': sources,
                   'theme': page_names})

file_names = {'テクノロジー': 'technology', 'ビジネス': 'business', '政治・経済': 'politics_economics', '金融・マーケット': 'finance_market', 'キャリア・教育': 'carrier_education', '社会・スポーツ': 'society_sports', 'イノベーション': 'innovation', 'ジョブオファー': 'others'}

csv_name = './datasets/{}.csv'.format(file_names[page_name])

df_origin = pd.read_csv(csv_name)

df_new = pd.concat([df_origin, df])

df_new.to_csv(csv_name, mode="w")

# TODO: インデックスの処理を何とかしないと、実行するたびに謎の列が追加されてしまうので、要対処
