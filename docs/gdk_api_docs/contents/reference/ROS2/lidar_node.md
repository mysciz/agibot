# Lidar Node
雷达数据获取

## Topic

| 话题名称 | 含义 |
|----------|------|
| /lidar/livox_front | 前侧激光雷达 |
| /lidar/livox_back | 背部激光雷达 |

## 消息类型

### sensor_msgs::msg::PointCloud2

| Field | Type | Description |
|-------|------|-------------|
| header | std_msgs/Header | 消息头，包含时间戳和坐标系信息 |
| height | uint32 | 点云的高度（如果点云是有组织的，否则为1） |
| width | uint32 | 点云的宽度（点的数量） |
| fields | PointField[] | 描述点云中每个点的字段结构 |
| is_bigendian | bool | 数据字节序（true表示大端序） |
| point_step | uint32 | 单个点占用的字节数 |
| row_step | uint32 | 一行数据占用的字节数 |
| data | uint8[] | 点云的原始二进制数据 |
| is_dense | bool | 如果为true，表示所有点都包含有效数据 |

#### PointField

| Field | Type | Description |
|-------|------|-------------|
| name | string | 字段名称（如："x", "y", "z", "rgb"等） |
| offset | uint32 | 字段在点数据中的字节偏移量 |
| datatype | uint8 | 数据类型(1表示INT8,2表示UINT8,3表示INT16,4表示UINT16,5表示INT32,6表示UINT32,7表示FLOAT32，8表示FLOAT64) |
| count | uint32 | 该字段的元素数量 |

## 启动ROS2转发节点

### 1. 使用默认配置启动
```bash
source ~/.cache/agibot/app/gdk/scripts/ros_env.sh gdk_lidar
ros2 launch gdk_lidar lidar.launch.py
```
这将启动所有默认的Lidar topics：
- `/lidar/livox_front`
- `/lidar/livox_back`

### 2. 自定义Lidar topics
```bash
source ~/.cache/agibot/app/gdk/scripts/ros_env.sh gdk_lidar

# 只启动特定的Lidar topics
#ros2 launch gdk_lidar lidar.launch.py lidar_topics:="/lidar/livox_back,/lidar/livox_front"

# 启动单个Lidar topic
#ros2 launch gdk_lidar lidar.launch.py lidar_topics:="/lidar/livox_back"
```
