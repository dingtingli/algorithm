# Futures 和 Promises

http://dist-prog-book.com/chapter/2/futures.html

Futures 和 Promises 是异步编程中经常使用的抽象，尤其是在分布式系统中。我们将介绍这些抽象的的动机和历史，并看看它们是如何随着时间的推移一步步演变的。我们将深入研究它们的不同语义和各种执行模型。这不经是历史和演变，我们还将深入研究今天在JS，Scala 和 C++ 等语言中最广泛使用的 Fetures 和 Promises。

## 介绍

作为一个人类，我们有能力进行多任务处理。比如，我们可以同时走路，说话和吃饭，但打喷嚏时除外。打喷嚏是一种阻塞活动，因为它迫使你短暂地停止赈灾做的事情，打完喷嚏后你在继续你的事情。我们可以把人类意义上的多任务看作是计算机中的多线程。

考虑一个简单的计算机处理器，没有并行能力，只有一次完成一个任务或者进程的能力。在这种场景下，有时候处理器会被阻塞，比如一些阻塞性操作被调用的时候。这些阻塞性操作可能包括 I/O 操作，比如读写硬盘，或者在网络上接收和发送数据包。作为一个程序员，我们知道阻塞性操作会比典型的 CPU 任务花费更多的时间，比如遍历一个数组。

处理器有两种方式来处理这些阻塞性操作：

1. 同步：处理器等待，直到阻塞性操作完成其任务并返回结果。之后，处理器再去执行下一个任务。这通常是有问题的，因为 CPU 没有被有效地理解，它可能会等待很长的时间。
2. 异步：当任务被异步处理时，在同步情况下等待的 CPU 时间将被用于处理其他任务，使用抢占时间的共享算法。也就是说，与其等待，不如处理其他任务。因而，只有更多的工作可以做，处理器就不会出现等待。

在编程的世界里，为了帮助程序员实现理想的资源利用，已经有很多结构被引入。可以说，其中最广泛使用的就是 Futures / Promises 。

在这一章中，我们将深入地探讨 Futures / Promises，这一流行的抽象，用于进行同步和异步编程。我们将回顾这些抽象的历史和动机，理解它们对哪些场景有用，并介绍他们是如何随着时间的推移而演化。我们也将介绍这些抽象的各种执行模型，最后，我们也会谈谈在不同编程语言，比如 JS ，scala，C++ 中如何使用 Futures 和 Promises。

## 基础概念

我们将会从最广泛的 Futures / Promises 概念出发，然后在扩展，涵盖不同语言对这些结构的解释，以及许多语义上的差异。

在最广泛的意义中

> future / promise 可以被认为是一个值，一个最终会变得可用的值。

或者换种说法，它是一个抽象概念，编码了一个时间的概念。通过使用这种结构，可以假设你的值现在可以有许多可能的状态，这取决于你请求它的时间点。最简单的变化包括两个与时间有关的状态， future/promise是以下两种情况之一：
 1. 完成/确定： 计算已经结束，future/promise 的值可以得到。
 2. 未完成/未确定：计算还未完成。

 正如我们后面将会看到的那样，在一些 future/promise 的变体中还引入了其他一些状态，以更好的支持异常处理和取消等需求。

最重要的是，future/promise 通常能够实现某种程度的并发。在 future 最初的定义中：

> 这个结构（future x）立即返回表达式x的只的future，并同时开始评估 future。当对 x 的评估产生一个值时，该值将取代 future。
>
> Halstead, 1985

有些对 futures/promises 的解释会有一个与之相关的类型，有些则没有。通常情况下，一个 future/promise 是单次分配，也就是说，它只能被写一次。有些解释是阻塞的（同步），有些是完全非阻塞的（异步）。有些解释必须明确地被启动（比如手动启动），而有些解释中，计算是隐式启动的。

受到函数式编程的启发，这种结构的不同解释之间的主要区别之一与pipeline或者组合有关。一些更流行的解释使得 链式操作成为可能，或者定义一个操作 pipeline ，在 future/promise所代表的计算完成后被调用。这与回调地狱或者更多直接阻塞的方式形成对比。

## 动机和用途

futures / promises 作为一个话题的兴起，是与并行和并发编程以及分布式系统的兴起同时发生的。这在某种程度上是自然而然的，因为作为一个编码时间的抽象，当延迟成为一个问题时，futures/promises 引入了一个很好的方式来推理状态的变化。当一个节点必须与分布式中的另一个节点通信时，这是程序员面临的普遍问题。

然而，futures / promises 被认为在许多其他情况下也是有用的，包括分布式和非分布式。这些情况包括：

* 请求响应模式。
* 输入/输入。
* 长时间运行的计算。
* 数据库查询。
* RPC（远程程序调用）
* 从Socket中读取数据
* Timeouts

如今许多现实世界的服务和系统在这些流行的背景下大量使用 futures/promises，这要归功于 future/promise 概念被引入流行的的语言和框架中，比如 JS， Node.js, Scala, Java, C++等。正如我们在接下来看到的那样，这种 futures/promises 的扩散，导致 futures/promises 的含义和名称随着时间和编程语言的变化而变化。

## 术语的分歧

Future， Promise Delay 或者 Deferred 通常指的是大致相同的同步机制，即一个对象作为尚不清楚的结果的代理。当结果可用的时候，一些其他的代码就会被执行。多年来，这些术语在不同的语言和生态系统中所指的语义略有不同。

有时候，一个语言可能有一个结构叫做 future， promise，delay， defered 等。

然而在其他情况下，一个语言可能有两个结构，通常被称为 futures 和 promises。像 scala, Java 和 Dart 就属于这种情况。在这种情况下：

* 一个 Future 是一个对尚未被计算的值的只读引用。
* 一个 Promise（或者叫 CompletableFuture / Completer 等等）是 Future 指向的一个单一赋值的变量。

换句话说，future 是一个写入 Promise 值的只读窗口，你可以通过调用一个 promise 的 future 方法来获得与之相关的 future，但在另一个方向的转换是不可以的。另一个观念是，如果你向某人promise（承诺）了什么，你就有责任遵守它，但如果某人向你做出了承诺（promise），你就希望他们在未来（future）兑现它。

在 Scala 中，它们的定义如下：

> future 是一个尚未存在结果的占位符对象。 promise 是一个可写的，单一赋值的容器，它完成了一个future。promise 可以用一个结果来完成 future，以表示成功，或者用一个异常来表示失败。
>
> Haller et al., 2013

Scala 和 Java(6) future 的一个重要区别是，Scala 的 future 在本质上是异步的。 Java 的 future 至少在 Java 6 之前，都是阻塞的。Java 7 引入了异步的 future。

Java 8 中， `Future<T>` 接口有一些方法可以检查计算是否完成，等待其完成，并在完成之后读取计算结果。 CompletableFutures 可以被认为是一个 promise，因为它们的值可以被显性的设置。然而，CompletableFuture 也实现了 Future 接口，允许它也被当作 Future 来使用。Promises 可以被认为是一个具有公共 set 方法的 future，调用者可以用它来设置 future 的值。

在 JavaScript 的世界，JQuery 引入了 Deffered 对象的概念，用来表示一个尚未完成的工作单元。Deffered 对象包含一个 promise 对象，代表该工作单元的结果。Promise 是一个函数的返回值。Deffered 对象可以由调用者取消。

像 Scala 和 Java 一样， C# 也对上述的 future 和 promise 结构进行了区分。在 C# 中， future 被成为 `Task<T>`，Promise 被称为 `TaskCompletionSource<T>` ，future 的结果在只读属性 `Task<T>.Result` 中可用，它返回 T，而`TaskCompletionSource<T>.Task<TResult>` 有方法用 T 类型的结果或用异常或取消来完成任务对象。重要的是要注意：在C#中，Task 是异步的。

令人困惑的是，JavaScript 社区已经对一个被称为 Promise 的单一结构进行了标准化，它可以像其他语言中的 future 一样使用。Promise 规范（Promise/A+，2013）只定义了一个接口，并将 promise 的细节实现留给规范的实现者。JavaScript 的 Promises 也是异步的，并且可以pipeline 。在支持 ECMAScript 6（ES6）的浏览器中 JavaScript 的 promises 被默认开启，获取在一些库中被使用，比如 Bluebird 和 Q。

正如我们所见，概念，语义，术语在语言和实现 futures/promise 的库中有所不同。这些术语和语义上的差异来自于历史悠久和独立的语言社区，这些社区已经扩散了对 futures/promises 的使用。

## 简史

下面是一个时间线，跨越了我们今天所知的 futures/promsies 的历史。

![PNG01](/doc/illustrations/asynchronous/1.png)

第一个 futures/promises 概念来自于 1961 年，即所谓的 thunks。thunks 可以被认为是 futures/promises 的一个原始的，连续的概念。根据其发明者P.Z. Ingerman的说法，thunks 是：

> 一段提供地址的编码。
>
> Ingerman, 1961

Thunks 被设计为一种在 Algol-60 过程调用中将实际参数和他们的形式定义（formal definitions）绑定在一起的方法。如果过程被调用是用一个表达式代替了一个形式参数（formal parameter），编译器会生成一个 thunk，他将计算表达式，并将结果的地址留在某个标准的位置。可以把 thunk 看作是一个延续或者函数，其目的是在单线程环境下进行评估。

第一次提及 futures，是在 Baker 和 Hewitt 的论文中（关于进程增量的垃圾回收 Incremental Garbage Collection of Processes 1977）。他们创造了术语 call by future，用来描述调用约定（convertion），方法的每个形参（formal parameter）绑定到一个进程，该进程与其他参数并行地评估参数中的表达式。在这篇论文之前，Algol 68 也提出了一种使用这种并发的参数评估成为可能的方法，使用并行条款进行参数绑定。

在论文中，Baker 和 Hewitt 提出了 Fetures 的概念，即代表一个表达式的 E 的 3 元组：

1. 一个评估表达式 E 的过程。
2. 一个需要存储 E 的结果的内存位置。
3. 一个正在等待 E 的进程列表。

但重要的是，他们工作的重点不是 futures 的作用以及它们在异步分布式计算中的作用。相反，他们关注的是对那些评估函数不需要的表达式的进程进行垃圾回收。