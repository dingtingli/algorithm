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


def BUILDMAXHEAP(a):
    n = len(a)
    i = n // 2

    # 从最后一个父节点开始，自底向上维护堆特性
    while i >= 1:
        MAXHEAPIFY(a, i, n)
        i -= 1


def geti(a, i):
    return a[i - 1]


def seti(a, i, key):
    a[i - 1] = key


def HEAPMAXIMUM(a):
    return geti(a, 1)


def FASTHEAPSORT(a):
    # 1. 将所有元素放入有效的最大堆中
    BUILDMAXHEAP(a)

    n = len(a)
    sorted_array = []

    while n >= 1:
        max = HEAPMAXIMUM(a)
        sorted_array.append(max)  # 将最大元素插入到sorted_array
        seti(a, 1, float("-inf"))  # 删除堆顶，创建一个空缺 "V"
        FASTMAXHEAPIFY(a, 1, len(a))  # 比较 V 正下方的两个子堆首领，将最大的那个提升到空缺中
        n -= 1

    return sorted_array[::-1]  # 反转sorted_array并返回


def FASTMAXHEAPIFY(a, i, n):
    while True:
        left = 2 * i
        right = 2 * i + 1

        # 如果没有子节点，直接退出
        if left > n:
            break

        # 默认选择左子节点
        largest = left

        # 如果右子节点存在且大于左子节点，则选择右子节点
        if right <= n and less(a, left, right):
            largest = right

        # 如果当前节点已经是其子树中的最大值，退出循环
        if geti(a, i) >= geti(a, largest):
            break

        exch(a, i, largest)
        i = largest

a = [3, 5, 1, 6, 2, 7, 10, 4, 9, 8]
sort = FASTHEAPSORT(a)
print(sort)