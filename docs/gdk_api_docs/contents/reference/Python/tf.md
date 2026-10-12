# GDK TF 接口文档（Python）

## 概述

TF（Transform，坐标变换）模块为G02机器人提供了坐标系变换功能。通过Python接口，开发者可以方便地获取机器人各部件之间的坐标变换关系，适用于坐标变换、传感器标定、运动学计算等多种场景。

## 接口说明

### TF 类

该类封装了坐标变换的主要功能接口。

#### 1. `get_all_tf_from_base_link()`

- **功能**：获取从base_link到所有子坐标系的变换关系
- **参数**：无
- **返回值**：`list[TransformStamped]`，包含所有变换关系的列表，失败时抛出异常

- **TransformStamped 对象属性**：

| 属性名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `frame_id` | `str` | 父坐标系ID | 字符串 |
| `child_frame_id` | `str` | 子坐标系ID | 字符串 |
| `transform.translation.x` | `float` | 平移X分量 | 米 |
| `transform.translation.y` | `float` | 平移Y分量 | 米 |
| `transform.translation.z` | `float` | 平移Z分量 | 米 |
| `transform.rotation.x` | `float` | 旋转四元数X分量 | 无单位 |
| `transform.rotation.y` | `float` | 旋转四元数Y分量 | 无单位 |
| `transform.rotation.z` | `float` | 旋转四元数Z分量 | 无单位 |
| `transform.rotation.w` | `float` | 旋转四元数W分量 | 无单位 |
| `timestamp_ns` | `int` | 时间戳 | 纳秒 |

- **示例**：

  ```python
  import agibot_gdk
  import time

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  tf = agibot_gdk.TF()
  time.sleep(2)  # 等待TF初始化

  # 获取所有变换关系
  transforms = tf.get_all_tf_from_base_link()
  print(f"获取到 {len(transforms)} 个变换关系:")

  for transform_stamped in transforms:
      print(f"坐标系: {transform_stamped.frame_id} -> {transform_stamped.child_frame_id}")
      print(f"  平移: x={transform_stamped.transform.translation.x:.3f}, "
            f"y={transform_stamped.transform.translation.y:.3f}, "
            f"z={transform_stamped.transform.translation.z:.3f}")
      print(f"  旋转: x={transform_stamped.transform.rotation.x:.3f}, "
            f"y={transform_stamped.transform.rotation.y:.3f}, "
            f"z={transform_stamped.transform.rotation.z:.3f}, "
            f"w={transform_stamped.transform.rotation.w:.3f}")
      print(f"  时间戳: {transform_stamped.timestamp_ns}")
      print()

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

#### 2. `get_tf_from_base_link()`

- **功能**：获取从base_link到指定子坐标系的变换关系
- **参数**：
  - `child_frame_id`：子坐标系ID（字符串）
- **返回值**：`Transform`对象，包含变换信息，失败时抛出异常

- **Transform 对象属性**：

| 属性名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `translation.x` | `float` | 平移X分量 | 米 |
| `translation.y` | `float` | 平移Y分量 | 米 |
| `translation.z` | `float` | 平移Z分量 | 米 |
| `rotation.x` | `float` | 旋转四元数X分量 | 无单位 |
| `rotation.y` | `float` | 旋转四元数Y分量 | 无单位 |
| `rotation.z` | `float` | 旋转四元数Z分量 | 无单位 |
| `rotation.w` | `float` | 旋转四元数W分量 | 无单位 |

- **示例**：

  ```python
  import agibot_gdk
  import time

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  tf = agibot_gdk.TF()
  time.sleep(2)  # 等待TF初始化

  # 获取指定坐标系的变换关系
  child_frame_id = "head_link3"
  transform = tf.get_tf_from_base_link(child_frame_id)

  print(f"从base_link到{child_frame_id}的变换:")
  print(f"  平移: x={transform.translation.x:.3f}, "
        f"y={transform.translation.y:.3f}, "
        f"z={transform.translation.z:.3f}")
  print(f"  旋转: x={transform.rotation.x:.3f}, "
        f"y={transform.rotation.y:.3f}, "
        f"z={transform.rotation.z:.3f}, "
        f"w={transform.rotation.w:.3f}")

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

#### 3. `get_tf_from_sensor()`

- **功能**：获取从base_link到指定传感器的变换关系
- **参数**：
  - `sensor_extrinsic_type`：传感器外参类型（枚举值）
- **返回值**：`Transform`对象，包含变换信息，失败时抛出异常

- **SensorExtrinsicType 枚举值**：

| 枚举值 | 描述 |
| :--- | :--- |
| `kUnknown` | 未知类型 |
| `kHeadLeftStereoToHeadRightStereo` | 头部左立体相机到右立体相机 |
| `kLeftHandDepthToLeftHandColor` | 左手深度相机到彩色相机 |
| `kRightHandDepthToRightHandColor` | 右手深度相机到彩色相机 |
| `kHeadDepthToHeadColor` | 头部深度相机到彩色相机 |
| `kHeadLeftStereoToHeadLink3` | 头部左立体相机到头部链接3 |
| `kHeadRightStereoToHeadLink3` | 头部右立体相机到头部链接3 |
| `kHeadLeftFisheyeToHeadLink3` | 头部左鱼眼相机到头部链接3 |
| `kHeadRightFisheyeToHeadLink3` | 头部右鱼眼相机到头部链接3 |
| `kHeadBackFisheyeToHeadLink3` | 头部后鱼眼相机到头部链接3 |
| `kChassisFrontLidarToBaseLink` | 底盘前激光雷达到base_link |
| `kChassisBackLidarToBaseLink` | 底盘后激光雷达到base_link |
| `kChassisBackLidarToChassisFrontLidar` | 底盘后激光雷达到前激光雷达 |
| `kChassisMid360ImuToChassisMid360Lidar` | 底盘Mid360 IMU到底盘Mid360激光雷达 |
| `kChassisImuToBaseLink` | 底盘IMU到base_link |
| `kLeftHandRGBDToArmLEndLink` | 左手RGBD到左臂末端链接 |
| `kRightHandRGBDToArmREndLink` | 右手RGBD到右臂末端链接 |
| `kHeadRGBDToHeadLink3` | 头部RGBD到头部链接3 |

- **示例**：

  ```python
  import agibot_gdk
  import time

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  tf = agibot_gdk.TF()
  time.sleep(2)  # 等待TF初始化

  # 获取头部左立体相机到右立体相机的变换关系
  sensor_type = agibot_gdk.SensorExtrinsicType.kHeadLeftStereoToHeadRightStereo
  transform = tf.get_tf_from_sensor(sensor_type)

  print(f"从头部左立体相机到右立体相机的变换:")
  print(f"  平移: x={transform.translation.x:.3f}, "
        f"y={transform.translation.y:.3f}, "
        f"z={transform.translation.z:.3f}")
  print(f"  旋转: x={transform.rotation.x:.3f}, "
        f"y={transform.rotation.y:.3f}, "
        f"z={transform.rotation.z:.3f}, "
        f"w={transform.rotation.w:.3f}")

  # 获取底盘前激光雷达到base_link的变换关系
  lidar_transform = tf.get_tf_from_sensor(agibot_gdk.SensorExtrinsicType.kChassisFrontLidarToBaseLink)
  print(f"\n从底盘前激光雷达到base_link的变换:")
  print(f"  平移: x={lidar_transform.translation.x:.3f}, "
        f"y={lidar_transform.translation.y:.3f}, "
        f"z={lidar_transform.translation.z:.3f}")
  print(f"  旋转: x={lidar_transform.rotation.x:.3f}, "
        f"y={lidar_transform.rotation.y:.3f}, "
        f"z={lidar_transform.rotation.z:.3f}, "
        f"w={lidar_transform.rotation.w:.3f}")

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

#### 4. `lookup_transform_latest()`

- **功能**：查询两个坐标系之间的最新变换关系
- **参数**：
  - `target_frame`：目标坐标系ID（字符串）
  - `source_frame`：源坐标系ID（字符串）
  - `return_timestamp`：是否返回时间戳（布尔值，可选，默认为`False`）
- **返回值**：
  - 如果`return_timestamp=False`：返回`tuple(Transform, None)`
  - 如果`return_timestamp=True`：返回`tuple(Transform, int)`，其中第二个元素是时间戳（纳秒）
  - 失败时抛出异常

- **示例**：

  ```python
  import agibot_gdk
  import time

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  tf = agibot_gdk.TF()
  time.sleep(2)  # 等待TF初始化

  # 查询最新变换（不返回时间戳）
  transform, _ = tf.lookup_transform_latest("base_link", "arm_l_end_link")
  print("从arm_l_end_link到base_link的最新变换:")
  print(f"  平移: x={transform.translation.x:.3f}, "
        f"y={transform.translation.y:.3f}, "
        f"z={transform.translation.z:.3f}")
  print(f"  旋转: x={transform.rotation.x:.3f}, "
        f"y={transform.rotation.y:.3f}, "
        f"z={transform.rotation.z:.3f}, "
        f"w={transform.rotation.w:.3f}")

  # 查询最新变换（返回时间戳）
  transform, timestamp_ns = tf.lookup_transform_latest(
      "base_link", "arm_l_end_link", return_timestamp=True
  )
  print(f"\n时间戳: {timestamp_ns} ns")

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

#### 5. `lookup_transform()`

- **功能**：查询两个坐标系在特定时间的变换关系（支持时间插值）
- **参数**：
  - `target_frame`：目标坐标系ID（字符串）
  - `source_frame`：源坐标系ID（字符串）
  - `time_ns`：查询时间（纳秒时间戳，整数）
- **返回值**：`Transform`对象，包含变换信息，失败时抛出异常

- **示例**：

  ```python
  import agibot_gdk
  import time

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  tf = agibot_gdk.TF()
  time.sleep(2)  # 等待TF初始化

  # 获取当前时间戳（纳秒）
  current_time_ns =  tf.get_latest_timestamp("arm_l_end_link")
  # 查询1秒前的变换
  target_time_ns = current_time_ns - 1_000_000_000  # 1秒前

  transform = tf.lookup_transform("base_link", "arm_l_end_link", target_time_ns)
  print(f"从arm_l_end_link到base_link在时间 {target_time_ns} 的变换:")
  print(f"  平移: x={transform.translation.x:.3f}, "
        f"y={transform.translation.y:.3f}, "
        f"z={transform.translation.z:.3f}")
  print(f"  旋转: x={transform.rotation.x:.3f}, "
        f"y={transform.rotation.y:.3f}, "
        f"z={transform.rotation.z:.3f}, "
        f"w={transform.rotation.w:.3f}")

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

#### 6. `can_transform()`

- **功能**：检查两个坐标系之间是否存在变换关系
- **参数**：
  - `target_frame`：目标坐标系ID（字符串）
  - `source_frame`：源坐标系ID（字符串）
- **返回值**：`bool`，如果存在变换关系返回`True`，否则返回`False`

- **示例**：

  ```python
  import agibot_gdk
  import time

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  tf = agibot_gdk.TF()
  time.sleep(2)  # 等待TF初始化

  # 检查是否存在变换
  if tf.can_transform("base_link", "arm_l_end_link"):
      print("存在从arm_l_end_link到base_link的变换")
  else:
      print("不存在从arm_l_end_link到base_link的变换")

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

#### 7. `get_all_frame_names()`

- **功能**：获取所有可用的坐标系名称
- **参数**：无
- **返回值**：`list[str]`，包含所有坐标系名称的列表

- **示例**：

  ```python
  import agibot_gdk
  import time

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  tf = agibot_gdk.TF()
  time.sleep(2)  # 等待TF初始化

  # 获取所有坐标系名称
  frame_names = tf.get_all_frame_names()
  print(f"所有可用坐标系 ({len(frame_names)} 个):")
  for name in frame_names:
      print(f"  - {name}")

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

#### 8. `get_latest_timestamp()`

- **功能**：获取指定坐标系的最新时间戳
- **参数**：
  - `frame_id`：坐标系ID（字符串）
- **返回值**：`int`，最新时间戳（纳秒），失败时抛出异常

- **示例**：

  ```python
  import agibot_gdk
  import time

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  tf = agibot_gdk.TF()
  time.sleep(2)  # 等待TF初始化

  timestamp_ns = tf.get_latest_timestamp("arm_l_end_link")
  print(f"arm_l_end_link 最新时间戳: {timestamp_ns} ns")

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

#### 9. `clear()`

- **功能**：清空TF缓存中的所有变换关系
- **参数**：无
- **返回值**：无

- **示例**：

  ```python
  import agibot_gdk
  import time

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  tf = agibot_gdk.TF()
  time.sleep(2)  # 等待TF初始化

  # 清空TF缓存
  tf.clear()
  print("TF缓存已清空")

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

## 完整使用示例

### 坐标系变换查询示例

```python
import agibot_gdk
import time

# 初始化GDK系统
if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
    print("GDK初始化失败")
    exit(1)
print("GDK初始化成功")

tf = agibot_gdk.TF()
time.sleep(2)  # 等待TF初始化

# 1. 获取所有变换关系
print("=== 获取所有变换关系 ===")
transforms = tf.get_all_tf_from_base_link()
print(f"总共有 {len(transforms)} 个坐标系变换关系")

for i, transform_stamped in enumerate(transforms):
    print(f"{i+1}. {transform_stamped.frame_id} -> {transform_stamped.child_frame_id}")
    print(f"   平移: ({transform_stamped.transform.translation.x:.3f}, "
          f"{transform_stamped.transform.translation.y:.3f}, "
          f"{transform_stamped.transform.translation.z:.3f})")
    print(f"   旋转: ({transform_stamped.transform.rotation.x:.3f}, "
          f"{transform_stamped.transform.rotation.y:.3f}, "
          f"{transform_stamped.transform.rotation.z:.3f}, "
          f"{transform_stamped.transform.rotation.w:.3f})")
    print()

# 2. 查询特定坐标系的变换
print("=== 查询特定坐标系变换 ===")
target_frames = ["head_camera_link", "left_hand_link", "right_hand_link"]

for frame_id in target_frames:
    try:
        transform = tf.get_tf_from_base_link(frame_id)
        print(f"{frame_id}:")
        print(f"  平移: ({transform.translation.x:.3f}, "
              f"{transform.translation.y:.3f}, "
              f"{transform.translation.z:.3f})")
        print(f"  旋转: ({transform.rotation.x:.3f}, "
              f"{transform.rotation.y:.3f}, "
              f"{transform.rotation.z:.3f}, "
              f"{transform.rotation.w:.3f})")
    except Exception as e:
        print(f"{frame_id}: 获取失败 - {e}")
    print()

# 3. 查询传感器外参
print("=== 查询传感器外参 ===")
sensor_types = [
    (agibot_gdk.SensorExtrinsicType.kHeadLeftStereoToHeadRightStereo, "头部左立体相机到右立体相机"),
    (agibot_gdk.SensorExtrinsicType.kHeadDepthToHeadColor, "头部深度相机到彩色相机"),
    (agibot_gdk.SensorExtrinsicType.kChassisFrontLidarToBaseLink, "底盘前激光雷达到base_link"),
    (agibot_gdk.SensorExtrinsicType.kChassisImuToBaseLink, "底盘IMU到base_link")
]

for sensor_type, sensor_name in sensor_types:
    try:
        transform = tf.get_tf_from_sensor(sensor_type)
        print(f"{sensor_name}:")
        print(f"  平移: ({transform.translation.x:.3f}, "
              f"{transform.translation.y:.3f}, "
              f"{transform.translation.z:.3f})")
        print(f"  旋转: ({transform.rotation.x:.3f}, "
              f"{transform.rotation.y:.3f}, "
              f"{transform.rotation.z:.3f}, "
              f"{transform.rotation.w:.3f})")
    except Exception as e:
        print(f"{sensor_name}: 获取失败 - {e}")
    print()

# 释放GDK系统资源
if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
    print("GDK释放失败")
else:
    print("GDK释放成功")
```

### 传感器标定辅助示例

```python
import agibot_gdk
import time
import math

# 初始化GDK系统
if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
    print("GDK初始化失败")
    exit(1)
print("GDK初始化成功")

tf = agibot_gdk.TF()
time.sleep(2)  # 等待TF初始化

def quaternion_to_euler(x, y, z, w):
    """将四元数转换为欧拉角（弧度）"""
    # Roll (x-axis rotation)
    sinr_cosp = 2 * (w * x + y * z)
    cosr_cosp = 1 - 2 * (x * x + y * y)
    roll = math.atan2(sinr_cosp, cosr_cosp)

    # Pitch (y-axis rotation)
    sinp = 2 * (w * y - z * x)
    if abs(sinp) >= 1:
        pitch = math.copysign(math.pi / 2, sinp)  # use 90 degrees if out of range
    else:
        pitch = math.asin(sinp)

    # Yaw (z-axis rotation)
    siny_cosp = 2 * (w * z + x * y)
    cosy_cosp = 1 - 2 * (y * y + z * z)
    yaw = math.atan2(siny_cosp, cosy_cosp)

    return roll, pitch, yaw

def print_transform_info(transform, name):
    """打印变换信息"""
    print(f"{name}:")
    print(f"  平移: ({transform.translation.x:.6f}, "
          f"{transform.translation.y:.6f}, "
          f"{transform.translation.z:.6f}) 米")

    # 转换为欧拉角
    roll, pitch, yaw = quaternion_to_euler(
        transform.rotation.x, transform.rotation.y,
        transform.rotation.z, transform.rotation.w
    )

    print(f"  旋转四元数: ({transform.rotation.x:.6f}, "
          f"{transform.rotation.y:.6f}, "
          f"{transform.rotation.z:.6f}, "
          f"{transform.rotation.w:.6f})")
    print(f"  旋转欧拉角: Roll={math.degrees(roll):.2f}°, "
          f"Pitch={math.degrees(pitch):.2f}°, "
          f"Yaw={math.degrees(yaw):.2f}°")
    print()

# 获取所有相机的变换关系
print("=== 相机外参标定信息 ===")
camera_sensors = [
    (agibot_gdk.SensorExtrinsicType.kHeadLeftStereoToHeadRightStereo, "头部左立体相机到右立体相机"),
    (agibot_gdk.SensorExtrinsicType.kLeftHandDepthToLeftHandColor, "左手深度相机到彩色相机"),
    (agibot_gdk.SensorExtrinsicType.kRightHandDepthToRightHandColor, "右手深度相机到彩色相机"),
    (agibot_gdk.SensorExtrinsicType.kHeadDepthToHeadColor, "头部深度相机到彩色相机"),
    (agibot_gdk.SensorExtrinsicType.kHeadLeftStereoToHeadLink3, "头部左立体相机到头部链接3"),
    (agibot_gdk.SensorExtrinsicType.kHeadRightStereoToHeadLink3, "头部右立体相机到头部链接3"),
    (agibot_gdk.SensorExtrinsicType.kHeadLeftFisheyeToHeadLink3, "头部左鱼眼相机到头部链接3"),
    (agibot_gdk.SensorExtrinsicType.kHeadRightFisheyeToHeadLink3, "头部右鱼眼相机到头部链接3"),
    (agibot_gdk.SensorExtrinsicType.kHeadBackFisheyeToHeadLink3, "头部后鱼眼相机到头部链接3")
]

for sensor_type, sensor_name in camera_sensors:
    try:
        transform = tf.get_tf_from_sensor(sensor_type)
        print_transform_info(transform, sensor_name)
    except Exception as e:
        print(f"{sensor_name}: 获取失败 - {e}")

# 获取其他传感器的变换关系
print("=== 其他传感器外参信息 ===")
other_sensors = [
    (agibot_gdk.SensorExtrinsicType.kChassisFrontLidarToBaseLink, "底盘前激光雷达到base_link"),
    (agibot_gdk.SensorExtrinsicType.kChassisBackLidarToBaseLink, "底盘后激光雷达到base_link"),
    (agibot_gdk.SensorExtrinsicType.kChassisBackLidarToChassisFrontLidar, "底盘后激光雷达到前激光雷达"),
    (agibot_gdk.SensorExtrinsicType.kChassisMid360ImuToChassisMid360Lidar, "底盘Mid360 IMU到激光雷达"),
    (agibot_gdk.SensorExtrinsicType.kChassisImuToBaseLink, "底盘IMU到base_link"),
    (agibot_gdk.SensorExtrinsicType.kLeftHandRGBDToArmLEndLink, "左手RGBD到左臂末端链接"),
    (agibot_gdk.SensorExtrinsicType.kRightHandRGBDToArmREndLink, "右手RGBD到右臂末端链接"),
    (agibot_gdk.SensorExtrinsicType.kHeadRGBDToHeadLink3, "头部RGBD到头部链接3")
]

for sensor_type, sensor_name in other_sensors:
    try:
        transform = tf.get_tf_from_sensor(sensor_type)
        print_transform_info(transform, sensor_name)
    except Exception as e:
        print(f"{sensor_name}: 获取失败 - {e}")

# 释放GDK系统资源
if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
    print("GDK释放失败")
else:
    print("GDK释放成功")
```

## 使用注意事项

1. **GDK初始化**：使用TF功能前必须先调用`agibot_gdk.gdk_init()`初始化GDK系统
2. **GDK释放**：程序结束前必须调用`agibot_gdk.gdk_release()`释放GDK系统资源
3. **初始化等待**：创建TF对象后，建议等待2秒以确保系统初始化完成
4. **坐标系约定**：遵循机器人标准坐标系约定（右手坐标系）
5. **时间戳精度**：时间戳以纳秒为单位，注意精度处理
6. **异常处理**：所有接口在失败时会抛出`RuntimeError`异常，需要适当处理
7. **传感器类型**：使用传感器外参查询时，确保使用正确的传感器类型枚举
8. **变换矩阵**：四元数表示旋转，注意与旋转矩阵的转换
9. **坐标系ID**：使用字符串查询时，确保坐标系ID正确且存在，可通过`get_all_frame_names()`获取所有可用坐标系
10. **实时性**：TF数据可能随时间变化，注意数据的时效性
11. **变换查询**：`lookup_transform_latest()`查询最新变换，`lookup_transform()`支持时间插值查询历史变换
12. **变换检查**：使用`can_transform()`在查询前检查变换是否存在，避免查询失败
13. **时间插值**：`lookup_transform()`支持时间插值，可以查询历史任意时刻的变换关系
14. **缓存管理**：使用`clear()`可以清空TF缓存，适用于需要重置变换关系的场景
15. **时间戳查询**：`get_latest_timestamp()`可以获取指定坐标系的最新更新时间
16. **返回值处理**：`lookup_transform_latest()`根据`return_timestamp`参数返回不同的元组格式

## 应用场景

- **坐标变换**：获取机器人各部件之间的坐标变换关系
- **传感器标定**：获取传感器相对于机器人本体的外参
- **运动学计算**：为机器人运动学计算提供坐标变换数据
- **视觉处理**：为相机图像处理提供坐标系信息
- **导航定位**：为SLAM和导航提供坐标系变换
- **机械臂控制**：为机械臂运动规划提供坐标系信息
- **多传感器融合**：统一不同传感器的坐标系
- **标定验证**：验证传感器标定结果的正确性
