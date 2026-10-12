# GDK UltrasonicRadar 接口文档（C++）

## 概述

UltrasonicRadar（超声波雷达）模块为G02机器人提供了获取实时超声波雷达数据的功能。通过C++接口，开发者可以方便地获取机器人的障碍物检测数据，适用于避障、导航、安全检测、近距离障碍物感知等多种场景。

## 接口说明

### UltrasonicRadar 类

该类封装了超声波雷达传感器的主要数据获取接口。

#### 1. `GetLatestUltrasonicRadar()`

- **功能**：获取最新的超声波雷达数据
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `ultrasonic_radar` | `std::shared_ptr<UltrasonicRadars>&` | 输出参数，超声波雷达数据指针 |

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`，`ultrasonic_radar`参数包含超声波雷达数据

#### UltrasonicRadars对象详细说明

**UltrasonicRadars结构体包含以下成员**：

| 成员名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `timestamp_ns` | `uint64_t` | 超声波雷达数据采集的时间戳（底盘传感器时间戳） | 纳秒 |
| `ultrasonic_radar_datas` | `std::vector<UltrasonicRadarData>` | 超声波雷达数据列表 | 无单位 |

```cpp
struct UltrasonicRadars{
  uint64_t timestamp_ns{0};  ///< timestamp in nanoseconds
  std::vector<UltrasonicRadarData> ultrasonic_radar_datas;  ///< ultrasonic radar datas
};
```

**ultrasonic_radar_datas (雷达数据列表)**：

每个`UltrasonicRadarData`包含以下属性：

| 成员名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `id` | `uint32_t` | 超声波雷达ID | 无 |
| `distance_mm` | `uint32_t` | 检测到的距离 | 毫米 |
| `fault_state` | `uint8_t` | 故障状态（0表示正常，非0表示存在故障） | 无 |

```cpp
struct UltrasonicRadarData {
  uint32_t id{};           ///< ultrasonic_radar_id
  uint32_t distance_mm{};  ///< distance in millimeters
  uint8_t fault_state{};  ///< fault state
};
```

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

      agibot::gdk::UltrasonicRadar radar;
      std::this_thread::sleep_for(std::chrono::seconds(1)); // 等待1秒以确保DDS连接建立

      std::shared_ptr<agibot::gdk::UltrasonicRadars> ultrasonic_radar;
      auto res = radar.GetLatestUltrasonicRadar(ultrasonic_radar);

      if (res == agibot::gdk::GDKRes::kSuccess && ultrasonic_radar != nullptr) {
          std::cout << "✅ 时间戳: " << ultrasonic_radar->timestamp_ns << std::endl;
          std::cout << "超声波雷达数量: " << ultrasonic_radar->ultrasonic_radar_datas.size() << std::endl;

          for (const auto& data : ultrasonic_radar->ultrasonic_radar_datas) {
              std::cout << "  雷达[" << data.id << "]: "
                        << "距离=" << data.distance_mm << " mm, "
                        << "故障状态=" << static_cast<int>(data.fault_state) << std::endl;
          }
      } else {
          std::cout << "未获取到超声波雷达数据" << std::endl;
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

#### 2. `GetNearestUltrasonicRadar()`

- **功能**：获取指定时间戳附近最近的超声波雷达数据
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `timestamp_ns` | `const uint64_t` | 目标时间戳（纳秒） |
| `ultrasonic_radar` | `std::shared_ptr<UltrasonicRadars>&` | 输出参数，超声波雷达数据指针 |

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`，`ultrasonic_radar`参数包含超声波雷达数据

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

      agibot::gdk::UltrasonicRadar radar;
      std::this_thread::sleep_for(std::chrono::seconds(1)); // 等待1秒以确保DDS连接建立

      // 先获取最新数据
      std::shared_ptr<agibot::gdk::UltrasonicRadars> latest_radar;
      radar.GetLatestUltrasonicRadar(latest_radar);

      if (latest_radar != nullptr) {
          std::cout << "✅ 最新数据时间戳: " << latest_radar->timestamp_ns << std::endl;

          // 查找最近的数据（往前1秒）
          std::shared_ptr<agibot::gdk::UltrasonicRadars> nearest_radar;
          agibot::gdk::GDKRes res = radar.GetNearestUltrasonicRadar(
              latest_radar->timestamp_ns - 1000000000LL, // 往前1秒
              nearest_radar
          );
          if (res == agibot::gdk::GDKRes::kSuccess && nearest_radar != nullptr) {
              std::cout << "✅ 最近数据时间戳: " << nearest_radar->timestamp_ns << std::endl;
              std::cout << "时间差: " << (nearest_radar->timestamp_ns > latest_radar->timestamp_ns - 1000000000LL ?
                                            nearest_radar->timestamp_ns - (latest_radar->timestamp_ns - 1000000000LL) :
                                            (latest_radar->timestamp_ns - 1000000000LL) - nearest_radar->timestamp_ns)
                        << " ns" << std::endl;
              std::cout << "超声波雷达数量: " << nearest_radar->ultrasonic_radar_datas.size() << std::endl;
          } else {
              std::cout << "❌ 未找到最近的超声波雷达数据" << std::endl;
          }
      } else {
          std::cout << "未获取到超声波雷达数据" << std::endl;
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

#### 3. `GetUltrasonicRadarFps()`

- **功能**：获取超声波雷达数据采集帧率
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `fps` | `float&` | 输出参数，超声波雷达帧率（FPS） |

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

      agibot::gdk::UltrasonicRadar radar;
      std::this_thread::sleep_for(std::chrono::seconds(2)); // 等待2秒让数据积累

      float fps;
      if (radar.GetUltrasonicRadarFps(fps) != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "获取帧率失败" << std::endl;
      } else {
          std::cout << "超声波雷达帧率: " << fps << " fps" << std::endl;
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

#### 4. `GetUltrasonicRadarLatency()`

- **功能**：获取超声波雷达数据延迟统计信息
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
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

      agibot::gdk::UltrasonicRadar radar;
      std::this_thread::sleep_for(std::chrono::seconds(1)); // 等待1秒以确保DDS连接建立

      // 等待一段时间收集数据
      std::this_thread::sleep_for(std::chrono::seconds(10));

      agibot::gdk::LatencyStats latency;
      if (radar.GetUltrasonicRadarLatency(10.0, latency) != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "获取延迟统计失败" << std::endl;
      } else {
          std::cout << "超声波雷达延迟统计:" << std::endl;
          std::cout << "  最大延迟: " << latency.max_latency_ms << "ms" << std::endl;
          std::cout << "  平均延迟: " << latency.avg_latency_ms << "ms" << std::endl;
          std::cout << "  P99延迟: " << latency.p99_latency_ms << "ms" << std::endl;
          std::cout << "  P99.9延迟: " << latency.p999_latency_ms << "ms" << std::endl;
          std::cout << "  P99.99延迟: " << latency.p9999_latency_ms << "ms" << std::endl;
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

#### 5. `Close()`

- **功能**：关闭超声波雷达DDS连接
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

      agibot::gdk::UltrasonicRadar radar;
      std::cout << "UltrasonicRadar init" << std::endl;

      // 使用超声波雷达...

      // 关闭超声波雷达
      if (radar.Close() != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "关闭超声波雷达失败" << std::endl;
      } else {
          std::cout << "超声波雷达关闭成功" << std::endl;
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

1. **GDK初始化**：使用UltrasonicRadar功能前必须先调用`agibot::gdk::GDKInit()`初始化GDK系统
2. **GDK释放**：程序结束前必须调用`agibot::gdk::GDKRelease()`释放GDK系统资源
3. **初始化等待**：创建UltrasonicRadar对象后，建议等待1秒以确保DDS连接建立
4. **返回值检查**：使用前请检查GDKRes返回值是否为kSuccess
5. **智能指针管理**：UltrasonicRadars对象使用shared_ptr管理，注意生命周期
6. **时间戳精度**：时间戳单位为纳秒，是底盘传感器的时间戳，可用于精确的时间同步
7. **距离单位**：距离单位为毫米（mm），使用时注意单位转换
8. **故障状态**：`fault_state`为0表示正常，非0值表示存在故障，使用时需要检查
9. **数据获取**：`GetLatestUltrasonicRadar()`返回当前最新数据，如果没有新数据可能返回失败
10. **时间戳查找**：`GetNearestUltrasonicRadar()`根据时间戳查找最接近的数据，如果时间戳超出范围可能返回失败
11. **帧率统计**：`GetUltrasonicRadarFps()`需要等待一段时间（建议至少2秒）让数据积累后才能获得准确的帧率
12. **延迟统计**：`GetUltrasonicRadarLatency()`需要等待一段时间（建议至少10秒）让数据积累后才能获得准确的统计信息
13. **资源释放**：使用完毕后调用`Close()`释放资源
14. **错误处理**：始终检查GDKRes返回值，确保操作成功

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
