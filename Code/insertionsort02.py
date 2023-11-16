def binary_search(arr, val, start, end):
    while start <= end:
        mid = (start + end) // 2
        if arr[mid] < val:
            start = mid + 1
        elif arr[mid] > val:
            end = mid - 1
        else:  # arr[mid] == val
            start = mid + 1  # move to right for stability

    return start


def insertion_sort(arr):
    for i in range(1, len(arr)):
        selected = arr[i]
        j = i - 1

        # find location where selected should be inserted
        loc = binary_search(arr, selected, 0, j)

        # Move all elements after location to create space
        while j >= loc:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = selected


arr = [6, 5, 3, 1, 8, 7, 2, 4]
insertion_sort(arr)

print(arr)
