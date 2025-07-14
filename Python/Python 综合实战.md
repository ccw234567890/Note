# 🚀 Python 综合实战：构建多线程 GUI 聊天室

> [!TIP] 项目架构核心
> 本项目完美融合了三大技术，理解它们的职责是关键：
> - **<span style="color:#9b59b6;">`wxPython` (GUI)</span>**: 负责构建用户能看到和操作的**界面** (窗口, 按钮, 文本框)，它是程序的“脸面”。
> - **<span style="color:#3498db;">`socket` (网络)</span>**: 负责在客户端和服务器之间建立通信**管道**，收发数据，它是程序的“电话线”。
> - **<span style="color:#e67e22;">`threading` (多线程)</span>**: 负责处理**耗时任务** (如等待网络消息)，防止主界面卡死，它是程序的“分身术”。

---

## <span style="color:#9b59b6;">① `wxPython` 界面设计</span>

### <span style="color:#a5b1c2;">服务器端界面 (`server_ui.py`)</span>
服务器界面需要一个日志区、一个在线用户列表和一个启动按钮。

```python
# server_ui.py
import wx

class ServerFrame(wx.Frame):
    def __init__(self, parent, title):
        super(ServerFrame, self).__init__(parent, title=title, size=(550, 400))
        
        # 创建面板和垂直布局管理器
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # 1. 服务器日志显示区
        # wx.TE_MULTILINE: 多行文本, wx.TE_READONLY: 只读
        self.log_text_ctrl = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        vbox.Add(self.log_text_ctrl, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)

        # 2. 在线用户列表
        # wx.LC_REPORT: 报告样式, wx.LC_SINGLE_SEL: 单选
        self.user_list_ctrl = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.user_list_ctrl.InsertColumn(0, '用户名', width=150)
        self.user_list_ctrl.InsertColumn(1, 'IP 地址', width=200)
        self.user_list_ctrl.InsertColumn(2, '端口', width=100)
        vbox.Add(self.user_list_ctrl, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)

        # 3. 启动服务器按钮
        self.start_button = wx.Button(panel, label="启动服务器")
        vbox.Add(self.start_button, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)

        panel.SetSizer(vbox)
        self.Centre()
        self.Show()
```

### <span style="color:#a5b1c2;">客户端界面 (`client_ui.py`)</span>
客户端界面需要一个聊天记录区、一个消息输入框、一个发送按钮和一个连接按钮。

```python
# client_ui.py
import wx

class ClientFrame(wx.Frame):
    def __init__(self, parent, title):
        super(ClientFrame, self).__init__(parent, title=title, size=(500, 450))

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # 顶部水平布局 (用户名、连接按钮)
        hbox_top = wx.BoxSizer(wx.HORIZONTAL)
        self.username_label = wx.StaticText(panel, label="用户名:")
        self.username_ctrl = wx.TextCtrl(panel)
        self.connect_button = wx.Button(panel, label="连接服务器")
        hbox_top.Add(self.username_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        hbox_top.Add(self.username_ctrl, 1, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        hbox_top.Add(self.connect_button, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        vbox.Add(hbox_top, 0, wx.EXPAND)

        # 1. 聊天记录显示区
        self.chat_history_ctrl = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        vbox.Add(self.chat_history_ctrl, 1, wx.EXPAND | wx.ALL, 5)

        # 2. 消息输入区
        self.message_input_ctrl = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER)
        vbox.Add(self.message_input_ctrl, 0, wx.EXPAND | wx.ALL, 5)

        # 3. 发送按钮
        self.send_button = wx.Button(panel, label="发送")
        vbox.Add(self.send_button, 0, wx.EXPAND | wx.ALL, 5)
        
        panel.SetSizer(vbox)
        self.Centre()
        self.Show()

```

---
## <span style="color:#2ecc71;">② 服务器端完整实现 (`server_main.py`)</span>
这是将**界面、网络、多线程**整合在一起的核心代码。

```python
# server_main.py
import wx
import socket
import threading
import time

# 导入上面定义的界面类
from server_ui import ServerFrame

class ChatServer(ServerFrame):
    def __init__(self, parent):
        # 初始化父类（界面）
        super(ChatServer, self).__init__(parent, title="聊天室服务器")

        # --- 设置服务器必要属性 ---
        self.server_socket = None
        self.clients = {}  # 字典，用于存储客户端信息 {conn: (addr, username)}
        self.lock = threading.Lock() # 线程锁，用于保护共享资源 self.clients
        
        # --- 绑定界面事件 ---
        self.start_button.Bind(wx.EVT_BUTTON, self.on_start_server)
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def log(self, message):
        """线程安全地在日志区追加日志"""
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        log_message = f"[{current_time}] {message}\n"
        
        # 使用 wx.CallAfter 确保 GUI 更新在主线程中执行
        wx.CallAfter(self.log_text_ctrl.AppendText, log_message)
        
        # 保存聊天记录到文件
        with open("chat_log.txt", "a", encoding="utf-8") as f:
            f.write(log_message)

    def update_user_list(self):
        """线程安全地更新在线用户列表"""
        def do_update():
            self.user_list_ctrl.DeleteAllItems()
            with self.lock:
                for conn, (addr, username) in self.clients.items():
                    index = self.user_list_ctrl.InsertItem(self.user_list_ctrl.GetItemCount(), username)
                    self.user_list_ctrl.SetItem(index, 1, str(addr[0]))
                    self.user_list_ctrl.SetItem(index, 2, str(addr[1]))
        wx.CallAfter(do_update)

    def on_start_server(self, event):
        """服务器端启动服务的功能实现"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('0.0.0.0', 8888))
        self.server_socket.listen(5)
        
        # 禁用启动按钮，防止重复启动
        self.start_button.Disable()
        self.log("服务器已启动，在 8888 端口监听...")
        
        # 创建并启动一个新线程，专门用于接受客户端连接，防止主界面卡死
        threading.Thread(target=self.accept_clients, daemon=True).start()

    def accept_clients(self):
        """在独立线程中循环接受客户端连接"""
        while True:
            try:
                conn, addr = self.server_socket.accept()
                # 为每个连接成功的客户端再创建一个新的处理线程
                threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True).start()
            except OSError:
                break # 服务器socket关闭时会引发异常

    def handle_client(self, conn, addr):
        """服务器端会话线程代码实现 (每个客户端一个)"""
        try:
            # 第一个消息应为用户名
            username = conn.recv(1024).decode('utf-8')
            if not username:
                return

            # --- 客户端连接成功后的处理 ---
            with self.lock:
                self.clients[conn] = (addr, username)
            
            self.log(f"用户 '{username}' ({addr}) 已连接。")
            self.broadcast_message(f"系统通知: 欢迎 '{username}' 加入聊天室！", exclude_conn=None)
            self.update_user_list()

            # --- 循环接收客户端消息 ---
            while True:
                data = conn.recv(1024)
                if not data: # 客户端断开
                    break
                message = data.decode('utf-8')
                self.log(f"收到来自 '{username}' 的消息: {message}")
                # 广播消息
                self.broadcast_message(f"{username}: {message}", exclude_conn=conn)
        
        finally:
            # --- 客户端断开连接功能实现 ---
            with self.lock:
                if conn in self.clients:
                    username = self.clients[conn][1]
                    del self.clients[conn]
                    self.log(f"用户 '{username}' ({addr}) 已断开连接。")
                    self.broadcast_message(f"系统通知: '{username}' 离开了聊天室。", exclude_conn=None)
                    self.update_user_list()
            conn.close()

    def broadcast_message(self, message, exclude_conn):
        """向所有客户端（或除某个之外的所有客户端）广播消息"""
        with self.lock:
            for conn in list(self.clients.keys()):
                if conn != exclude_conn:
                    try:
                        conn.sendall(message.encode('utf-8'))
                    except:
                        # 发送失败，可能该客户端也已断开
                        pass
    
    def on_close(self, event):
        """关闭窗口时的清理工作"""
        if self.server_socket:
            self.server_socket.close()
        self.Destroy()


if __name__ == '__main__':
    app = wx.App(False)
    server = ChatServer(None)
    app.MainLoop()

```

---

## <span style="color:#e74c3c;">③ 客户端完整实现 (`client_main.py`)</span>
客户端同样需要整合**界面、网络、多线程**。

```python
# client_main.py
import wx
import socket
import threading

# 导入上面定义的界面类
from client_ui import ClientFrame

class ChatClient(ClientFrame):
    def __init__(self, parent):
        super(ChatClient, self).__init__(parent, title="聊天室客户端")
        
        # --- 客户端属性 ---
        self.client_socket = None
        self.is_connected = False
        
        # --- 绑定界面事件 ---
        self.connect_button.Bind(wx.EVT_BUTTON, self.on_connect)
        self.send_button.Bind(wx.EVT_BUTTON, self.on_send)
        # 绑定回车键发送消息
        self.message_input_ctrl.Bind(wx.EVT_TEXT_ENTER, self.on_send)
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def show_message(self, message):
        """线程安全地在聊天记录区显示消息"""
        wx.CallAfter(self.chat_history_ctrl.AppendText, f"{message}\n")

    def on_connect(self, event):
        """客户端连接服务器功能实现"""
        if self.is_connected:
            return
            
        username = self.username_ctrl.GetValue()
        if not username:
            wx.MessageBox("请输入用户名！", "提示", wx.OK | wx.ICON_INFORMATION)
            return

        try:
            # 创建并连接服务器
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect(('127.0.0.1', 8888))
            
            # 发送用户名作为第一条消息
            self.client_socket.sendall(username.encode('utf-8'))
            
            self.is_connected = True
            self.connect_button.Disable()
            self.username_ctrl.Disable()
            self.show_message("成功连接到服务器！")
            
            # 启动一个新线程来持续接收服务器消息
            threading.Thread(target=self.receive_messages, daemon=True).start()

        except Exception as e:
            wx.MessageBox(f"连接失败: {e}", "错误", wx.OK | wx.ICON_ERROR)

    def receive_messages(self):
        """在独立线程中接收服务器消息"""
        while self.is_connected:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                # 服务器端显示聊天信息/客户端显示服务器通知的功能实现
                self.show_message(data.decode('utf-8'))
            except:
                break
        
        self.show_message("与服务器的连接已断开。")
        self.is_connected = False
        wx.CallAfter(self.connect_button.Enable)
        wx.CallAfter(self.username_ctrl.Enable)


    def on_send(self, event):
        """客户端发送信息到聊天室"""
        if not self.is_connected:
            wx.MessageBox("请先连接到服务器！", "提示", wx.OK | wx.ICON_INFORMATION)
            return
            
        message = self.message_input_ctrl.GetValue()
        if message:
            try:
                self.client_socket.sendall(message.encode('utf-8'))
                # 清空输入框
                self.message_input_ctrl.Clear()
            except Exception as e:
                self.show_message(f"发送失败: {e}")

    def on_close(self, event):
        """客户端断开连接"""
        if self.client_socket and self.is_connected:
            self.client_socket.close()
        self.Destroy()


if __name__ == '__main__':
    app = wx.App(False)
    client = ChatClient(None)
    app.MainLoop()

```