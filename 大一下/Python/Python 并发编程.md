# 🏭 Python 并发编程：进程与线程

> [!TIP] 核心比喻：工厂与工人
> - **进程 (Process)** 就像一个**工厂** 🏭。它拥有自己独立的资源（土地、电力、原材料）。建一个新工厂开销很大。
> - **线程 (Thread)** 就像工厂里的一名**工人** 👷。多个工人在同一个工厂里共享资源，协同工作。雇一个新工人开销很小。
> - **程序 (Program)** 就像工厂的**设计蓝图** 📜。它本身是静态的，只有按照蓝图开办工厂（运行程序），才有了进程。

---

## <span style="color:#3498db;">第一部分：进程 (Process) - 独立的车间</span>

### <span style="color:#5dade2;">① 程序与进程</span>
- **程序 (Program)**: 存储在磁盘上的**静态文件**，如 `.py` 文件、`.exe` 文件。
- **进程 (Process)**: 程序的一次**动态执行过程**。操作系统会为每个进程分配独立的内存空间和系统资源。进程是操作系统进行**资源分配**的基本单位。

### <span style="color:#5dade2;">② 创建进程 (`multiprocessing` 模块)</span>
Python 通过 `multiprocessing` 模块支持多进程编程。

#### <span style="color:#a5b1c2;">实战代码：创建并运行一个子进程</span>
```python
import multiprocessing
import os
import time

# 这是子进程要执行的任务
def worker_task(name):
    print(f"子进程启动，ID: {os.getpid()}, 参数: {name}")
    time.sleep(2) # 模拟任务耗时
    print(f"子进程 {os.getpid()} 结束。")

# __name__ == '__main__' 是启动多进程的必要保护
if __name__ == '__main__':
    print(f"主进程启动，ID: {os.getpid()}")
    
    # 1. 创建一个 Process 对象
    # target=worker_task 指定了子进程要执行的函数
    # args=('任务A',) 是传递给函数的参数，注意是元组形式
    p = multiprocessing.Process(target=worker_task, args=('任务A',))
    
    # 2. 启动子进程
    p.start()
    
    print("主进程继续执行其他任务...")
    
    # 3. 等待子进程执行结束
    # 主进程会在这里阻塞，直到子进程 p 完成任务
    p.join()
    
    print("主进程结束。")
```

### <span style="color:#5dade2;">③ 进程间通信 (IPC - Inter-Process Communication)</span>
因为进程间的内存是隔离的，所以需要借助特殊的工具来通信。`multiprocessing.Queue` 是最常用的工具之一。

#### <span style="color:#a5b1c2;">实战代码：使用 `Queue` 在两个进程间传递数据</span>
```python
import multiprocessing
import time

# 写数据进程
def writer(q):
    print(f"Writer 进程启动...")
    for i in ['A', 'B', 'C']:
        print(f"向队列中放入: {i}")
        q.put(i) # 将数据放入队列
        time.sleep(1)
    print(f"Writer 进程结束。")

# 读数据进程
def reader(q):
    print(f"Reader 进程启动...")
    while True:
        try:
            # 从队列中获取数据，如果队列为空，会阻塞等待
            value = q.get(timeout=5) # 设置5秒超时
            print(f"从队列中读到: {value}")
        except:
            # 队列为空且超时，退出循环
            print("队列已空，Reader 进程结束。")
            break

if __name__ == '__main__':
    # 1. 创建一个进程安全的队列
    q = multiprocessing.Queue()
    
    # 2. 创建读写两个进程
    pw = multiprocessing.Process(target=writer, args=(q,))
    pr = multiprocessing.Process(target=reader, args=(q,))
    
    # 3. 启动进程
    pw.start()
    pr.start()
    
    # 4. 等待进程结束
    pw.join()
    pr.join()
```

---

## <span style="color:#e67e22;">第二部分：线程 (Thread) - 协作的工人</span>

### <span style="color:#f1c40f;">④ 进程 vs. 线程</span>
| 特性 | <span style="color:#3498db;">进程 (Process)</span> | <span style="color:#e67e22;">线程 (Thread)</span> |
| :--- | :--- | :--- |
| **定义** | **资源分配**的基本单位 | **CPU调度**的基本单位 |
| **内存空间** | ✅ **独立**，互不干扰，安全性高 | ❌ **共享**，数据共享方便，但需处理同步问题 |
| **创建开销** | **大**，慢 | **小**，快 |
| **通信** | 复杂，需要 IPC (如 Queue) | 简单，直接读写共享变量 (但需加锁) |
| **GIL 影响** | 不受 GIL 影响，可实现真正的**并行计算** (利用多核) | 受 GIL 影响，同一时刻只有一个线程能执行 Python 字节码 (适用于 I/O 密集型任务) |

> [!WARNING] **GIL (全局解释器锁)**
> 这是 CPython 解释器的一个特性，它保证在任何时刻只有一个线程在执行 Python 字节码。因此，Python 的多线程对于**计算密集型**任务（如大规模数学运算）提升不大，但对于**I/O密集型**任务（如网络请求、文件读写）效果显著，因为它可以在一个线程等待 I/O 时，切换到另一个线程执行。

### <span style="color:#f1c40f;">⑤ 创建线程 (`threading` 模块)</span>

#### <span style="color:#a5b1c2;">实战代码：创建并运行一个子线程</span>
```python
import threading
import time

def thread_task(name, duration):
    print(f"线程 {name} 启动...")
    time.sleep(duration)
    print(f"线程 {name} 结束。")

print("主线程启动...")

# 1. 创建线程对象
t1 = threading.Thread(target=thread_task, args=("音乐播放", 3))
t2 = threading.Thread(target=thread_task, args=("文件下载", 2))

# 2. 启动线程
t1.start()
t2.start()

print("主线程继续执行...")

# 3. 等待子线程结束
t1.join()
t2.join()

print("所有子线程已结束，主线程结束。")
```

### <span style="color:#f1c40f;">⑥ 线程间通信与同步</span>
线程共享内存，通信方便，但也带来了**数据竞争 (Race Condition)** 的风险。必须使用**锁 (Lock)** 来保证数据安全。

#### <span style="color:#a5b1c2;">实战代码：使用 `Lock` 保护共享数据</span>
```python
import threading

# 共享的银行账户余额
balance = 0
# 创建一个锁
lock = threading.Lock()

# 模拟取钱操作
def withdraw(amount):
    global balance
    for _ in range(100000):
        # 1. 获取锁 (如果锁已被占用，则在此阻塞)
        lock.acquire()
        # --- 临界区开始 ---
        balance -= amount 
        # --- 临界区结束 ---
        # 2. 释放锁
        lock.release()

# 模拟存钱操作
def deposit(amount):
    global balance
    for _ in range(100000):
        lock.acquire()
        balance += amount
        lock.release()

t_withdraw = threading.Thread(target=withdraw, args=(10,))
t_deposit = threading.Thread(target=deposit, args=(10,))

t_withdraw.start()
t_deposit.start()
t_withdraw.join()
t_deposit.join()

# 理想结果应为 0，如果不加锁，结果会是一个随机数
print(f"最终余额: {balance}")
```

---

## <span style="color:#2ecc71;">第三部分：生产者-消费者模式</span>

### <span style="color:#27ae60;">⑦ 掌握经典并发模型</span>
这是最经典的多线程/多进程协作模式，用于**解耦**生产任务和消费任务，平衡两者的速度差异。

> [!NOTE] 核心组件
> - **生产者 (Producer)**: 负责创建数据，并放入共享的“**缓冲区**”。
> - **消费者 (Consumer)**: 负责从“**缓冲区**”中取出数据，并进行处理。
> - **缓冲区 (Buffer)**: 通常使用一个线程安全的**队列 (`queue.Queue`)** 来实现。

#### <span style="color:#a5b1c2;">实战代码：基于 `queue` 的生产者消费者模型</span>
```python
import threading
import queue
import time
import random

# 1. 创建一个线程安全的队列作为缓冲区
buffer_queue = queue.Queue(maxsize=5) # 缓冲区最大容量为5

# 生产者线程
def producer(name):
    for i in range(10):
        item = f"产品-{i}"
        time.sleep(random.uniform(0.1, 0.5)) # 模拟生产耗时
        buffer_queue.put(item) # 将产品放入缓冲区
        print(f"生产者 {name} 生产了 {item}, 当前库存: {buffer_queue.qsize()}")
    print(f"生产者 {name} 完成生产。")

# 消费者线程
def consumer(name):
    while True:
        try:
            # 从缓冲区获取产品，如果为空则阻塞等待，设置1秒超时
            item = buffer_queue.get(timeout=1) 
            time.sleep(random.uniform(0.2, 0.8)) # 模拟消费耗时
            print(f"消费者 {name} 消费了 {item}, 剩余库存: {buffer_queue.qsize()}")
            # buffer_queue.task_done() # 可选，用于 q.join()
        except queue.Empty:
            # 如果队列在超时后仍然为空，说明可能生产结束
            print(f"消费者 {name} 等待超时，退出。")
            break

# 创建并启动线程
p = threading.Thread(target=producer, args=("P1",))
c1 = threading.Thread(target=consumer, args=("C1",))
c2 = threading.Thread(target=consumer, args=("C2",))

p.start()
c1.start()
c2.start()

p.join()
c1.join()
c2.join()

print("所有任务完成！")
```