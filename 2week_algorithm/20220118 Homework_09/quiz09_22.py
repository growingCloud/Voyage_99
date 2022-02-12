# Chapter09_22. 일일 온도 (252p)
# 난이도 : ★★
# Leet code Num. : 739

# 매일의 화씨 온도 (F) 리스트 T를 입력 받아서, 더 따뜻한 날씨를 위해서는 며칠을 더 기다려야 하는지를 출력하라
# 예제 1.
# 입력 >> T = [73, 74, 75, 71, 69, 72, 76, 73]
# 출력 >> [1, 1, 4, 2, 1, 1, 0, 0]

T = [73, 74, 75, 71, 69, 72, 76, 73]
answer = []

class Node :
    def __init__(self, item, next):
        self.item = item
        self.next = next


class Stack:
    def __init__(self):
        self.top = None

    def push(self, value):
        self.top = Node(value, self.top)

    def pop(self):
        if self.top in None:
            return None

        topNode = self.top
        self.top = self.top.next
        return topNode.item

    def is_empty(self):
        return self.top is None


