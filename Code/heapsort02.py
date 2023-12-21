def geti(a, i):
    return a[i - 1]


def seti(a, i, key):
    a[i - 1] = key


def PARENT(i):
    return i // 2


def HEAPMAXIMUM(a):
    return geti(a, 1)


def HEAPEXTRACTMAX(a):
    if len(a) < 1:
        raise ValueError("heap underflow")
    max = geti(a, 1)
    seti(a, 1, geti(a, len(a)))
    a.pop()  # 移除最后一个元素
    MAXHEAPIFY(a, 1, len(a))
    return max


def HEAPINCREASEKEY(a, i, key):
    if key < geti(a, i):  # 注意：Python的数组索引从0开始
        raise ValueError("new key is smaller than current key")
    seti(a, i, key)
    while i > 1 and geti(a, PARENT(i)) < geti(a, i):  # PARENT(i) = i // 2
        exch(a, i, PARENT(i))
        i = PARENT(i)


def MAXHEAPINSERT(a, key):
    a.append(float("-inf"))  # 插入负无穷大
    HEAPINCREASEKEY(a, len(a), key)


def MAXHEAPIFY(a, i, n):
    while True:
        largest = i
        left = 2 * i
        right = 2 * i + 1

        # Check if left child is larger than the current node
        if left <= n and less(a, i, left):
            largest = left

        # Check if right child is larger than the largest node so far
        if right <= n and less(a, largest, right):
            largest = right

        # If the largest node is the current node, break the loop
        if largest == i:
            break

        # Swap the current node with the largest node
        exch(a, i, largest)
        i = largest


def less(a, i, j):
    return a[i - 1] < a[j - 1]


def exch(a, i, j):
    a[i - 1], a[j - 1] = a[j - 1], a[i - 1]


# test
maxPriorityQueue = []
maxPriorityQueueLength = 7
numbers = [8, 4, 2, 6, 5, 9, 3, 10, 7, 1]

for i in range(0, maxPriorityQueueLength):
    MAXHEAPINSERT(maxPriorityQueue, numbers[i])

for i in range(maxPriorityQueueLength, len(numbers)):
    if numbers[i] < HEAPMAXIMUM(maxPriorityQueue):
        HEAPEXTRACTMAX(maxPriorityQueue)
        MAXHEAPINSERT(maxPriorityQueue, numbers[i])

print(maxPriorityQueue)
