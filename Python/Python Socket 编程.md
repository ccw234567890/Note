# 🔌 Python Socket 编程深度解析

> [!TIP] 核心比喻：把 Socket 当作一部电话 ☎️
> - **`socket()`**: 买一部电话机。
> - **`bind()`**: 给你的电话机申请一个号码 (IP + 端口)。
> - **`listen()`**: 打开电话铃声，等待来电。
> - **`accept()`**: 接听来电，建立通话。
> - **`connect()`**: 拨打别人的号码。
> - **`send()`/`recv()`**: 在通话中说话和听讲。
> - **`close()`**: 挂断电话。

---
## <span style="color:#3498db;">① 什么是 Socket (套接字)？</span>

> [!NOTE] 定义
> Socket 是应用程序与操作系统网络内核之间的一个**编程接口 (API)**。它是在网络上进行数据交换的**端点**，封装了底层的 TCP/IP 协议，让我们可以像读写文件一样方便地收发网络数据。

简单说，Socket 就是你的程序用来**收发网络消息的“插头”**。

---

## <span style="color:#3498db;">② Socket 编程核心流程</span>

网络通信分为**服务器端 (Server)** 和**客户端 (Client)**，它们的 Socket 操作流程不同。

### <span style="color:#e74c3c;">📞 TCP (可靠通话) 流程</span>
| 服务器端 (Server) | 客户端 (Client) |
| :--- | :--- |
| 1. `socket()` 创建套接字 | 1. `socket()` 创建套接字 |
| 2. `bind()` 绑定地址和端口 | |
| 3. `listen()` 开始监听 | |
| 4. `accept()` 接受连接 | 2. `connect()` 连接服务器 |
| 5. `recv()`/`send()` 数据收发 | 3. `send()`/`recv()` 数据收发 |
| 6. `close()` 关闭连接 | 4. `close()` 关闭连接 |

### <span style="color:#f1c40f;">📮 UDP (无连接明信片) 流程</span>
| 服务器端 (Server) | 客户端 (Client) |
| :--- | :--- |
| 1. `socket()` 创建套接字 | 1. `socket()` 创建套接字 |
| 2. `bind()` 绑定地址和端口 | |
| 3. `recvfrom()` 接收数据和地址 | 2. `sendto()` 发送数据到地址 |
| 4. `sendto()` 发送数据到地址 | 3. `recvfrom()` (可选)接收响应 |
| 5. `close()` 关闭套接字 | 4. `close()` 关闭套接字 |

---
## <span style="color:#3498db;">③ 核心 Socket 函数详解</span>

- `socket.socket(family, type)`: 创建 Socket。
  - `family`: `AF_INET` (IPv4) 或 `AF_INET6` (IPv6)。
  - `type`: `SOCK_STREAM` (TCP) 或 `SOCK_DGRAM` (UDP)。
- `sk.bind((host, port))`: 绑定IP地址和端口号。`host` 通常设为 `0.0.0.0` 或空字符串 `''` 表示监听所有网络接口。
- `sk.listen(backlog)`: (仅TCP) 使服务器进入监听状态。`backlog` 是等待连接的队列大小。
- `sk.accept()`: (仅TCP) 阻塞并等待客户端连接。成功后返回 `(conn, addr)` 元组，其中 `conn` 是**新的**专门用于与此客户端通信的 Socket，`addr` 是客户端地址。
- `sk.connect((host, port))`: (仅TCP) 客户端主动连接服务器。
- `sk.recv(bufsize)`: 接收数据，`bufsize` 是单次接收的最大字节数。
- `sk.send(bytes)`: 发送数据，数据必须是**字节 (bytes)** 类型。
- `sk.recvfrom(bufsize)`: (仅UDP) 接收数据，并返回 `(data, addr)` 元组。
- `sk.sendto(bytes, addr)`: (仅UDP) 将数据发送到指定的 `addr` 地址。
- `sk.close()`: 关闭 Socket 连接。

---

## <span style="color:#3498db;">④ 实战代码示例</span>

### <span style="color:#e74c3c;">示例 1：TCP 简单聊天程序</span>
这是一个可靠的、一对一的聊天程序，完美展示了 TCP 的连接过程。

#### <span style="color:#fd79a8;">TCP 服务器 (`tcp_server.py`)</span>
```python
import socket

# 1. 创建 TCP Socket
# AF_INET = 使用 IPv4协议, SOCK_STREAM = 使用 TCP协议
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. 绑定 IP 和端口
# '0.0.0.0' 表示监听本机所有 IP 地址的请求
server.bind(('0.0.0.0', 8080))

# 3. 开启监听
server.listen(5) # 允许最多5个客户端排队等待连接
print("服务器已启动，等待客户端连接...")

# 4. 接受客户端连接 (这是一个阻塞操作)
# conn 是专门为此客户端服务的新 socket 对象
# addr 是客户端的 (IP, 端口)
conn, addr = server.accept()
print(f"与 {addr} 建立连接")

# 5. 循环收发数据
while True:
    try:
        # 接收客户端消息，1024是缓冲区大小(字节)
        data = conn.recv(1024)
        # 如果接收到空数据，表示客户端已断开
        if not data:
            break
        print(f"收到消息: {data.decode('utf-8')}")
        
        # 向客户端回显消息
        conn.send(data.upper()) # 将收到的消息转为大写后发回
    except ConnectionResetError:
        break # 客户端强制断开连接

# 6. 关闭连接
print(f"与 {addr} 的连接已断开")
conn.close()
server.close()
```

#### <span style="color:#fd79a8;">TCP 客户端 (`tcp_client.py`)</span>
```python
import socket

# 1. 创建 TCP Socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. 连接服务器
client.connect(('127.0.0.1', 8080))
print("已连接到服务器！可以开始发送消息了 (输入 'quit' 退出)。")

# 3. 循环发送和接收消息
while True:
    msg = input(">> ").strip()
    if not msg:
        continue
    if msg == 'quit':
        break
    
    # 发送消息，必须编码为 bytes
    client.send(msg.encode('utf-8'))
    
    # 接收服务器返回的消息
    data = client.recv(1024)
    print(f"服务器响应: {data.decode('utf-8')}")

# 4. 关闭连接
client.close()
```

### <span style="color:#f1c40f;">示例 2：UDP 回显服务器</span>
这个例子展示了 UDP 的无连接特性，服务器只是一个消息中转站。

#### <span style="color:#ffda79;">UDP 服务器 (`udp_server.py`)</span>
```python
import socket

# 1. 创建 UDP Socket
# 注意 type 是 SOCK_DGRAM
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 2. 绑定 IP 和端口
server.bind(('0.0.0.0', 8888))
print("UDP 服务器已启动，等待消息...")

# 3. 循环接收和发送数据 (UDP不需要 listen 和 accept)
while True:
    # 接收数据，同时获取客户端的地址
    data, client_addr = server.recvfrom(1024)
    print(f"收到来自 {client_addr} 的消息: {data.decode('utf-8')}")
    
    # 将收到的数据转为大写，然后发送回原地址
    server.sendto(data.upper(), client_addr)
```

#### <span style="color:#ffda79;">UDP 客户端 (`udp_client.py`)</span>
```python
import socket

# 1. 创建 UDP Socket
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 2. 定义服务器地址
server_addr = ('127.0.0.1', 8888)

# 3. 循环发送数据 (UDP 不需要 connect)
while True:
    msg = input(">> ").strip()
    if msg == 'quit':
        break
    
    # 直接向服务器地址发送数据
    client.sendto(msg.encode('utf-8'), server_addr)
    
    # 接收回显数据
    data, addr = client.recvfrom(1024)
    print(f"服务器回显: {data.decode('utf-8')}")

client.close()
```

### <span style="color:#2ecc71;">示例 3：TCP 文件传输</span>
这是一个更实用的例子，展示了如何用 Socket 传输二进制文件。

#### <span style="color:#55efc4;">文件发送端 (`file_sender.py`)</span>
```python
import socket
import os

# --- 配置 ---
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 9001
BUFFER_SIZE = 4096 # 每次发送的块大小
FILENAME = "my_document.pdf" # 待发送的文件
# ----------------

# 1. 创建文件（用于测试）
with open(FILENAME, "w") as f:
    f.write("This is a test file for socket transmission.\n" * 1000)

# 2. 创建 TCP Socket 并连接服务器
s = socket.socket()
print(f"[+] 正在连接到 {SERVER_HOST}:{SERVER_PORT}")
s.connect((SERVER_HOST, SERVER_PORT))
print("[+] 连接成功。")

# 3. 发送文件名和文件大小（用特殊分隔符隔开）
filesize = os.path.getsize(FILENAME)
s.send(f"{FILENAME}<SEPARATOR>{filesize}".encode())

# 4. 以二进制读取模式打开文件，并循环发送
print(f"[+] 正在发送文件: {FILENAME}")
with open(FILENAME, "rb") as f:
    while True:
        # 读取文件块
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            # 文件传输完毕
            break
        # 发送读取到的文件块
        s.sendall(bytes_read)
print("[+] 文件发送完毕。")

# 5. 关闭连接
s.close()
# 清理测试文件
os.remove(FILENAME)
```
#### <span style="color:#55efc4;">文件接收端 (`file_receiver.py`)</span>
```python
import socket
import os

# --- 配置 ---
SERVER_HOST = '0.0.0.0' # 监听所有接口
SERVER_PORT = 9001
BUFFER_SIZE = 4096
# ----------------

# 1. 创建并绑定监听 Socket
s = socket.socket()
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(5)
print(f"[*] 正在监听 {SERVER_HOST}:{SERVER_PORT}")

# 2. 接受连接
client_socket, address = s.accept() 
print(f"[+] {address} 已连接。")

# 3. 接收文件名和大小
received = client_socket.recv(BUFFER_SIZE).decode()
filename, filesize = received.split("<SEPARATOR>")
filename = os.path.basename(filename) # 移除路径，只保留文件名
filesize = int(filesize)

# 4. 以二进制写入模式打开文件，并循环接收数据
print(f"[+] 正在接收文件: {filename}")
with open(f"received_{filename}", "wb") as f:
    bytes_received = 0
    while bytes_received < filesize:
        # 从客户端接收数据块
        bytes_read = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:
            break
        # 将数据块写入文件
        f.write(bytes_read)
        bytes_received += len(bytes_read)
print("[+] 文件接收完毕。")

# 5. 关闭连接
client_socket.close()
s.close()
```