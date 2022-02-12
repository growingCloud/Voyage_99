# Chapter12_34. 순열 (341p)
# 난이도 : ★★
# Leet code Num. : 46

# 서로 다른 정수를 입력받아 가능한 모든 순열을 리턴하라
# 예제 1.
# 입력 >> [1, 2, 3]
# 출력 >> [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]


# ***** 접근 방식 *****
# 1) 일반적으로 수학문제를 풀때, 순열 문제에서 하나씩 숫자를 고정시켜 놓고 나머지를 곱하여 경우의 수를 계산하는 방법을 활용
# 2) 하나씩 고정 시키는 방법을, 스택에서 하나 꺼내는 걸로 활용할 수 있겠다는 생각이 들었음
# 3) 그래서 숫자와 문자 상관없이 순열 경우의 수를 나타내기 위해 받는 리스트의 인덱스를 활용하여 문제를 풀어보기로 함


# [풀이 1] DFS(깊이 우선 탐색), 스택을 활용한 순열 생성
# 최소 조건, lists 요소 3개 이상, nums 2 이상이어야 동작합니다.
def permute_stack(lists, nums):
    returns = []
    # list(range(len(lists))), 입력받은 lists의 인덱스를 생성합니다.
    idx = [i for i in range(len(lists))]
    print("0. idx: ", idx)


    stack = []
    for i in idx:
        stack.append([i])                           # 빈 스택을(리스트) 하나 생성하여, lists의 인덱스를 스택으로 받습니다. (list 형태로 받음)
    print('1. stack :', stack)

    while len(stack) != 0:
        current = stack.pop()                        # 스택에서 하나씩, 제일 마지막에 들어온 인덱스를 꺼냅니다.
        print('2. curr :', current)

        for i in idx:
            if i not in current:                     # 인덱스 숫자 하나를 고정 시켜놓고 current에서 다음 인덱스를 뽑습니다.
                temp = current + [i]                 # 이 부분때문에 제한 조건이 발생하게 됩니다.
                print('3. temp :', temp)
                print('4. [i] :', [i])

                if len(temp) == nums:                # temp에 넣어놓은 요소들이 내가 뽑고자 하는 갯수와 일치한다면,
                    element = []

                    for t in temp:
                        print('5. lists[t] :', lists[t])
                        print('6. temp :', temp)
                        element.append(lists[t])     # 받아온 인덱스를 다시 문자열로 바꿔준 후


                    returns.append(element)          # temp에 있던 요소를 element에 추가 해 줍니다.
                    print('7. returns :', returns)


                else:
                    stack.append(temp)                # 내가 뽑고자 하는 갯수보다 모자라다면, 다시 연산의 대상으로 보고 stack으로 집어 넣습니다.

    return returns




# [풀이 2] itertools 모듈 사용

import itertools

def permute_itertools(lists):
    return list((itertools.permutations(lists)))



print(permute_stack(['a', 'b', 'c'], 3))
# print(permute_itertools(['a', 'b', 'c']))