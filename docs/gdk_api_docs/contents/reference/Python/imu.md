# GDK IMU 接口文档（Python）

## 概述

IMU（惯性测量单元）模块为G02机器人提供了获取实时惯性数据的功能。通过Python接口，开发者可以方便地获取机器人的方向、角速度和线性加速度信息，适用于姿态检测、运动分析、导航等多种场景。

## 接口说明

### Imu 类

该类封装了IMU传感器的主要数据获取接口。

#### 1. `get_latest_imu()`

- **功能**：获取最新的IMU数据
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `type` | `ImuType` | IMU类型枚举值 |
| `timeout` | `float` | 超时时间（毫秒） |

- **返回值**：`ImuData`对象，包含以下属性：

| 属性名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `timestamp_ns` | `int` | 数据采集的时间戳，精度为纳秒 | 纳秒 |
| `angular_velocity` | `Vector3` | 角速度，机器人在三个轴上的角速度 | 弧度/秒 |
| `linear_acceleration` | `Vector3` | 线性加速度，机器人在三个轴上的线性加速度 | 米/秒² |

#### ImuData对象详细说明

**angular_velocity (角速度对象)**：

- `x`: X轴角速度
- `y`: Y轴角速度
- `z`: Z轴角速度

**linear_acceleration (线性加速度对象)**：

- `x`: X轴加速度
- `y`: Y轴加速度
- `z`: Z轴加速度

**IMU类型**：
- `kImuUnknown`: 未知IMU
- `kImuFront`: 前部IMU
- `kImuBack`: 后部IMU
- `kImuChassis`: 底盘IMU

**示例**：

  ```python
  import agibot_gdk
  import time

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  imu = agibot_gdk.Imu()
  time.sleep(2)  # 等待IMU初始化

  for i in range(10):
      # 获取最新IMU数据
      imu_data = imu.get_latest_imu(agibot_gdk.ImuType.kImuFront, 1000.0)

      if imu_data is not None:
          print(f"\n--- IMU数据 #{i+1} ---")
          print(f"时间戳: {imu_data.timestamp_ns}")

          # 角速度
          print(f"角速度: x={imu_data.angular_velocity.x:.4f}, "
                f"y={imu_data.angular_velocity.y:.4f}, "
                f"z={imu_data.angular_velocity.z:.4f}")
          # 线性加速度
          print(f"线性加速度: x={imu_data.linear_acceleration.x:.4f}, "
                f"y={imu_data.linear_acceleration.y:.4f}, "
                f"z={imu_data.linear_acceleration.z:.4f}")
      else:
          print(f"未收到IMU数据 #{i+1}")
      time.sleep(1.0)

  # 关闭IMU
  imu.close_imu()

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

#### 2. `get_nearest_imu()`

- **功能**：获取指定时间戳附近最近的IMU数据
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `type` | `ImuType` | IMU类型枚举值 |
| `timestamp` | `int` | 目标时间戳（纳秒） |
| `timeout` | `float` | 超时时间（毫秒） |

- **返回值**：`ImuData`对象，结构与`get_latest_imu()`相同

- **示例**：

  ```python
  import agibot_gdk
  import time

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  imu = agibot_gdk.Imu()
  time.sleep(1.0)
  imu_type = agibot_gdk.ImuType.kImuFront

  # 先获取最新IMU数据
  imu_data = imu.get_latest_imu(imu_type, 1000.0)

  if imu_data is not None:
      # 获取历史IMU数据（往前1秒）
      imu_data_nearest = imu.get_nearest_imu(imu_type, imu_data.timestamp_ns-1000000000, 1000.0)

      if imu_data_nearest is not None:
          print(f"✅ 最近IMU数据: {imu_data_nearest.timestamp_ns}")
          print(f"角速度: x={imu_data_nearest.angular_velocity.x:.4f}, "
                f"y={imu_data_nearest.angular_velocity.y:.4f}, "
                f"z={imu_data_nearest.angular_velocity.z:.4f}")
          print(f"线性加速度: x={imu_data_nearest.linear_acceleration.x:.4f}, "
                f"y={imu_data_nearest.linear_acceleration.y:.4f}, "
                f"z={imu_data_nearest.linear_acceleration.z:.4f}")
      else:
          print(f"❌ 未找到最近的 {imu_type} 数据")

  # 关闭IMU
  imu.close_imu()

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

#### 3. `get_imu_fps()`

- **功能**：获取IMU数据采集帧率
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `type` | `ImuType` | IMU类型枚举值 |

- **返回值**：`int`，IMU帧率（FPS）

- **示例**：

  ```python
  import agibot_gdk
  import time

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  imu = agibot_gdk.Imu()
  time.sleep(2)  # 等待IMU初始化

  imu_type = agibot_gdk.ImuType.kImuChassis
  try:
      fps = imu.get_imu_fps(imu_type)
      print(f"IMU帧率: {fps} FPS")
  except RuntimeError as e:
      print(f"获取帧率失败: {e}")

  # 关闭IMU
  imu.close_imu()

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

#### 4. `get_imu_latency()`

- **注意事项**：获取IMU数据延迟统计信息前，需要先进行时间同步，否则延迟统计结果不准确
- **功能**：获取IMU数据延迟统计信息
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `type` | `ImuType` | IMU类型枚举值 |
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

  imu = agibot_gdk.Imu()
  time.sleep(2)  # 等待IMU初始化

  imu_type = agibot_gdk.ImuType.kImuChassis
  
  try:
      latency = imu.get_imu_latency(imu_type, 1.0)
      print("IMU延迟统计:")
      print(f"  最大延迟: {latency.max_latency_ms}ms")
      print(f"  平均延迟: {latency.avg_latency_ms}ms")
      print(f"  P99延迟: {latency.p99_latency_ms}ms")
      print(f"  P99.9延迟: {latency.p999_latency_ms}ms")
      print(f"  P99.99延迟: {latency.p9999_latency_ms}ms")
  except RuntimeError as e:
      print(f"获取延迟统计失败: {e}")

  # 关闭IMU
  imu.close_imu()

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

#### 5. `close_imu()`

- **功能**：关闭IMU连接
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

  imu = agibot_gdk.Imu()

  # 使用IMU...

  # 关闭IMU
  result = imu.close_imu()
  if result == agibot_gdk.GDKRes.kSuccess:
      print("IMU关闭成功")
  else:
      print("IMU关闭失败")

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

## 使用注意事项

1. **GDK初始化**：使用IMU功能前必须先调用`agibot_gdk.gdk_init()`初始化GDK系统
2. **GDK释放**：程序结束前必须调用`agibot_gdk.gdk_release()`释放GDK系统资源
3. **初始化等待**：创建Imu对象后，建议等待2秒以确保DDS连接建立
4. **超时设置**：根据实际需求设置合适的超时时间，避免长时间阻塞
5. **数据有效性**：使用前请检查返回的IMU数据是否为None
6. **时间戳精度**：时间戳单位为纳秒，可用于精确的时间同步
7. **资源管理**：使用完毕后调用`close_imu()`释放IMU资源
8. **异常处理**：所有接口在失败时会抛出`std::runtime_error`异常，需要适当处理
9. **未实现方法**：`get_imu_fps()`和`get_imu_latency()`当前未实现，使用时需注意

## 应用场景

- **运动分析**：利用角速度和线性加速度分析机器人运动状态
- **导航定位**：结合其他传感器数据进行SLAM和定位
- **平衡控制**：基于IMU数据实现机器人的平衡控制
- **数据融合**：与其他传感器数据进行融合，提高定位精度
- **振动监测**：通过加速度数据监测机器人振动状态

