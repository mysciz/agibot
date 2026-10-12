---
title: C++
order: 2
---

## 安装GDK

将开发机与G02机器人通过网线直连，配置开发机的静态IP为10.42.1.102。确保ping 10.42.1.101通信正常。

在开发机环境安装GDK依赖：

```
curl -sSL http://10.42.1.101:8849/install.sh | bash
```

## 通过CMakeLists编译

安装cmake
```
sudo apt install cmake
```

编译
```
cd ~/.cache/agibot/app/gdk/examples/cpp
cmake -B build
make -C build
```

## 运行机器人运控示例
```
source ~/.cache/agibot/app/env.sh
./build/mc_example joint_name1 pos1 joint_name2 pos2 ...
```
joint_name为机器人关节名称，pos为关节目标位置，单位为弧度。

joint_name列表如下：


```
"idx01_body_joint1", #腰部五自由度（从底部往上）
"idx02_body_joint2",
"idx03_body_joint3",
"idx04_body_joint4",
"idx05_body_joint5",
"idx11_head_joint1", #头部三自由度（r,p,y）
"idx13_head_joint3",
"idx12_head_joint2",
"idx21_arm_l_joint1", #左手臂七自由度（从肩部往下）
"idx22_arm_l_joint2",
"idx23_arm_l_joint3",
"idx24_arm_l_joint4",
"idx25_arm_l_joint5",
"idx26_arm_l_joint6",
"idx27_arm_l_joint7",
"idx61_arm_r_joint1", #右手臂七自由度（从肩部往下）
"idx62_arm_r_joint2",
"idx63_arm_r_joint3",
"idx64_arm_r_joint4",
"idx65_arm_r_joint5",
"idx66_arm_r_joint6",
"idx67_arm_r_joint7",
```
