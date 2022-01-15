# Chapter06_05. 그룹 애너그램 (153p)
# 난이도 : ★★
# Leet code Num. : 49

# 문자열 배열을 받아 애너그램 단위로 그룹핑하라.
# 예제 1.
# 입력 >> ["eat", "tea", "ate", "nat", "tan", "bat"]
# 출력 >> [ ["ate", "eat", "tea"], ["nat", "tan"], ["bat"] ]

import collections
from typing import List

def groupAnagrams(strs: List[str]):
    anagrams = collections.defaultdict(list)

    for word in strs:
        # 정렬하여 딕셔너리에 추가
        anagrams[''.join(sorted(word))].append(word)
    return list(anagrams.values())

li = ["eat", "tea", "ate", "nat", "tan", "bat"]

print(groupAnagrams(li))
