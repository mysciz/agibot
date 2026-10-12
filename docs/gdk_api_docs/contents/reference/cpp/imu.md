# GDK IMU 接口文档（C++）

## 概述

IMU（惯性测量单元）模块为G02机器人提供了获取实时惯性数据的功能。通过C++接口，开发者可以方便地获取机器人的方向、角速度和线性加速度信息，适用于姿态检测、运动分析、导航等多种场景。

## 接口说明

### Imu 类

该类封装了IMU传感器的主要数据获取接口。

#### 1. `GetLatestImu()`

- **功能**：获取最新的IMU数据
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `imu_type` | `const ImuType&` | IMU类型枚举值 |
| `timeout_ms` | `const float` | 超时时间（毫秒） |
| `imu` | `std::shared_ptr<ImuData>&` | 输出参数，IMU数据指针 |

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`，`imu`参数包含IMU数据

#### ImuData对象详细说明

**ImuData结构体包含以下成员**：

```cpp
struct ImuData {
  Vector3 angular_velocity{};     ///< imu current angular velocity
  Vector3 linear_acceleration{}; ///< imu current linear acceleration
  uint64_t timestamp_ns{0};      ///< imu timestamp(ns)
};
```

| 成员名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `angular_velocity` | `Vector3` | 角速度，机器人在三个轴上的角速度 | 弧度/秒 |
| `linear_acceleration` | `Vector3` | 线性加速度，机器人在三个轴上的线性加速度 | 米/秒² |
| `timestamp_ns` | `uint64_t` | 数据采集的时间戳，精度为纳秒 | 纳秒 |
**Vector3 结构体说明**：

| 成员名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `x` | `double` | X轴分量 |
| `y` | `double` | Y轴分量 |
| `z` | `double` | Z轴分量 |

```cpp
struct Vector3 {
  double x{};
  double y{};
  double z{};
};
```

**IMU类型**：
- `ImuType::kImuFront`: 前部IMU
- `ImuType::kImuBack`: 后部IMU
- `ImuType::kImuChassis`: 底盘IMU

- **示例**：

  ```cpp
  #include <iostream>
  #include <chrono>
  #include <thread>
  #include "gdk/gdk.h"

  int main()
  {
      // 初始化GDK系统
      if (agibot::gdk::GDKInit() != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "GDK初始化失败" << std::endl;
          return -1;
      }
      std::cout << "GDK初始化成功" << std::endl;

      std::cout<< "IMU示例程序" << std::endl;
      agibot::gdk::Imu imu;
      std::this_thread::sleep_for(std::chrono::seconds(1)); // 等待1秒以确保DDS连接建立
      std::shared_ptr<agibot::gdk::ImuData> imu_data;
      imu.GetLatestImu(agibot::gdk::ImuType::kImuChassis, 500.0, imu_data);

      if (imu_data != nullptr) {
          std::cout << "\n--- IMU数据 ---" << std::endl;
          std::cout << "时间戳: " << imu_data->timestamp_ns << std::endl;

          // 角速度
          std::cout << "角速度: x=" << imu_data->angular_velocity.x << ", "
                << "y=" << imu_data->angular_velocity.y << ", "
                << "z=" << imu_data->angular_velocity.z << std::endl;

          // 线性加速度
          std::cout << "线性加速度: x=" << imu_data->linear_acceleration.x << ", "
                << "y=" << imu_data->linear_acceleration.y << ", "
                << "z=" << imu_data->linear_acceleration.z << std::endl;
      } else {
          std::cout << "未收到IMU数据" << std::endl;
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

#### 2. `GetNearestImu()`

- **功能**：获取指定时间戳附近最近的IMU数据
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `imu_type` | `const ImuType&` | IMU类型枚举值 |
| `timestamp_ns` | `const uint64_t` | 目标时间戳（纳秒） |
| `timeout_ms` | `const float` | 超时时间（毫秒） |
| `imu` | `std::shared_ptr<ImuData>&` | 输出参数，IMU数据指针 |

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`，`imu`参数包含IMU数据

- **示例**：

  ```cpp
  #include <iostream>
  #include <iomanip>
  #include <chrono>
  #include <thread>
  #include "gdk/gdk.h"

  int main()
  {
      // 初始化GDK系统
      if (agibot::gdk::GDKInit() != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "GDK初始化失败" << std::endl;
          return -1;
      }
      std::cout << "GDK初始化成功" << std::endl;

      std::cout << "IMU示例程序" << std::endl;
      agibot::gdk::Imu imu;
      std::this_thread::sleep_for(std::chrono::seconds(1)); // 等待1秒以确保DDS连接建立

      agibot::gdk::ImuType imu_type = agibot::gdk::ImuType::kImuChassis;
      std::shared_ptr<agibot::gdk::ImuData> imu_data;
      imu.GetLatestImu(imu_type, 500.0, imu_data);

      if (imu_data != nullptr) {
          std::cout << "\n--- IMU数据 ---" << std::endl;
          std::cout << "时间戳: " << imu_data->timestamp_ns << std::endl;

          // 角速度
          std::cout << "角速度: x=" << imu_data->angular_velocity.x << ", "
                    << "y=" << imu_data->angular_velocity.y << ", "
                    << "z=" << imu_data->angular_velocity.z << std::endl;

          // 线性加速度
          std::cout << "线性加速度: x=" << imu_data->linear_acceleration.x << ", "
                    << "y=" << imu_data->linear_acceleration.y << ", "
                    << "z=" << imu_data->linear_acceleration.z << std::endl;

          // 查找最近的IMU数据
          for (int i = 0; i < 10; ++i) {
              std::shared_ptr<agibot::gdk::ImuData> imu_data_nearest;
              agibot::gdk::GDKRes res = imu.GetNearestImu(
                  imu_type,
                  imu_data->timestamp_ns - 1000000000LL, // 往前1秒
                  1000.0,
                  imu_data_nearest
              );
              if (res == agibot::gdk::GDKRes::kSuccess && imu_data_nearest != nullptr) {
                  std::cout << "✅ 最近IMU数据: " << imu_data_nearest->timestamp_ns << std::endl;
                  std::cout << std::fixed << std::setprecision(4);
                  std::cout << "角速度: x=" << imu_data_nearest->angular_velocity.x
                            << ", y=" << imu_data_nearest->angular_velocity.y
                            << ", z=" << imu_data_nearest->angular_velocity.z << std::endl;
                  std::cout << "线性加速度: x=" << imu_data_nearest->linear_acceleration.x
                            << ", y=" << imu_data_nearest->linear_acceleration.y
                            << ", z=" << imu_data_nearest->linear_acceleration.z << std::endl;
              } else {
                  std::cout << "❌ 未找到最近的 IMU 数据" << std::endl;
              }
              std::this_thread::sleep_for(std::chrono::seconds(1));
          }
      } else {
          std::cout << "未收到IMU数据" << std::endl;
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

#### 3. `GetImuFps()`

- **功能**：获取IMU数据采集帧率
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `imu_type` | `const ImuType&` | IMU类型枚举值 |
| `fps` | `int&` | 输出参数，IMU帧率（FPS） |

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

      agibot::gdk::Imu imu;
      std::this_thread::sleep_for(std::chrono::seconds(1)); // 等待1秒以确保DDS连接建立

      agibot::gdk::ImuType imu_type = agibot::gdk::ImuType::kImuChassis;
      
      float fps;
      if (imu.GetImuFps(imu_type, fps) != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "Failed to get imu fps" << std::endl;
      } else {
          std::cout << "IMU fps: " << fps << std::endl;
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

#### 4. `GetImuLatency()`

- **注意事项**：获取IMU数据延迟统计信息前，需要先进行时间同步，否则延迟统计结果不准确
- **功能**：获取IMU数据延迟统计信息
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `imu_type` | `const ImuType&` | IMU类型枚举值 |
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

      agibot::gdk::Imu imu;
      std::this_thread::sleep_for(std::chrono::seconds(1)); // 等待1秒以确保DDS连接建立

      agibot::gdk::ImuType imu_type = agibot::gdk::ImuType::kImuChassis;
      
      agibot::gdk::LatencyStats latency;
      if (imu.GetImuLatency(imu_type, 1.0, latency) != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "Failed to get imu latency" << std::endl;
      } else {
          std::cout << "IMU latency stats:" << std::endl;
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

#### 5. `CloseImu()`

- **功能**：关闭IMU DDS连接
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

      agibot::gdk::Imu imu;
      std::cout << "IMU init" << std::endl;

      // 使用IMU...
      
      // 关闭IMU
      if (imu.CloseImu() != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "Failed to close imu" << std::endl;
      } else {
          std::cout << "IMU closed successfully" << std::endl;
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

1. **GDK初始化**：使用IMU功能前必须先调用`agibot::gdk::GDKInit()`初始化GDK系统
2. **GDK释放**：程序结束前必须调用`agibot::gdk::GDKRelease()`释放GDK系统资源
3. **初始化等待**：创建Imu对象后，建议等待1秒以确保DDS连接建立
4. **超时设置**：根据实际需求设置合适的超时时间，避免长时间阻塞
5. **返回值检查**：使用前请检查GDKRes返回值是否为kSuccess
6. **智能指针管理**：ImuData对象使用shared_ptr管理，注意生命周期
7. **时间戳精度**：时间戳单位为纳秒，可用于精确的时间同步
8. **数据融合**：IMU数据通常需要与其他传感器数据进行融合以提高精度
9. **资源释放**：使用完毕后调用`CloseImu()`释放资源
10. **错误处理**：始终检查GDKRes返回值，确保操作成功
11. **未实现方法**：`GetImuFps()`和`GetImuLatency()`当前未实现，使用时需注意

## 应用场景

- **运动分析**：利用角速度和线性加速度分析机器人运动状态
- **导航定位**：结合其他传感器进行机器人定位和导航
- **平衡控制**：用于机器人的平衡和稳定性控制
- **数据融合**：与其他传感器数据进行卡尔曼滤波等融合算法
- **运动预测**：基于历史数据预测机器人运动轨迹
- **异常检测**：检测机器人的异常运动状态
- **校准补偿**：进行传感器校准和误差补偿
- **振动监测**：监测机器人的振动和冲击情况
