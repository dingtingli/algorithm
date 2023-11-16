def insertion_sort(arr):
    for i in range(1, len(arr)):
        val = arr[i]
        j = i - 1

        while j >= 0 and arr[j] > val:
            arr[j + 1] = arr[j]  # move
            j -= 1
        arr[j + 1] = val  # insert


arr = [6, 5, 3, 1, 8, 7, 2, 4]
insertion_sort(arr)

print(arr)
