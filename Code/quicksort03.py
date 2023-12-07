def media_three(arr, lo, mid, hi):
    a, b, c = arr[lo], arr[mid], arr[hi]
    if (a <= b <= c) or (c <= b <= a):
        return mid
    elif (b <= a <= c) or (c <= a <= b):
        return lo
    else:
        return hi