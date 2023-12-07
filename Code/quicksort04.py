def partition(arr, low, high):
    pivot = arr[low]
    i = low
    j = high + 1

    while True:
        i += 1
        while i <= high and arr[i] < pivot:
            i += 1

        j -= 1
        while arr[j] > pivot:
            j -= 1

        if i > j:
            break

        arr[i], arr[j] = arr[j], arr[i]

    arr[low], arr[j] = arr[j], arr[low]

    return j


def insertionsort(arr, low, high):
    for i in range(low, high + 1):
        val = arr[i]
        j = i - 1

        while j >= 0 and arr[j] > val:
            arr[j + 1] = arr[j]  # move
            j -= 1
        arr[j + 1] = val  # insert


def quicksort(A, lo, hi):
    M = 5
    if hi <= lo + M:
        insertionsort(A, lo, hi)
    if lo < hi:
        pivot_index = partition(A, lo, hi)
        quicksort(A, lo, pivot_index - 1)
        quicksort(A, pivot_index + 1, hi)


arr = [4, 2, 6, 5, 3, 9, 7]
quicksort(arr, 0, len(arr) - 1)
print(arr)