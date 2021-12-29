import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta


headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=20200303',headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')
trs = soup.select('#old_content > table > tbody > tr')

for tr in trs :
    a_tag = tr.select_one('td.title > div > a')

    if a_tag is not None :
        title = a_tag.text
        rank = tr.select_one('td:nth-child(1) > img')['alt']
        star = tr.select_one('td.point').text

        doc = {'rank' : rank, 'title' : title, 'star' : star, }
        db.movies.insert_one(doc)


# 1. 영화제목 '매트릭스'의 평점을 가져오기
target_movie = db.movies.find_one({'title':'매트릭스'})
print (target_movie['star'])

# 2. '매트릭스'의 평점과 같은 평점의 영화 제목들을 가져오기
target_movie = db.movies.find_one({'title':'매트릭스'})
target_star = target_movie['star']

movies = list(db.movies.find({'star':target_star}))

for movie in movies:
    print(movie['title'])

# 3. 매트릭스 영화의 평점을 0으로 만들기
db.movies.update_one({'title':'매트릭스'},{'$set':{'star':'0'}})