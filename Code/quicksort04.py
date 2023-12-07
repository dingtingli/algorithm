def quicksort(A, lo, hi):
    if hi <= lo + M:
        insertionsort(A, lo, hi)
    if lo < hi:
        pivot_index = partition(A, lo, hi)
        quicksort(A, lo, pivot_index - 1)
        quicksort(A, pivot_index + 1, hi)