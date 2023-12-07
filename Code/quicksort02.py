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


def quicksort(arr, low, high):
    if low < high:
        pivot_index = partition(arr, low, high)
        quicksort(arr, low, pivot_index - 1)
        quicksort(arr, pivot_index + 1, high)


arr = [4, 2, 6, 5, 3, 9]
# arr = [3, 3, 3]
quicksort(arr, 0, len(arr) - 1)
print(arr)