# 插入排序（Insertion Sort），使用频率最高的排序算法

想象你在玩麻将或扑克，每次抽牌后都会把新牌插入到手中已经排好序的牌堆中。这个直观的过程与插入排序算法很像。

在插入排序中，初始状态下我们假定数组的第一个元素是已排序的，从第二个元素开始，将每个元素依次插入到正确的位置，重复这个过程，直至数组完全有序。

![动图 插入排序](/doc/illustrations/Insertionsort/insertionsort01.gif)

插入排序操作的核心在于两点：**比较**和**移动**。

**通过比较，我们能够确定新元素的插入点；通过移动，我们为新元素的插入腾出空间。**

## 插入排序复杂度分析

在最坏情况下，即数组完全逆序，第 `n` 个元素可能需要与前面所有 `n-1` 个元素比较才能找到自己的位置，比较次数达到 `1+2+3+...+n-1 = (n-1)(n)/2` 次，复杂度为 `O(n^2)`。

同样地，移动操作此时也是如此。插入第 `n` 个元素，需要移动 `n-1` 个元素，因此总的移动次数也是 `O(n^2)`。

然而，在最佳情况下，即数组已经有序，插入排序则非常高效，每次仅需进行一次比较，总比较次数为 `n-1` 次，复杂度为 `O(n)`，而且无需移动任何元素。

![算法复杂度 O(n^2) O(nlogn) O(n)](/doc/illustrations//Insertionsort/insertionsort09.png)

## 插入排序优势

虽然插入排序的理论时间复杂度为 `O(n^2)`，并不如 `O(nlogn)` 的高效排序算法，但得益于其简洁的操作，在小规模数据集上的表现通常非常出色。


快速排序等 `O(nlogn)` 级别的算法，虽然在大规模数据集上效率高，但涉及的基本操作更多。**当处理的数据量小的时候，`n^2` 与 `nlogn` 之间的差距不大，复杂度不占主导作用，每轮的单元操作数量起到决定性因素。**

现在来看看简洁的插入排序算法的实现：

```python
def insertion_sort(arr):

    for i in range(1, len(arr)):
        val = arr[i]
        j = i - 1

        while j >= 0 and arr[j] > val:
            arr[j + 1] = arr[j]  # move
            j -= 1
        arr[j + 1] = val  # insert
```

源代码：[insertionsort01](/Code/insertionsort01.py)

## 插入排序中确定的移动次数

这里有一个有趣的结论：插入排序中移动元素的次数与数组中逆序对的数量相等。

这个结论初看上去不太好理解，我们考虑一个数组 `[4,2,3,1]`，从中可以找出以下六个数据对：`(4,2)`，`(4,3)`，`(4,1)`，`(2,3)`，`(2,1)`，`(3,1)`。

![动图 数据对](/doc/illustrations//Insertionsort/insertionsort03.gif)

在这些数据对中，除了 `(2,3)` 是正序对之外，其他都是逆序对。

![动图 正序对和逆序对](/doc/illustrations//Insertionsort/insertionsort04.gif)

- 当数字 `2` 被处理时，它移动到 `4` 的前面，消除了逆序对 `(4,2)`。
- 当数字 `3` 被处理时，它移动到 `4` 的前面，消除了逆序对 `(4,3)`
- 当数字 `1` 被处理时，它移动到每一个数字的前面，消除了逆序对 `(4,1)`、`(3,1)` 和 `(2,1)`。

![动图 移动减少倒序对](/doc/illustrations//Insertionsort/insertionsort05.gif)

每次移动都改变了两个逆序的元素的位置，相当于减少了一个逆序对。

**因此对于一个给定的数组，移动的总次数在插入排序开始前就已经固定了。**

## 插入排序的优化

既然移动次数是固定的，那么我们可以尝试从减少比较次数的角度来优化插入排序。

在插入排序中，数据被分为已排序部分和未排序部分。在已排序部分，我们寻找未排序部分下一个元素的正确位置时，通常会用到线性查找。

然而，**一个优化手段是利用二分查找法，在已排序的序列中寻找插入点。**

通过这种方式，我们可以将单次插入的比较次数降至 `O(log n)`，总的比较次数减少至 `O(nlog n)`。然而，由于移动操作的次数保持不变，整个算法的时间复杂度仍为 `O(n^2)`。

尽管如此，对于小规模的数据集而言，这样的优化是有益的，可以明显提高排序效率。

![动图 二分查找插入位置](/doc/illustrations//Insertionsort/insertionsort06.gif)

插入排序的一个重要特性是其稳定性。例如，在序列 `[4a, 4b, 3, 5]` 中，即使 `4a` 和 `4b` 的值相等，它们在排序后也应保持原有顺序。

使用普通的二分查找可能会破坏这一稳定性，因为它可能会无视相同元素的原始顺序。

**为了维护稳定性，我们对二分查找进行调整，确保遇到相等元素时总是将搜索范围移至右侧。** 这保证了我们可以定位到相等元素中最右侧的位置，并将新元素插入其后。

采用这种方法，我们可以得到一种**稳定的二分插入排序算法（stable binary insertion sort）**。

稳定的二分插入排序算法代码实现：

```python
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
```

源代码：[insertionsort02](/Code/insertionsort02.py)


## 总结

优化后的算法，以其在处理小型数据集时的卓越性能，已被集成到 `TimSort` 复合排序算法中。考虑到 `TimSort` 是众多编程语言默认的 `sort()` 方法算法，这种稳定的二分插入排序算法可能是世界上应用最普遍的排序算法之一。
