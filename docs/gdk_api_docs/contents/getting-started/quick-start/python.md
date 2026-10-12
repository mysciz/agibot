---
title: Python
order: 3
---

## 安装

将开发机与G02机器人通过网线直连，配置开发机的静态IP为10.42.1.102。确保ping 10.42.1.101通信正常。

在开发机环境安装GDK依赖：

```
curl -sSL http://10.42.1.101:8849/install.sh | bash
```

## 运行示例

### 声明python路径

```
source ~/.cache/agibot/app/env.sh
```

### 运行运控示例代码

```
cd ~/.cache/agibot/app/gdk/examples/python
python3 mc_example.py
```

#### 操作说明

| 按键 | 功能 |
|------|------|
| a/d | 切换关节 |
| w/s | 调整关节角度 |
| m | 切换动作序列 |
| p | 播放动作序列 |
| q | 退出程序 |

