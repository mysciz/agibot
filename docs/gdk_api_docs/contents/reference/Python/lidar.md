# GDK Lidar 接口文档（Python）

## 概述

Lidar（激光雷达）模块为G02机器人提供了获取实时点云数据的功能。通过Python接口，开发者可以方便地获取机器人的环境感知数据，适用于SLAM建图、障碍物检测、导航避障、环境建模等多种场景。

## 接口说明

### Lidar 类

该类封装了激光雷达传感器的主要数据获取接口。

#### 1. `get_latest_pointcloud()`

- **功能**：获取最新的点云数据
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `type` | `LidarType` | 雷达类型枚举值 |
| `timeout` | `float` | 超时时间（毫秒） |

- **返回值**：`PointCloud`对象，包含以下属性：

| 属性名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `timestamp_ns` | `int` | 点云数据采集的时间戳 | 纳秒 |
| `width` | `int` | 点云的宽度（点数） | 点数 |
| `height` | `int` | 点云的高度（点数） | 点数 |
| `point_step` | `int` | 每个点占用的字节数 | 字节 |
| `row_step` | `int` | 每行占用的字节数 | 字节 |
| `is_bigendian` | `bool` | 数据是否为大端序 | 布尔值 |
| `is_dense` | `bool` | 是否为密集点云（无无效点） | 布尔值 |
| `fields` | `list` | 字段信息列表，定义点云中每个点的属性结构 | 无单位 |
| `data` | `bytes` | 点云的原始二进制数据 | 字节 |

#### PointCloud对象详细说明

**fields (字段信息列表)**：

每个字段包含以下属性：

- `name`: 字段名称（如"x", "y", "z", "intensity"）
- `offset`: 在点数据中的偏移量
- `datatype`: 数据类型
- `count`: 该字段的元素数量

**data (原始数据)**：

- **类型**：`bytes`
- **描述**：点云的原始二进制数据
- **注意**：需要根据fields信息进行解析

**雷达类型**：
- `kLidarUnknown`: 未知雷达
- `kLidarFront`: 前部雷达
- `kLidarBack`: 后部雷达

- **示例**：

  ```python
  import agibot_gdk
  import time

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  lidar = agibot_gdk.Lidar()
  time.sleep(2)  # 等待激光雷达初始化

  pointcloud = lidar.get_latest_pointcloud(agibot_gdk.LidarType.kLidarFront, 1000.0)

  if pointcloud is not None:
      print(f"✅ 时间戳: {pointcloud.timestamp_ns}")
      print(f"点云尺寸: {pointcloud.width} x {pointcloud.height}")
      print(f"点步长: {pointcloud.point_step}")
      print(f"行步长: {pointcloud.row_step}")
      print(f"是否大端序: {pointcloud.is_bigendian}")
      print(f"是否密集: {pointcloud.is_dense}")
      print(f"数据大小: {pointcloud.data_size} 字节")

      # 打印字段信息
      print(f"字段数量: {len(pointcloud.fields)}")
      for j, field in enumerate(pointcloud.fields):
          print(f"  字段 {j+1}: {field.name} (偏移: {field.offset}, "
                f"类型: {field.datatype}, 数量: {field.count})")
  else:
      print("未获取到点云数据")

  # 关闭激光雷达
  lidar.close_lidar()

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

#### 2. `get_nearest_pointcloud()`

- **功能**：获取指定时间戳附近最近的点云数据
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `type` | `LidarType` | 雷达类型枚举值 |
| `timestamp` | `int` | 目标时间戳（纳秒） |
| `timeout` | `float` | 超时时间（毫秒） |

- **返回值**：`PointCloud`对象，结构与`get_latest_pointcloud()`相同

- **示例**：

  ```python
  import agibot_gdk
  import time

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  lidar = agibot_gdk.Lidar()
  time.sleep(1.0)
  
  # 先获取最新点云数据
  pointcloud = lidar.get_latest_pointcloud(agibot_gdk.LidarType.kLidarFront, 1000.0)
  
  if pointcloud is not None:
      # 获取历史点云数据（往前1秒）
      pointcloud_nearest = lidar.get_nearest_pointcloud(
          agibot_gdk.LidarType.kLidarFront, 
          pointcloud.timestamp_ns - 1000000000, 
          1000.0
      )

      if pointcloud_nearest is not None:
          print(f"✅ 最近点云数据: {pointcloud_nearest.timestamp_ns}")
          print(f"点云尺寸: {pointcloud_nearest.width} x {pointcloud_nearest.height}")
          print(f"点步长: {pointcloud_nearest.point_step}")
          print(f"行步长: {pointcloud_nearest.row_step}")
          print(f"数据大小: {pointcloud_nearest.data_size} 字节")
      else:
          print("❌ 未找到最近的点云数据")
  else:
      print("未获取到最新点云数据")

  # 关闭激光雷达
  lidar.close_lidar()

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

#### 3. `get_lidar_fps()`

- **功能**：获取激光雷达数据采集帧率
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `type` | `LidarType` | 雷达类型枚举值 |

- **返回值**：`float`，激光雷达帧率（FPS）

- **示例**：

  ```python
  import agibot_gdk
  import time

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  lidar = agibot_gdk.Lidar()
  time.sleep(2)  # 等待激光雷达初始化

  lidar_type = agibot_gdk.LidarType.kLidarFront
  
  try:
      fps = lidar.get_lidar_fps(lidar_type)
      print(f"激光雷达帧率: {fps} FPS")
  except RuntimeError as e:
      print(f"获取帧率失败: {e}")

  # 关闭激光雷达
  lidar.close_lidar()

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

#### 4. `get_lidar_latency()`

- **注意事项**：获取激光雷达数据延迟统计信息前，需要先进行时间同步，否则延迟统计结果不准确
- **功能**：获取激光雷达数据延迟统计信息
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `type` | `LidarType` | 雷达类型枚举值 |
| `window_seconds` | `float` | 统计窗口时间（秒） |

- **返回值**：`LatencyStats`对象，包含以下属性：

| 属性名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `max_latency_ms` | `float` | 最大延迟 | 毫秒 |
| `avg_latency_ms` | `float` | 平均延迟 | 毫秒 |
| `p99_latency_ms` | `float` | 99分位延迟 | 毫秒 |
| `p999_latency_ms` | `float` | 99.9分位延迟 | 毫秒 |
| `p9999_latency_ms` | `float` | 99.99分位延迟 | 毫秒 |

- **示例**：

  ```python
  import agibot_gdk
  import time

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  lidar = agibot_gdk.Lidar()
  time.sleep(2)  # 等待激光雷达初始化

  lidar_type = agibot_gdk.LidarType.kLidarFront
  
  try:
      latency = lidar.get_lidar_latency(lidar_type, 1.0)
      print("激光雷达延迟统计:")
      print(f"  最大延迟: {latency.max_latency_ms}ms")
      print(f"  平均延迟: {latency.avg_latency_ms}ms")
      print(f"  P99延迟: {latency.p99_latency_ms}ms")
      print(f"  P99.9延迟: {latency.p999_latency_ms}ms")
      print(f"  P99.99延迟: {latency.p9999_latency_ms}ms")
  except RuntimeError as e:
      print(f"获取延迟统计失败: {e}")

  # 关闭激光雷达
  lidar.close_lidar()

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

#### 5. `close_lidar()`

- **功能**：关闭激光雷达连接
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

  lidar = agibot_gdk.Lidar()
  
  # 使用激光雷达...
  
  # 关闭激光雷达
  result = lidar.close_lidar()
  if result == agibot_gdk.GDKRes.kSuccess:
      print("激光雷达关闭成功")
  else:
      print("激光雷达关闭失败")

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

## 使用注意事项

1. **GDK初始化**：使用激光雷达功能前必须先调用`agibot_gdk.gdk_init()`初始化GDK系统
2. **GDK释放**：程序结束前必须调用`agibot_gdk.gdk_release()`释放GDK系统资源
3. **初始化等待**：创建Lidar对象后，建议等待2秒以确保DDS连接建立
4. **超时设置**：根据实际需求设置合适的超时时间，避免长时间阻塞
5. **数据有效性**：使用前请检查返回的点云数据是否为None
6. **时间戳精度**：时间戳单位为纳秒，可用于精确的时间同步
7. **点云处理**：点云数据量较大，处理时注意内存使用
8. **雷达选择**：根据应用场景选择合适的雷达类型（前部/后部）
9. **资源管理**：使用完毕后调用`close_lidar()`释放激光雷达资源
10. **异常处理**：所有接口在失败时会抛出`std::runtime_error`异常，需要适当处理
11. **未实现方法**：`get_lidar_fps()`和`get_lidar_latency()`当前未实现，使用时需注意

## 应用场景

- **SLAM建图**：利用点云数据进行同时定位与地图构建
- **障碍物检测**：实时检测环境中的障碍物
- **导航避障**：为机器人导航提供环境感知信息
- **环境建模**：构建3D环境模型
- **目标识别**：结合点云数据进行目标检测和识别
- **路径规划**：基于点云数据规划安全路径
- **数据融合**：与其他传感器数据进行融合，提高感知精度
