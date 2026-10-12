# GDK UltrasonicRadar 接口文档（Python）

## 概述

UltrasonicRadar（超声波雷达）模块为G02机器人提供了获取实时超声波雷达数据的功能。通过Python接口，开发者可以方便地获取机器人的障碍物检测数据，适用于避障、导航、安全检测、近距离障碍物感知等多种场景。

## 接口说明

### UltrasonicRadar 类

该类封装了超声波雷达传感器的主要数据获取接口。

#### 1. `get_latest_ultrasonic_radar()`

- **功能**：获取最新的超声波雷达数据
- **参数**：无
- **返回值**：`dict`，包含超声波雷达数据的字典，失败时抛出异常

**返回值字典结构**：

| 键名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `timestamp_ns` | `int` | 时间戳（底盘传感器时间戳） | 纳秒 |
| `ultrasonic_radar_datas` | `list[dict]` | 超声波雷达数据列表 | 无单位 |

**`ultrasonic_radar_datas` 列表中每个字典的字段**：

| 键名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `id` | `int` | 超声波雷达ID | 无 |
| `distance_mm` | `int` | 检测到的距离 | 毫米 |
| `fault_state` | `int` | 故障状态（0表示正常，非0表示存在故障） | 无 |

- **示例**：

  ```python
  import agibot_gdk
  import time

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  radar = agibot_gdk.UltrasonicRadar()
  time.sleep(1)  # 等待1秒以确保DDS连接建立

  # 获取最新数据
  radar_data = radar.get_latest_ultrasonic_radar()

  print(f"✅ 时间戳: {radar_data['timestamp_ns']} ns")
  print(f"超声波雷达数量: {len(radar_data['ultrasonic_radar_datas'])}")

  for data in radar_data['ultrasonic_radar_datas']:
      print(f"  雷达[{data['id']}]: "
            f"距离={data['distance_mm']} mm, "
            f"故障状态={data['fault_state']}")

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

#### 2. `get_nearest_ultrasonic_radar()`

- **功能**：获取指定时间戳附近最近的超声波雷达数据
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `timestamp_ns` | `int` | 目标时间戳（纳秒） |

- **返回值**：`dict`，包含超声波雷达数据的字典，失败时抛出异常

**返回值字典结构**：

| 键名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `timestamp_ns` | `int` | 时间戳（底盘传感器时间戳） | 纳秒 |
| `ultrasonic_radar_datas` | `list[dict]` | 超声波雷达数据列表 | 无单位 |

**`ultrasonic_radar_datas` 列表中每个字典的字段**：

| 键名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `distance_mm` | `int` | 检测到的距离 | 毫米 |
| `fault_state` | `int` | 故障状态（0表示正常，非0表示存在故障） | 无 |

**注意**：`get_nearest_ultrasonic_radar()` 返回的雷达数据字典中不包含 `id` 字段。

- **示例**：

  ```python
  import agibot_gdk
  import time

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  radar = agibot_gdk.UltrasonicRadar()
  time.sleep(1)  # 等待1秒以确保DDS连接建立

  # 先获取最新数据
  latest_data = radar.get_latest_ultrasonic_radar()
  print(f"✅ 最新数据时间戳: {latest_data['timestamp_ns']} ns")

  # 查找最近的数据（往前1秒）
  target_timestamp = latest_data['timestamp_ns'] - 1000000000  # 1秒 = 1,000,000,000 纳秒
  nearest_data = radar.get_nearest_ultrasonic_radar(target_timestamp)

  print(f"✅ 最近数据时间戳: {nearest_data['timestamp_ns']} ns")
  time_diff = abs(nearest_data['timestamp_ns'] - target_timestamp)
  print(f"时间差: {time_diff} ns")
  print(f"超声波雷达数量: {len(nearest_data['ultrasonic_radar_datas'])}")

  for i, data in enumerate(nearest_data['ultrasonic_radar_datas']):
      print(f"  雷达[{i}]: "
            f"距离={data['distance_mm']} mm, "
            f"故障状态={data['fault_state']}")

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

#### 3. `get_ultrasonic_radar_fps()`

- **功能**：获取超声波雷达数据采集帧率
- **参数**：无
- **返回值**：`float`，超声波雷达帧率（FPS），失败时抛出异常

- **示例**：

  ```python
  import agibot_gdk
  import time

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  radar = agibot_gdk.UltrasonicRadar()
  time.sleep(2)  # 等待2秒让数据积累

  # 获取帧率
  fps = radar.get_ultrasonic_radar_fps()
  print(f"超声波雷达帧率: {fps} fps")

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

#### 4. `get_ultrasonic_radar_latency()`

- **功能**：获取超声波雷达数据延迟统计信息
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `window_seconds` | `float` | 统计窗口时间（秒），默认10.0秒 |

- **返回值**：`LatencyStats`对象，包含延迟统计信息，失败时抛出异常

**LatencyStats 对象属性**：

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

  radar = agibot_gdk.UltrasonicRadar()
  time.sleep(1)  # 等待1秒以确保DDS连接建立

  # 等待一段时间收集数据
  time.sleep(10)

  # 获取延迟统计
  latency = radar.get_ultrasonic_radar_latency(10.0)

  print("超声波雷达延迟统计:")
  print(f"  最大延迟: {latency.max_latency_ms} ms")
  print(f"  平均延迟: {latency.avg_latency_ms} ms")
  print(f"  P99延迟: {latency.p99_latency_ms} ms")
  print(f"  P99.9延迟: {latency.p999_latency_ms} ms")
  print(f"  P99.99延迟: {latency.p9999_latency_ms} ms")

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

#### 5. `close_ultrasonic_radar()`

- **功能**：关闭超声波雷达DDS连接
- **参数**：无
- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes.kSuccess`

- **示例**：

  ```python
  import agibot_gdk
  import time

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  radar = agibot_gdk.UltrasonicRadar()
  print("UltrasonicRadar init")

  # 使用超声波雷达...

  # 关闭超声波雷达
  if radar.close_ultrasonic_radar() != agibot_gdk.GDKRes.kSuccess:
      print("关闭超声波雷达失败")
  else:
      print("超声波雷达关闭成功")

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

## 完整示例

```python
import agibot_gdk
import time

# 初始化GDK系统
if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
    print("GDK初始化失败")
    exit(1)
print("GDK初始化成功")

# 创建超声波雷达对象
radar = agibot_gdk.UltrasonicRadar()

# 等待初始化完成
time.sleep(1)

# 获取最新数据
radar_data = radar.get_latest_ultrasonic_radar()

print("=== 超声波雷达数据 ===")
print(f"时间戳: {radar_data['timestamp_ns']} ns")
print(f"雷达数量: {len(radar_data['ultrasonic_radar_datas'])}")

for data in radar_data['ultrasonic_radar_datas']:
    print(f"  雷达[{data['id']}]: "
          f"距离={data['distance_mm']} mm, "
          f"故障状态={data['fault_state']}")

# 获取帧率
fps = radar.get_ultrasonic_radar_fps()
print(f"帧率: {fps} fps")

# 获取延迟统计
time.sleep(5)
latency = radar.get_ultrasonic_radar_latency(5.0)
print("延迟统计:")
print(f"  最大延迟: {latency.max_latency_ms} ms")
print(f"  平均延迟: {latency.avg_latency_ms} ms")

# 关闭接口
radar.close_ultrasonic_radar()

# 释放GDK系统资源
if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
    print("GDK释放失败")
else:
    print("GDK释放成功")
```

## 使用注意事项

1. **GDK初始化**：使用UltrasonicRadar功能前必须先调用`agibot_gdk.gdk_init()`初始化GDK系统
2. **GDK释放**：程序结束前必须调用`agibot_gdk.gdk_release()`释放GDK系统资源
3. **初始化等待**：创建UltrasonicRadar对象后，建议等待1秒以确保DDS连接建立
4. **异常处理**：所有接口在失败时会抛出异常，建议使用try-except进行异常处理
5. **时间戳精度**：时间戳单位为纳秒，是底盘传感器的时间戳，可用于精确的时间同步
6. **距离单位**：距离单位为毫米（mm），使用时注意单位转换
7. **故障状态**：`fault_state`为0表示正常，非0值表示存在故障，使用时需要检查
8. **数据获取**：`get_latest_ultrasonic_radar()`返回当前最新数据，如果没有新数据可能抛出异常
9. **时间戳查找**：`get_nearest_ultrasonic_radar()`根据时间戳查找最接近的数据，如果时间戳超出范围可能抛出异常
10. **数据格式差异**：`get_latest_ultrasonic_radar()`返回的雷达数据包含`id`字段，而`get_nearest_ultrasonic_radar()`返回的数据不包含`id`字段
11. **帧率统计**：`get_ultrasonic_radar_fps()`需要等待一段时间（建议至少2秒）让数据积累后才能获得准确的帧率
12. **延迟统计**：`get_ultrasonic_radar_latency()`需要等待一段时间（建议至少10秒）让数据积累后才能获得准确的统计信息
13. **资源释放**：使用完毕后调用`close_ultrasonic_radar()`释放资源
14. **字典访问**：返回值是字典类型，使用字典键名访问数据，注意键名的大小写和拼写

## 应用场景

- **避障检测**：实时检测机器人周围的障碍物，用于避障决策
- **近距离感知**：检测近距离的障碍物，补充激光雷达的盲区
- **安全检测**：监控机器人周围的安全区域，防止碰撞
- **导航辅助**：为机器人导航提供近距离障碍物信息
- **停车辅助**：辅助机器人进行精确停车和定位
- **低速导航**：在低速移动时提供可靠的障碍物检测
- **多传感器融合**：与其他传感器（如激光雷达、相机）数据进行融合，提高感知精度
- **安全区域监控**：监控机器人周围的安全区域，确保安全运行
- **障碍物分类**：结合距离信息进行障碍物分类和识别
- **路径规划**：基于超声波雷达数据规划安全路径

