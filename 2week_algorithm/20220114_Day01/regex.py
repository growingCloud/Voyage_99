# 정규표현식 (regular expression, regex) : 문자열 형식을 확인하는 식
# 언제 사용하는가??
# 웹 개발 (010-1234-1234, a@naver.com)

import re
# search(), findall(), split(), sub()
# \w : alphaber + number
# \d : number
# \s : space character

if __name__ == "__main__" :
    str = "The rain in Spain"
    x = re. search("^The", str)

    print(x)

