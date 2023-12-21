def maxheapify(a, i, n):
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


def build_maxheap(a):
    n = len(a)
    i = n // 2

    # Bottom-up maintenance of heap
    # starting from the last parent node
    while i >= 1:
        maxheapify(a, i, n)
        i -= 1


def heapsort(a):
    # Step 1: Build a max heap
    build_maxheap(a)

    n = len(a)
    while n >= 2:
        # Step 2: Swap the first and last element
        exch(a, 1, n)
        n -= 1
        # Step 3: Rebuild the max heap
        maxheapify(a, 1, n)


a = [3, 5, 1, 6, 2, 7, 10, 4, 9, 8]
heapsort(a)
print(a)