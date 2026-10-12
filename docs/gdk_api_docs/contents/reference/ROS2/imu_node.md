# Imu Node
Imu数据获取

## Topic

| 话题名称 | 含义 |
|----------|------|
| /imu/livox_front | 前侧雷达imu |
| /imu/livox_back | 背部雷达imu |
| /imu_chassis | 底盘imu |

## 消息类型

### sensor_msgs::msg::Imu

| Field | Type | Description |
|-------|------|-------------|
| header | std_msgs/Header | 消息头，包含时间戳和坐标系信息 |
| angular_velocity | geometry_msgs/Vector3 | 三维角速度（rad/s） |
| linear_acceleration | geometry_msgs/Vector3 | 三维线性加速度（m/s²） |

## 启动ROS2转发节点

### 1. 使用默认配置启动
```bash
source ~/.cache/agibot/app/gdk/scripts/ros_env.sh gdk_imu
ros2 launch gdk_imu imu.launch.py
```
这将启动所有默认的IMU topics：
- `/imu/livox_front`
- `/imu/livox_back`
- `/imu/chassis`

### 2. 自定义IMU topics
```bash
source ~/.cache/agibot/app/gdk/scripts/ros_env.sh gdk_imu

# 只启动特定的IMU topics
#ros2 launch gdk_imu imu.launch.py imu_topics:="/imu/livox_back,/imu/livox_front"

# 启动单个IMU topic
#ros2 launch gdk_imu imu.launch.py imu_topics:="/imu/chassis"
```

