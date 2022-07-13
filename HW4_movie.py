import requests
from bs4 import BeautifulSoup
import sqlite3

conn = sqlite3.connect('movie_info.db')
"""
conn.execute('''CREATE TABLE MOVIE_INFO
(MOVIE_CHINESE_NAME TEXT    NOT NULL,
MOVIE_FOREIGN_NAME  TEXT    NOT NULL,
COMING_TIME         TEXT    NOT NULL);''')
"""
movie = conn.cursor()

response = requests.get("https://movies.yahoo.com.tw/movie_intheaters.html")

soup = BeautifulSoup(response.text, 'lxml')
info_items = soup.find_all('div', 'release_info')
for item in info_items:
    name = item.find('div', 'release_movie_name').a.text.strip()
    english_name = item.find('div', 'en').a.text.strip()
    release_time = item.find('div', 'release_movie_time').text.strip()
    movie.execute('INSERT INTO MOVIE_INFO VALUES(?,?,?)', (name,english_name,release_time))
    print('{}({}) 上映日：{}'.format(name, english_name, release_time))


