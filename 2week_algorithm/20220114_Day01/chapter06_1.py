# 138p, 유효한 팰린드롬 문제

# 알고리즘 문제 풀이를 할 때, 함수로 만들어서 풀어주는 것이 좋음!
def isPalindrome(str):
    #moom

    # i = in order (정방향으로 가는 것)
    # j = in reverse order (거꾸로 가는것)
    isPalin = True
    for i in range(len(str) // 2):
        j = len(str) - i - 1
        if str[i] != str [j]:
            isPalin = False
            break
    print(isPalin)



def isPalindrome2(str):
    isPalin2 = True
    for i in range(len(str) // 2):
        if str[i] != str[-i-1]:
            isPalin2 = False
            break
    print(isPalin2)


# 초기값 예외처리 필요
# 1) 대소문자를 구분하지 않음
# 2) 영문자와 숫자만을 대상으로 함

str = str.lower()



if __name__ == "__main__" :
    # mom, rotator

    isPalindrome("mom")
    isPalindrome("rotator")
    isPalindrome("abcdefg")




# Q1. 유효한 팰린드롬  (p.138)


def isPalindrome(str):
    # moom
    # mom

    # i: in order (0
    # j: in reverse order (2

    # 초기값 예외처리
    # 1) 대소문자를 구분하지 않음
    # 2) 영문자와 숫자만 대상으로 함 (isalnum(), alphabet+number)
    #  1-1) 영문자와 숫자인 문자열만 타겟으로 보겠다 (만약 특수기호가 들어가면 False)
    #  1-2) 만약에 특수기호가 들어가면 특수기호는 무시하고 보겠다
    #       mo,m => palindrome

    str = str.lower()

    i = 0
    j = - i - 1
    isPalin = True
    while True:
        if i + 1 == len(str) // 2 or j + 1 == len(str) // 2:
            break

        if not str[i].isalnum():
            i += 1
        if not str[j].isalnum():
            j -= 1

        if str[i] != str[j]:
            isPalin = False
            break

        i += 1
        j -= 1

    return isPalin


if __name__ == "__main__":
    # mom, rotator, ...
    palin = isPalindrome("m.om")
    print(palin)