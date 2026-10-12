---
title: Web相机查看器 (camera_web_viewer.py)
order: 2
---

# Web相机查看器 (camera_web_viewer.py)

`camera_web_viewer.py` 是一个基于 Web 的相机图像查看工具，可以在浏览器中实时查看机器人所有相机的图像画面，支持多相机同时显示。

## 功能特性

- Web 界面，无需安装客户端
- 支持多相机同时显示（最多9个相机）
- 自动检测可用相机
- 实时图像刷新（10fps）
- 智能缓存机制，减少重复处理
- 支持多种图像格式（JPEG、PNG、未压缩RGB/BGR/灰度、深度图）
- 深度相机伪彩色显示
- 显示相机信息（尺寸、帧率）

## 安装要求

### 必需依赖

- Python 3.10+
- GDK Python 包 (`agibot_gdk`)
- Flask（用于 Web 服务器）

### 可选依赖

- OpenCV（推荐，用于图像处理和优化）
- NumPy（推荐，用于图像数据处理）

### 安装依赖

```bash
# 安装 Flask
pip install flask

# 安装 OpenCV（推荐）
pip install opencv-python

# 安装 NumPy（通常随 OpenCV 一起安装）
pip install numpy
```

## 使用方法

### 1. 运行工具

```bash
cd ~/.cache/agibot/app/gdk/examples/python
source ~/.cache/agibot/app/env.sh
python3 camera_web_viewer.py
```

### 2. 访问 Web 界面

工具启动后，会在终端显示访问地址：

```
访问地址: http://0.0.0.0:5000
```

在浏览器中打开该地址即可查看相机画面。

### 3. 支持的相机类型

工具支持以下9种相机类型：

1. **头部后视鱼眼相机** (`kHeadBackFisheye`)
2. **头部左侧鱼眼相机** (`kHeadLeftFisheye`)
3. **头部右侧鱼眼相机** (`kHeadRightFisheye`)
4. **头部双目左相机** (`kHeadStereoLeft`)
5. **头部双目右相机** (`kHeadStereoRight`)
6. **左手彩色相机** (`kHandLeftColor`)
7. **右手彩色相机** (`kHandRightColor`)
8. **头部深度相机** (`kHeadDepth`)
9. **头部彩色相机** (`kHeadColor`)

### 4. 功能说明

#### 自动检测可用相机

工具会自动检测哪些相机可用，只显示可用的相机画面。如果某个相机不可用，不会在界面上显示。

#### 实时图像刷新

- 所有可用相机的图像每 100ms 自动刷新一次（10fps）
- 使用智能缓存机制，避免重复处理相同帧
- 显示处理统计信息（新帧数、缓存数、错误数）

#### 相机信息显示

每个相机卡片显示：
- 相机名称
- 图像尺寸（宽 x 高）
- 实时帧率（FPS）

#### 深度相机特殊处理

深度相机会自动进行以下处理：
- 深度值归一化到 0-255 范围
- 应用伪彩色映射（JET 色彩方案）
- 显示深度范围信息（最小/最大深度值）

## 配置选项

### 修改服务器地址和端口

在代码中修改 `WebCameraViewer` 的初始化参数：

```python
viewer = WebCameraViewer(host='0.0.0.0', port=5000)
```

- `host`: 服务器监听地址（默认：`0.0.0.0`，允许外部访问）
- `port`: 服务器端口（默认：`5000`）

### 修改图像质量

在 `image_to_base64()` 方法中修改 `quality` 参数：

```python
image_b64 = self.image_to_base64(decoded_image, quality=75)
```

- 范围：1-100
- 默认：75
- 值越大，图像质量越高，但文件也越大

### 修改刷新频率

在 HTML 模板中修改 `setInterval` 的时间间隔：

```javascript
// 每100ms更新一次（10fps）
setInterval(updateAllImages, 100);
```

## 使用示例

### 示例1：本地访问

```bash
# 运行工具
python3 camera_web_viewer.py

# 在浏览器中打开
# http://localhost:5000
```

### 示例2：远程访问

```bash
# 运行工具（监听所有网络接口）
python3 camera_web_viewer.py

# 在其他设备上访问
# http://<机器人IP>:5000
```

### 示例3：自定义端口

修改代码中的端口号：

```python
viewer = WebCameraViewer(host='0.0.0.0', port=8080)
```

然后访问：`http://localhost:8080`
