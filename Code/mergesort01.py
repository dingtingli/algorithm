def merge(arr, left, mid, right):
    """Merge the left and right subarrays"""
    # Left subarray is [left, mid], right subarray is [mid+1, right]

    # Create a temporary array 'tmp' to store the merged result
    tmp = [0] * (right - left + 1)

    # Initialize indices
    i, j, k = left, mid + 1, 0

    # Compare and copy the smaller element into the temporary array
    while i <= mid and j <= right:
        if arr[i] <= arr[j]:
            tmp[k] = arr[i]
            i += 1
        else:
            tmp[k] = arr[j]
            j += 1
        k += 1

    # Check for any remaining elements
    while i <= mid:
        tmp[k] = arr[i]
        i += 1
        k += 1
    while j <= right:
        tmp[k] = arr[j]
        j += 1
        k += 1

    # Copy the elements from the temporary array 'tmp' back to the original array
    for k in range(0, len(tmp)):
        arr[left + k] = tmp[k]


def merge_sort(arr, left, right):
    """Merge Sort"""
    # Conquer
    if left >= right:
        return  # A single element can be considered as already sorted
    # Divide
    mid = (left + right) // 2  # Divide the array
    merge_sort(arr, left, mid)  # Recursively sort the left subarray
    merge_sort(arr, mid + 1, right)  # Recursively sort the right subarray
    # Merge
    merge(arr, left, mid, right)


arr = [6, 5, 3, 1, 8, 7, 2, 4]
merge_sort(arr, 0, len(arr) - 1)
print("Merged array:", arr)
