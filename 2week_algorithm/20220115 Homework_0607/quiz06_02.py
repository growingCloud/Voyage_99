# Chapter06_02. 문자열 뒤집기 (145p)
# 난이도 : ★
# Leet code Num. : 344

# 문자열을 뒤집는 함수를 작성하라. 입력값은 문자 배열이며, 리턴없이 리스트 내부를 직접 조작하라.
# 예제 1.
# 입력 >> ["h", "e", "l", "l", "o"]
# 출력 >> ["o", "l", "l", "e", "h"]
# 예제 2.
# 입력 >> ["H", "a", "n", "n", "a", "h"]
# 출력 >> ["h", "a", "n", "n", "a", "H"]


from typing import List
# 이거 왜 안돼 ....?!?!?!?!?!?!?!?!?!?!?!?!?!?!?!?!?!?!?!?!?!!?!?

# 2) 파이썬 함수 사용
def reverseString2(s: List[str]) -> None :
    s.reverse()

# 1) 투포인터 스왑
def reverseString(s: List[str]) -> None :
    left, right = 0, len(s) -1
    while left < right :
        s[left], s[right] = s[right], s[left]
        left += 1
        right -= 1


question = ["h", "e", "l", "l", "o"]

print(reverseString(question))
print(reverseString2(question))