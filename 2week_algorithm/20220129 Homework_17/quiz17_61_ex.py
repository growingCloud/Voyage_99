# Chapter17_61. 가장 큰 수 (504p)
# 난이도 : ★★
# Leet code Num. : 179

# 항목들을 조합하여 만들 수 있는 가장 큰 수를 출력하라
# 예제 1.
# 입력 >> [10, 2]
# 출력 >> "210"
# 예제 2.
# 입력 >> [3, 30, 34, 5, 9]
# 출력 >> "9534330"

nums = [3, 30, 300, 3000, 34, 5, 9, 95]

class Solution:
    def largestNumber(self, nums: List[int]) -> str:
        li = list(map(str, nums))
        print('1:', li)

        li.sort(reverse = True)
        print('2:',li)
        check = li[:]

        while True: # Thanks to 선주님, 민수님, 재훈님, 태영님
            for i in range(1, len(li)):
                if (li[i-1] + li[i]) < (li[i] + li[i-1]):
                    li[i-1], li[i] = li[i], li[i-1]
                    print('3:', li)
            if check == li :
                break
            else:
                check = li[:]

        print('4:',li)

        answer = str(int(''.join(map(str, li))))

        return answer


