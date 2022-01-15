# Chapter06_04. 가장 흔한 단어 (151p)
# 난이도 : ★☆
# Leet code Num. : 819

# 금지된 단어를 제외한 가장 흔하게 등장하는 단어를 출력하라. 대소문자 구분을 하지 않으며, 구두점 (마침표, 쉼표) 또한 무시한다.

# 예제 1.
# 입력 >> paragraph = "Bob hit a ball, the hit BALL flew far after it was hit."
#        banned = ["hit"]
# 출력 >> "ball"

from typing import List
import collections
import re

def mostCommonWord(paragraph: str, banned: List[str]) :
    words = [word for word in re.sub(r'^\w', ' ', paragraph)
        .lower().split()
             if word not in banned]

    counts = collections.Counter(words)
    # 가장 흔하게 등장하는 단어의 첫번째 인덱스 리턴
    return counts.most_common(1)[0][0]


paragraph = "Bob hit a ball, the hit BALL flew far after it was hit."
banned = ["hit"]

print(mostCommonWord(paragraph, banned))