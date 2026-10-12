# GDK TF 接口文档（C++）

## 概述

TF（坐标变换）模块为G02机器人提供了坐标变换查询功能。通过C++接口，开发者可以方便地获取机器人各部件之间的坐标变换关系，适用于坐标变换、传感器标定、多传感器融合、SLAM建图等多种场景。

## 接口说明

### TF 类

该类封装了坐标变换的主要查询接口。

#### 1. `GetAllTfFromBaseLink()`

- **功能**：获取从base_link到所有子坐标系的变换关系
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `transforms` | `std::vector<TransformStamped>&` | 输出参数，变换关系列表 |

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`，`transforms`参数包含所有变换关系

#### TransformStamped对象详细说明

**TransformStamped结构体包含以下成员**：

| 成员名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `frame_id` | `std::string` | 父坐标系ID | 字符串 |
| `child_frame_id` | `std::string` | 子坐标系ID | 字符串 |
| `transform` | `Transform` | 变换信息 | 变换对象 |
| `timestamp_ns` | `uint64_t` | 时间戳 | 纳秒 |

```cpp
struct TransformStamped {
  std::string frame_id{};        ///< frame id
  std::string child_frame_id{};  ///< child frame id
  Transform transform{};         ///< transform
  uint64_t timestamp_ns{0};      ///< transform timestamp(ns)
};
```

**Transform结构体**：

| 成员名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `translation` | `Vector3` | 平移向量 | 米 |
| `rotation` | `Quaternion` | 旋转四元数 | 无单位 |

```cpp
struct Transform {
  Vector3 translation{};  ///< translation
  Quaternion rotation{};  ///< rotation
};
```

**Vector3结构体**：

| 成员名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `x` | `double` | X轴分量 | 米 |
| `y` | `double` | Y轴分量 | 米 |
| `z` | `double` | Z轴分量 | 米 |

**Quaternion结构体**：

| 成员名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `x` | `double` | 四元数X分量 | 无单位 |
| `y` | `double` | 四元数Y分量 | 无单位 |
| `z` | `double` | 四元数Z分量 | 无单位 |
| `w` | `double` | 四元数W分量 | 无单位 |

- **示例**：

  ```cpp
  #include "gdk/gdk.h"
  #include <iostream>
  #include <chrono>
  #include <thread>

  int main()
  {
      // 初始化GDK系统
      if (agibot::gdk::GDKInit() != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "GDK初始化失败" << std::endl;
          return -1;
      }
      std::cout << "GDK初始化成功" << std::endl;

      agibot::gdk::TF tf;
      std::cout << "TF init" << std::endl;
      std::this_thread::sleep_for(std::chrono::seconds(1));

      std::vector<agibot::gdk::TransformStamped> transforms;
      if (tf.GetAllTfFromBaseLink(transforms) != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "Failed to get all transforms" << std::endl;
      } else {
          std::cout << "获取到 " << transforms.size() << " 个变换关系:" << std::endl;
          for (const auto& transform_stamped : transforms) {
              std::cout << "坐标系: " << transform_stamped.frame_id
                        << " -> " << transform_stamped.child_frame_id << std::endl;
              std::cout << "  平移: x=" << transform_stamped.transform.translation.x
                        << ", y=" << transform_stamped.transform.translation.y
                        << ", z=" << transform_stamped.transform.translation.z << std::endl;
              std::cout << "  旋转: x=" << transform_stamped.transform.rotation.x
                        << ", y=" << transform_stamped.transform.rotation.y
                        << ", z=" << transform_stamped.transform.rotation.z
                        << ", w=" << transform_stamped.transform.rotation.w << std::endl;
              std::cout << "  时间戳: " << transform_stamped.timestamp_ns << std::endl;
              std::cout << std::endl;
          }
      }

      // 释放GDK系统资源
      if (agibot::gdk::GDKRelease() != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "GDK释放失败" << std::endl;
          return -1;
      }
      std::cout << "GDK释放成功" << std::endl;

      return 0;
  }
  ```

#### 2. `GetTfFromBaseLink()`

- **功能**：获取从base_link到指定子坐标系的变换关系
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `child_frame_id` | `const std::string&` | 子坐标系ID |
| `transform` | `Transform&` | 输出参数，变换信息对象 |

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`，`transform`参数包含变换信息

- **示例**：

  ```cpp
  #include "gdk/gdk.h"
  #include <iostream>
  #include <chrono>
  #include <thread>

  int main()
  {
      // 初始化GDK系统
      if (agibot::gdk::GDKInit() != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "GDK初始化失败" << std::endl;
          return -1;
      }
      std::cout << "GDK初始化成功" << std::endl;

      agibot::gdk::TF tf;
      std::cout << "TF init" << std::endl;
      std::this_thread::sleep_for(std::chrono::seconds(1));

      agibot::gdk::Transform transform;
      std::string child_frame_id = "arm_l_end_link";

      if (tf.GetTfFromBaseLink(child_frame_id, transform) != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "Failed to get transform for " << child_frame_id << std::endl;
      } else {
          std::cout << "从base_link到 " << child_frame_id << " 的变换:" << std::endl;
          std::cout << "  平移: x=" << transform.translation.x
                    << ", y=" << transform.translation.y
                    << ", z=" << transform.translation.z << std::endl;
          std::cout << "  旋转: x=" << transform.rotation.x
                    << ", y=" << transform.rotation.y
                    << ", z=" << transform.rotation.z
                    << ", w=" << transform.rotation.w << std::endl;
      }

      // 释放GDK系统资源
      if (agibot::gdk::GDKRelease() != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "GDK释放失败" << std::endl;
          return -1;
      }
      std::cout << "GDK释放成功" << std::endl;

      return 0;
  }
  ```

#### 3. `GetTfFromSensor()`

- **功能**：获取传感器外参变换关系
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `sensor_extrinsic_type` | `const SensorExtrinsicType&` | 传感器外参类型枚举 |
| `transform` | `Transform&` | 输出参数，变换信息对象 |

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`，`transform`参数包含传感器外参变换信息

#### SensorExtrinsicType枚举详细说明

**支持的传感器外参类型**：

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

```cpp
enum class SensorExtrinsicType {
  kUnknown = 0,
  kHeadLeftStereoToHeadRightStereo,
  kLeftHandDepthToLeftHandColor,
  kRightHandDepthToRightHandColor,
  kHeadDepthToHeadColor,
  kHeadLeftStereoToHeadLink3,
  kHeadRightStereoToHeadLink3,
  kHeadLeftFisheyeToHeadLink3,
  kHeadRightFisheyeToHeadLink3,
  kHeadBackFisheyeToHeadLink3,
  kChassisFrontLidarToBaseLink,
  kChassisBackLidarToBaseLink,
  kChassisBackLidarToChassisFrontLidar,
  kChassisMid360ImuToChassisMid360Lidar,
  kChassisImuToBaseLink,
  kLeftHandRGBDToArmLEndLink,
  kRightHandRGBDToArmREndLink,
  kHeadRGBDToHeadLink3
};
```

- **示例**：

  ```cpp
  #include "gdk/gdk.h"
  #include <iostream>
  #include <chrono>
  #include <thread>

  int main()
  {
      // 初始化GDK系统
      if (agibot::gdk::GDKInit() != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "GDK初始化失败" << std::endl;
          return -1;
      }
      std::cout << "GDK初始化成功" << std::endl;

      agibot::gdk::TF tf;
      std::cout << "TF init" << std::endl;
      std::this_thread::sleep_for(std::chrono::seconds(1));

      agibot::gdk::Transform transform;
      agibot::gdk::SensorExtrinsicType sensor_type =
          agibot::gdk::SensorExtrinsicType::kHeadLeftStereoToHeadRightStereo;

      if (tf.GetTfFromSensor(sensor_type, transform) != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "Failed to get sensor extrinsic transform" << std::endl;
      } else {
          std::cout << "传感器外参变换:" << std::endl;
          std::cout << "  平移: x=" << transform.translation.x
                    << ", y=" << transform.translation.y
                    << ", z=" << transform.translation.z << std::endl;
          std::cout << "  旋转: x=" << transform.rotation.x
                    << ", y=" << transform.rotation.y
                    << ", z=" << transform.rotation.z
                    << ", w=" << transform.rotation.w << std::endl;
      }

      // 释放GDK系统资源
      if (agibot::gdk::GDKRelease() != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "GDK释放失败" << std::endl;
          return -1;
      }
      std::cout << "GDK释放成功" << std::endl;

      return 0;
  }
  ```

#### 4. `LookupTransformLatest()`

- **功能**：查询两个坐标系之间的最新变换关系
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `target_frame` | `const std::string&` | 目标坐标系ID |
| `source_frame` | `const std::string&` | 源坐标系ID |
| `transform` | `Transform&` | 输出参数，变换信息对象（从source到target） |
| `timestamp_ns` | `uint64_t*` | 输出参数，时间戳指针（可选，可为nullptr） |

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`，`transform`参数包含变换信息

- **示例**：

  ```cpp
  #include "gdk/gdk.h"
  #include <iostream>
  #include <chrono>
  #include <thread>

  int main()
  {
      // 初始化GDK系统
      if (agibot::gdk::GDKInit() != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "GDK初始化失败" << std::endl;
          return -1;
      }
      std::cout << "GDK初始化成功" << std::endl;

      agibot::gdk::TF tf;
      std::cout << "TF init" << std::endl;
      std::this_thread::sleep_for(std::chrono::seconds(1));

      agibot::gdk::Transform transform;
      uint64_t timestamp_ns = 0;

      // 查询从arm_l_end_link到base_link的最新变换
      if (tf.LookupTransformLatest("base_link", "arm_l_end_link", transform, &timestamp_ns)
          != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "Failed to lookup transform" << std::endl;
      } else {
          std::cout << "从arm_l_end_link到base_link的最新变换:" << std::endl;
          std::cout << "  平移: x=" << transform.translation.x
                    << ", y=" << transform.translation.y
                    << ", z=" << transform.translation.z << std::endl;
          std::cout << "  旋转: x=" << transform.rotation.x
                    << ", y=" << transform.rotation.y
                    << ", z=" << transform.rotation.z
                    << ", w=" << transform.rotation.w << std::endl;
          std::cout << "  时间戳: " << timestamp_ns << " ns" << std::endl;
      }

      // 释放GDK系统资源
      if (agibot::gdk::GDKRelease() != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "GDK释放失败" << std::endl;
          return -1;
      }
      std::cout << "GDK释放成功" << std::endl;

      return 0;
  }
  ```

#### 5. `LookupTransform()`

- **功能**：查询两个坐标系在特定时间的变换关系（支持时间插值）
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `target_frame` | `const std::string&` | 目标坐标系ID |
| `source_frame` | `const std::string&` | 源坐标系ID |
| `time_ns` | `uint64_t` | 查询时间（纳秒时间戳） |
| `transform` | `Transform&` | 输出参数，变换信息对象（从source到target） |

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`，`transform`参数包含变换信息

- **示例**：

  ```cpp
  #include "gdk/gdk.h"
  #include <iostream>
  #include <chrono>
  #include <thread>

  int main()
  {
      // 初始化GDK系统
      if (agibot::gdk::GDKInit() != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "GDK初始化失败" << std::endl;
          return -1;
      }
      std::cout << "GDK初始化成功" << std::endl;

      agibot::gdk::TF tf;
      std::cout << "TF init" << std::endl;
      std::this_thread::sleep_for(std::chrono::seconds(1));

      // 获取当前时间戳
      auto now = std::chrono::system_clock::now();
      uint64_t current_time_ns = std::chrono::duration_cast<std::chrono::nanoseconds>(
          now.time_since_epoch()).count();

      // 查询1秒前的变换
      uint64_t target_time_ns = current_time_ns - 1000000000ULL; // 1秒前

      agibot::gdk::Transform transform;
      if (tf.LookupTransform("base_link", "arm_l_end_link", target_time_ns, transform)
          != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "Failed to lookup transform at time " << target_time_ns << std::endl;
      } else {
          std::cout << "从arm_l_end_link到base_link在时间 " << target_time_ns << " 的变换:" << std::endl;
          std::cout << "  平移: x=" << transform.translation.x
                    << ", y=" << transform.translation.y
                    << ", z=" << transform.translation.z << std::endl;
          std::cout << "  旋转: x=" << transform.rotation.x
                    << ", y=" << transform.rotation.y
                    << ", z=" << transform.rotation.z
                    << ", w=" << transform.rotation.w << std::endl;
      }

      // 释放GDK系统资源
      if (agibot::gdk::GDKRelease() != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "GDK释放失败" << std::endl;
          return -1;
      }
      std::cout << "GDK释放成功" << std::endl;

      return 0;
  }
  ```

#### 6. `CanTransform()`

- **功能**：检查两个坐标系之间是否存在变换关系
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `target_frame` | `const std::string&` | 目标坐标系ID |
| `source_frame` | `const std::string&` | 源坐标系ID |

- **返回值**：`bool`，如果存在变换关系返回`true`，否则返回`false`

- **示例**：

  ```cpp
  #include "gdk/gdk.h"
  #include <iostream>
  #include <chrono>
  #include <thread>

  int main()
  {
      // 初始化GDK系统
      if (agibot::gdk::GDKInit() != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "GDK初始化失败" << std::endl;
          return -1;
      }
      std::cout << "GDK初始化成功" << std::endl;

      agibot::gdk::TF tf;
      std::cout << "TF init" << std::endl;
      std::this_thread::sleep_for(std::chrono::seconds(1));

      // 检查是否存在变换
      if (tf.CanTransform("base_link", "arm_l_end_link")) {
          std::cout << "存在从arm_l_end_link到base_link的变换" << std::endl;
      } else {
          std::cout << "不存在从arm_l_end_link到base_link的变换" << std::endl;
      }

      // 释放GDK系统资源
      if (agibot::gdk::GDKRelease() != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "GDK释放失败" << std::endl;
          return -1;
      }
      std::cout << "GDK释放成功" << std::endl;

      return 0;
  }
  ```

#### 7. `GetAllFrameNames()`

- **功能**：获取所有可用的坐标系名称
- **参数**：无
- **返回值**：`std::vector<std::string>`，包含所有坐标系名称的列表

- **示例**：

  ```cpp
  #include "gdk/gdk.h"
  #include <iostream>
  #include <chrono>
  #include <thread>

  int main()
  {
      // 初始化GDK系统
      if (agibot::gdk::GDKInit() != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "GDK初始化失败" << std::endl;
          return -1;
      }
      std::cout << "GDK初始化成功" << std::endl;

      agibot::gdk::TF tf;
      std::cout << "TF init" << std::endl;
      std::this_thread::sleep_for(std::chrono::seconds(1));

      // 获取所有坐标系名称
      std::vector<std::string> frame_names = tf.GetAllFrameNames();
      std::cout << "所有可用坐标系 (" << frame_names.size() << " 个):" << std::endl;
      for (const auto& name : frame_names) {
          std::cout << "  - " << name << std::endl;
      }

      // 释放GDK系统资源
      if (agibot::gdk::GDKRelease() != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "GDK释放失败" << std::endl;
          return -1;
      }
      std::cout << "GDK释放成功" << std::endl;

      return 0;
  }
  ```

#### 8. `GetLatestTimestamp()`

- **功能**：获取指定坐标系的最新时间戳
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `frame_id` | `const std::string&` | 坐标系ID |
| `timestamp_ns` | `uint64_t&` | 输出参数，最新时间戳（纳秒） |

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`，`timestamp_ns`参数包含最新时间戳

- **示例**：

  ```cpp
  #include "gdk/gdk.h"
  #include <iostream>
  #include <chrono>
  #include <thread>

  int main()
  {
      // 初始化GDK系统
      if (agibot::gdk::GDKInit() != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "GDK初始化失败" << std::endl;
          return -1;
      }
      std::cout << "GDK初始化成功" << std::endl;

      agibot::gdk::TF tf;
      std::cout << "TF init" << std::endl;
      std::this_thread::sleep_for(std::chrono::seconds(1));

      uint64_t timestamp_ns = 0;
      if (tf.GetLatestTimestamp("arm_l_end_link", timestamp_ns)
          != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "Failed to get latest timestamp" << std::endl;
      } else {
          std::cout << "arm_l_end_link 最新时间戳: " << timestamp_ns << " ns" << std::endl;
      }

      // 释放GDK系统资源
      if (agibot::gdk::GDKRelease() != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "GDK释放失败" << std::endl;
          return -1;
      }
      std::cout << "GDK释放成功" << std::endl;

      return 0;
  }
  ```

#### 9. `Clear()`

- **功能**：清空TF缓存中的所有变换关系
- **参数**：无
- **返回值**：无（`void`）

- **示例**：

  ```cpp
  #include "gdk/gdk.h"
  #include <iostream>
  #include <chrono>
  #include <thread>

  int main()
  {
      // 初始化GDK系统
      if (agibot::gdk::GDKInit() != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "GDK初始化失败" << std::endl;
          return -1;
      }
      std::cout << "GDK初始化成功" << std::endl;

      agibot::gdk::TF tf;
      std::cout << "TF init" << std::endl;
      std::this_thread::sleep_for(std::chrono::seconds(1));

      // 清空TF缓存
      tf.Clear();
      std::cout << "TF缓存已清空" << std::endl;

      // 释放GDK系统资源
      if (agibot::gdk::GDKRelease() != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "GDK释放失败" << std::endl;
          return -1;
      }
      std::cout << "GDK释放成功" << std::endl;

      return 0;
  }
  ```

## 使用注意事项

1. **GDK初始化**：使用TF功能前必须先调用`agibot::gdk::GDKInit()`初始化GDK系统
2. **GDK释放**：程序结束前必须调用`agibot::gdk::GDKRelease()`释放GDK系统资源
3. **初始化等待**：创建TF对象后，建议等待1秒以确保DDS连接建立
4. **坐标系命名**：使用正确的坐标系名称，可通过`GetAllFrameNames()`获取所有可用坐标系的名称
5. **时间戳精度**：时间戳单位为纳秒，可用于精确的时间同步
6. **变换矩阵**：变换信息包含平移和旋转，可用于坐标转换计算
7. **传感器标定**：使用`GetTfFromSensor()`获取传感器外参，用于多传感器数据融合
8. **实时性**：变换关系会实时更新，反映机器人当前状态
9. **错误处理**：始终检查GDKRes返回值，确保操作成功
10. **变换查询**：`LookupTransformLatest()`查询最新变换，`LookupTransform()`支持时间插值查询历史变换
11. **变换检查**：使用`CanTransform()`在查询前检查变换是否存在，避免查询失败
12. **时间插值**：`LookupTransform()`支持时间插值，可以查询历史任意时刻的变换关系
13. **缓存管理**：使用`Clear()`可以清空TF缓存，适用于需要重置变换关系的场景
14. **时间戳查询**：`GetLatestTimestamp()`可以获取指定坐标系的最新更新时间

## 应用场景

- **坐标变换**：实现不同坐标系之间的坐标转换
- **传感器标定**：获取传感器外参，用于多传感器标定
- **多传感器融合**：结合多个传感器的数据，提高感知精度
- **SLAM建图**：为SLAM算法提供坐标系变换信息
- **路径规划**：在规划路径时考虑不同部件的坐标系关系
- **视觉处理**：将图像坐标转换为机器人坐标系
- **运动控制**：在控制机器人运动时考虑坐标系变换
- **数据同步**：基于时间戳进行多传感器数据同步
