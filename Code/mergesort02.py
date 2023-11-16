def binary_search(arr, x, start, end):
    """Use binary search to find the correct position for x in arr."""
    while start < end:
        mid = (start + end) // 2
        if arr[mid] < x:
            start = mid + 1
        else:
            end = mid
    return start


def optimized_merge(arr, left, mid, right):
    """Optimized merging process to reduce the number of elements that need to be moved."""
    # Find the insertion positions
    left_insert_pos = binary_search(arr, arr[mid + 1], left, mid + 1)
    right_insert_pos = binary_search(arr, arr[mid], mid + 1, right + 1)

    # Determine the smaller part and copy it to a temporary array
    if mid - left_insert_pos + 1 > right_insert_pos - mid - 1:
        # If the right part is smaller
        temp = arr[mid + 1 : right_insert_pos]
        arr_pos = right_insert_pos - 1
        left_pos = mid
        temp_pos = len(temp) - 1

        while temp_pos >= 0:
            if left_pos >= left_insert_pos and arr[left_pos] > temp[temp_pos]:
                arr[arr_pos] = arr[left_pos]
                left_pos -= 1
            else:
                arr[arr_pos] = temp[temp_pos]
                temp_pos -= 1
            arr_pos -= 1
    else:
        # If the left part is smaller
        temp = arr[left_insert_pos : mid + 1]
        arr_pos = left_insert_pos
        right_pos = mid + 1
        temp_pos = 0

        while temp_pos < len(temp):
            if right_pos < right_insert_pos and arr[right_pos] < temp[temp_pos]:
                arr[arr_pos] = arr[right_pos]
                right_pos += 1
            else:
                arr[arr_pos] = temp[temp_pos]
                temp_pos += 1
            arr_pos += 1


arr = [1, 2, 3, 6, 10, 4, 5, 7, 9, 12, 14, 17]
optimized_merge(arr, 0, 4, len(arr) - 1)
# arr = [1, 2, 3, 5, 6, 10, 4, 7, 12, 14, 17]
# optimized_merge(arr, 0, 5, len(arr) - 1)
print("Merged array:", arr)
