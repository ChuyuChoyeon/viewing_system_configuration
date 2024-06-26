﻿# Windows 系统配置查看器

这是一个用 Python 和 Tkinter 编写的简单的系统信息查看工具,可以查看你的电脑硬件和软件配置信息。

## 功能

- 查看 CPU、内存、GPU、硬盘、声卡、网络适配器等硬件信息
- 查看操作系统、显示器等系统信息
- 使用 Sun Valley 主题风格美化界面

## 依赖库

- `tkinter`: Python 自带的GUI库
- `ttkthemes`: 用于提供主题支持
- `sv_ttk`: 用于设置 Sun Valley 主题
- `wmi`: 用于获取 Windows 系统信息
- `psutil`: 用于获取系统资源使用情况
- `GPUtil`: 用于获取 GPU 信息
- `screeninfo`: 用于获取显示器信息

## 使用方法

1. 下载或克隆项目代码
    ```
    git clone https://github.com/ChuyuChoyeon/viewing_system_configuration.git
    ```
   
2. 安装依赖库 运行程序
    ```shell
   # 安装poetry
   pip install poetry
   # 初始化虚拟环境
   poetry install
   # 运行
   poetry run python main.py
    ```
## 界面预览

![系统信息查看器界面](img/index.png)
![系统信息查看器界面](img/about.png)

## 版本信息

- 版本: 1.0
- 作者: Choyeon
- 联系方式: Choyeon@foxmail.com

## 许可证

本项目采用 [MIT 许可证](LICENSE)。

