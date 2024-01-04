# 从二分法的本质出发，理解为什么排序算法的复杂度不可能小于 O(NlogN)

我们之前了解二分法本质时介绍了[猜数字游戏](./guessgame.md)，在这个游戏中，你每次提问，答案只能是“是”或“否”。你的目标是用最少的问题找出正确的数字。

理论上，每次提问后，剩下的可能性减半。比如，开始有 100 个可能性，提问一次后就剩 50 个可能性，再问一次就剩 25 个，以此类推。

从猜数字游戏出发，我们引出了一种解决搜索问题的策略：
1. 定义解空间；
2. 基于问题特征减小解空间。

接下来，我们将使用这个策略来探讨排序算法的复杂度。


## 解空间

排序问题可以被认为是确定元素之间的相对顺序。对于任何给定的 `N` 个元素，都有 `N!`（N的阶乘）种可能的排列，其中只有一种排列是满足题意的（譬如从小到大排列）。

例如，考虑三个元素的数组 `[a, b, c]`，它一共有 3! = 6 种排列组合。我们的目的是从中找到一个满足需求的组合。

![3! = 6 种排列](/doc/illustrations/nlogn/onlogn%2001.png)


## 基于问题特征减小解空间

假定有两个序列 `a1, a2,...,ai,...,an` 和  `b1, b2,...,bi,...,bn`，我们需要对它们的大小进行比较。

这两个序列的比较规则是这样的：我们从头开始逐个元素比较，直到找到它们之间的第一个不同的元素。例如，如果`ai`是第一个与`bi`不同的元素，且`ai <= bi`，那么第一个序列就小于第二个序列。

在 `N` 个元素的 `N!` 种可能的排列中，最小的序列是将其中每一个元素从小到大排好序的那个序列。

**通过元素的比较挑出最小的一个排列，就是比较排序的本质。**

所以，任何基于比较的排序算法的**基本操作都是比较两个元素。**

比较两个元素，就相当于猜数字游戏里面的一个提问，显然这个提问的答案只能是“是”或“否”。一个只有两种输出的问题最多只能将可能性空间切成两半，根据猜数字游戏的思路，最佳方法就是切成50和50。

例如，如果我们有一个简单的数组列表 `[a, b, c]`，我们可以首先比较 `a` 和 `b`。通过这次比较，我们可以确定 `a` 和 `b` 的相对位置，排除一半的可能性。然后，我们可以再比较 `a`和 `c`，或者 `b` 和 `c` ，来排除剩下的可能。

![比较排序](/doc/illustrations/nlogn/onlogn%2002.png)

我们希望在每次比较后剩余的可能排列减少为之前的一半，从 N!/2，N!/4，N!/8，...，N!/（2^k），……，1。

也就是说，对于 N 个元素的序列，最坏的情况下需要进行 k 次比较才能确定一个特定的排列，其中 `2^k = N!`，这将导致 `k = log(N!)`。

## 斯特林(Stirling)公式

在前文中，我们得出结论，为了确定 `N` 个元素的唯一排列，需要进行 `log(N!)` 次比较。接下来，我们将利用 Stirling 公式，来进一步分析 `log(N!)` 的增长率。

使用 Stirling 公式，我们可以估计 (N!) 的值。该公式是：

$$[N! \approx \sqrt{2\pi N} \left(\frac{N}{e}\right)^N]$$

如果取这个估计的对数，得到：

$$[\log_2(N!) \approx \log_2(\sqrt{2\pi N}) + N \log_2\left(\frac{N}{e}\right)]$$

现在，如果我们再次忽略常数和低阶项，那么 `log(N!)` 的主要影响是 `O(N logN)`，这与第二个表达式相匹配。

因此，尽管两者不完全相等，但从增长率的角度来看，它们是类似的。

*具体类容可以参考：[如何清晰地理解算法复杂度 Big O?](/bigo.md)*

**看不懂公式也没关系。简单来说，为了从 `N` 个元素的所有可能排列中选择一个，我们至少需要 `log(N!)` 次比较，而这可以简化为 `O(N logN)`。**

## 结论

通过上述分析，我们可以得出结论：**任何基于比较的排序算法，其复杂度的下限是 `O(NlogN)`。**

这是因为对于 `N` 个元素的序列，其可能的排列有 `N!`种，而每次比较最多只能将可能性空间减少一半。因此，为了确定唯一的排列，至少需要进行 `log(N!)`次比较。这也就是说，（根据 Stirling 公式）比较排序算法的复杂度不可能小于 `O(NlogN)`。

这个结论是非常重要的，因为它表明了我们在设计排序算法时的一个基本限制。即便是最优的比较排序算法，其复杂度也不能低于 `O(NlogN)`。这对于理解和评估比较排序算法的性能是至关重要的。