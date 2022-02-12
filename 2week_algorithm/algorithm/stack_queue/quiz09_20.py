# Chapter09_20. 유효한 괄호 (245p)
# 난이도 : ★
# Leet code Num. : 20

# 괄호로 된 입력값이 올바른지 판별하라
# 예제 1.
# 입력 >> ()[]{}
# 출력 >> true


# s "[]()"

def is_valid(s) :
    pair = {
        '}': '{',
        ')': '(',
        ']': '[',
    }

    opener = "{[("
    stack = []
    for char in s:
        # 여는 괄호는 스택에 넣고, 닫는 괄호면 비교?
        if char in opener:
            stack.append(char)
        else:
            if not stack:
                return False

            top = stack.pop()   # pop from empty list : 빈 리스트에서는 pop 할 수 없음!
            if pair[char] != top:
                return False

    return not stack


assert is_valid("{}()[]")
assert is_valid("{[]}")
assert is_valid("({[]})")

assert not is_valid("{}]")
assert not is_valid("{{{{{{{}}}}}}")