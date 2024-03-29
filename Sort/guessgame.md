# 一个游戏让你理解二分法的本质

你是否曾在综艺节目中见过这样的情景：嘉宾们头顶挂有一张神秘的牌子，但他们并不知道上面写着什么。他们的任务是通过提出“是”或“否”的问题来揭示牌子上的内容。

这样的游戏背后是否隐藏着某种规律呢？

## 猜数游戏

为了简化这个问题，让我们将猜内容变为猜数字。假设你需要确定一个位于 0 至 31 之间的整数 x，你会用多少个“是/否”的问题来确定它？

我想很少有人会按顺序逐个提问：“是 0 吗？”、“是 1 吗？”或“是 2 吗？”……

你可能已经想到了——**二分法**。你可以首先询问“数字在 0 至 16 之间吗？”从而排除一半的可能性，然后继续在剩下的范围里二分搜索。

## 二分法

让我们深入探究这个游戏的核心，理解为什么二分法是最佳选择。

这不只是一个简单的猜数游戏，它更像是一次搜索探险。

首先，考虑这个搜索任务的**解空间**。数字从 0 到 31，任何一个都可能是答案，因此解空间包括 32 种可能。

其次，作为搜索任务，我们需要**找到问题的特征来避免不必要的搜索**。我们只有“是”或“否”的回答，如何最大化这个特征的效用？

由于答案只有二元选项，我们可以将其分为两个分支。若这两个分支的可能性相等，则我们有效地减半了搜索范围。这也说明二分法是最优解。

![binary guess](/doc/illustrations/guessgame/guess02.PNG)

## 从信息论的角度看问题

在 MacKay 的信息论中，我们可以获得了一个全新的视角。

*MacKay 的信息论:
https://www.inference.org.uk/itprnn/book.pdf*


首先，让我们回顾一下二进制。我们常用的十进制基于 10 个数字，而二进制仅用到 0 和 1。

例如，数字 2 在二进制中表示为 `10`，3 为 `11`，4 为 `100`。

当我们回到这个游戏，如果将{是, 否}的答案转为{1, 0}，那么每个答案都相当于 1 个比特的信息。

要猜的整数 x 有 32 种可能。31 在二进制中是 `11111`，所以可能答案从 `00000` 到 `11111`，这需要 5 个比特来表示。

为了最快找到答案，我们可以逐个确定这 5 位中的每一位。

我们可以询问：

    1: x ≥ 16 吗？
    2: x mod 16 ≥ 8 吗？
    3: x mod 8 ≥ 4 吗？
    4: x mod 4 ≥ 2 吗？
    5: x mod 2 = 1 吗？

其中 mod 是求余的意思。x mod 16，就是 x 除以 16 的余数是多少。

事实上，这些问题试图从高到低逐个确定 5 位中的每一位。

![Information Theory guess](/doc/illustrations/guessgame/guess01.PNG)

## 结论

从两种角度来看，二分法都是猜数游戏的最优策略。而信息论为我们提供了这一策略的形式化解释。

从猜数字游戏出发，我们引出了一种解决搜索问题的策略：
1. 定义解空间；
2. 基于问题特征减小解空间。

当我们面对类似的搜索问题时，这种方法可以有效地帮助我们找到最优解。

除了熟悉了猜数字游戏和二分法，你是否想过可能还存在三分法、四分法等其他方法？当然，随着问题的复杂度增加，策略也会随之增多。

最后，我为大家留下一个思考题：

题目：给定一个天平和12个小球，其中有一个是假球，而我们不知道它是轻还是重。你至少需要称重多少次来确定哪个是假球？

想知道答案吗？关注我，下篇文章为您讲解。

本文参考资料：
1. http://mindhacks.cn/2008/06/13/why-is-quicksort-so-quick/

2. https://www.inference.org.uk/itprnn/book.pdf

