# ★ 오늘 하루도 열공하는 하루 되세요 ★ - 작성자 5기 D반 8조 구름

# Chapter06_01. 유효한 팰린드롬 (138p)
# 난이도 : ★
# Leet code Num. : 125

# 주어진 문자열이 팰린드롬인지 확인하라. 대소문자룰 구분하지 않으며, 영문자와 숫자만을 대상으로 한다.
# 예제 1.
# 입력 >> "A man, a plan, a canal: Panama"
# 출력 >> true
# 예제 2.
# 입력 >> "race a car"
# 출력 >> false

import re

def isPalindrome(s: str) -> bool :
    s = s.lower()
    # 정규식으로 불필요한 문자 필터링
    s = re.sub('[^a-z@0-9]', '', s)

    return s == s[::-1] # 슬라이싱


print(isPalindrome("A man, a plan, a canal: Panama"))
print(isPalindrome("race a car"))