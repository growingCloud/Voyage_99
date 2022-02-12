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

nums = [3, 30, 34, 5, 9]

class Solution:
    def largestNumber(self, nums: List[int]) -> str:
        def check_swap(a, b):
            return str(a) + str(b) < str(b) + str(a) # 스왑 한 경우가 더 큰 경우 (True 반환)
        i = 1
        while i < len(nums):
            j = i
            while j > 0 and check_swap(nums[j - 1], nums[j]):
                nums[j - 1], nums[j] = nums[j], nums[j - 1]
                j -= 1
            i += 1
        return str(int(''.join(map(str,nums))))