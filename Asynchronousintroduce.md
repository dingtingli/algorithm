在平坦的路上曲折前行

# Futures 和 Promises

作者：KISALAYA PRASAD, AVANTI PATIL, 和 HEATHER MILLER

原文地址：http://dist-prog-book.com/chapter/2/futures.html

在异步编程领域，尤其是针对分布式系统，Futures 和Promises 是一种广泛认可的编程抽象方法。

本文将介绍这些方法的起源和发展历程，探讨它们的设计初衷及其随时间的演变。此外，我们还会详细分析它们的语义差异以及不同的执行模型。

本文不仅回顾历史和发展，还将深入探讨如今在 JavaScript、Scala 和 C++ 等编程语言中广泛应用的 Futures 和 Promises。


## 引言

我们人类具备同时处理多项任务的能力，比如可以边走路边说话边吃东西，但打喷嚏时除外。因为打喷嚏会短暂地让我们停下手头的活，等喷嚏过后再接着做。

这种情况，可以类比于计算机中的多线程处理，在多任务进行时，某些任务会暂时阻塞其他任务的进行。

设想一个简单的计算机处理器，它不具备并行处理能力，一次只能完成一个任务。在这种情况下，当执行某些阻塞操作时，处理器有时会停下来。

这种阻塞操作可能包括输入/输出（I/O）操作，如读写硬盘或通过网络发送接收数据。

我们作为程序员都知道，相比于 CPU 密集型的任务，如遍历一个列表，I/O 等阻塞操作往往会占用更多的时间。

处理器处理阻塞调用有两种方式：

- 同步方式：处理器会等待阻塞任务调用完成并返回结果后，再继续执行下一个任务。这种方式有时会导致 CPU 利用率不高，因为它可能需要等待较长时间。

- 异步方式：通过异步处理任务，原本同步等待的 CPU 时间被用来执行其他任务，采用了一种叫做抢占式时间共享的算法。这意味着，处理器不再简单等待，而是转而执行另一个任务。这样，只要还有任务需要执行，处理器就不会空闲等待。

在编程领域，为了帮助程序员更高效地利用资源，引入了许多技术和概念。其中最广泛应用的概念之一就是 Futures 和 Promises。它们通过一种优雅的方式管理异步操作，使得资源利用更加高效。

在本章中，我们将详细介绍 Futures 和 Promises，这两种编程中用于同步与异步操作的重要抽象概念。

我们会探索引入这些概念的原因、它们的发展历程，以及它们适用的场景。

同时，我们还将讨论随时间如何演进，并分析与之相关的不同执行模型。

最后，我们会着重介绍在当前流行的几种编程语言中，如 JavaScript、Scala 和 C++，如何广泛应用 Futures 和 Promises。

## 基础理念

正如我们接下来要探讨的，我们如何定义和称呼这个概念，以及它的精确定义，往往存在差异。我们首先给出 future/promise 概念最宽泛的定义，然后再逐步深入，探讨不同编程语言中对这些概念的不同理解和语义差异。

广义上，

> Future 或 Promise 可以视为一个将来某时刻会准备好的值。

或者说，它是一个涵盖时间维度的抽象概念。通过采用这种构造，意味着我们承认一个值在不同时间点可能处于不同的状态。最简单的形式包含两种依时间变化的状态：一个 future/promise 可能是：

1. 已完成/确定：计算已经完成，future/promise 的值已经就绪。

2. 未完成/待定：计算还在进行中，其值尚未准备好。

这种区分帮助我们理解，在编程中如何处理还未准备好的数据，以及如何通过这些抽象构造有效管理异步操作。

为了更好地满足错误处理和取消操作等需求，futures 和 promises 的一些变种引入了额外的状态。

更为重要的是，futures 和 promises 通常支持并发操作，这意味着它们能够同时处理多个任务。也就是说，最初对 futures 定义的一个版本：

>构造（future X）会立即返回一个代表表达式 X 结果的future，并且开始并行地计算 X。当 X 的计算完成并产生了结果时，这个结果会取代原来的 future。
>
>（Halstead, 1985）


对 futures 和 promises 的不同解释中，有些与特定的数据类型相关联，而有些则不是。通常情况下，一个 future 或 promise 只能被赋值一次，这意味着它们在创建后只能接收一个值。

根据不同的解释，有的是阻塞式（同步）的，有的则是完全非阻塞式（异步）的。在一些情况下，需要明确地启动计算（即手动触发），而在其他情况下，计算则是隐式地、自动开始的。

受到函数式编程思想的影响，不同解释之间的一个重要区别在于它们是否支持操作的链式连接或组合。在 futures 和 promises 的一些流行解释中，可以将多个操作连接起来，或定义一个操作序列，在 future 或 promise 代表的计算完成后执行。

这种方式与那些需要大量回调或依赖直接阻塞的更命令式的方法形成鲜明对比。

## 动机与应用

Promises 和 Futures 之所以成为一个热门话题，主要是因为它们与并行、并发编程和分布式系统的发展密切相关。

这种联系颇为自然，因为 futures 和 promises 作为一种时间维度的抽象工具，为我们在处理因网络延迟等问题而导致的状态变化提供了一个清晰的思考框架；这种延迟是分布式系统中一个节点需要与另一个节点通信时，程序员经常遇到的挑战。

尽管 promises 和 futures 主要与并行、并发编程和分布式系统的发展相关联，但它们在许多其他场景中也非常有用，无论是分布式的还是非分布式的。具体应用场景包括：

- **请求-响应模式**，例如 HTTP 的 Web 服务调用。Future 可以表示 HTTP 请求的响应结果。

- **输入/输出操作**，例如需要用户输入的 UI 对话框，或者从磁盘读取大型文件。Future 可以代表 IO 操作及其结果，比如读取到的数据。

- **长时间运行的计算**。例如，如果你不希望因一个复杂算法的长时间计算而阻塞，而是希望同时进行其他任务，可以使用 Future 来代表这一长时间的计算过程及其结果。

- **数据库查询**。与长时间的计算一样，数据库查询可能需要较长时间。因此，将查询操作异步化，让程序能够继续执行后续任务而不是等待，可以通过 Future 来实现，代表查询及其结果。

- **RPC（远程过程调用）**。由于网络延迟，RPC 调用可能会受到影响。为了避免等待 RPC 调用的结果，可以将调用过程异步化，通过 Future 代表这一调用及其结果。

- **从套接字读取数据**，尤其是因网络延迟而变得耗时。为了不阻塞等待数据到来，可以将读取操作异步化，通过 Future 代表读取过程及其结果。

- **超时管理**，如 Web 服务中的超时处理。代表超时的 Future 可以不返回任何结果，或返回一个特殊的空结果，如类型化编程语言中的 Unit 类型，以此来处理超时情况。

在当今的许多实际服务和系统中，futures 和 promises 被广泛应用于众多流行的场景，这一现象得益于 future 或 promise 的概念被纳入了JavaScript、Node.js、Scala、Java、C++ 等多种广泛使用的语言和框架中。正如我们在后续章节将要探讨的，随着 futures 和 promises 在不同编程语言中的普及，它们的含义和命名也随之发生了变化和演进。

## 术语的分化

在编程中，Future、Promise、Delay 和 Deferred 这些术语基本上指的是同一种同步机制，即通过一个代理对象来管理一个还未确定的结果。

一旦这个结果成为可用状态，随后就会执行一段特定的代码。然而，随着时间的推移，这些术语在不同的编程语言和框架中逐渐演化出了一些细微的语义差别。

在某些情况下，一种编程语言可能只有一个这样的构造，可能称之为 future、promise、delay 或 deferred。

但在其他情况下，一些语言中会明确区分两种构造，通常被称作 futures 和 promises。Scala、Java 和 Dart 等语言就属于这种情况。具体来说，

- Future 是一个指向将来某个时刻会确定的值的只读引用。
- Promise（或者称为 CompletableFuture、Completer 等）是一个与 Future 相关联的单次赋值变量，用于存放最终计算得到的值。

换种方式来说，future 可以视为对 promise 中结果的一个只读视角。通过对 promise 调用 future 方法，你可以获得与之相关联的 Future，但是你不能将 Future 转换回 Promise。

这个概念可以用人际关系中的承诺来类比：如果你对某人做出了承诺（promise），那么履行承诺的责任在你；反之，如果别人对你做出承诺，你则期待在未来（future）他们能够兑现。

Promise 代表了一个可能还未完成的操作或计算的承诺，而 Future 则为我们提供了一个观察和等待这个承诺兑现的窗口。

在 Scala 语言中，Future 和 Promise 的定义如下所示：

>Future 是一个代表尚未生成结果的占位符对象。Promise 则是一个可写入的、只能赋值一次的容器，用于完成 Future 的构建。Promise 可以通过提供结果来完成 Future，表明操作成功，或者通过抛出异常来表示操作失败。
>
>(Haller等人，2013)

Scala 与 Java（至Java 6）在 futures 上的一个显著不同在于 Scala 的 futures 天生支持异步操作。Java 的 Future，在 Java 6 及之前的版本中，是基于阻塞（blocking）的设计。Java 7 的更新为异步 futures 带来了重大改进，这一变化受到了广泛的欢迎。

在 Java 8 版本中，`Future<T>` 接口提供了方法来确认计算是否已完成、等待计算完成以及在计算完成时获取结果。`CompletableFutures` 可以看作是一种 promise 机制，因为它们允许显式地设定其值。此外，`CompletableFuture` 还实现了 `Future` 接口，因此既可以作为 Future 使用，也具备 Promise 的特性，即它允许通过公开的 set 方法由调用者或其他任何人设定其结果值。

在 JavaScript 领域，JQuery 引入了 `Deferred` 对象的概念，用于表示尚未完成的工作单元。`Deferred` 对象内部包含一个 promise 对象，代表该工作单元的最终结果。Promise 是由函数返回的值。此外，`Deferred` 对象还可以被创建它的调用者取消。

与 Scala 和 Java 类似，C# 也明确区分了上述的 future 和 promise 概念。在C#中，futures 被称为 `Task<T>`，而 promises 则被称为 `TaskCompletionSource<T>`。Future 的结果可以通过`Task<T>.Result` 这个只读属性访问，它返回一个 `T` 类型的结果；而 `TaskCompletionSource<T>` 提供了方法来以 `T` 类型的结果、异常或取消完成 `Task` 对象。需要注意的是，C# 中的 `Tasks` 是基于异步模型设计的。

在 JavaScript 社区，存在着一个名为 `Promise` 的统一构造，这种构造的方式使其能够类似于其他语言中对 futures 的处理方式。根据 Promises 规范（Promises/A+，2013）的定义，Promise 仅有一个接口，而具体如何实现（或兑现）Promise 的细节则交给了该规范的实现方。在 JavaScript 中，Promises 不仅支持异步操作，还能进行操作的管道化。在支持 ECMAScript 6（EC6）的浏览器中，JavaScript 的 Promises 默认可用，同时也可以通过如 [Bluebird](http://bluebirdjs.com/docs/getting-started.html) 和 [Q](https://github.com/kriskowal/q) 等多个库来使用。

正如我们所见，不同编程语言和库对 futures/promises 的概念、语义和术语的理解存在差异。这些差异源于 futures/promises 背后丰富的历史以及推动其发展的独立语言社区。

每个社区根据自己的需求和背景，对这些概念进行了不同的诠释和实现，从而形成了今天我们看到的多样化的异步编程模型。这种多样性虽然在一定程度上增加了理解和使用上的复杂性，但也反映了编程社区在不断探索和优化异步处理机制的过程。

---

解释：

当然，我们可以根据上述提到的不同编程语言中的实现来具体说明如何使用Future和Promise。

### 1. Java中的Future<T>和CompletableFutures

在Java中，`Future<T>`接口允许你开始一个异步计算，并使用返回的`Future`对象查询计算是否完成。如果计算完成，你可以检索其结果。使用`CompletableFuture<T>`，你可以创建一个完成时会被自动触发的异步操作。

```java
CompletableFuture<String> completableFuture = CompletableFuture.supplyAsync(() -> "Hello");
try {
    String result = completableFuture.get(); // 等待异步操作完成并获取结果
    System.out.println(result);
} catch (InterruptedException | ExecutionException e) {
    e.printStackTrace();
}
```

在Java示例中，我直接使用了`CompletableFuture`而没有单独展示传统的`Future`用法，这是因为`CompletableFuture`是`Future`的一个增强实现，提供了更多的灵活性和功能。`CompletableFuture`不仅实现了`Future`接口，还引入了诸如完成动作、异常处理和结果转换等功能，使得异步编程更加方便。

传统的`Future`用法通常与`ExecutorService`一起使用，来执行异步任务，并通过返回的`Future`对象来控制任务和获取结果。这里提供一个使用传统`Future`的示例来补充说明：

```java
ExecutorService executor = Executors.newCachedThreadPool();
Future<String> future = executor.submit(() -> {
    Thread.sleep(1000); // 模拟长时间运行的任务
    return "Hello, Future!";
});

try {
    // get()方法会阻塞，直到异步操作完成，返回结果
    String result = future.get();
    System.out.println(result); // 输出: Hello, Future!
} catch (InterruptedException | ExecutionException e) {
    e.printStackTrace();
}

executor.shutdown();
```

在这个示例中，我们通过`ExecutorService`的`submit`方法提交了一个异步任务，这个方法返回一个`Future<String>`对象。我们可以调用`future.get()`来阻塞当前线程，直到异步任务完成并返回结果。

相比之下，`CompletableFuture`提供了非阻塞的方式来处理完成事件，支持链式调用，并允许组合和转换多个`CompletableFuture`，因此在实际使用中更加灵活和强大。这也是为什么在初步介绍时我选择直接使用`CompletableFuture`的原因。

### 2. JQuery中的`Deferred`对象

在JQuery中，`Deferred`对象用来表示一个尚未完成的操作。它可以创建一个Promise对象，用于后续的链式调用。

```javascript
function asyncGreet(name) {
  var deferred = $.Deferred();
  setTimeout(function() {
    deferred.resolve("Hello, " + name + "!");
  }, 1000);
  return deferred.promise();
}

asyncGreet("World").done(function(greeting) {
  console.log(greeting); // 输出: Hello, World!
});
```

### 3. C#中的Task<T>和TaskCompletionSource<T>

在C#中，`Task<T>`用于表示一个异步操作。`TaskCompletionSource<T>`允许手动控制`Task<T>`的完成状态，这在创建自定义的异步操作时非常有用。

```csharp
public Task<string> GetDataAsync() {
    var tcs = new TaskCompletionSource<string>();
    // 模拟异步操作
    Task.Run(() => {
        Thread.Sleep(1000); // 模拟延时
        tcs.SetResult("Hello World");
    });
    return tcs.Task;
}

// 使用
var task = GetDataAsync();
Console.WriteLine(await task); // 输出: Hello World
```

### 4. JavaScript中的Promise

在JavaScript（ECMAScript 6及更高版本）中，`Promise`是处理异步操作的首选方式。`Promise`对象代表一个最终将完成（成功或失败）的操作。

```javascript
let promise = new Promise(function(resolve, reject) {
  setTimeout(() => resolve("Hello World!"), 1000);
});

promise.then(
  result => console.log(result), // 输出: Hello World!
  error => console.log(error)
);
```

每种语言的实现细节和语法可能有所不同，但它们共同的目的是提供一种更优雅的方式来处理异步操作，使得代码更容易理解和维护。

---

---

解释：

当然可以，使用`async`和`await`可以使异步代码更加清晰易读。下面是根据之前示例修改成`async`和`await`模式的代码。

### 1. Java中的CompletableFuture与async/await

Java原生不支持`async`和`await`关键字，但是可以通过`CompletableFuture`来实现类似的异步编程模式。

```java
public static void main(String[] args) {
    CompletableFuture.supplyAsync(() -> "Hello")
        .thenAccept(result -> System.out.println(result)); // 输出: Hello
}
```

### 2. JQuery没有原生的async/await支持

由于JQuery是基于JavaScript，但JavaScript的`async`和`await`功能并不依赖于JQuery，因此对于原生JavaScript函数，我们可以这样做：

```javascript
async function asyncGreet(name) {
  return new Promise(resolve => {
    setTimeout(() => resolve("Hello, " + name + "!"), 1000);
  });
}

async function greet() {
  const greeting = await asyncGreet("World");
  console.log(greeting); // 输出: Hello, World!
}

greet();
```

### 3. C#中的Task<T>与async/await

在C#中，可以直接使用`async`和`await`关键字来处理`Task<T>`的异步操作。

```csharp
public async Task<string> GetDataAsync() {
    await Task.Delay(1000); // 模拟延时
    return "Hello World";
}

// 使用
public async Task RunAsync() {
    string result = await GetDataAsync();
    Console.WriteLine(result); // 输出: Hello World
}

RunAsync().Wait();
```

### 4. JavaScript中的Promise与async/await

JavaScript中的`Promise`可以与`async`和`await`结合使用，以更直观地处理异步操作。

```javascript
async function asyncHello() {
  let promise = new Promise((resolve, reject) => {
    setTimeout(() => resolve("Hello World!"), 1000);
  });
  let result = await promise; // 等待直到Promise解决
  console.log(result); // 输出: Hello World!
}

asyncHello();
```

通过使用`async`和`await`，代码更加接近同步编写的样式，使得异步流程的管理变得更加直观和易于理解。

---



## 简史

这是一个简要的时间线，回顾了我们今天所熟知的 futures 和 promises 的发展史：

![时间线](/doc/illustrations/asynchronous/1.png)

最早与 futures/promises 相关的概念出现在 1961 年，称为 thunks。Thunks 可以视为 future 或 promise 概念的一个早期、简单形式。根据其发明者 P. Z. Ingerman 的描述，thunks 是：

>一段生成地址的代码
>
>(Ingerman, 1961)[https://dl.acm.org/doi/10.1145/366062.366084]

Thunks 旨在为 Algol-60 程序调用中实际参数与其形式定义之间的绑定提供一种方式。当一个程序使用表达式作为形式参数进行调用时，编译器会创建一个 thunk，这个 thunk 负责计算表达式，并将结果的地址存放在一个预定的位置。可以把 thunk 看作是一种在单线程环境下执行的延续或函数。

---

解释：

Algol-60是一种非常早期的编程语言，而且由于它的历史地位，实际上很少有现代编程环境支持直接运行Algol-60代码。因此，直接提供一个精确的、可以在现代环境中执行的Algol-60示例可能是不可行的。不过，我可以提供一个简化的伪代码示例来解释thunk在Algol-60中的用途，并尝试解释这个概念。

在Algol-60及其相关文献中，thunk通常被用来实现参数的延迟计算，尤其是在过程调用中。在这里，thunk充当一个封装了表达式计算逻辑的代码块，只有当实际需要其结果时才进行计算。

### 伪代码示例

假设我们有一个过程（在Algol-60中称为`procedure`），它接受一个数值参数，并计算某个基于这个参数的表达式。在不使用thunk的情况下，参数在过程调用之前就被计算了。但是，如果我们想要延迟这个计算，直到实际需要这个值的时候，我们可以使用thunk。

不使用thunk的情况：

```algol
procedure compute(x);
begin
    print(x + 10);
end;

x := 5;
compute(x); // 直接传递x的值
```

使用thunk的情况：

```algol
procedure compute(thunkX);
begin
    x := thunkX(); // 在需要使用x的值时调用thunk
    print(x + 10);
end;

thunk procedure thunkX(); // 定义一个thunk
begin
    x := 5; // 延迟计算x的值
    return x;
end;

compute(thunkX); // 传递thunk而非直接值
```

### 解释

在这个伪代码示例中，我们定义了一个`compute`过程，它接受一个名为`thunkX`的参数。与直接传递一个数值不同，`thunkX`是一个延迟执行的函数（或者说是thunk），它封装了一个表达式的计算。

- 在不使用thunk的例子中，`x`的值在传递给`compute`过程之前就已经确定了。
- 使用thunk后，我们将计算`x`值的逻辑封装在`thunkX`过程中，并且只有在`compute`过程实际需要`x`的值时，`thunkX`才会被调用执行。

这种方式允许Algol-60程序实现参数的延迟计算，从而为早期的编程语言提供了处理异步计算和优化性能的一种方法。尽管这个示例是伪代码，但它展示了thunk如何在过程调用中用于实现延迟参数计算的基本理念。

---

Futures 这一概念最早出现在 Baker 和 Hewitt 发表的一篇论文中，主题为进程的增量垃圾收集（Incremental Garbage Collection of Processes, Baker & Hewitt, 1977）。他们首次使用了“call-by-futures”这一术语，描述了一种特殊的调用机制，其中每一个方法的形参都被绑定到一个独立进程，这个进程将与其他形参中的表达式并行进行计算。在这篇论文发布之前，Algol 68 也探索了并发参数评估的可能性，通过引入并行子句和并行子句来进行参数绑定。

在他们的研究中，Baker 和 Hewitt 提出了 Futures 作为一种三元组的概念，这一三元组代表了一个表达式 `E`，其中包括：

1. 用于计算 `E` 的进程，
2. 存储 `E` 计算结果的内存位置，
3. 等待 `E` 计算结果的进程列表。

然而，值得注意的是，他们的研究重点并不是探讨 Futures 在异步分布式计算中的作用，而是聚焦于如何垃圾收集那些函数不再需要的表达式评估所产生的进程。

Multilisp 语言（Halstead, 1985），由 Halstead 在1985年提出，是在 call-by-future 概念基础上进一步发展，并引入了 future 注解。在 Multilisp 中，如果一个变量与一个 future 表达式绑定，系统就会启动一个新进程来计算该表达式，并将结果与代表其最终输出的变量关联起来。这意味着，Multilisp 为在新进程中并行执行任意表达式提供了方法，使得程序能够在不等待 future 完成的情况下继续向前执行。如果 future 的结果值最终没有被用到，那么启动该计算的进程也不会被阻塞，有效避免了可能的死锁问题。此外，MultiLisp 还引入了一种名为 “delay” 的 lazy future 变种，这种变体只有在程序其他部分首次请求其值时才会进行计算。


---

解释：

在 Multilisp 中，`future` 关键字用于创建一个并行计算过程，允许程序在等待计算结果的同时继续执行其他任务。下面是一个使用 `future` 的简单示例，以及对其使用方式的详细解释。

### 示例

假设我们有两个计算密集型函数 `compute-a` 和 `compute-b`，它们分别计算并返回两个数值。我们希望并行执行这两个函数，然后将它们的结果相加。

```lisp
(define (compute-sum)
  (let ((a (future (compute-a)))
        (b (future (compute-b))))
    (+ (force a) (force b))))
```

### 解释

- `future` 关键字创建了一个新的并行计算过程。在这个例子中，`(future (compute-a))` 和 `(future (compute-b))` 分别启动了两个并行进程，这两个进程分别计算 `compute-a` 和 `compute-b` 函数的结果。
- `let` 绑定构造用于将 `future` 表达式的结果（即并行计算过程）绑定到变量 `a` 和 `b`。此时，`a` 和 `b` 并不直接存储函数的计算结果，而是存储了这些结果的 `future` 引用。
- 使用 `force` 函数来获取 `future` 引用的实际计算结果。在 `(+ (force a) (force b))` 表达式中，`force` 被用于 `a`和`b`，这会阻塞当前进程直到 `a` 和 `b` 所代表的计算完成，并获取它们的结果。
- 最终，通过 `force` 获取到的 `a` 和 `b` 的结果被相加，返回最终的求和结果。

通过这种方式，`future` 使得 `compute-a` 和 `compute-b` 可以并行执行，而主进程不必在这两个函数计算完成之前就阻塞等待。这样不仅提高了程序的执行效率，还使得代码能够更灵活地处理并行计算任务。在等待 `compute-a` 和 `compute-b` 的结果期间，主进程可以继续执行其他操作，直到需要这些结果进行下一步计算时才通过 `force` 获取它们。

---


Multilisp 对 futures 的创新设计对 Argus 编程语言中所谓的 promises 构造产生了深远的影响，这一构造由 Liskov 和 Shrira 在 1988 年引入（Liskov & Shrira, 1988; Liskov, 1988）。与 Multilisp 中的 futures 相似，Argus 中的 promises 设计为未来某个时刻可用值的结果的占位符。不同于 Multilisp 的单机并发焦点，Argus 被设计为支持分布式编程，特别是通过 promises 将异步 RPC 整合进 Argus 编程语言中。

一个关键的创新是，Argus 通过为 promises 引入类型系统，从而扩展了 Multilisp 中 futures 的概念。因此，在 Argus 中，一旦发起 promise 调用，就会创建一个立即返回的 promise，并在新的进程中启动一个类型安全的异步 RPC 调用。当 RPC 调用完成后，返回值就可以被调用方获取。

Argus 引入了一种名为 call streams 的概念，它为并发执行的调用序列提供了一种顺序执行的强制机制。通过这种机制，一个发送方和一个接收方被一个流所连接，允许进行常规的（同步）RPC 调用或者流调用，在流调用中，发送方可以在还未收到回复的情况下继续发起更多调用。尽管如此，底层的运行时系统确保即便是非阻塞的流调用也能保证所有调用及其随后的回复都是按照发起顺序进行的。也就是说，call-streams 实现了确保每次调用都精确且有序地完成交付。此外，Argus 通过引入特定的构造来组合 call-streams，以此构建起计算的管道或计算的有向无环图（DAGs），这种方式为复杂计算模型提供了支持。

---

解释：

Argus 是一种为分布式系统设计的编程语言，其中引入了 promises 概念，以支持异步操作和提高分布式编程的效率。虽然 Argus 作为一种较早的语言，在当前可能不再被广泛使用，但其对 promises 的实现提供了对现代异步编程概念的早期理解。以下是一个虚构的示例，用以说明在 Argus 或类似支持 promises 的语言中，如何使用 promises 进行异步 RPC 调用。

假设有一个分布式应用，其中一个服务需要从另一个远程服务获取数据。在没有 promises 的情况下，这可能需要阻塞调用，直到远程服务响应。使用 promises，这个过程可以异步进行。

```argus
// 假设的Argus代码，展示promises的使用

// 定义一个远程服务调用，返回一个promise
function fetchRemoteData(): Promise<String> {
    // 在这里启动异步RPC调用
    var promise = new Promise<String>();
    
    // 模拟异步操作，假设完成后调用promise的resolve方法
    asyncRPC("http://example.com/data", (result) => {
        promise.resolve(result); // 当RPC调用完成，使用返回的结果解决promise
    }, (error) => {
        promise.reject(error); // 如果RPC调用失败，拒绝promise
    });
    
    return promise;
}

// 使用promise处理异步结果
function processData() {
    var dataPromise = fetchRemoteData();
    
    // 当promise完成时处理数据
    dataPromise.then((data) => {
        console.log("Received data: " + data);
        // 这里可以进行数据处理
    }).catch((error) => {
        console.error("Error fetching data: " + error);
    });
}

// 调用processData开始处理
processData();
```

在这个示例中，`fetchRemoteData`函数发起一个异步RPC调用来获取远程数据，返回一个promise对象。这个promise对象被用来表示异步操作的最终结果。通过`then`方法，我们为promise注册了一个回调函数，该函数在promise被解决时执行，即当远程数据被成功获取时。如果RPC调用失败，通过`catch`方法注册的回调函数将被执行，处理错误情况。

虽然这是一个在现代JavaScript风格下构造的Argus示例，但它清楚地展示了promises在异步编程中的使用方式，以及如何利用promises来处理异步RPC调用的结果，无需阻塞等待远程服务的响应。这种模式在现代编程语言中仍然非常重要，对于理解和实现非阻塞的异步编程模型至关重要。

---


E 语言是为分布式计算设计的面向对象编程语言，由 Mark S. Miller、Dan Bornstein 等人于 1997 年创立。E 语言的核心贡献之一是其对 promises 的独特解释和实现，这一点源自于它的前身——数据流编程语言 Joule。

E 语言引入了 `<-` 这一最终操作符，引领了所谓的“最终发送”机制，允许程序在不等待当前操作完成的情况下，继续执行下一条语句，这与同步调用的传统语义形成鲜明对比。

这种机制使得程序能够异步排队执行调用，并立即返回一个 promise，而不阻塞当前执行流。通过这种方式，即使 promise 的结果尚未准备好，后续的消息也可以排队并在 promise 解决后被转发，实现了对异步操作的流畅处理。

也就是说，一旦我们有了一个promise，我们就能够链式地进行几次管道化的最终发送，就好像初始promise已经解决了一样。这种promise管道的概念（Miller, Tribble, & Jellinghaus, 2007）已被大多数当代futures/promises的解释所采纳。

---

解释：

由于E语言专注于安全的分布式计算，并引入了独特的异步通信机制，下面提供了一个假想的E语言示例，以说明promises的使用方式。请注意，这个示例旨在概念性地展示E语言如何处理异步操作和promises，而不是一个真实的代码示例。

### 假想的E语言示例

假设我们有一个分布式系统，其中一个节点需要从另一个节点请求数据。在E语言中，我们可以使用`<-`操作符来实现这一异步调用，并利用promise来处理返回的结果。

```e
def remoteService := locateNode("DataService");

// 发起异步RPC调用
def resultPromise := remoteService <- fetchData("queryParam");

// 使用eventually关键字处理promise的结果
eventually(resultPromise) to be (result) {
  println(`查询结果是: ${result}`);
} catch (problem) {
  println(`查询发生错误: ${problem}`);
}
```

### 解释

1. **定位远程服务：** 首先，我们使用`locateNode`函数来定位网络中提供数据服务的节点，并将其赋值给`remoteService`变量。

2. **发起异步调用：** 通过`<-`操作符，我们对`remoteService`发起一个异步的`fetchData`调用，并传入查询参数`"queryParam"`。这个调用立即返回一个promise对象，代表将来可获得的结果，而不会阻塞当前线程。

3. **处理异步结果：** 使用`eventually`关键字来注册对promise结果的处理逻辑。当`resultPromise`被解决（fulfilled）时，`eventually`块内的代码将被执行。这里，我们使用一个lambda表达式来处理成功获取的结果或捕获可能发生的异常。

4. **结果或错误处理：** 如果`fetchData`调用成功返回结果，`result`变量将被赋值，然后打印查询结果。如果过程中发生错误，例如网络问题或服务端错误，将执行`catch`部分的代码，打印出错误信息。

这个示例展示了E语言如何使用promises和最终发送（eventual send）来处理分布式系统中的异步操作。通过这种方式，E语言支持高效的非阻塞通信模式，使得开发者能够在保持代码简洁的同时，构建复杂的分布式应用。这种对异步操作的优雅处理，尤其在开发需要快速响应和高并发处理能力的分布式系统时，显示出极大的优势。

---

直到 2000 年代初期，Futures 和 Promises 的概念在很大程度上仍然被视为学术界的研究主题。然而，随着网络应用和网络系统开发的迅速发展，以及对更加流畅和响应式用户界面的需求日益增长，这些概念开始在实际开发中显示出其价值。

在主流编程语言当中，Python 在 2002 年通过引入 Twisted 库（Lefkowitz, 2002）成为了首批采纳与 E 语言 Promises 相似概念的语言之一。Twisted 库引进了 Deferred 对象的概念，这些对象被设计用来承载一个异步操作的最终结果，这一结果在对象创建时尚未知晓。在 Twisted 框架中，Deferred 对象作为一等公民，意味着它们可以像任何普通 Python 对象一样被传递和操作，其主要区别在于 Deferred 对象本身并不直接持有值。而是，这些对象提供了一种机制，允许开发者注册一系列回调函数，这些回调将在异步操作完成时被触发执行。

---

解释：

在 Twisted 库中，`Deferred` 对象是处理异步编程的核心。一个 `Deferred` 对象代表了一个尚未完成的操作，允许你附加回调函数来处理操作完成时的结果。以下是一个简单的示例，展示了如何使用 Twisted 中的 `Deferred` 对象实现异步编程，并对其进行详细解释。

### Twisted Deferred示例代码

```python
from twisted.internet.defer import Deferred

def callback(result):
    print("回调被调用，结果是:", result)
    return "处理完成"

def errback(failure):
    print("错误回调被调用，错误是:", failure)
    return "错误处理完成"

# 创建Deferred对象
d = Deferred()

# 添加回调和错误回调
d.addCallback(callback)
d.addErrback(errback)

# 模拟异步操作完成，并设置结果
d.callback("异步操作的结果")

# 如果异步操作失败，可以使用d.errback(...)触发错误回调
# d.errback(Exception("异步操作失败"))
```

### 详细解释

1. **创建Deferred对象：** 示例中首先创建了一个 `Deferred` 对象`d`。这个对象代表了一个尚未完成的异步操作。

2. **添加回调和错误回调：** 通过 `addCallback` 方法，我们为 `Deferred` 对象添加了一个回调函数 `callback`，该函数在异步操作成功完成时被调用。通过 `addErrback` 方法，我们添加了一个错误回调函数 `errback`，用于处理异步操作失败的情况。

3. **触发回调：** 使用 `Deferred` 对象的 `callback` 方法可以模拟异步操作的完成，并将结果传递给回调函数。在这个示例中，我们传递了字符串`"异步操作的结果"`作为操作的结果，这会导致 `callback` 函数被调用，并打印出结果。

4. **错误处理：** 如果异步操作失败，我们可以使用 `Deferred` 对象的 `errback` 方法来模拟这一情况。这将触发之前通过 `addErrback` 添加的错误回调函数 `errback`，并传递一个异常对象给它。在这个示例中，我们注释掉了 `errback` 的调用，以展示成功的情况。如果要测试错误处理，可以取消注释 `d.errback(...)` 这行代码。

通过这种方式，Twisted 的 `Deferred` 对象提供了一种强大的机制来管理和组织异步编程中的回调，使得代码更加清晰和易于维护。`Deferred` 对象使开发者能够优雅地处理异步操作的成功完成和潜在的错误情况，而无需深入底层的事件循环或其他复杂的异步处理逻辑。


Python的`asyncio`库是Python 3.4中引入的一个用于编写单线程并发代码的库，它使用`async`和`await`语法来定义协程（coroutines），这是一种比基于回调的异步编程更清晰、更直观的方式。与Twisted的`Deferred`对象相比，`asyncio`提供了一种不同的异步编程范式。

### Twisted与asyncio的主要区别：

1. **编程模型：** Twisted 使用回调模型来处理异步操作，而 `asyncio` 使用协程模型。协程允许使用更接近同步代码的方式来编写异步代码，使得代码更容易理解和维护。

2. **语法：** Twisted 的异步模型主要依赖于 `Deferred` 对象和回调函数，而 `asyncio` 使用 `async` 和 `await` 关键字来定义和等待异步操作。

3. **社区和生态系统：** `asyncio` 是 Python 标准库的一部分，因此它与 Python 的其他部分（如类型提示）更加集成，并且得到了更广泛的社区支持。Twisted 是一个独立的项目，拥有自己的生态系统和一系列专门的库和工具。

### 使用 asyncio 的示例代码

下面是如何使用 `asyncio` 库来实现上述 Twisted 示例的异步操作：

```python
import asyncio

async def async_operation():
    # 模拟异步操作
    await asyncio.sleep(1)
    return "异步操作的结果"

async def main():
    try:
        # 等待异步操作完成并获取结果
        result = await async_operation()
        print("异步操作完成，结果是:", result)
    except Exception as e:
        # 处理可能发生的错误
        print("异步操作失败，错误是:", e)

# 运行事件循环
asyncio.run(main())
```

### 详细解释

1. **定义异步操作：** 使用 `async def` 定义了一个异步函数 `async_operation`，它模拟一个异步操作（这里使用 `asyncio.sleep` 来模拟）并返回一个结果。

2. **等待异步操作：** 在 `main` 函数中，使用 `await` 关键字等待 `async_operation` 函数的结果。这里的 `await` 会暂停当前协程的执行，直到被等待的协程完成，然后继续执行并获取结果。

3. **错误处理：** 通过 `try...except` 块来处理异步操作中可能发生的错误。

4. **事件循环：** 使用 `asyncio.run(main())` 来运行主函数。`asyncio.run` 函数负责运行事件循环 Event Loop，执行 `main` 函数，并在函数完成后关闭事件循环。

通过这个 `asyncio` 示例，可以看到 `async/await` 语法提供了一种更简洁和直观的方式来处理异步操作，相比于基于回调的方式，它使得异步代码的结构更接近传统的同步代码，从而更易于理解和维护。

---

在 JavaScript 领域，promises 的概念可能是近年来最为人所熟知的。2007 年，受到 Python 的 Twisted 库启发，Dojo Toolkit 的开发者实现了一个类似于 Twisted 的 deferred 对象的 JavaScript 版本，即 `dojo.Deferred`。

这一创新随后激发了 Kris Zyp 于 2009 年提出 CommonJS Promises/A 规范。同年，Ryan Dahl 推出了 Node.js，其早期版本在非阻塞 API 中采用了 promises。然而，随着 Node.js 转向错误优先的回调 API，对于一个标准化的 promises API 的需求变得更加迫切。

这个空白期间，Kris Kowal 开发的 Q.js 成为了 Promises/A 规范的一个实现，而 AJ O'Neal 的 FuturesJS 库则试图以不同的方式解决流控制问题。

2011 年，jQuery v1.5 将 promises 引入到了更广泛的开发者群体中，尽管其 promises API 与 Promises/A 规范在某些细节上有所不同。

随着 HTML5 和多种 API 的兴起，不一致和复杂的接口问题加剧了所谓的“回调地狱”的问题。为了解决这些问题，Promises/A+ 规范应运而生，并最终在社区的广泛接受下，promises 在 ECMAScript® 2015 语言规范中被正式采纳。尽管如此，由于 Promises/A+ 规范缺乏向后兼容性和一些额外特性，像 BlueBird 和 Q.js 这样的库在 JavaScript 生态系统中仍然扮演着重要角色。

---

解释：

JavaScript 中 promises 的概念经历了从早期的实验性实现到成为语言规范的一部分的演变过程。以下是几个关键阶段的代码示例，展示了这一演变过程。

### 1. Dojo的`dojo.Deferred`

早期的实验性实现，受到 Python Twisted 库的启发。

```javascript
var deferred = new dojo.Deferred();

deferred.then(function(result) {
  console.log("成功:", result);
}, function(error) {
  console.log("失败:", error);
});

// 模拟异步操作
setTimeout(function() {
  deferred.resolve("操作成功");
  // 或者在失败时调用 deferred.reject("操作失败");
}, 1000);
```

在这个示例中，`dojo.Deferred` 创建了一个 Deferred 对象。通过 `.then` 方法添加了成功和失败的回调。

### 2. CommonJS Promises/A

提案引入了 Promise 的概念，强调了 thenable 接口。

```javascript
// 假设有一个符合Promises/A规范的promise库
var promise = asyncOperation();

promise.then(function(result) {
  console.log("成功:", result);
}, function(error) {
  console.log("失败:", error);
});
```
这个阶段的代码示例更加抽象，强调了 promise 的基本用法，即通过 `.then` 处理异步操作的结果。

### 3. ES2015 (ES6) Promises

ECMAScript 2015 (ES6) 将Promises正式纳入语言规范。

```javascript
let promise = new Promise(function(resolve, reject) {
  // 模拟异步操作
  setTimeout(function() {
    resolve("操作成功");
    // 或者 reject("操作失败");
  }, 1000);
});

promise.then(function(result) {
  console.log(result);
}).catch(function(error) {
  console.log(error);
});
```

在这个阶段，`Promise` 构造函数接受一个执行器函数，该函数包含 `resolve` 和 `reject` 方法来决定 promise 的状态。`.then` 和 `.catch` 方法用于处理成功和失败的结果。

### 4. Async/Await

ES2017 引入了async/await，进一步简化了异步操作的处理。

```javascript
async function asyncOperation() {
  return "操作成功";
}

async function run() {
  try {
    let result = await asyncOperation();
    console.log(result);
  } catch (error) {
    console.log(error);
  }
}

run();
```

在这个示例中，`async` 函数 `run` 通过 `await` 关键字等待 `asyncOperation` 的结果，使得异步代码看起来更像是同步代码。

以上代码示例展示了 JavaScript 中 promises 概念从早期实验性实现到成为语言规范一部分的演变过程，以及如何通过新的语言特性（如 async/await）进一步简化异步编程。

---

---

解释：

关键发展
1. Python 的异步支持：Python 通过 asyncio 库进一步增强了对异步编程的支持，该库是 Python 3.4 中引入的，旨在使用 async 和 await 关键字来编写异步代码。这标志着 Python 对于 futures 和 promises 概念的原生支持，进一步简化了异步编程。

2. JavaScript 的 Promise：随着 ECMAScript 2015（即ES6）的发布，Promise 成为了 JavaScript 语言规范的一部分，为异步编程提供了原生支持。这使得开发者能够更加轻松地编写处理异步操作的代码，尤其是在构建复杂的 Web 应用时。

3. C# 的 Task 和 async/await：C# 通过引入 Task 类和 async/await 语法，提供了对异步编程的强大支持。这些特性自 .NET Framework 4.5 和 C# 5.0 起被引入，大大简化了异步编程模型，使得编写异步代码几乎和同步代码一样简单。

4. Java 的 CompletableFuture：Java 8 引入了 CompletableFuture，它提供了一个非阻塞的方式来处理异步编程。通过允许开发者以声明式的方式处理异步操作的结果，CompletableFuture 在 Java 社区中受到了广泛欢迎。

---

## 执行的语义

随着技术的演进，架构和运行时环境经历了显著的变化，对 futures/promises 的实现方法也随之发展，目的是使这些抽象能够更高效地利用系统资源。

在本节中，我们即将深入探讨构成 futures/promises 基础的三种主要执行模型，这些模型在当下流行的编程语言和库中得到了广泛应用。

具体来说，我们将揭示在这些 API 背后，futures 和 promises 是如何被实际执行和解决的，以及这些过程如何影响到程序的性能和资源管理。

### 线程池

线程池是一种编程抽象，它允许开发者利用一组预先创建且处于等待状态的线程来执行任务。

这种机制通过集中处理线程的创建、管理和任务调度，避免了直接操作线程时可能遇到的许多复杂性和高昂的资源成本。

线程池的设计和实现多种多样，它们可以根据不同的任务调度策略和执行需求来选择，线程数量既可以是固定的，也可以设计为根据系统负载动态调整，以优化资源利用和响应性。

Java 的 `Executor` 框架是线程池实现的一个经典例子，它通过 `Executor` 对象来执行实现了 `Runnable` 接口的任务。`Executor` 框架的设计理念在于提供一个高级的抽象，使开发者不需要关注任务将如何被具体执行的细节，如任务将由哪个线程执行、任务的调度策略等。这些细节被隐藏在 `Executor` 接口的底层实现之中，允许开发者通过简单的 API 调用来提交任务，而具体的执行逻辑则由 `Executor` 框架自动管理。

---

解释：

Java的`Executor`框架提供了一个强大的机制来异步执行任务。下面是一个使用`ExecutorService`（`Executor`框架的一个子接口）来执行任务的简单示例，以及对其工作原理的详细讲解。

### 示例代码

```java
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class ExecutorExample {
    public static void main(String[] args) {
        // 创建一个固定大小的线程池
        ExecutorService executor = Executors.newFixedThreadPool(2);

        // 提交三个任务到线程池执行
        for (int i = 0; i < 3; i++) {
            int taskId = i;
            executor.submit(() -> {
                System.out.println("正在执行任务 " + taskId + " 由线程 " + Thread.currentThread().getName() + " 执行");
                try {
                    // 模拟任务执行时间
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            });
        }

        // 关闭ExecutorService，不再接受新任务，已提交的任务继续执行
        executor.shutdown();
    }
}
```

### 工作原理讲解

1. **创建线程池：** 示例中使用`Executors.newFixedThreadPool(2)`创建了一个固定大小为2的线程池。这意味着线程池内部会维护两个线程，准备执行提交给它的任务。

2. **提交任务：** 通过`executor.submit()`方法提交任务给线程池执行。在这个示例中，提交了三个Lambda表达式作为任务。每个任务简单地打印出任务ID和执行它的线程的名称，然后通过`Thread.sleep(1000)`模拟长时间执行。

3. **任务执行：** 线程池中的线程会并发地执行提交的任务。由于线程池的大小为2，因此任何时刻最多只有两个任务被并行执行。第三个任务将会等待，直到线程池中有线程变为可用。

4. **关闭线程池：** 使用`executor.shutdown()`方法关闭线程池。这个调用并不会立即终止线程池，而是不再接受新的任务，已提交的任务则会继续执行直至完成。

通过这个简单的示例，我们可以看到`Executor`框架如何简化并发任务的执行，通过提供一个高级的任务提交机制，允许开发者专注于任务的实现，而不是任务的执行细节。线程池的使用还有助于提高资源的利用率和程序的响应性，是Java并发编程中一个非常实用的工具。

---

与 Java 的 `Executor` 类似，Scala 通过其 `scala.concurrent` 包提供了 `ExecutionContext` 作为并发编程的一部分。Scala 的 `ExecutionContext` 与 Java 的 `Executor` 追求相同的目标：它负责高效地并行执行任务，同时免除开发者需要直接处理诸如任务调度等并发编程的复杂细节。`ExecutionContext` 的设计充分考虑了灵活性，它被设计成一个接口，这意味着开发者可以根据需要替换底层的线程池实现，而不影响到使用线程池的代码逻辑。

---

解释：

在 Scala 中，`scala.concurrent`包提供了丰富的并发编程工具，其中`ExecutionContext`是执行异步任务的关键组件。`ExecutionContext`充当 Scala 中异步代码的执行环境，它抽象了线程池的细节，使得开发者可以更加专注于业务逻辑而不是底层的线程管理和调度问题。以下是一个使用 `ExecutionContext` 进行线程池操作的示例，以及对其工作原理的详细解释。

### 示例代码

```scala
import scala.concurrent.{ExecutionContext, Future}
import scala.concurrent.ExecutionContext.Implicits.global

object ExecutionContextExample extends App {
  // 定义一个简单的异步任务
  val futureTask: Future[Int] = Future {
    // 假设这是一个计算密集型任务
    println(s"执行任务的线程：${Thread.currentThread.getName}")
    42
  }(ExecutionContext.global)

  futureTask.onComplete {
    case scala.util.Success(result) => println(s"任务结果：$result")
    case scala.util.Failure(exception) => exception.printStackTrace()
  }(ExecutionContext.global)

  // 防止程序过早退出
  Thread.sleep(1000)
}
```

### 工作原理解释

1. **引入必要的类和对象：**示例首先引入了`scala.concurrent`包中的`ExecutionContext`和`Future`，以及`ExecutionContext.Implicits.global`，这是一个全局的`ExecutionContext`实例，提供了一个通用的线程池。

2. **定义异步任务：**通过`Future`构造函数定义了一个异步任务，这个任务在`ExecutionContext.global`提供的线程池中异步执行。在这个示例中，任务是一个简单的计算操作。

3. **执行任务：**`Future`构造函数接受一个代码块作为参数，这个代码块包含了需要异步执行的任务。在这个代码块中，我们打印了当前线程的名称，并返回了一个结果。

4. **处理结果：**通过`futureTask.onComplete`方法注册了一个回调函数来处理任务完成后的结果。这个回调函数同样在`ExecutionContext.global`指定的线程池中执行。

5. **阻塞等待：**最后，为了防止主程序直接退出而不等待异步任务完成，使用了`Thread.sleep(1000)`来简单地等待一段时间。

通过这个示例，可以看到`ExecutionContext`如何在Scala中被用来管理和执行异步任务，同时也展示了`Future`和`ExecutionContext`如何协同工作，以在Scala中实现高效的并发编程。

---

虽然 Scala 允许开发者根据需求选择不同的线程池实现，但其默认的 ExecutionContext 实现背后是 Java 的 ForkJoinPool。ForkJoinPool 采用了一种高效的工作窃取算法，使得处于空闲状态的线程能够主动接手原本分配给其他忙碌线程的任务。这种设计使得 ForkJoinPool 成为了一个广受欢迎的线程池选择，主要原因在于其相较于传统的 Executors 实现，能够提供更优的性能，更有效地避免因线程池导致的死锁现象，并且显著减少了线程之间切换的时间消耗。

---

解释：

Java的`ForkJoinPool`是专为了高效执行大量小任务而设计的，并发框架的一部分，利用工作窃取算法来平衡线程之间的工作负载。下面是一个简单的`ForkJoinPool`使用示例，我们将通过这个示例详细解释其运行机制。

### 示例代码

假设我们需要计算从1加到100的总和，这个任务可以被分解为更小的任务，然后由`ForkJoinPool`并发执行。

首先，定义一个任务类，该类继承自`RecursiveTask`（用于有返回结果的任务），并重写`compute`方法来实现任务的拆分和计算逻辑：

```java
import java.util.concurrent.RecursiveTask;
import java.util.concurrent.ForkJoinPool;

public class SumTask extends RecursiveTask<Long> {
    private final long start;
    private final long end;
    private static final long THRESHOLD = 10; // 任务分解的阈值

    public SumTask(long start, long end) {
        this.start = start;
        this.end = end;
    }

    @Override
    protected Long compute() {
        long length = end - start;
        if (length <= THRESHOLD) {
            // 任务足够小,直接计算
            long sum = 0;
            for (long i = start; i <= end; i++) {
                sum += i;
            }
            return sum;
        } else {
            // 任务过大,一分为二
            long middle = (start + end) / 2;
            SumTask task1 = new SumTask(start, middle);
            SumTask task2 = new SumTask(middle + 1, end);
            invokeAll(task1, task2); // 并行执行两个小任务
            return task1.join() + task2.join(); // 获取结果并合并
        }
    }

    public static void main(String[] args) {
        ForkJoinPool pool = new ForkJoinPool(); // 创建ForkJoinPool实例
        SumTask task = new SumTask(1, 100); // 创建任务
        long result = pool.invoke(task); // 执行任务并获取结果
        System.out.println("The sum from 1 to 100 is: " + result);
    }
}
```

### 运行机制解释

1. **任务分解（Fork）:** `SumTask`继承自`RecursiveTask`，允许它通过递归的方式将大任务分解成足够小的子任务，直到子任务的规模达到定义的阈值`THRESHOLD`。在上述例子中，如果任务计算的数字范围超过10，我们就将任务一分为二，分别计算。

2. **工作窃取算法:** `ForkJoinPool`内部的每个工作线程都维护着一个待执行任务的双端队列。当一个线程完成了自己队列中的所有任务后，它可以从其他线程的队列末尾“窃取”任务来执行。这种策略有效地减少了线程间的工作不均衡现象。

3. **任务执行（Join）:** 一旦子任务的计算完成，通过`join`方法可以获取子任务的结果，并将这些结果合并起来。在上述例子中，当任务被分解成足够小的子任务后，这些子任务被并发执行，并通过`join`方法收集最终的计算结果。

4. **结果汇总:** 所有子任务的结果最终被合并，计算出最初大任务的结果。

通过这种方式，`ForkJoinPool`使得并行执行大量小任务成为可能，提高了程序在多核处理器上的执行效率。

---

Scala 的 futures（和promises）基于这个 ExecutionContext 接口到一个底层的线程池。虽然通常用户使用的是由 ForkJoinPool 支持的底层默认 ExecutionContext，但如果用户需要特定的行为，如阻塞 futures，他们也可以选择提供（或实现）自己的 ExecutionContext。

在 Scala 编程中，每次使用 future 或 promise 时，都需要依赖一个 ExecutionContext 实例，这通常是通过隐式参数来传递的。默认情况下，大多数 Scala 应用会使用 ExecutionContext.global，这实际上是背后由 ForkJoinPool 支持的 ExecutionContext 的一个实例。

例如，在下面的代码中，我们创建并异步执行了一个返回字符串 "hello world" 的future：

```scala
implicit val ec = ExecutionContext.global
val f: Future[String] = Future { "hello world" }
```

在这个示例中，我们利用了全局执行上下文来异步执行定义的 future。值得注意的是，Future 构造函数中的 ExecutionContext 参数是隐式传递的。这表示如果 Scala 编译器在当前的隐式作用域中能够找到一个 ExecutionContext 实例，它就会自动将这个实例用作 Future 调用的参数，而无需开发者显式指定。在上述代码示例中，通过将 ec 声明为隐式变量，我们将其放入了隐式作用域。


在 Scala 中，futures 和 promises 提供了一种优雅的回调方式来处理异步操作，这一点通过下面的示例得到了很好的体现：

```scala
implicit val ec = ExecutionContext.global

val f = Future {
  Http("http://api.fixed.io/latest?base=USD").asString
}

f.onComplete {
  case Success(response) => println(response)
  case Failure(t) => println(t.getMessage())
}
```

在这个示例中，我们首先定义了一个名为 `f` 的 future，该 future 代表了一个异步的 HTTP 请求。使用 `onComplete` 方法，我们为这个future 指定了一个回调，这个回调根据 future 的完成状态——成功或失败——执行不同的操作。如果请求成功完成，我们将打印出请求的响应。如果在执行过程中遇到错误，我们将打印出错误消息。

这种使用模式展示了 Scala 异步编程的核心特性：能够在不阻塞当前线程的情况下，优雅地处理异步操作的结果。通过隐式提供的 `ExecutionContext`，Scala 确保了这些异步操作能够在合适的线程中执行，同时通过回调机制，开发者可以轻松地管理成功或失败的结果处理逻辑。

