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