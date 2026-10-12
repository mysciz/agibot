# GDK Lidar 接口文档（C++）

## 概述

Lidar（激光雷达）模块为G02机器人提供了获取实时点云数据的功能。通过C++接口，开发者可以方便地获取机器人的环境感知数据，适用于SLAM建图、障碍物检测、导航避障、环境建模等多种场景。

## 接口说明

### Lidar 类

该类封装了激光雷达传感器的主要数据获取接口。

#### 1. `GetLatestPointCloud()`

- **功能**：获取最新的点云数据
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `lidar_type` | `const LidarType&` | 激光雷达类型枚举值 |
| `timeout_ms` | `const float` | 超时时间（毫秒） |
| `pointcloud` | `std::shared_ptr<PointCloud>&` | 输出参数，点云数据指针 |

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`，`pointcloud`参数包含点云数据

#### PointCloud对象详细说明

**PointCloud结构体包含以下成员**：

| 成员名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `timestamp_ns` | `uint64_t` | 点云数据采集的时间戳 | 纳秒 |
| `width` | `int` | 点云的宽度（点数） | 点数 |
| `height` | `int` | 点云的高度（点数） | 点数 |
| `point_step` | `int` | 每个点占用的字节数 | 字节 |
| `row_step` | `int` | 每行占用的字节数 | 字节 |
| `is_bigendian` | `bool` | 数据是否为大端序 | 布尔值 |
| `is_dense` | `bool` | 是否为密集点云（无无效点） | 布尔值 |
| `fields` | `std::vector<PointField>` | 字段信息列表，定义点云中每个点的属性结构 | 无单位 |
| `data_view` | `DataView` | 点云的原始二进制数据视图 | 数据视图 |

 ```cpp
 struct PointCloud {
  int width{0};   ///< point cloud width
  int height{0};  ///< point cloud height

  std::vector<PointField> fields{};  ///< point cloud fields
  int point_step{0};                 ///< point step
  int row_step{0};                   ///< row step
  bool is_bigendian{false};          ///< is bigendian
  bool is_dense{true};               ///< is dense

  DataView data_view{};      ///< point cloud data view
  uint64_t timestamp_ns{0};  ///< point cloud timestamp(ns)
 };
 ```
**fields (字段信息列表)**：

每个字段包含以下属性：

| 成员名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `name` | `std::string` | 字段名称（如"x", "y", "z", "intensity"） |
| `offset` | `uint32_t` | 在点数据中的偏移量 |
| `datatype` | `uint8_t` | 数据类型 |
| `count` | `uint32_t` | 该字段的元素数量 |

 ```cpp
 struct PointField {
  std::string name{};   // point field name (x, y, z, intensity, etc.)
  uint32_t offset{0};   // point field offset
  uint8_t datatype{0};  // point field datatype
  uint32_t count{1};    // point field count
 };
 ```

**data_view (原始数据)**：

- **类型**：`DataView`
- **描述**：点云的原始二进制数据视图
- **注意**：需要根据fields信息进行解析

 ```cpp
 class DataView {
 public:
  /// @enum OwnershipType
  /// @brief ownership type
  /// @details ownership type related information
  enum class OwnershipType { OWNED, BORROWED };

  DataView() = default;

  DataView(const void* data, size_t size);

  explicit DataView(const std::vector<uint8_t>& vec);

  DataView(const DataView& other);

  DataView& operator=(const DataView& other);
  DataView(DataView&& other) noexcept;
  DataView& operator=(DataView&& other) noexcept;

  /// @brief data
  /// @details use to get the data of the data view
  /// @return the data of the data view
  const uint8_t* data() const { return data_; }

  /// @brief mutable_data
  /// @details use to get the mutable data of the data view
  /// @return the mutable data of the data view
  uint8_t* mutable_data() { return const_cast<uint8_t*>(data_); }

  /// @brief size
  /// @details use to get the size of the data view
  /// @return the size of the data view
  size_t size() const { return size_; }

  /// @brief IsOwned
  /// @details use to check if the data view is owned
  /// @return true if the data view is owned, false otherwise
  bool IsOwned() const { return ownership_ == OwnershipType::OWNED; }

  /// @brief Clone
  /// @details use to clone the data view
  /// @return the cloned data view
  DataView Clone() const;

  /// @brief CreateOwnedFrom
  /// @details use to create a data view from owned data
  /// @param data the data of the data view, input parameter
  /// @param size the size of the data view, input parameter
  /// @return the created data view
  static DataView CreateOwnedFrom(const void* data, size_t size);

  /// @brief AssignOwnedData
  /// @details use to assign owned data to the data view
  /// @param data the data of the data view, input parameter
  /// @param size the size of the data view, input parameter
  void AssignOwnedData(const void* data, size_t size);

 private:
  const uint8_t* data_ = nullptr;
  size_t size_ = 0;
  OwnershipType ownership_ = OwnershipType::BORROWED;
  std::vector<uint8_t> owned_buffer_;
 };
 ```

**激光雷达类型**：
- `LidarType::kLidarFront`: 前部激光雷达
- `LidarType::kLidarBack`: 后部激光雷达

- **示例**：

  ```cpp
  #include <iostream>
  #include <chrono>
  #include <thread>
  #include <memory>
  #include "gdk/gdk.h"

  int main() {
      // 初始化GDK系统
      if (agibot::gdk::GDKInit() != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "GDK初始化失败" << std::endl;
          return -1;
      }
      std::cout << "GDK初始化成功" << std::endl;

      agibot::gdk::Lidar lidar;

      // 可选类型: kLidarFront（前部雷达）、kLidarBack（后部雷达）
      agibot::gdk::LidarType lidar_type = agibot::gdk::LidarType::kLidarFront;
      std::this_thread::sleep_for(std::chrono::seconds(1)); // 等待1秒以确保DDS连接建立
      std::shared_ptr<agibot::gdk::PointCloud> pointcloud = std::make_shared<agibot::gdk::PointCloud>();
      lidar.GetLatestPointCloud(lidar_type, 500.0, pointcloud);

      if (pointcloud != nullptr) {
          std::cout << "✅ 时间戳: " << pointcloud->timestamp_ns << std::endl;
          std::cout << "点云尺寸: " << pointcloud->width << " x " << pointcloud->height << std::endl;
          std::cout << "点步长: " << pointcloud->point_step << std::endl;
          std::cout << "行步长: " << pointcloud->row_step << std::endl;
          std::cout << "是否大端序: " << (pointcloud->is_bigendian ? "是" : "否") << std::endl;
          std::cout << "是否密集: " << (pointcloud->is_dense ? "是" : "否") << std::endl;

          // 打印字段信息
          std::cout << "字段数量: " << pointcloud->fields.size() << std::endl;
          for (size_t j = 0; j < pointcloud->fields.size(); ++j) {
              const auto& field = pointcloud->fields[j];
              std::cout << "  字段 " << (j + 1) << ": " << field.name
                      << " (偏移: " << field.offset
                      << ", 类型: " << field.datatype
                      << ", 数量: " << field.count << ")" << std::endl;
          }
      } else {
          std::cout << "未获取到点云数据" << std::endl;
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

#### 2. `GetNearestPointCloud()`

- **功能**：获取指定时间戳附近最近的点云数据
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `lidar_type` | `const LidarType&` | 激光雷达类型枚举值 |
| `timestamp_ns` | `const uint64_t` | 目标时间戳（纳秒） |
| `timeout_ms` | `const float` | 超时时间（毫秒） |
| `pointcloud` | `std::shared_ptr<PointCloud>&` | 输出参数，点云数据指针 |

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`，`pointcloud`参数包含点云数据

- **示例**：

  ```cpp
  #include <iostream>
  #include <chrono>
  #include <thread>
  #include <memory>
  #include "gdk/gdk.h"

  int main() {
      // 初始化GDK系统
      if (agibot::gdk::GDKInit() != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "GDK初始化失败" << std::endl;
          return -1;
      }
      std::cout << "GDK初始化成功" << std::endl;

      agibot::gdk::Lidar lidar;

      // 可选类型: kLidarFront（前部雷达）、kLidarBack（后部雷达）
      agibot::gdk::LidarType lidar_type = agibot::gdk::LidarType::kLidarFront;
      std::this_thread::sleep_for(std::chrono::seconds(1)); // 等待1秒以确保DDS连接建立
      std::shared_ptr<agibot::gdk::PointCloud> pointcloud = std::make_shared<agibot::gdk::PointCloud>();
      lidar.GetLatestPointCloud(lidar_type, 500.0, pointcloud);

      if (pointcloud != nullptr) {
          std::cout << "✅ 时间戳: " << pointcloud->timestamp_ns << std::endl;
          std::cout << "点云尺寸: " << pointcloud->width << " x " << pointcloud->height << std::endl;
          std::cout << "点步长: " << pointcloud->point_step << std::endl;
          std::cout << "行步长: " << pointcloud->row_step << std::endl;
          std::cout << "是否大端序: " << (pointcloud->is_bigendian ? "是" : "否") << std::endl;
          std::cout << "是否密集: " << (pointcloud->is_dense ? "是" : "否") << std::endl;

          // 打印字段信息
          std::cout << "字段数量: " << pointcloud->fields.size() << std::endl;
          for (size_t j = 0; j < pointcloud->fields.size(); ++j) {
              const auto& field = pointcloud->fields[j];
              std::cout << "  字段 " << (j + 1) << ": " << field.name
                      << " (偏移: " << field.offset
                      << ", 类型: " << field.datatype
                      << ", 数量: " << field.count << ")" << std::endl;
          }

          // 查找最近的点云数据
          std::shared_ptr<agibot::gdk::PointCloud> pointcloud_nearest = std::make_shared<agibot::gdk::PointCloud>();
          agibot::gdk::GDKRes res = lidar.GetNearestPointCloud(
              lidar_type,
              pointcloud->timestamp_ns - 1000000000LL, // 往前1秒
              1000.0,
              pointcloud_nearest
          );
          if (res == agibot::gdk::GDKRes::kSuccess && pointcloud_nearest != nullptr) {
              std::cout << "✅ 最近点云数据: " << pointcloud_nearest->timestamp_ns << std::endl;
              std::cout << "点云尺寸: " << pointcloud_nearest->width << " x " << pointcloud_nearest->height << std::endl;
          } else {
              std::cout << "❌ 未找到最近的 Front 雷达数据" << std::endl;
          }
      } else {
          std::cout << "未获取到点云数据" << std::endl;
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

#### 3. `GetLidarFps()`

- **功能**：获取激光雷达数据采集帧率
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `lidar_type` | `const LidarType&` | 激光雷达类型枚举值 |
| `fps` | `float&` | 输出参数，激光雷达帧率（FPS） |

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`，`fps`参数包含帧率值

- **示例**：

  ```cpp
  #include <iostream>
  #include <chrono>
  #include <thread>
  #include "gdk/gdk.h"

  int main() {
      // 初始化GDK系统
      if (agibot::gdk::GDKInit() != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "GDK初始化失败" << std::endl;
          return -1;
      }
      std::cout << "GDK初始化成功" << std::endl;

      agibot::gdk::Lidar lidar;
      std::this_thread::sleep_for(std::chrono::seconds(1)); // 等待1秒以确保DDS连接建立

      agibot::gdk::LidarType lidar_type = agibot::gdk::LidarType::kLidarFront;
      
      float fps;
      if (lidar.GetLidarFps(lidar_type, fps) != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "Failed to get lidar fps" << std::endl;
      } else {
          std::cout << "Lidar fps: " << fps << std::endl;
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

#### 4. `GetLidarLatency()`

- **注意事项**：获取激光雷达数据延迟统计信息前，需要先进行时间同步，否则延迟统计结果不准确
- **功能**：获取激光雷达数据延迟统计信息
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `lidar_type` | `const LidarType&` | 激光雷达类型枚举值 |
| `window_seconds` | `const float` | 统计窗口时间（秒） |
| `latency` | `LatencyStats&` | 输出参数，延迟统计信息 |

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`，`latency`参数包含延迟统计信息

- **LatencyStats结构体说明**：

```cpp
struct LatencyStats {
  double max_latency_ms{0.0};    ///< max latency(ms)
  double avg_latency_ms{0.0};    ///< average latency(ms)
  double p99_latency_ms{0.0};    ///< 99th percentile latency(ms)
  double p999_latency_ms{0.0};   ///< 99.9th percentile latency(ms)
  double p9999_latency_ms{0.0};  ///< 99.99th percentile latency(ms)
};
```

| 成员名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `max_latency_ms` | `double` | 最大延迟 | 毫秒 |
| `avg_latency_ms` | `double` | 平均延迟 | 毫秒 |
| `p99_latency_ms` | `double` | 99分位延迟 | 毫秒 |
| `p999_latency_ms` | `double` | 99.9分位延迟 | 毫秒 |
| `p9999_latency_ms` | `double` | 99.99分位延迟 | 毫秒 |

- **示例**：

  ```cpp
  #include <iostream>
  #include <chrono>
  #include <thread>
  #include "gdk/gdk.h"

  int main() {
      // 初始化GDK系统
      if (agibot::gdk::GDKInit() != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "GDK初始化失败" << std::endl;
          return -1;
      }
      std::cout << "GDK初始化成功" << std::endl;

      agibot::gdk::Lidar lidar;
      std::this_thread::sleep_for(std::chrono::seconds(1)); // 等待1秒以确保DDS连接建立

      agibot::gdk::LidarType lidar_type = agibot::gdk::LidarType::kLidarFront;
      
      agibot::gdk::LatencyStats latency;
      if (lidar.GetLidarLatency(lidar_type, 1.0, latency) != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "Failed to get lidar latency" << std::endl;
      } else {
          std::cout << "Lidar latency stats:" << std::endl;
          std::cout << "  Max latency: " << latency.max_latency_ms << "ms" << std::endl;
          std::cout << "  Average latency: " << latency.avg_latency_ms << "ms" << std::endl;
          std::cout << "  P99 latency: " << latency.p99_latency_ms << "ms" << std::endl;
          std::cout << "  P99.9 latency: " << latency.p999_latency_ms << "ms" << std::endl;
          std::cout << "  P99.99 latency: " << latency.p9999_latency_ms << "ms" << std::endl;
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

#### 5. `CloseLidar()`

- **功能**：关闭激光雷达DDS连接
- **参数**：无
- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`

- **示例**：

  ```cpp
  #include <iostream>
  #include <chrono>
  #include <thread>
  #include "gdk/gdk.h"

  int main() {
      // 初始化GDK系统
      if (agibot::gdk::GDKInit() != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "GDK初始化失败" << std::endl;
          return -1;
      }
      std::cout << "GDK初始化成功" << std::endl;

      agibot::gdk::Lidar lidar;
      std::cout << "Lidar init" << std::endl;

      // 使用激光雷达...
      
      // 关闭激光雷达
      if (lidar.CloseLidar() != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "Failed to close lidar" << std::endl;
      } else {
          std::cout << "Lidar closed successfully" << std::endl;
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

## 使用注意事项

1. **GDK初始化**：使用Lidar功能前必须先调用`agibot::gdk::GDKInit()`初始化GDK系统
2. **GDK释放**：程序结束前必须调用`agibot::gdk::GDKRelease()`释放GDK系统资源
3. **初始化等待**：创建Lidar对象后，建议等待1秒以确保DDS连接建立
4. **超时设置**：根据实际需求设置合适的超时时间，避免长时间阻塞
5. **返回值检查**：使用前请检查GDKRes返回值是否为kSuccess
6. **智能指针管理**：PointCloud对象使用shared_ptr管理，注意生命周期
7. **时间戳精度**：时间戳单位为纳秒，可用于精确的时间同步
8. **点云处理**：点云数据量较大，处理时注意内存使用
9. **雷达选择**：根据应用场景选择合适的雷达类型（前部/后部）
10. **数据解析**：需要根据fields信息正确解析点云数据
11. **坐标系**：注意点云数据的坐标系定义
12. **资源释放**：使用完毕后调用`CloseLidar()`释放资源
13. **错误处理**：始终检查GDKRes返回值，确保操作成功
14. **未实现方法**：`GetLidarFps()`和`GetLidarLatency()`当前未实现，使用时需注意

## 应用场景

- **SLAM建图**：利用点云数据进行同时定位与地图构建
- **障碍物检测**：实时检测环境中的障碍物
- **导航避障**：为机器人导航提供环境感知信息
- **环境建模**：构建3D环境模型
- **目标识别**：结合点云数据进行目标检测和识别
- **路径规划**：基于点云数据规划安全路径
- **数据融合**：与其他传感器数据进行融合，提高感知精度
- **3D重建**：利用点云数据进行3D场景重建
- **距离测量**：精确测量到障碍物的距离
- **安全监控**：监控机器人周围的安全区域
