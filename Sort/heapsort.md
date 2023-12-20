# 堆排序（HeapSort）

## 1. 完全二叉树 

二叉树（Binary tree）是一种特殊的数据结构。在这种结构中，每个节点都有两个子节点，通常被称为“左子树”和“右子树”。

![二叉树](/doc/illustrations//Heapsort/heapsort01.png)

在这种数据结构中，每个节点都有指向其父节点、左右子节点的三个指针。

当一棵二叉树的特性满足以下条件时，它被称为完全二叉树（Complete Binary Tree）：

- 除最底层外，其他层的节点数均已满。
- 最底层的节点都集中在左侧。

![完全二叉树](/doc/illustrations//Heapsort/heapsort02.png)

与普通的二叉树不同，完全二叉树可以使用数组进行隐式表示，无需使用指针。

这种表示方法是将树上的所有节点按顺序存放在数组中。节点间的关系可以通过其在数组中的位置来确定。

![完全二叉树数组结构](/doc/illustrations//Heapsort/heapsort03.png)

例如，根节点存放在数组的第 `1` 位置，其左右子节点分别位于 `2` 和 `3` 位置。对于任意位置 `i` 的节点，其父节点和子节点的位置可以通过以下公式计算：

```js
  Parent = i / 2
  Left = 2 * i
  Right = 2 * i + 1
```

其中，Parent 表示节点 `i` 的父节点位置，Left 和 Right 分别表示其左子节点和右子节点的位置。

![完全二叉树数组节点公式](/doc/illustrations//Heapsort/heapsort05.png)

以图中的数组为例，当 `i=4` 时，我们可以直接计算出其父节点和两个子节点的位置。

![完全二叉树数组节点 i=4](/doc/illustrations//Heapsort/heapsort04.png)

最后，我们来思考一个问题：

我们选择从数组的第 `1` 位置开始存储完全二叉树的节点。这种方式确实使得节点关系的计算变得直观和简单。但我们都知道，传统的数组索引是从 `0` 开始的。那么，如何在实际编程中实现这种存储方式呢？

## 2. 堆

堆是一种特殊的完全二叉树，它满足一个关键特性：

**每个父节点的值都大于或等于其子节点的值。** 这意味着在堆的数组表示中，最大的元素总是位于根节点。

![最大堆](/doc/illustrations//Heapsort/heapsort06.png)

这种堆被称为最大堆（Max Heap）。而如果每个父节点的值都小于或等于其子节点，那么这样的堆就是最小堆（Min Heap）。

在本文中，我们将重点讨论最大堆。

**如何维护最大堆的特性？**

当一个子节点的值大于其父节点，这就违反了最大堆的特性。此时，我们需要交换这两个节点。

![动图 节点交换](/doc/illustrations//Heapsort/heapsort07.gif)

如果一个节点的左右子树都是最大堆，但该节点的值小于其子节点，该如何操作？

例如，节点 `i` 的左右子树都是最大堆，但节点 `i` 的值小于其子节点。为了解决这个问题，我们可以让节点 `i` 在堆中“逐级下降”，直至找到合适的位置。

![动图 堆中节点逐级下降](/doc/illustrations//Heapsort/heapsort08.gif)

将上述的“逐级下降”过程转化为代码是一个有趣的挑战，你可以先思考一下如何实现。文章末尾是我为维护最大堆特性编写的函数，以供参考。

最后，让我们深入思考一个问题：

面对一个随机数组，如果左右子树都不满足最大堆特性，如何将其转化为最大堆？

这不仅是理论上的问题，也是很多算法，如堆排序的基础。期待你的深入思考和实现！

```python
def MAXHEAPIFY(a, i, n):
     # Maintains the max-heap property for the given array.
    while True:
        largest = i
        left = 2 * i
        right = 2 * i + 1

        # Check if left child is larger than the current node
        if left <= n and less(a, i, left):
            largest = left

        # Check if right child is larger than the largest node so far
        if right <= n and less(a, largest, right):
            largest = right

        # If the largest node is the current node, break the loop
        if largest == i:
            break

        # Swap the current node with the largest node
        exch(a, i, largest)
        i = largest

def less(a, i, j):
     # Returns True if element at index i is less than element at index j.
    return a[i - 1] < a[j - 1]


def exch(a, i, j):
    # Swaps elements at indices i and j in the array.
    a[i - 1], a[j - 1] = a[j - 1], a[i - 1]
```

在上一篇文章中，我们提到了从数组的第 `1` 位置开始存储完全二叉树的节点，而传统数组索引是从 `0` 开始。这个问题的答案其实隐藏在 `less` 和 `exch` 函数中。

通过调整索引 `i - 1` 和 `j - 1`，我们实现了从 `1` 开始的直观存储方式，同时避免了浪费数组的第 `0` 位置。

## 3. 如何建立最大堆

上一篇文章，我们留下了一个问题：

面对一个随机数组，如何将其转化为最大堆？

回顾上一篇文章，最大的贡献就是实现了维护最大堆特性的 `MAXHEAPIFY` 函数。

![动图 逐级下降维护最大堆](/doc/illustrations//Heapsort/heapsort08.gif)

所以问题的答案是：我们可以从数组的最后一个父节点开始，自底向上地使用维护堆特性的 `MAXHEAPIFY` 函数，从而将任意排序的数组转换成最大堆。

为了实现这个思路，首先需要确定完全二叉树的最后一个父节点。回顾我们之前提到的位置 `i` 父节点和字节的计算公式:

```js
  Parent = i / 2
  Left = 2 * i
  Right = 2 * i + 1
```

当节点 `i = n/2` 时，其左子节点为 `left = 2 * (n/2) = n`，而 `n` 即数组中的最后一个元素。

因此，完全二叉树的最后一个父节点的位置为 `n/2`。

![完全二叉树的最后一个父节点](/doc/illustrations//Heapsort/heapsort09.png)

接下来，我们从最后一个父节点开始，自底向上地对每个父节点调用维护堆特性的 `MAXHEAPIFY` 函数。这样，我们可以逐步将任意排序的数组转换为满足最大堆特性的数组。

![动图 建立最大堆](/doc/illustrations//Heapsort/heapsort10_1.gif)

如何将这个过程转化为代码呢？你可以先尝试自己实现，然后再参考下面的函数：

```python
def BUILDMAXHEAP(a):
    n = len(a)
    i = n // 2

    # 从最后一个父节点开始，自底向上维护堆特性
    while i >= 1:
        MAXHEAPIFY(a, i, n)
        i -= 1
```

在这篇文章中，我们学习了如何从一个随机数组构建最大堆。通过自底向上的方法和调用维护堆特性的 `MAXHEAPIFY` 函数，我们可以有效地将任意数组转化为最大堆。

在下篇文章中，我们将进一步探讨如何利用最大堆。

## 4. 堆排序算法

上一篇文章中，我们成功地实现了建立最大堆的 `BUILDMAXHEAP` 函数，这为我们提供了一个有效的方法将任意数组转化为最大堆。

回顾最大堆的核心特性：每个父节点的值都大于或等于其子节点的值。 这确保了在堆的数组表示中，最大的元素始终位于根节点。

![最大堆示意图](/doc/illustrations//Heapsort/heapsort11.png)

现在，我们将利用这个特性和 `BUILDMAXHEAP` 函数来实现堆排序。

1. **建立最大堆：** 使用 `BUILDMAXHEAP` 函数将任意数组转化为最大堆。

2. **找到最大元素并交换：** 最大的元素始终位于数组的第一个位置，将数组的第一个元素与最后一个元素交换。

3. **重建最大堆：** 排除最后一个元素，并在剩余的元素中重新构建最大堆。

![动图 重建最大堆示意图](/doc/illustrations//Heapsort/heapsort12.gif)

1. **重复上述过程：** 继续交换、排除和重建，直到堆的大小为 2。

因为对于只有两个节点的堆，我们可以直接通过 `MAXHEAPIFY` 函数完成排序，再进一步交换即可完成排序。

![动图 堆排序过程示意图](/doc/illustrations//Heapsort/heapsort13.gif)

如何将上述过程转化为代码呢？以下是我为堆排序编写的函数，你可以先尝试自己实现，然后再参考：

```python
def HEAPSORT(a):
    # Step 1: Build a max heap
    BUILDMAXHEAP(a)

    n = len(a)
    while n >= 2:
        # Step 2: Swap the first and last element
        exch(a, 1, n)
        n -= 1
        # Step 3: Rebuild the max heap
        MAXHEAPIFY(a, 1, n)
```

尽管堆排序在理论上很有吸引力，但在实际应用中，它往往不如快速排序高效。

这是因为堆排序在数组中的大范围跳跃可能导致缓存命中率降低。而快速排序，由于其连续的数据访问模式，更适合现代计算机的缓存系统。

但这并不意味着堆没有价值。作为一种数据结构，堆在其他场景，如优先队列中，仍然发挥着关键作用。

## 5. 优先队列 Priority Queue

在我们之前的探讨中，我们了解了堆的基本概念和堆排序。但实际上，堆最常见的使用场景并不是排序，而是实现优先队列。

设想一下：要在一个存有10亿个数的文件中找出最小的100万个数，如何高效地实现？

直接对10亿个数进行排序显然不是最佳选择，因为这样的规模会带来巨大的计算和存储压力。这时，最大堆（一种特殊的完全二叉树，其中每个节点的值都大于或等于其子节点的值）就派上了用场。

具体方法如下：

1. 读取文件中的前100万个数，并构建一个最大堆。
2. 继续读取文件中的数，对于每一个数：

    a. 如果该数大于堆顶元素，忽略它。

    b. 如果该数小于堆顶元素，移除堆顶元素，并将新数加入堆中。
3. 读完文件后，堆中的100万个数即为所需的最小的100万个数。

![动图 优先队列过程示意图](/doc/illustrations//Heapsort/heapsort16.gif)

这种利用最大堆来找出最小的N个数的方法，实际上就是利用了一种叫做“优先队列”的数据结构。

传统的队列遵循先进先出的原则，而优先队列则不同：它允许基于优先级的顺序出队。**在最大优先队列中，优先级最高的元素首先被移除，然后是次高的，以此类推。**

优先队列在现实生活中有广泛的应用。例如，计算机系统中，多个任务需要共享有限的资源，如CPU或内存。通过优先队列，系统可以确保资源被优先分配给最紧急或最重要的任务。再如，你的手机可能会为来电分配比正在运行的游戏更高的优先级。

现在，你已经了解了优先队列的基本概念和其在实际中的应用，为何不尝试自己实现一个呢？

下面是我实现最大优先队列的伪代码：


1. **HEAPMAXIMUM(a):**
    - **功能**: 返回堆中的最大元素。
    - **工作原理**: 在最大堆中，最大的元素始终位于根节点，即数组的第一个位置。因此，这个函数简单地返回数组的第一个元素。

    ```pseudo
    HEAPMAXIMUM(a):
        return a[1]
    ```

2. **HEAPEXTRACTMAX(a):**
    - **功能**: 返回堆中的最大元素，并将其从堆中删除。
    - **工作原理**: 
        - 首先，检查堆是否为空（即堆下溢）。
        - 然后，保存堆的最大元素（即数组的第一个元素）。
        - 将堆的最后一个元素移到根节点，并减少堆的大小。
        - 使用`MAXHEAPIFY`函数确保新的根节点满足最大堆的性质。
        - 最后，返回保存的最大元素。

    ```pseudo
    HEAPEXTRACTMAX(a):
        if len(a) < 1:
            error "heap underflow"
        max = a[1]
        a[1] = a[len(a)]
        a.size = a.size - 1
        MAXHEAPIFY(a, 1)
        return max
    ```

3. **HEAPINCREASEKEY(a, i, key):**
    - **功能**: 增加堆中第`i`个元素的值，并确保堆的性质得到维护。
    - **工作原理**: 
        - 首先，检查新的键值是否小于当前的键值。
        - 然后，将第`i`个元素的值设置为新的键值。
        - 如果新的键值大于其父节点的值，将其与父节点交换，并继续检查其新的父节点，直到堆的性质得到满足或达到根节点。
     
    ```pseudo      
    HEAPINCREASEKEY(a, i, key):
        if key < a[i]:
            error "new key is smaller than current key"
        a[i] = key
        while i > 1 and a[PARENT(i)] < a[i]:
            exchange a[i] with a[PARENT(i)]
            i = PARENT(i)
    ```

4. **MAXHEAPINSERT(a, key):**
    - **功能**: 将一个新的元素插入到堆中。
    - **工作原理**: 
        - 首先，增加堆的大小。
        - 将新元素的值初始化为负无穷大（确保它小于堆中的任何现有元素）。
        - 使用`HEAPINCREASEKEY`函数将新元素的值设置为给定的键值。

    ```pseudo  
    MAXHEAPINSERT(a, key):
        a.size = a.size + 1
        a[a.size] = -∞
        HEAPINCREASEKEY(a, a.size, key)
    ```

这些函数共同提供了一个最大优先队列的实现，其中元素可以按照它们的优先级（在这种情况下是它们的值）插入、检索和删除。


我们使用上述的最大优先队列操作来实现从10亿个数中找出最小的100万个数的伪代码：

```pseudo
FindSmallestNumbers(filename):
    maxPriorityQueue = empty array of size 1000000
    file = open(filename)

    // 初始化优先队列
    for i = 1 to 1000000:
        number = read a number from file
        MAXHEAPINSERT(maxPriorityQueue, number)

    // 遍历文件的其余部分
    while there are more numbers in file:
        number = read a number from file
        if number < HEAPMAXIMUM(maxPriorityQueue):
            HEAPEXTRACTMAX(maxPriorityQueue)
            MAXHEAPINSERT(maxPriorityQueue, number)

    close file
    return maxPriorityQueue
```

这个伪代码首先使用文件中的前100万个数初始化一个最大优先队列。然后，它遍历文件的其余部分，对于每个读取的数，如果该数小于优先队列中的最大值，它就从优先队列中移除最大值，并将新数插入到优先队列中。这样，当所有的数都被读取后，优先队列中的数就是文件中最小的100万个数。

如何将上述伪代码转化为代码呢？以下是我编写的最大优先队列函数，你可以先尝试自己实现，然后再参考：

```python
def geti(a, i):
    return a[i - 1]

def seti(a, i, key):
    a[i - 1] = key

def PARENT(i):
    return i // 2

def HEAPMAXIMUM(a):
    return geti(a, 1)

def HEAPEXTRACTMAX(a):
    if len(a) < 1:
        raise ValueError("heap underflow")
    max = geti(a, 1)
    seti(a, 1, geti(a, len(a)))
    a.pop()  # 移除最后一个元素
    MAXHEAPIFY(a, 1, len(a))
    return max

def HEAPINCREASEKEY(a, i, key):
    if key < geti(a, i):  # 注意：Python的数组索引从0开始
        raise ValueError("new key is smaller than current key")
    seti(a, i, key)
    while i > 1 and geti(a, PARENT(i)) < geti(a, i):  # PARENT(i) = i // 2
        exch(a, i, PARENT(i))
        i = PARENT(i)

def MAXHEAPINSERT(a, key):
    a.append(float('-inf'))  # 插入负无穷大
    HEAPINCREASEKEY(a, len(a), key)

```

## 6. 快速堆排序

堆排序（HEAPSORT）虽然在理论上很吸引人，但在实际应用中，其比较计数的效率并不高。原因在于它将元素从堆的底部提升到顶部，然后再让它们逐渐下沉，与较大的元素交换位置。

![动图 重建最大堆示意图](/doc/illustrations//Heapsort/heapsort12.gif)

这种做法似乎有些反直觉：为什么要将一个可能很小的元素放在可能很大的元素之上，然后再观察其下沉的过程呢？难道就没有更优雅的方法，直接将两个子堆中的较大元素提升到堆的顶部吗？

考虑以下改进：

**优化后的 HEAPSORT**（肯定有前人已经探索过这种方法）：

1. 将所有元素放入有效的最大堆中
2. 删除堆顶，创建一个空缺 "V"
3. 比较 V 正下方的两个子堆首领，将最大的那个提升到空缺中。
4. 递归重复第 3 步，重新定义 V 为新的空缺，直到堆的底部。	
5. 转到步骤 2


![动图 快速堆排序示意图](/doc/illustrations//Heapsort/heapsort14.gif)

这种方法的优势在于，我们实际上是将一个已知较大的元素提升到堆顶，无需进行额外的比较。

我们将这种改进的算法称为 "快速堆排序"（FAST HEAPSORT）。虽然它不是完全原地的，但与传统的堆排序（HEAPSORT）相比，它每次从堆顶提取一个排序项，效率更高。

如何将上述过程转化为代码呢？以下是我为快速堆排序编写的函数，你可以先尝试自己实现，然后再参考：

```python
def FASTHEAPSORT(a):
    # 1. 将所有元素放入有效的最大堆中
    BUILDMAXHEAP(a)

    n = len(a)
    sorted_array = []

    while n >= 1:
        max = HEAPMAXIMUM(a)
        sorted_array.append(max)  # 将最大元素插入到sorted_array
        seti(a, 1, float("-inf"))  # 2. 删除堆顶，创建一个空缺 "V"
        FASTMAXHEAPIFY(a, 1, len(a))  # 3. 比较 V 正下方的两个子堆首领，将最大的那个提升到空缺中
        n -= 1

    return sorted_array[::-1]  # 反转sorted_array并返回


def FASTMAXHEAPIFY(a, i, n):
    while True:
        left = 2 * i
        right = 2 * i + 1

        # 如果没有子节点，直接退出
        if left > n:
            break

        # 默认选择左子节点
        largest = left

        # 如果右子节点存在且大于左子节点，则选择右子节点
        if right <= n and less(a, left, right):
            largest = right

        # 如果当前节点已经是其子树中的最大值，退出循环
        if geti(a, i) >= geti(a, largest):
            break

        exch(a, i, largest)
        i = largest
```