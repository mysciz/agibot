# Camera Compress Node
相机压缩图像转发节点

## Topic

| Topic | 描述 |
|-------|------|
| /camera/head_back_fisheye | 头部背部鱼眼相机压缩图像 |
| /camera/head_left_fisheye | 头部左侧鱼眼相机压缩图像 |
| /camera/head_right_fisheye | 头部右侧鱼眼相机压缩图像 |
| /camera/head_stereo_left | 头部左眼相机压缩图像 |
| /camera/head_stereo_right | 头部右眼相机压缩图像 |
| /camera/hand_left_color | 腕部左侧彩色相机压缩图像 |
| /camera/hand_right_color | 腕部右侧彩色相机压缩图像 |
| /camera/head_color | 头部RGB相机压缩图像 |
| /camera/head_depth | 头部深度相机压缩图像 |
| /camera/hand_left_depth | 腕部左侧深度相机压缩图像 |
| /camera/hand_right_depth | 腕部右侧深度相机压缩图像 |

## 消息类型

### sensor_msgs::msg::CompressedImage

| Field | Type | Description |
|-------|------|-------------|
| header | std_msgs/Header | 消息头，包含时间戳和坐标系信息 |
| format | string | 压缩格式字符串（如 "jpeg", "png"） |
| data | uint8[] | 压缩后的图像数据 |

#### 压缩格式

| Format | Description |
|--------|-------------|
| jpeg | JPEG 压缩格式（默认） |
| png | PNG 压缩格式 |

**注意**: 当前实现中，所有压缩图像均使用 JPEG 格式（`format = "jpeg"`）。

## 启动方式

### 1. 使用默认配置启动
```bash
source ~/.cache/agibot/app/gdk/scripts/ros_env.sh gdk_camera_compress
ros2 launch gdk_camera_compress camera_compress.launch.py
```
这将启动所有默认的Camera压缩图像 topics：
- `/camera/head_back_fisheye`
- `/camera/head_left_fisheye`
- `/camera/head_right_fisheye`
- `/camera/head_stereo_left`
- `/camera/head_stereo_right`
- `/camera/hand_left_color`
- `/camera/hand_right_color`
- `/camera/head_color`
- `/camera/head_depth`
- `/camera/hand_left_depth`
- `/camera/hand_right_depth`

### 2. 自定义Camera topics
```bash
source ~/.cache/agibot/app/gdk/scripts/ros_env.sh gdk_camera_compress

# 只启动特定的Camera topics
#ros2 launch gdk_camera_compress camera_compress.launch.py camera_topics:="/camera/head_color,/camera/head_depth"

# 启动单个Camera topic
#ros2 launch gdk_camera_compress camera_compress.launch.py camera_topics:="/camera/head_color"

# 启动鱼眼相机
#ros2 launch gdk_camera_compress camera_compress.launch.py camera_topics:="/camera/head_back_fisheye,/camera/head_left_fisheye,/camera/head_right_fisheye"

# 启动手部相机
#ros2 launch gdk_camera_compress camera_compress.launch.py camera_topics:="/camera/hand_left_color,/camera/hand_right_color"

# 启动手部深度相机
#ros2 launch gdk_camera_compress camera_compress.launch.py camera_topics:="/camera/hand_left_depth,/camera/hand_right_depth"
```

## 与 Camera Node 的区别

| 特性 | Camera Node | Camera Compress Node |
|------|-------------|---------------------|
| 消息类型 | `sensor_msgs::msg::Image` | `sensor_msgs::msg::CompressedImage` |
| 数据格式 | 未压缩的原始像素数据 | JPEG 压缩数据 |
| 带宽占用 | 较高 | 较低 |
| 适用场景 | 需要原始图像数据 | 需要减少带宽占用 |

**建议**:
- 需要原始图像数据进行分析或处理时，使用 `camera_node`
- 需要通过网络传输或减少带宽占用时，使用 `camera_compress_node`
