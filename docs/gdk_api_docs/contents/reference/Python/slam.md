# GDK SLAM 接口文档（Python）

## 概述

SLAM（Simultaneous Localization and Mapping，同时定位与地图构建）模块为G02机器人提供了实时建图和定位功能。通过Python接口，开发者可以方便地实现机器人的环境感知、地图构建、位置估计等功能，适用于自主导航、环境建模、定位服务等多种场景。

## 接口说明

### Slam 类

该类封装了SLAM系统的主要功能接口。

#### 1. `get_slam_state()`

- **功能**：获取SLAM系统当前状态
- **参数**：无
- **返回值**：`int`，SLAM状态码，失败时抛出异常（1：开始建图 2：停止建图 0：取消建图）

- **示例**：

  ```python
  import agibot_gdk
  import time

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  slam = agibot_gdk.Slam()
  time.sleep(2)  # 等待SLAM初始化
  
  # 获取SLAM状态
  slam_state = slam.get_slam_state()
  print(f"SLAM状态: {slam_state}")

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

#### 2. `start_mapping()`

- **功能**：开始建图
- **参数**：无
- **返回值**：无，失败时抛出异常

- **示例**：

  ```python
  import agibot_gdk
  import time

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  slam = agibot_gdk.Slam()
  time.sleep(2)  # 等待SLAM初始化
  
  # 开始建图
  try:
      slam.start_mapping()
      print("开始建图成功")
  except Exception as e:
      print(f"开始建图失败: {e}")
  
  # 检查建图状态
  time.sleep(2)
  slam_state = slam.get_slam_state()
  print(f"建图状态: {slam_state}")

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

#### 3. `stop_mapping()`

- **功能**：停止且保存建图
- **参数**：无
- **返回值**：无，失败时抛出异常

- **示例**：

  ```python
  import agibot_gdk
  import time

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  slam = agibot_gdk.Slam()
  time.sleep(2)  # 等待SLAM初始化
  
  # 停止建图
  try:
      slam.stop_mapping()
      print("停止建图成功")
  except Exception as e:
      print(f"停止建图失败: {e}")
  
  # 检查建图状态
  time.sleep(2)
  slam_state = slam.get_slam_state()
  print(f"建图状态: {slam_state}")

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

#### 4. `cancel_mapping()`

- **功能**：取消建图
- **参数**：无
- **返回值**：无，失败时抛出异常

- **示例**：

  ```python
  import agibot_gdk
  import time

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  slam = agibot_gdk.Slam()
  time.sleep(2)  # 等待SLAM初始化
  
  # 取消建图
  try:
      slam.cancel_mapping()
      print("取消建图成功")
  except Exception as e:
      print(f"取消建图失败: {e}")
  
  # 检查建图状态
  time.sleep(2)
  slam_state = slam.get_slam_state()
  print(f"建图状态: {slam_state}")

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

#### 5. `get_odom_info()`

- **功能**：获取里程计信息
- **参数**：无
- **返回值**：`OdomInfo`对象，包含以下属性：

| 属性名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `pose.position.x` | `float` | 当前位置X坐标 | 米 |
| `pose.position.y` | `float` | 当前位置Y坐标 | 米 |
| `pose.position.z` | `float` | 当前位置Z坐标 | 米 |
| `pose.orientation.x` | `float` | 当前方向四元数X分量 | 无单位 |
| `pose.orientation.y` | `float` | 当前方向四元数Y分量 | 无单位 |
| `pose.orientation.z` | `float` | 当前方向四元数Z分量 | 无单位 |
| `pose.orientation.w` | `float` | 当前方向四元数W分量 | 无单位 |
| `twist.linear.x` | `float` | 线速度X分量 | 米/秒 |
| `twist.linear.y` | `float` | 线速度Y分量 | 米/秒 |
| `twist.linear.z` | `float` | 线速度Z分量 | 米/秒 |
| `twist.angular.x` | `float` | 角速度X分量 | 弧度/秒 |
| `twist.angular.y` | `float` | 角速度Y分量 | 弧度/秒 |
| `twist.angular.z` | `float` | 角速度Z分量 | 弧度/秒 |
| `is_stationary` | `bool` | 是否静止 | 布尔值 |
| `is_sliping` | `bool` | 是否打滑 | 布尔值 |
| `loc_confidence` | `float` | 定位置信度 | 无单位 |
| `loc_state` | `int` | 定位状态 | 整数 |
| `velocity` | `Vector3` | 速度向量 | 米/秒 |
| `velocity_body` | `Vector3` | 机体坐标系速度 | 米/秒 |
| `acceleration` | `Vector3` | 加速度向量 | 米/秒² |
| `ang_vel` | `Vector3` | 角速度向量 | 弧度/秒 |
| `orientation_euler` | `Vector3` | 欧拉角方向 | 弧度 |

- **示例**：

  ```python
  import agibot_gdk
  import time

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  slam = agibot_gdk.Slam()
  time.sleep(2)  # 等待SLAM初始化
  
  # 获取里程计信息
  odom_info = slam.get_odom_info()
  print(f"位置: ({odom_info.pose.position.x:.3f}, {odom_info.pose.position.y:.3f}, {odom_info.pose.position.z:.3f})")
  print(f"方向: ({odom_info.pose.orientation.x:.3f}, {odom_info.pose.orientation.y:.3f}, {odom_info.pose.orientation.z:.3f}, {odom_info.pose.orientation.w:.3f})")
  print(f"线速度: ({odom_info.twist.linear.x:.3f}, {odom_info.twist.linear.y:.3f}, {odom_info.twist.linear.z:.3f})")
  print(f"角速度: ({odom_info.twist.angular.x:.3f}, {odom_info.twist.angular.y:.3f}, {odom_info.twist.angular.z:.3f})")
  print(f"是否静止: {odom_info.is_stationary}")
  print(f"是否打滑: {odom_info.is_sliping}")
  print(f"定位置信度: {odom_info.loc_confidence:.3f}")
  print(f"定位状态: {odom_info.loc_state}")

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

#### 6. `record_spec_loc()` （该接口暂未上线）

- **功能**：记录当前位置为充电点位置
- **参数**：无
- **返回值**：无，失败时抛出异常

- **示例**：

  ```python
  import agibot_gdk
  import time

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  slam = agibot_gdk.Slam()
  time.sleep(2)  # 等待SLAM初始化
  
  # 记录特定位置
  try:
      slam.record_spec_loc()
      print("记录特定位置成功")
  except Exception as e:
      print(f"记录特定位置失败: {e}")

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

#### 7. `get_curr_pose()`

- **功能**：获取当前位姿
- **参数**：无
- **返回值**：`Pose`对象，包含以下属性：

| 属性名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `position.x` | `float` | 位置X坐标 | 米 |
| `position.y` | `float` | 位置Y坐标 | 米 |
| `position.z` | `float` | 位置Z坐标 | 米 |
| `orientation.x` | `float` | 方向四元数X分量 | 无单位 |
| `orientation.y` | `float` | 方向四元数Y分量 | 无单位 |
| `orientation.z` | `float` | 方向四元数Z分量 | 无单位 |
| `orientation.w` | `float` | 方向四元数W分量 | 无单位 |

- **示例**：

  ```python
  import agibot_gdk
  import time

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  slam = agibot_gdk.Slam()
  time.sleep(2)  # 等待SLAM初始化
  
  # 获取当前位姿
  pose = slam.get_curr_pose()
  print(f"当前位置: ({pose.position.x:.3f}, {pose.position.y:.3f}, {pose.position.z:.3f})")
  print(f"当前方向: ({pose.orientation.x:.3f}, {pose.orientation.y:.3f}, {pose.orientation.z:.3f}, {pose.orientation.w:.3f})")

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

#### 8. 完整使用示例

- **功能**：演示SLAM模块的完整使用流程
- **示例**：

  ```python
  import agibot_gdk
  import time

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  # 初始化SLAM模块
  slam = agibot_gdk.Slam()
  time.sleep(2)  # 等待SLAM初始化

  # 开始建图
  try:
      slam.start_mapping()
      print("开始建图成功")
  except Exception as e:
      print(f"开始建图失败: {e}")

  # 建图过程中监控状态和位置
  for i in range(10):
      try:
          odom_info = slam.get_odom_info()
          print(f"里程计位置: ({odom_info.pose.position.x:.3f}, {odom_info.pose.position.y:.3f}, {odom_info.pose.position.z:.3f})")
          print(f"里程计方向: ({odom_info.pose.orientation.x:.3f}, {odom_info.pose.orientation.y:.3f}, {odom_info.pose.orientation.z:.3f}, {odom_info.pose.orientation.w:.3f})")
          
          slam_state = slam.get_slam_state()
          print(f"SLAM状态: {slam_state}")
          
          pose = slam.get_curr_pose()
          print(f"当前位姿: ({pose.position.x:.3f}, {pose.position.y:.3f}, {pose.position.z:.3f})")
          
      except Exception as e:
          print(f"获取信息失败: {e}")
      
      time.sleep(1)

  # 记录特定位置
  try:
      slam.record_spec_loc()
      print("记录特定位置成功")
  except Exception as e:
      print(f"记录特定位置失败: {e}")

  # 停止建图
  try:
      slam.stop_mapping()
      print("停止建图成功")
  except Exception as e:
      print(f"停止建图失败: {e}")

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

## 使用注意事项

1. **GDK初始化**：使用SLAM功能前必须先调用`agibot_gdk.gdk_init()`初始化GDK系统
2. **GDK释放**：程序结束前必须调用`agibot_gdk.gdk_release()`释放GDK系统资源
3. **初始化等待**：创建Slam对象后，建议等待2秒以确保系统初始化完成
4. **建图环境**：确保建图环境有足够的特征点，避免在空旷或重复性强的环境中建图
5. **状态监控**：及时检查SLAM状态，确保系统正常运行
6. **数据质量**：保证传感器数据质量，避免在传感器故障时进行建图
7. **计算资源**：SLAM算法计算量较大，注意系统资源使用情况
8. **异常处理**：所有接口在失败时会抛出`std::runtime_error`异常，需要适当处理
9. **位姿精度**：SLAM位姿估计可能存在漂移，建议定期校正
10. **地图保存**：建图完成后及时保存地图，避免数据丢失

## 应用场景

- **环境建图**：构建机器人工作环境的详细地图
- **自主定位**：在已知环境中实现精确定位
- **导航服务**：为路径规划提供环境信息
- **环境监控**：实时监控环境变化
- **数据采集**：收集环境数据用于后续分析
- **位置记录**：标记和记录重要位置点
- **轨迹跟踪**：跟踪机器人的运动轨迹
- **地图更新**：动态更新环境地图信息

