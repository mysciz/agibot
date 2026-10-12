# Camera Node
相机图像转发节点
## Topic

| Topic | 描述 |
|-------|------|
| /camera/head_back_fisheye | 头部背部鱼眼相机 |
| /camera/head_left_fisheye | 头部左侧鱼眼相机 |
| /camera/head_right_fisheye | 头部右侧鱼眼相机 |
| /camera/head_stereo_left | 头部左眼相机 |
| /camera/head_stereo_right | 头部右眼相机 |
| /camera/hand_left | 腕部深度相机 |
| /camera/hand_right | 腕部深度相机 |
| /camera/head_color | 头部rgb相机 |
| /camera/head_depth | 头部深度相机 |
| /camera/hand_left_depth | 腕部左侧深度相机 |
| /camera/hand_right_depth | 腕部右侧深度相机 |

## 消息类型

### sensor::msgs::msg::Image

| Field | Type | Description |
|-------|------|-------------|
| header | std_msgs/Header | 消息头，包含时间戳和坐标系信息 |
| height | uint32 | 图像高度（像素行数） |
| width | uint32 | 图像宽度（像素列数） |
| encoding | string | 像素数据的编码格式字符串 |
| is_bigendian | bool | 数据字节序（true表示大端序） |
| step | uint32 | 单行数据占用的字节数 |
| data | uint8[] | 图像的原始像素数据 |

#### 单通道图像

| Encoding | Description | Bytes per Pixel |
|----------|-------------|-----------------|
| mono8 | 8位灰度图 | 1 |
| mono16 | 16位灰度图 | 2 |
| bayer_bggr8 | Bayer BGGR 格式 | 1 |
| bayer_rggb8 | Bayer RGGB 格式 | 1 |

#### 多通道图像

| Encoding | Description | Bytes per Pixel |
|----------|-------------|-----------------|
| bgr8 | 8位 BGR 彩色 | 3 |
| rgb8 | 8位 RGB 彩色 | 3 |
| bgra8 | 8位 BGRA 带透明度 | 4 |
| rgba8 | 8位 RGBA 带透明度 | 4 |

## 启动方式


### 1. 使用默认配置启动
```bash
source ~/.cache/agibot/app/gdk/scripts/ros_env.sh gdk_camera_compress
ros2 launch gdk_camera camera.launch.py
```
这将启动所有默认的Camera topics：
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
source ~/.cache/agibot/app/gdk/scripts/ros_env.sh gdk_camera

# 只启动特定的Camera topics
#ros2 launch gdk_camera camera.launch.py camera_topics:="/camera/head_color,/camera/head_depth"

# 启动单个Camera topic
#ros2 launch gdk_camera camera.launch.py camera_topics:="/camera/head_color"

# 启动鱼眼相机
#ros2 launch gdk_camera camera.launch.py camera_topics:="/camera/head_back_fisheye,/camera/head_left_fisheye,/camera/head_right_fisheye"

# 启动手部相机
#ros2 launch gdk_camera camera.launch.py camera_topics:="/camera/hand_left_color,/camera/hand_right_color"

# 启动手部深度相机
#ros2 launch gdk_camera camera.launch.py camera_topics:="/camera/hand_left_depth,/camera/hand_right_depth"
```
