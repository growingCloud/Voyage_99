from stack_queue.structures import Node, Stack, Queue


def test_node():
    assert Node(1, None).item == 1   # 노드를 여러개 만들어서 스택에 넣어보겠다는 의미


def test_stack():
    '''
    스택은 3가지 기능을 요구합니다.
    1) push()
    2) pop()
    3) is_empty()
    '''

    stack = Stack()

    stack.push(1)
    stack.push(2)
    stack.push(3)
    stack.push(4)
    stack.push(5)

    assert stack.pop() == 5
    assert stack.pop() == 4
    assert stack.pop() == 3
    assert stack.pop() == 2
    assert stack.pop() == 1
    assert stack.pop() is None  # 아무것도 없을때 없다고 띄워줘야 함
    assert stack.is_empty()


def test_queue():

    queue = Queue()

    queue.push(1)
    queue.push(2)
    queue.push(3)
    queue.push(4)
    queue.push(5)

    assert queue.pop() == 1
    assert queue.pop() == 2
    assert queue.pop() == 3
    assert queue.pop() == 4
    assert queue.pop() == 5
    assert queue.pop() is None  # 아무것도 없을때 없다고 띄워줘야 함
    assert queue.is_empty()

test_node()
test_stack()
test_queue()
