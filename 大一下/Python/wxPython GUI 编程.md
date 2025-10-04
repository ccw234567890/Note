# 🎨 wxPython GUI 编程与多线程实战

> [!TIP] 核心挑战与解决方案
> - **挑战 😱**: GUI 应用都运行在一个主循环 (MainLoop) 中。如果在 GUI 线程里执行耗时操作（如等待网络消息 `socket.recv()`），整个界面会**卡死**，无法响应用户操作。
> - **解决方案 💡**: 使用**多线程**！
>   - **主线程 (UI 线程)**: 只负责绘制界面和响应用户的快速操作（如点击按钮）。
>   - **工作线程 (Worker Thread)**: 专门负责执行耗时的网络监听、数据处理等任务。
>   - **线程间通信**: 工作线程处理完数据后，通过一种**安全**的方式通知主线程更新界面。

---

## <span style="color:#3498db;">① 了解第三方库 wxPython</span>

> [!NOTE] 定义
> `wxPython` 是 Python 的一个**跨平台** GUI 工具库。它是对 C++ 编写的著名界面库 `wxWidgets` 的封装。简单说，用 `wxPython` 写的程序，在 Windows, macOS, Linux 上都能运行，并且外观符合对应系统的原生风格。

### <span style="color:#5dade2;">wxPython 核心概念 (盖房子比喻 🏠)</span>
- **`wx.App`**: 整个**建筑项目**。任何 wxPython 程序都必须有且仅有一个 `App` 对象。
- **`wx.Frame`**: 房子的**主框架**，也就是我们的主窗口。
- **`wx.Panel`**: 房子里的**墙壁或房间**。通常我们在 `Panel` 上放置其他控件。
- **控件 (Widgets)**: 房间里的**家具**，如 `wx.Button` (按钮), `wx.TextCtrl` (文本框), `wx.StaticText` (标签)。
- **布局管理器 (Sizers)**: **室内设计师**，如 `wx.BoxSizer`，负责自动排列和调整家具（控件）的位置和大小，让界面更美观且自适应。

### <span style="color:#a5b1c2;">实战代码 1：一个最简单的 "Hello World" 窗口</span>
```python
import wx

# 1. 创建一个应用程序对象
app = wx.App()

# 2. 创建一个顶级窗口 (房子的框架)
# parent=None 表示没有父窗口, title 是窗口标题
frame = wx.Frame(None, title="Hello wxPython", size=(300, 200))

# 3. 创建一个面板 (墙壁)
panel = wx.Panel(frame)

# 4. 在面板上创建一个静态文本控件 (家具)
# label 是显示的文字, pos 是位置坐标
label = wx.StaticText(panel, label="Hello, World!", pos=(100, 50))

# 5. 显示窗口
frame.Show()

# 6. 启动应用程序的事件主循环
# 程序会在这里一直运行，直到窗口被关闭
app.MainLoop()
```
---

## <span style="color:#3498db;">② 使用 wxPython 实现聊天室界面</span>
在动手写网络逻辑前，我们先用**布局管理器 (Sizer)** 搭建出聊天室的静态界面。Sizer 能让界面在窗口缩放时自动调整，比手动设置坐标 `pos` 优雅得多。

### <span style="color:#a5b1c2;">实战代码 2：搭建聊天室 UI 布局</span>
```python
import wx

class ChatFrame(wx.Frame):
    def __init__(self):
        # 初始化父类 wx.Frame
        super().__init__(None, title="聊天室界面", size=(400, 500))

        # --- 界面元素创建 ---
        panel = wx.Panel(self)
        
        # 聊天记录显示框 (多行、只读)
        self.history_text = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        # 消息输入框
        self.message_text = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER)
        # 发送按钮
        self.send_button = wx.Button(panel, label="发送")

        # --- 布局管理器设置 ---
        # 创建一个垂直方向的 BoxSizer
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # 将聊天记录框添加到 sizer
        # proportion=1 表示它在垂直方向上可伸展
        # flag=wx.EXPAND|wx.ALL 表示填充可用空间，并有5像素边距
        main_sizer.Add(self.history_text, 1, wx.EXPAND | wx.ALL, 5)

        # 创建一个水平方向的 sizer 用于放置输入框和按钮
        bottom_sizer = wx.BoxSizer(wx.HORIZONTAL)
        bottom_sizer.Add(self.message_text, 1, wx.EXPAND | wx.ALL, 5) # 输入框可伸展
        bottom_sizer.Add(self.send_button, 0, wx.ALIGN_CENTER | wx.ALL, 5) # 按钮固定大小

        # 将底部的 sizer 添加到主 sizer
        main_sizer.Add(bottom_sizer, 0, wx.EXPAND)
        
        # 设置面板使用主 sizer 进行布局
        panel.SetSizer(main_sizer)

if __name__ == '__main__':
    app = wx.App()
    frame = ChatFrame()
    frame.Show()
    app.MainLoop()
```
---
## <span style="color:#3498db;">③ 掌握网络编程与多线程的综合应用</span>

这是本章的精髓！我们将把**网络通信**和**多线程**集成到上面的聊天室界面中。

### <span style="color:#2ecc71;">最终实战代码 3：完整的多线程 GUI 聊天客户端</span>
为了能运行客户端，我们先提供一个极简的聊天服务器。

#### <span style="color:#a5b1c2;">配套的极简聊天服务器 (`chat_server.py`)</span>
```python
# 先运行这个服务器
import socket
import threading

clients = []

def handle_client(conn, addr):
    print(f"新连接: {addr}")
    clients.append(conn)
    while True:
        try:
            message = conn.recv(1024)
            if not message: break
            broadcast(message, conn)
        except:
            break
    clients.remove(conn)
    conn.close()
    print(f"断开连接: {addr}")

def broadcast(message, sender_conn):
    for client in clients:
        if client != sender_conn:
            try:
                client.send(message)
            except:
                clients.remove(client)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 9999))
server.listen()
print("服务器已启动在 9999 端口...")

while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
```

#### <span style="color:#a5b1c2;">多线程聊天客户端 (`gui_chat_client.py`)</span>
```python
import wx
import socket
import threading

class ChatFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="多线程聊天客户端", size=(400, 500))

        # --- UI 布局 (同上) ---
        panel = wx.Panel(self)
        self.history_text = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.message_text = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER)
        self.send_button = wx.Button(panel, label="发送")
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(self.history_text, 1, wx.EXPAND | wx.ALL, 5)
        bottom_sizer = wx.BoxSizer(wx.HORIZONTAL)
        bottom_sizer.Add(self.message_text, 1, wx.EXPAND | wx.ALL, 5)
        bottom_sizer.Add(self.send_button, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        main_sizer.Add(bottom_sizer, 0, wx.EXPAND)
        panel.SetSizer(main_sizer)

        # --- 绑定事件 ---
        self.send_button.Bind(wx.EVT_BUTTON, self.on_send)
        self.message_text.Bind(wx.EVT_TEXT_ENTER, self.on_send)

        # --- 网络与线程初始化 ---
        self.init_network()
        
    def init_network(self):
        # 1. 创建 socket 并连接服务器
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect(('127.0.0.1', 9999))
            # 2. 连接成功后，启动一个专门接收消息的“工作线程”
            self.receive_thread = threading.Thread(target=self.receive_messages)
            self.receive_thread.daemon = True # 设置为守护线程，主程序退出时它也退出
            self.receive_thread.start()
            self.history_text.AppendText("成功连接到聊天服务器！\n")
        except ConnectionRefusedError:
            self.history_text.AppendText("无法连接到服务器，请先启动服务器。\n")

    # [核心] 工作线程执行的函数：负责接收网络消息
    def receive_messages(self):
        while True:
            try:
                # 3. 在此阻塞等待接收消息，不会卡住 UI
                message = self.sock.recv(1024).decode('utf-8')
                if message:
                    # 4. [关键] 不能直接更新UI!
                    # 使用 wx.CallAfter 将UI更新任务“邮寄”给主线程去执行
                    wx.CallAfter(self.history_text.AppendText, f"对方: {message}\n")
            except:
                wx.CallAfter(self.history_text.AppendText, "与服务器的连接已断开。\n")
                break
    
    # 主线程执行的函数：当点击“发送”按钮时触发
    def on_send(self, event):
        message = self.message_text.GetValue()
        if message:
            try:
                # 5. 发送消息是瞬间完成的，可以在主线程执行
                self.sock.send(message.encode('utf-8'))
                self.history_text.AppendText(f"我: {message}\n")
                self.message_text.Clear() # 清空输入框
            except:
                self.history_text.AppendText("发送失败，连接已断开。\n")

    def OnClose(self, event):
        self.sock.close()
        self.Destroy()

if __name__ == '__main__':
    app = wx.App()
    frame = ChatFrame()
    # 绑定窗口关闭事件
    frame.Bind(wx.EVT_CLOSE, frame.OnClose)
    frame.Show()
    app.MainLoop()
```