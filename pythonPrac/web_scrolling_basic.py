import requests
from bs4 import BeautifulSoup

# 타겟 URL을 읽어서 HTML를 받아오고,
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=20200303',headers=headers)

# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
# soup이라는 변수에 "파싱 용이해진 html"이 담긴 상태가 됨
# 이제 코딩을 통해 필요한 부분을 추출하면 된다.
soup = BeautifulSoup(data.text, 'html.parser')

title = soup.select_one('#old_content > table > tbody > tr:nth-child(2) > td.title > div > a')
print(title)            # 하나를 불러올 때 사용하는 select_one
print(title.text)       # 그 하나에 있는 텍스트를 콕 찝어서 가져옴
print(title['href'])    # 태그의 속성을 가지고 오고 싶을 때, 딕셔너리인지는 모름.. 만든사람 마음!
print()

# old_content > table > tbody > tr:nth-child(1) > td.title > div > a
# old_content > table > tbody > tr:nth-child(2) > td.title > div > a
# old_content > table > tbody > tr:nth-child(3) > td.title > div > a
# copy selector를 해서 가져오면, 여기서 nth-child(n) 부분이 순위에 따라 바뀌는 것을 확인할 수 있다!
# 따라서 저 부분을 떼어버린다면 (old_content > table > tbody > tr:) 해당하는 값을 전부 가져올 수 있음


trs = soup.select('#old_content > table > tbody > tr')
# 다수를 가져올 때 사용하는 select, 얘는 결과를 리스트로 보여준다

for tr in trs :
    # print(tr) -> tr들이 하나씩 나옴, 그 안에서 제목, 별점 등을 찾으면 OK

    a_tag = tr.select_one('td.title > div > a')
    # tr 까지 찾아놓은 곳에서 또 세부적으로 찾는 과정
    # print(a_tag.text) -> 웹 페이지마다 양식이 달라서, 구분선 때문에 NonType을 text로 가져올 수 없음

    if a_tag is not None :
        title = a_tag.text
        print(title)    # NonType을 제외하고 제목 텍스트만 가져옴
