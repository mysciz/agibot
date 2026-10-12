---
title: 部署
order: 1
---

## 环境要求

### 硬件需求

- 符合ISO/IEC 11801：2002和EIA/TIA 568B或ISO/IEC 11801:2002和EIA/TIA 568-B.2-1标准的网线
- 开发机（Ubuntu22.04，x86_64，Intel i9及以上性能CPU）

### 网络配置

使用网线连接G2接口面板的Debug网口和开发机网口，然后给开发机的网卡配置静态IP：

```
IP：10.42.1.xxx(10.42.1.10~10.42.1.99)
MASK：255.255.255.0
```

在开发机上验证与G2的通信是否正常：

```
ping 10.42.1.101
```

## 安装GDK

### 混合部署

在开发机执行以下命令安装GDK：

```
curl -sSL http://10.42.1.101:8849/install.sh | bash
```

## 获取示例代码

### 从G2上获取示例代码压缩包

```
curl -sSL http://10.42.1.101:8849/install_example.sh | bash
```

该示例文件夹主要包含运控控制，相机图像，传感器数据读取等示例demo，涉及C++、Python、ROS三种编程语言。

### 文件夹结构

```
├── cpp
│   ├── CMakeLists.txt
│   └── src
├── python
│   ├── camera_demo.py
│   ├── camera_web_viewer.py
│   ├── imu_demo.py
│   ├── lidar_demo.py
│   ├── mc_example.py
│   ├── move_chassis.py
│   ├── pnc_example.py
│   ├── robot_demo.py
│   ├── slam_demo.py
│   ├── uss_demo.py
│   ├── proto
│   └── saved_commands
└── ros
    ├── camera_example
    └── control_example


```
