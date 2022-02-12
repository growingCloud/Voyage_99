# Chapter08_15. 역순 연결 리스트 (219p)
# 난이도 : ★
# Leet code Num. : 206

# 연결 리스트를 뒤집어라
# 예제 1.
# 입력 >> 1->2->3->4->5->NULL
# 출력 >> 5->4->3->2->1->NULL

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self):
        self.nodeCount = 0
        self.head = None
        self.tail = None

    def reverseList(self, head):
        node, prev = head, None

        while node:
            next, node.next = node.next, prev
            prev, node = node, next
        return prev