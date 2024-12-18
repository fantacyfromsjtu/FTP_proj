# FTP_Proj
## 1.Quick Start

1. 运行平台：经测试，在Window11系统和Ubuntu23.10系统上均可运行
2. 安装依赖

```bash
conda create -n tmp python=3.9
pip install -r requirements.txt
```

3. 服务端运行

   直接启动服务器：

```bash
python server/server_main.py
```

​	查看命令行参数（具体参数细节后面给出）：

```
python server/server_main.py -h
```

4. 客户端运行

```bash
python client/main.py
```

## 2.文件结构
```
FTP_proj
│
├─ .gitignore
├─ client
│  ├─ core
│  │  ├─ file_operations.py
│  │  ├─ ftp_client.py
│  │  └─ __init__.py
│  ├─ main.py
│  ├─ ui
│  │  ├─ file_browser.py
│  │  ├─ login_window.py
│  │  ├─ main_window.py
│  │  ├─ progress_bar.py
│  │  └─ __init__.py
│  └─ __init__.py
├─ LICENSE
├─ README.md
├─ requirements.txt
└─ server
   ├─ config.py
   ├─ core
   │  ├─ file_system.py
   │  ├─ ftp_server.py
   │  ├─ logging.py
   │  ├─ user_management.py
   │  └─ __init__.py
   ├─ server_main.py
   ├─ users.json
   └─ __init__.py

```