import requests
from bs4 import BeautifulSoup

page = requests.get('https://www.mlb.com/reds/schedule/2020-03')

html = BeautifulSoup(page.text, 'lxml')

schedule_table = html.find('table', attrs={'class': 'grid-calendar-day-cells-table'})

print(html)