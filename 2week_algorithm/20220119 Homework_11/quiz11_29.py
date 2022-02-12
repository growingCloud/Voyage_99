# Chapter11_29. 보석과 돌 (298p)
# 난이도 : ★
# Leet code Num. : 771

# J는 보석이며, S는 갖고 있는 돌이다. S에는 보석이 몇 개나 있을까? (대소문자를 구분한다)
# 예제 1.
# 입력 >> J = "aA", S = "aAAbbbb"
# 출력 >> 3


# 찾고나서 pop하면 S의 길이 자체가 줄어듬
# 그런 방식으로 하면 좀 더 짧아지지 않나 ..?

J = "bA"
S = "aAAbbaaaaAAAaaabb"
count = 0
S_li = list(S)
reset = len(S_li)

for j in list(J):
    s_num = 0
    while s_num < len(S_li):
        if j == S_li[s_num] :
            a = S_li.pop(s_num)
            print(a)
            count += 1
        else:
            s_num += 1

print(count)