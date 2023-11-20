
# 归并排序（Merge Sort）：一个被所有教科书嫌弃的算法，我们为什么还要学？

在之前的文章中，我们探讨了插入排序，一个通过扫描整个有序序列来为新元素寻找合适插入点的过程。

现在，我们将转向归并排序（Merge Sort），一种历史可能比电子计算机还要久远的算法，最早在 1945 年由著名计算机科学家冯·诺伊曼提出。

归并排序在许多教科书中被视为基础的话题。然而，往往在对它的优缺点做了简要总结后，便会转向其更加高效的算法，例如快速排序。

它就像一个被人嫌弃的孩子，孤独地躺在角落里，缺乏人们的关注。

那么，我们为什么还要学习归并排序呢？这次我们就来重新审视归并排序，看看它的潜力和价值，或许能让我们有全新的认识。

## 合并过程：有序数组的高效融合

归并排序的核心思想基于两个重要的计算机思维：分治和递归。

特别是递归的使用，它要求我们我们转换常规的思维方式，从下往上倒过来思考问题。

假设我们有两个有序数组，我们的目标是将它们合并成一个大的有序数组。

合并过程包括对两个数组的头部元素进行比较，并将较小的元素移至新数组中。这个过程持续进行，直到所有元素都被合并进新数组，形成一个完全有序的数组。

![动图 归并排序 合并过程](/doc/illustrations/mergesort/mergesort01.gif)

```python
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
```
源代码：[mergesort01](/Code/mergesort01.py)

尽管这种方法能够有效地将两个有序数组合并成一个更大的有序数组，但它并未解决如何对一个无序数组进行排序的问题。

## 分割过程：从无序到有序的过渡

继续沿着合并的思路，如果要对一个无序的数组进行排序，我们首先需要找到两个有序的子数组。

但这里出现了一个新问题：这两个子数组是如何变得有序的？

答案在于，这些子数组也不知道它们是如何变得有序的，而是需要进一步查询它们自身的子数组。

具体来说，就是将原数组不断地被拆分，直到被拆分的子数组有序。

例如，一个含有 8 个元素的数组会被分成两个各含 4 个元素的子数组。这个拆分过程一直持续，直到子数组不能再被分割，也就是说，每个子数组只含有一个元素。

![分割子数组](/doc/illustrations/mergesort/mergesort02.png)

由于单个元素本身就是有序的，因此当两个子数组各自只含有一个元素时，我们可以利用之前的合并方法，将它们合并成一个含有两个元素的有序数组。这个过程持续下去，最终我们可以回答最初的问题：原数组的两个子数组是如何完成排序的。

![合并子数组](/doc/illustrations/mergesort/mergesort03.png)

我们通过递归的方式，来实现上述步骤，最终形成完整的归并排序过程。

![动图 归并排序的实现](/doc/illustrations/mergesort/mergesort0401.gif)

```python
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

```
源代码：[mergesort01](/Code/mergesort01.py)

## 分治算法：归并排序的核心策略

在归并排序中，核心思想是将一个大数组的排序分解为两个更小数组的排序，然后将这些已排序的小数组合并成一个大数组。

这是分治算法是一种常见的方式，通过将复杂问题分解为更小、更易于管理的子问题来解决。

分治算法主要包含三个步骤：分割（divide）、解决（conquer）、合并（combine）。

1. **分割（Divide）**：将原始问题划分为一系列更小的子问题，这些子问题彼此相似但规模更小。
2. **解决（Conquer）**：解决每个子问题。如果子问题足够小，则可以直接求解。否则，可以递归地应用分治策略继续分解。
3. **合并（Combine）**：将所有子问题的解决方案合并成原始问题的解。

在归并排序中，分割步骤将大问题简化为多个小问题，而合并步骤则解决这些小问题并逐步构建出最终问题的解决方案。而解决步骤，由于单个元素本身就是有序的，所以隐式地完成了。

![分治 归并排序](/doc/illustrations/mergesort/mergesort05.png)

分治思想不仅局限于排序算法，它还广泛应用于其他领域，例如 Google 的 MapReduce，它将大规模数据处理任务分配到多台服务器上，然后将各服务器的中间结果汇总到特定服务器上以得到最终结果。

## 优化归并排序：提高效率降低消耗

归并排序的时间复杂度为 O(nlogn)，但由于合并阶段需要临时存储空间来保存中间结果，导致其空间复杂度为 O(n)。对于长度为 n 的数组，所需的临时空间大小与数组长度相同。

![归并排序 合并过程的临时空间](/doc/illustrations/mergesort/mergesort06.png)

*注意：如果对于 O(nlogn) 的算法复杂度不太清楚，可以回顾之前的文章：为什么排序算法的时间复杂度上限是O(n log n)。*

是否有方法减少临时空间的使用呢？这成为了归并算法优化的主要方向。

举例来说，如果我们有两个已排序的数组 [1, 2, 3, 6, 10] 和 [4, 5, 7, 9, 12, 14, 17]，我们的目标是将它们合并。

我们发现：
- 第二个数组中的最小元素（4）必须被添加到第一个数组的第四个位置以保持顺序，
- 而第一个数组中的最大元素（10）必须被添加到第二个数组的第五个位置以保持顺序。

因此，两个数组中的 [1, 2, 3] 和 [12, 14, 17] 已经位于它们的最终位置，不需要移动。需要合并的是 [6, 10] 和 [4, 5, 7, 9]。

现在，我们只需要分配一个大小为 2 的临时数组，将 [6, 10] 复制到其中，然后在原数组中将它们与 [4, 5, 7, 9] 合并。

![动图 归并排序 优化合并过程](/doc/illustrations/mergesort//mergesort07.gif)

我们可以总结归并算法的优化策略：
1. 执行一个二分查找，找到第二个数组中的第一个元素将被插入到第一个数组的位置，以保持其有序性。
2. 再进行一次同样的算法，找到第一个数组中的最后一个元素将被插入到第二个数组的位置，以保持其有序性。
3. 确定在这些位置之前和之后的元素已处于正确位置，无需合并。
4. 将剩余元素较小的数组复制到临时数组中。
5. 根据哪个数组的剩余元素较小，决定合并过程是从前往后还是从后往前进行。

上面的示例展示了从前往后合并的过程，下面的示例演示了另一种情况，即从后往前合并的过程。

![动态图 归并排序 从后往前合并](/doc/illustrations/mergesort/mergesort08.gif)

与传统归并排序相比，这种优化方法减少了元素移动的次数，缩短了运行时间，并减少了临时空间的占用。

```python
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
        temp = arr[mid + 1:right_insert_pos]
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
        temp = arr[left_insert_pos:mid + 1]
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

```
源代码：[mergesort02](/Code/mergesort02.py)

## 总结: 学习的终点在哪里

归并排序的起源可以追溯到冯·诺依曼为EDVAC（电子离散变量自动计算机）撰写的一份创新性手稿。在这份探讨计算机数组应用及其排序问题的文献中，冯·诺依曼首次详细描述了归并排序这一算法。

当时这份手稿被军方标记为“绝密”，而如今，几乎每位学习过算法的计算机工程师都熟悉它。

你有没有思考过，除了学习算法本身，我们还可以从中学到什么呢？

首先，归并排序是理解分治思想和递归思想的优秀入门教材。这两种思想在计算机领域至关重要，掌握它们可以帮助我们用计算机的思维分析和解决问题。

此外，当我们在类库中调用 sort() 方法进行排序时，它通常采用的是TimSort算法——一种结合了插入排序和归并排序的复合型排序算法。在处理大量数据时，其中的归并排序正是我们在本文中讨论的优化版本。

学习过程可以是从具体到抽象，从了解算法的具体实现到理解背后的思想；也可以是从浅入深，不断优化并超越自己。