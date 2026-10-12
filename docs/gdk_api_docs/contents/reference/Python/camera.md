# GDK Camera 接口文档（Python）

## 概述

Camera（相机）模块为G02机器人提供了获取实时图像数据的功能。通过Python接口，开发者可以方便地获取机器人的视觉感知数据，适用于目标检测、图像识别、视觉导航、SLAM建图、环境监控等多种场景。

## 接口说明

### Camera 类

该类封装了相机传感器的主要数据获取接口。

#### 1. `get_latest_image()`

- **功能**：获取最新的图像数据
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `type` | `CameraType` | 相机类型枚举值 |
| `timeout` | `float` | 超时时间（毫秒） |

- **返回值**：`Image`对象，包含以下属性：

| 属性名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `timestamp_ns` | `int` | 图像采集的时间戳 | 纳秒 |
| `width` | `int` | 图像的宽度（像素） | 像素 |
| `height` | `int` | 图像的高度（像素） | 像素 |
| `encoding` | `str` | 图像的编码格式 | 字符串 |
| `color_format` | `str` | 图像的颜色格式 | 字符串 |
| `bit_depth` | `int` | 每个像素的位数 | 位 |
| `data` | `bytes` | 图像的原始像素数据 | 字节 |

##### Image对象详细说明

**encoding (编码格式)**：

- **类型**：`str`
- **常见值**：
  - `"rgb8"`: RGB彩色图像，每通道8位
  - `"bgr8"`: BGR彩色图像，每通道8位
  - `"mono8"`: 灰度图像，8位
  - `"mono16"`: 灰度图像，16位
  - `"32FC1"`: 单通道32位浮点（深度图）

**color_format (颜色格式)**：

- **类型**：`str`
- **常见值**：
  - `"RGB"`: 红绿蓝
  - `"BGR"`: 蓝绿红
  - `"GRAY"`: 灰度
  - `"DEPTH"`: 深度

**bit_depth (位深度)**：

- **类型**：`int`
- **常见值**：
  - `8`: 8位（0-255）
  - `16`: 16位（0-65535）
  - `32`: 32位（浮点）

**data (图像数据)**：

- **类型**：`bytes`
- **描述**：图像的原始像素数据
- **用途**：图像处理、显示、保存
- **注意**：需要根据encoding和尺寸进行解析

**相机类型**：
- `kHeadBackFisheye`: 头部背部鱼眼相机
- `kHeadLeftFisheye`: 头部左侧鱼眼相机
- `kHeadRightFisheye`: 头部右侧鱼眼相机
- `kHeadStereoLeft`: 头部立体左相机
- `kHeadStereoRight`: 头部立体右相机
- `kHandLeftColor`: 左手彩色相机
- `kHandRightColor`: 右手彩色相机
- `kHeadColor`: 头部彩色相机
- `kHeadDepth`: 头部深度相机（输出为深度图）
- `kHandLeftDepth`: 左手深度相机（输出为深度图）
- `kHandRightDepth`: 右手深度相机（输出为深度图）
- `kHandLeftUpperColor`: 左手上部彩色相机 (预留)
- `kHandRightUpperColor`: 右手上部彩色相机 (预留)
- `kHandLeftLowerColor`: 左手下部彩色相机 (预留)
- `kHandRightLowerColor`: 右手下部彩色相机 (预留)
- `kHandLeftUpperDepth`: 左手上部深度相机（输出为深度图） (预留)
- `kHandRightUpperDepth`: 右手上部深度相机（输出为深度图） (预留)
- `kHandLeftLowerDepth`: 左手下部深度相机（输出为深度图） (预留)
- `kHandRightLowerDepth`: 右手下部深度相机（输出为深度图） (预留)

- 在常规模式下，默认打开头部立体左相机，头部立体右相机，左右彩色相机，右手彩色相机，头部彩色相机，头部深度相机，其余相机默认关闭，且不建议在常规模式下打开其余相机
- 可以在develop模式下开启或关闭其余相机

- **示例**：

  ```python
  import agibot_gdk
  import time

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  camera = agibot_gdk.Camera()
  time.sleep(3)  # 等待相机初始化

  image = camera.get_latest_image(agibot_gdk.CameraType.kHeadStereoLeft, 1000.0)
  if image is not None:
      print(f"✅ 时间戳: {image.timestamp_ns}")
      print(f"图像尺寸: {image.width} x {image.height}")
      print(f"编码格式: {image.encoding}")
      print(f"颜色格式: {image.color_format}")
      print(f"位深度: {image.bit_depth}")
  else:
      print("未获取到图像数据")

  # 关闭相机
  camera.close_camera()

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

#### 2. `get_nearest_image()`

- **功能**：获取指定时间戳附近最近的图像数据
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `type` | `CameraType` | 相机类型枚举值 |
| `timestamp` | `int` | 目标时间戳（纳秒） |
| `timeout` | `float` | 超时时间（毫秒） |

- **返回值**：`Image`对象，结构与`get_latest_image()`相同

- **示例**：

  ```python
  import agibot_gdk
  import time

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  camera = agibot_gdk.Camera()
  time.sleep(3)

  # 先获取最新图像数据
  image = camera.get_latest_image(agibot_gdk.CameraType.kHeadStereoLeft, 1000.0)

  if image is not None:
      # 获取历史图像数据（往前1秒）
      image_nearest = camera.get_nearest_image(
          agibot_gdk.CameraType.kHeadStereoLeft,
          image.timestamp_ns - 1000000000,
          1000.0
      )

      if image_nearest is not None:
          print(f"✅ 最近图像数据: {image_nearest.timestamp_ns}")
          print(f"图像尺寸: {image_nearest.width} x {image_nearest.height}")
          print(f"编码格式: {image_nearest.encoding}")
      else:
          print("❌ 未找到最近的图像数据")
  else:
      print("未获取到最新图像数据")

  # 关闭相机
  camera.close_camera()

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

#### 3. `get_image_shape()`

- **功能**：获取图像数据大小
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `type` | `CameraType` | 相机类型枚举值 |

- **返回值**：`tuple`，包含图像宽度和高度的元组 `(width, height)`

- **示例**：

  ```python
  import agibot_gdk

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  camera = agibot_gdk.Camera()

  shape = camera.get_image_shape(agibot_gdk.CameraType.kHeadStereoLeft)
  print(f"图像尺寸: {shape[0]} x {shape[1]}")

  # 关闭相机
  camera.close_camera()

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

#### 4. `get_image_fps()`

- **功能**：获取图像捕获帧率
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `type` | `CameraType` | 相机类型枚举值 |

- **返回值**：`float`，图像帧率（FPS）

- **示例**：

  ```python
  import agibot_gdk

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  camera = agibot_gdk.Camera()

  fps = camera.get_image_fps(agibot_gdk.CameraType.kHeadStereoLeft)
  print(f"图像帧率: {fps} FPS")

  # 关闭相机
  camera.close_camera()

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

#### 5. `get_image_latency()`

- **注意事项**：获取图像延迟统计信息前，需要先进行时间同步，否则延迟统计结果不准确
- **功能**：获取图像延迟统计信息
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `type` | `CameraType` | 相机类型枚举值 |
| `window_seconds` | `float` | 统计窗口时间（秒） |

- **返回值**：`LatencyStats`对象，包含延迟统计信息

- **示例**：

  ```python
  import agibot_gdk

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  camera = agibot_gdk.Camera()

  latency = camera.get_image_latency(agibot_gdk.CameraType.kHeadStereoLeft, 1.0)
  print(f"最大延迟: {latency.max_latency_ms} ms")
  print(f"平均延迟: {latency.avg_latency_ms} ms")

  # 关闭相机
  camera.close_camera()

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

#### 6. `get_camera_intrinsic()`

- **功能**：获取相机内参信息
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `type` | `CameraType` | 相机类型枚举值 |

- **返回值**：`CameraIntrinsic`对象，包含相机内参信息

- **注意**：并非所有相机类型都支持内参获取。支持内参的相机类型包括：`kHeadBackFisheye`、`kHeadLeftFisheye`、`kHeadRightFisheye`、`kHeadStereoLeft`、`kHeadStereoRight`、`kHandLeftColor`、`kHandRightColor`、`kHeadColor`、`kHeadDepth`、`kHandLeftDepth`、`kHandRightDepth`。对于不支持的相机类型，调用此接口将抛出异常。

#### CameraIntrinsic对象详细说明

**CameraIntrinsic结构体包含以下成员**：

| 成员名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `intrinsic` | `list[float]` | 相机内参 [fx, fy, cx, cy] | 像素 |
| `distortion` | `list[float]` | 畸变参数 [k1, k2, p1, p2, k3, k4, k5, k6] | 无单位 |

**不同相机类型的内参支持**：

| 相机类型 | intrinsic长度 | distortion长度 | 说明 |
| :--- | :--- | :--- | :--- |
| 双目相机 | 4 | 8 | fx,fy,cx,cy,k1,k2,p1,p2,k3,k4,k5,k6 |
| RGBD相机 | 4 | 5 | fx,fy,cx,cy,k1,k2,p1,p2,k3 |
| 鱼眼相机 | 4 | 6 | fx,fy,cx,cy,k1,k2,p1,p2,k3,k4 |

- **示例**：

  ```python
  import agibot_gdk

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  camera = agibot_gdk.Camera()

  intrinsic = camera.get_camera_intrinsic(agibot_gdk.CameraType.kHeadStereoLeft)
  print(f"相机内参:")
  print(f"  fx: {intrinsic.intrinsic[0]}")
  print(f"  fy: {intrinsic.intrinsic[1]}")
  print(f"  cx: {intrinsic.intrinsic[2]}")
  print(f"  cy: {intrinsic.intrinsic[3]}")

  print(f"畸变参数:")
  for i, dist in enumerate(intrinsic.distortion):
      print(f"  k{i+1}: {dist}")

  # 关闭相机
  camera.close_camera()

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

#### 7. `set_dev_camera_config()`

- **功能**：设置相机开发配置
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `cam_conf_path` | `str` | 相机配置文件路径 |

- **返回值**：无。成功时不返回，失败时抛出`std::runtime_error`异常

- **注意**：
  - 配置文件路径必须存在，否则会抛出异常
  - 每次修改客制化相机配置文件且调用接口后，需要重新切换模式至develop模式

##### 配置选项
GDK支持配置相机的开关与设置的帧率，相机客制化的配置文件在部署包下，其绝对路径通常为 `~/.cache/agibot/app/gdk/config/cam_config.json`（其中 `~` 表示用户主目录，如 `/home/your_name`）
设置publish为true开启相机，false关闭相机，设置fps来控制相机帧率
相机具体配置形式如下
```json
{
    "cam0": {
        "fps": "30",
        "name": "head_stereo_right",
        "publish": true
    },
    "cam3": {
        "fps": "30",
        "name": "head_stereo_left",
        "publish": true
    },
    "cam4": {
        "fps": "30",
        "name": "hand_left_depth",
        "publish": false
    },
    "cam5": {
        "fps": "30",
        "name": "hand_left_color",
        "publish": true
    },
    "cam6": {
        "fps": "30",
        "name": "hand_right_depth",
        "publish": false
    },
    "cam7": {
        "fps": "30",
        "name": "hand_right_color",
        "publish": true
    },
    "cam10": {
        "fps": "30",
        "name": "head_right_fisheye",
        "publish": false
    },
    "cam11": {
        "fps": "30",
        "name": "head_left_fisheye",
        "publish": false
    },
    "cam12": {
        "fps": "30",
        "name": "head_back_fisheye",
        "publish": false
    },
    "cam14": {
        "fps": "30",
        "name": "head_depth",
        "publish": true
    },
    "cam15": {
        "fps": "30",
        "name": "head_color",
        "publish": true
    }
}
```

- **示例**：

  ```python
  import agibot_gdk
  import time

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  camera = agibot_gdk.Camera()
  time.sleep(1)  # 等待相机初始化

  # 设置相机配置
  config_path = "/home/<your_name>/.cache/agibot/app/gdk/config/cam_config.json"
  try:
      camera.set_dev_camera_config(config_path)
      print("相机配置设置成功")
  except RuntimeError as e:
      print(f"设置相机配置失败: {e}")

  # 关闭相机
  camera.close_camera()

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

##### 模式切换
```bash
cd ~/.cache/agibot/app/bin
./mode_switch --mode develop # 切换到develop模式
```

如需切换回之前base模式，则执行
```bash
./mode_switch --mode base # 切换到base模式
```


#### 8. `close_camera()`

- **功能**：关闭相机连接
- **参数**：无
- **返回值**：`GDKRes`，操作结果状态码

- **示例**：

  ```python
  import agibot_gdk

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  camera = agibot_gdk.Camera()

  # 使用相机...

  # 关闭相机
  result = camera.close_camera()
  if result == agibot_gdk.GDKRes.kSuccess:
      print("相机关闭成功")
  else:
      print("相机关闭失败")

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

## 使用注意事项

1. **GDK初始化**：使用Camera功能前必须先调用`agibot_gdk.gdk_init()`初始化GDK系统
2. **GDK释放**：程序结束前必须调用`agibot_gdk.gdk_release()`释放GDK系统资源
3. **初始化等待**：创建Camera对象后，建议等待3秒以确保相机初始化完成
4. **超时设置**：根据实际需求设置合适的超时时间，避免长时间阻塞
5. **数据有效性**：使用前请检查返回的图像数据是否为None
6. **时间戳精度**：时间戳单位为纳秒，可用于精确的时间同步
7. **图像处理**：图像数据量较大，处理时注意内存使用
8. **相机选择**：根据应用场景选择合适的相机类型（鱼眼/立体/深度等）
9. **帧率控制**：注意相机的帧率限制，避免过度请求
10. **相机内参**：使用`get_camera_intrinsic()`获取相机内参，用于图像校正和3D重建
11. **相机配置**：使用`set_dev_camera_config()`设置相机配置时，确保配置文件路径有效
12. **资源管理**：使用完毕后调用`close_camera()`释放相机资源
13. **异常处理**：除`close_camera()`外，其他接口在失败时会抛出`std::runtime_error`异常，需要适当处理。`close_camera()`返回`GDKRes`状态码，不会抛出异常
14. **相机开关**：在常规模式/develop模式下，若打开更多相机，存在性能风险

## 应用场景

- **目标检测**：利用图像数据进行目标识别和检测
- **视觉导航**：为机器人导航提供视觉信息
- **SLAM建图**：结合图像数据进行同时定位与地图构建
- **环境监控**：实时监控周围环境变化
- **深度感知**：使用深度相机获取3D环境信息
- **立体视觉**：利用双目相机进行距离测量
- **图像识别**：进行物体分类和识别
- **数据融合**：与其他传感器数据进行融合，提高感知精度
- **相机标定**：使用内参进行图像校正和畸变补偿
- **3D重建**：结合内参进行三维点云重建
- **视觉测量**：利用相机内参进行精确的尺寸测量
- **AR/VR应用**：基于相机内参实现增强现实和虚拟现实功能
