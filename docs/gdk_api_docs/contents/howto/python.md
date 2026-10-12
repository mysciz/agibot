---
title: python
order: 3
---
# GDK Python 使用说明
GDK python默认使用3.10版本，如需使用其余版本的python，可指定python版本来编译pybind的源码，从而生成指定版本的GDK python包。

## 概述

GDK 的 Python模块，提供GDK所有功能的Python接口。

## 安装要求（如需使用python3.10以外的版本）

### 系统要求
- Linux (x86_64 或 aarch64)
- Python 3.8+

### 依赖库
- pybind11 >= 2.6.0
- numpy >= 1.19.0
- protobuf >= 5.28.3

#### protobuf安装
```
sudo apt update && sudo apt install -y libprotobuf-dev protobuf-compiler
```
## 安装方法

### 从源码安装


```bash
cd ~/.cache/agibot/app/gdk/build_dep/python/pybind/
pip install . --no-build-isolation
```

### 编译wheel打包
```bash
cd ~/.cache/agibot/app/gdk/build_dep/python/pybind/
python setup.py bdist_wheel --dist-dir dist
```

### 检查安装是否成功

#### 检查是否安装到系统中

```bash
pip list  
```

## 基本使用

### 完整案例

```
import agibot_gdk
import time

agibot_gdk.gdk_init()
robot = agibot_gdk.Robot()
time.sleep(1)

joint_states = robot.get_joint_states()
print(joint_states)

```

### 代码说明

#### 导入agibot_gdk模块

```
import agibot_gdk
```

#### 初始化gdk模块与机器人对象

```
agibot_gdk.gdk_init()
robot = agibot_gdk.Robot()
time.sleep(1)
```

#### 获取机器人关节信息

```
joint_states = robot.get_joint_states()
print(joint_states)
```


#### 声明python路径

```
source ~/.cache/agibot/app/env.sh
```

#### 执行程序

```
python3 <your_py>
```