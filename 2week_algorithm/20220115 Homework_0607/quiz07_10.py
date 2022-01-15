# Chapter07_10. 배열 파티션 1 (190p)
# 난이도 : ★
# Leet code Num. : 561

# n개의 페어를 이용한 min(a, b)의 합으로 만들 수 있는 가장 큰 수를 출력하라.
# 예제 1.
# 입력 >> [1, 4, 3, 2]
# 출력 >> 4

li = [1, 4, 3, 2]


def pairSum(numbers):
    numbers = list(numbers)
    numbers.sort()
    pair_li = []
    sums = 0

    for n in numbers:
        pair_li.append(n)
        if len(pair_li) == 2:
            sums += min(pair_li)
            pair_li = []

    return sums


print(pairSum(li))

