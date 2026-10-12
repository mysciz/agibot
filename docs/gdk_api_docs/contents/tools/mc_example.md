---
title: 关节控制工具 (mc_example.py)
order: 1
---

# 关节控制工具 (mc_example.py)

`mc_example.py` 是一个交互式的关节位置控制工具，可以通过键盘实时控制机器人关节位置，并支持播放预录制的动作序列。

## 功能特性

-  交互式键盘控制关节位置
-  支持所有22个关节的控制
-  播放预录制的动作序列
-  实时查看关节状态
-  支持多个动作文件切换

## 安装要求

在使用此工具前，请确保：

1. 已安装 GDK Python 包
2. 已配置好机器人连接（混合部署或机内部署）
3. 已准备好动作序列文件（JSON格式）

## 使用方法

### 1. 准备动作序列文件

工具会从 `saved_commands/` 目录读取 JSON 格式的动作序列文件。确保该目录存在并包含动作文件：

```bash
cd ~/.cache/agibot/app/gdk/examples/python
mkdir -p saved_commands
```

动作序列文件格式示例：

```json
{
  "recorded_commands": [
    {
      "joint_names": ["idx21_arm_l_joint1", "idx22_arm_l_joint2"],
      "joint_positions": [0.5, -0.3]
    },
    {
      "joint_names": ["idx21_arm_l_joint1", "idx22_arm_l_joint2"],
      "joint_positions": [0.8, -0.5]
    }
  ]
}
```

### 2. 运行工具

```bash
cd ~/.cache/agibot/app/gdk/examples/python
source ~/.cache/agibot/app/env.sh
python3 mc_example.py
```

### 3. 键盘控制

工具启动后，使用以下键盘按键进行控制：

| 按键 | 功能 |
|------|------|
| `w` / `W` | 当前关节正向移动（+0.1 弧度） |
| `s` / `S` | 当前关节负向移动（-0.1 弧度） |
| `a` / `A` | 切换到上一个关节 |
| `d` / `D` | 切换到下一个关节 |
| `p` / `P` | 播放当前动作序列的下一帧 |
| `m` / `M` | 切换到下一个动作文件 |
| `q` / `Q` | 退出程序 |

### 4. 支持的关节列表

工具支持控制以下22个关节：

**腰部关节（5个）：**
- `idx01_body_joint1` - 腰部关节1
- `idx02_body_joint2` - 腰部关节2
- `idx03_body_joint3` - 腰部关节3
- `idx04_body_joint4` - 腰部关节4
- `idx05_body_joint5` - 腰部关节5

**头部关节（3个）：**
- `idx11_head_joint1` - 头部关节1
- `idx12_head_joint2` - 头部关节2
- `idx13_head_joint3` - 头部关节3

**左手臂关节（7个）：**
- `idx21_arm_l_joint1` - 左手臂关节1
- `idx22_arm_l_joint2` - 左手臂关节2
- `idx23_arm_l_joint3` - 左手臂关节3
- `idx24_arm_l_joint4` - 左手臂关节4
- `idx25_arm_l_joint5` - 左手臂关节5
- `idx26_arm_l_joint6` - 左手臂关节6
- `idx27_arm_l_joint7` - 左手臂关节7

**右手臂关节（7个）：**
- `idx61_arm_r_joint1` - 右手臂关节1
- `idx62_arm_r_joint2` - 右手臂关节2
- `idx63_arm_r_joint3` - 右手臂关节3
- `idx64_arm_r_joint4` - 右手臂关节4
- `idx65_arm_r_joint5` - 右手臂关节5
- `idx66_arm_r_joint6` - 右手臂关节6
- `idx67_arm_r_joint7` - 右手臂关节7

## 配置参数

可以在代码中修改以下参数：

- `_step`: 每次按键移动的步长（默认：0.1 弧度）
- `_speed`: 关节运动速度（默认：0.3）

## 使用示例

### 示例1：控制单个关节

1. 运行程序
2. 使用 `a`/`d` 键选择要控制的关节（例如：`idx21_arm_l_joint1`）
3. 使用 `w`/`s` 键调整关节位置
4. 观察机器人关节运动

### 示例2：播放动作序列

1. 准备动作序列文件并放在 `saved_commands/` 目录
2. 运行程序
3. 使用 `m` 键切换到要播放的动作文件
4. 按 `p` 键逐帧播放动作序列
5. 连续按 `p` 键可以播放完整动作

## 注意事项

 **安全提示：**

- 使用前请确保机器人周围有足够的空间
- 注意关节的运动范围，避免超出限位
- 建议先在小幅度范围内测试
- 紧急情况下按 `q` 键退出程序

 **使用限制：**

- 工具需要从 `saved_commands/` 目录读取 JSON 文件，如果目录为空或文件格式错误，程序会报错
- 动作序列文件必须是有效的 JSON 格式
- 确保机器人已正确连接并初始化
