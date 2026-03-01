# 本地运行 AI 模型 (LFM2-350M) 最终操作指南

---

### **阶段〇：一次性环境准备 (在 Windows 上)**
这些步骤在新电脑上只需执行一次。

1.  **安装 WSL (Windows Subsystem for Linux)**
    * 以 **管理员身份** 打开 **Windows PowerShell**。
    * 运行命令：`wsl --install`
    * 根据提示**重启电脑**。重启后，系统会自动安装 Ubuntu，并要求您设置一个 **Linux 用户名和密码**。

2.  **安装 Docker Desktop**
    * 在 Windows 浏览器中访问官网：`https://www.docker.com/products/docker-desktop/`
    * 下载并安装 **Windows 版本** (`Download for Windows - AMD64`)。
    * 安装完成后，启动 Docker Desktop。

3.  **配置 Docker 与 WSL 的集成**
    * 右键点击任务栏的 Docker 图标 🐳，选择 **"Settings" (设置)**。
    * 进入 **"Resources" -> "WSL Integration"**。
    * 确保 "Ubuntu" 旁边的**开关是开启状态**。
    * 点击 **"Apply & Restart"** 保存设置。

---

### **阶段一：项目设置与模型下载**

1.  **创建项目文件夹**
    * 从 Windows 开始菜单打开 **Ubuntu** 终端。
    * 在 Ubuntu 终端中，运行以下命令：
        ```bash
        mkdir LFM2-Project
        cd LFM2-Project
        ```

2.  **手动下载模型文件 (最稳妥的方法)**
    * 在 **Windows 浏览器**中访问模型页面：`https://huggingface.co/LiquidAI/LFM2-350M`
    * 点击 **"Files and versions"** 标签页。
    * 点击页面右上角紫色的 **"Use this model"** 按钮旁边的**下拉小箭头 `▾`**，在菜单中选择 **"Download repository"**，将模型下载为一个 ZIP 压缩包。
    * 在 Windows 中解压这个 ZIP 文件，得到一个名为 `LFM2-350M` 的文件夹。

3.  **将模型文件放入 WSL**
    * 在 **Ubuntu 终端**中，为模型文件创建一个位置：
        ```bash
        # 确保你还在 LFM2-Project 文件夹内
        mkdir LFM2-350M
        ```
    * 打开 **Windows 文件资源管理器**，在地址栏输入 `\\wsl$` 并回车。
    * 依次进入 `Ubuntu` -> `home` -> `[你的Linux用户名]` -> `LFM2-Project` -> `LFM2-350M`。
    * 将您在 Windows 中解压好的文件夹里的**所有文件**，**复制并粘贴**到这个位置。

---

### **阶段二：构建 Docker 运行环境**
**注意**：从这一步开始，我们主要在 **Windows PowerShell** 中操作。

1.  **创建 Dockerfile**
    * 打开 **Windows PowerShell**，并进入项目目录：
        ```powershell
        cd \\wsl$\Ubuntu\home\[你的Linux用户名]\LFM2-Project
        ```
    * 运行以下命令，创建并编辑 `Dockerfile`：
        ```powershell
        wsl nano Dockerfile
        ```
    * 在打开的编辑器中，粘贴以下**最终版**内容：
        ```dockerfile
        # 使用一个官方的 Python 3.10 镜像作为基础
        FROM python:3.10-slim

        # 设置工作目录
        WORKDIR /app

        # 安装 PyTorch, Transformers, 和 Accelerate 库
        RUN pip install torch transformers accelerate

        # 将我们准备好的模型文件夹复制到容器中
        COPY ./LFM2-350M /app/LFM2-350M

        # 设置默认命令，让容器保持运行
        CMD ["tail", "-f", "/dev/null"]
        ```
    * 按 `Ctrl + O` 保存，按 `Enter` 确认，按 `Ctrl + X` 退出。

2.  **构建 Docker 镜像**
    * 在 PowerShell 中，运行构建命令（注意最后的 `.`）：
        ```powershell
        docker build -t lfm2-runner .
        ```
    * 这个过程第一次会比较耗时，请耐心等待。

---

### **阶段三：运行模型**

1.  **创建 Python 脚本**
    * 仍在 PowerShell 的项目目录中，创建并编辑脚本文件：
        ```powershell
        wsl nano run_model.py
        ```
    * 在打开的编辑器中，粘贴以下**最终版** Python 代码：
        ```python
        import torch
        from transformers import AutoTokenizer, AutoModelForCausalLM

        # 这是模型在容器内部的路径
        model_path = "/app/LFM2-350M"
        print("--- 正在从容器内加载模型 ---")

        # 加载分词器和模型
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            dtype=torch.float32, # 使用 dtype 替代已弃用的 torch_dtype
            device_map="auto"
        )
        print("--- 模型加载成功！ ---")

        # 在这里修改你想问的问题！
        prompt = "In a world where AI is king, "
        inputs = tokenizer(prompt, return_tensors="pt").to("cpu")

        print(f"\n输入提示: {prompt}")
        print("--- 正在生成文本... ---")

        # 生成文本
        outputs = model.generate(**inputs, max_new_tokens=50, pad_token_id=tokenizer.eos_token_id)
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        print("\n--- 模型生成结果 ---")
        print(generated_text)
        print("--------------------")
        ```
    * 按 `Ctrl + O` 保存，`Enter` 确认，`Ctrl + X` 退出。

2.  **启动、复制、进入并运行**
    * 在 PowerShell 中，依次执行以下命令：
        ```powershell
        # 1. 启动容器 (在后台运行)
        docker run -it -d --name my-lfm2-container lfm2-runner

        # 2. 将脚本复制到容器中
        docker cp run_model.py my-lfm2-container:/app/

        # 3. 进入容器的命令行
        docker exec -it my-lfm2-container /bin/bash
        ```
    * 进入容器后（提示符会变为 `root@...#`），运行脚本：
        ```bash
        python run_model.py
        ```
    * 至此，您应该能看到模型的输出了。

---

### **阶段四：日常使用与管理**

* **修改问题**：只需在 PowerShell 中用 `wsl nano run_model.py` 修改 `prompt` 内容，保存后，重新执行**阶段三**的第 `2` 步（`docker cp` 和 `docker exec`）即可。
* **管理容器** (在 PowerShell 中运行)：
    * 停止容器： `docker stop my-lfm2-container`
    * 再次启动： `docker start my-lfm2-container`
    * 彻底删除： `docker rm my-lfm2-container`