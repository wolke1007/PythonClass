import requests
from bs4 import BeautifulSoup
import sqlite3

#conn = sqlite3.connect('movie_info.db')
"""
conn.execute('''CREATE TABLE MOVIE_INFO
(MOVIE_CHINESE_NAME TEXT    NOT NULL,
MOVIE_FOREIGN_NAME  TEXT    NOT NULL,
COMING_TIME         TEXT    NOT NULL);''')
"""
#movie = conn.cursor()
movie_name = "中文片名:"
movie_eng_name = "英文片名:"
movie_res_time = "上映日期:"
response = requests.get("https://movies.yahoo.com.tw/movie_intheaters.html")
movie_list=[{}]
soup = BeautifulSoup(response.text, 'lxml')
info_items = soup.find_all('div', 'release_info')
for item in info_items:
    name = item.find('div', 'release_movie_name').a.text.strip()
    english_name = item.find('div', 'en').a.text.strip()
    release_time = item.find('div', 'release_movie_time').text.split('：')[1].strip()
    movie_info = dict(movie_name = name, movie_eng_name = english_name, movie_res_time = release_time)
    movie_list.append(movie_info)
#    movie.execute('INSERT INTO MOVIE_INFO VALUES(?,?,?)', (name,english_name,release_time))
#    conn.commit()
#    print('{}({}) 上映日：{}'.format(name, english_name, release_time))

print(movie_list)

