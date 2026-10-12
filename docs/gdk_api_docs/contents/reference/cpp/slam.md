# GDK SLAM 接口文档（C++）

## 概述

SLAM（Simultaneous Localization and Mapping，同时定位与地图构建）模块为G02机器人提供了实时建图和定位功能。通过C++接口，开发者可以方便地实现机器人的环境感知、地图构建、位置估计等功能，适用于自主导航、环境建模、定位服务等多种场景。

## 接口说明

### Slam 类

该类封装了SLAM系统的主要功能接口。

#### 1. `GetSlamState()`

- **功能**：获取SLAM系统当前状态
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `state` | `uint32_t&` | 输出参数，SLAM状态码 |

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`，`state`参数包含SLAM状态信息 （1：开始建图 2：停止建图 0：取消建图）

- **示例**：

  ```cpp
  #include "gdk/gdk.h"
  #include <iostream>
  #include <chrono>
  #include <thread>
  using namespace agibot::gdk;

  int main() {
      // 初始化GDK系统
      if (agibot::gdk::GDKInit() != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "GDK初始化失败" << std::endl;
          return -1;
      }
      std::cout << "GDK初始化成功" << std::endl;

      Slam slam;
      std::this_thread::sleep_for(std::chrono::seconds(1)); // 等待1秒以确保DDS连接建立
      uint32_t state;
      GDKRes result = slam.GetSlamState(state);
      
      if (result == GDKRes::kSuccess) {
          std::cout << "SLAM状态: " << state << std::endl;
      } else {
          std::cout << "获取SLAM状态失败" << std::endl;
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

#### 2. `StartMapping()`

- **功能**：开始建图
- **参数**：无

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`

- **示例**：

  ```cpp
  #include "gdk/gdk.h"
  #include <iostream>
  #include <unistd.h>
  #include <chrono>
  #include <thread>
  using namespace agibot::gdk;

  int main() {
      // 初始化GDK系统
      if (agibot::gdk::GDKInit() != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "GDK初始化失败" << std::endl;
          return -1;
      }
      std::cout << "GDK初始化成功" << std::endl;

      Slam slam;
      std::this_thread::sleep_for(std::chrono::seconds(1)); // 等待1秒以确保DDS连接建立
      // 开始建图
      GDKRes result = slam.StartMapping();
      
      if (result == GDKRes::kSuccess) {
          std::cout << "开始建图成功" << std::endl;
          
          // 检查建图状态
          sleep(2);
          uint32_t state;
          result = slam.GetSlamState(state);
          if (result == GDKRes::kSuccess) {
              std::cout << "建图状态: " << state << std::endl;
          }
      } else {
          std::cout << "开始建图失败" << std::endl;
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

#### 3. `StopMapping()`

- **功能**：停止且保存建图
- **参数**：无

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`

- **示例**：

  ```cpp
  #include "gdk/gdk.h"
  #include <iostream>
  #include <unistd.h>
  #include <chrono>
  #include <thread>
  using namespace agibot::gdk;

  int main() {
      // 初始化GDK系统
      if (agibot::gdk::GDKInit() != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "GDK初始化失败" << std::endl;
          return -1;
      }
      std::cout << "GDK初始化成功" << std::endl;

      Slam slam;
      std::this_thread::sleep_for(std::chrono::seconds(1)); // 等待1秒以确保DDS连接建立
      // 停止建图
      GDKRes result = slam.StopMapping();
      
      if (result == GDKRes::kSuccess) {
          std::cout << "停止建图成功" << std::endl;
          
          // 检查建图状态
          sleep(2);
          uint32_t state;
          result = slam.GetSlamState(state);
          if (result == GDKRes::kSuccess) {
              std::cout << "建图状态: " << state << std::endl;
          }
      } else {
          std::cout << "停止建图失败" << std::endl;
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

#### 4. `CancelMapping()`

- **功能**：取消建图
- **参数**：无

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`

- **示例**：

  ```cpp
  #include "gdk/gdk.h"
  #include <iostream>
  #include <unistd.h>
  #include <chrono>
  #include <thread>
  using namespace agibot::gdk;

  int main() {
      // 初始化GDK系统
      if (agibot::gdk::GDKInit() != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "GDK初始化失败" << std::endl;
          return -1;
      }
      std::cout << "GDK初始化成功" << std::endl;

      Slam slam;
      std::this_thread::sleep_for(std::chrono::seconds(1)); // 等待1秒以确保DDS连接建立
      // 取消建图
      GDKRes result = slam.CancelMapping();
      
      if (result == GDKRes::kSuccess) {
          std::cout << "取消建图成功" << std::endl;
          
          // 检查建图状态
          sleep(2);
          uint32_t state;
          result = slam.GetSlamState(state);
          if (result == GDKRes::kSuccess) {
              std::cout << "建图状态: " << state << std::endl;
          }
      } else {
          std::cout << "取消建图失败" << std::endl;
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

#### 5. `GetOdomInfo()`

- **功能**：获取里程计信息
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `odom_info` | `OdomInfo&` | 输出参数，里程计信息对象 |

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`，`odom_info`参数包含里程计信息

#### OdomInfo对象详细说明

**OdomInfo结构体包含以下成员**：

| 成员名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `pose` | `PoseWithCovariance` | 机器人当前位姿（带协方差） | 位姿 |
| `twist` | `TwistWithCovariance` | 机器人当前速度（带协方差） | 速度 |
| `is_stationary` | `bool` | 机器人是否静止 | 布尔值 |
| `is_sliping` | `bool` | 机器人是否打滑 | 布尔值 |
| `loc_confidence` | `int32_t` | 定位置信度 | 无单位 |
| `loc_state` | `int32_t` | 定位状态 | 无单位 |
| `velocity` | `Vector3` | 机器人当前速度 | 米/秒 |
| `velocity_body` | `Vector3` | 机器人本体速度 | 米/秒 |
| `acceleration` | `Vector3` | 机器人当前加速度 | 米/秒² |
| `ang_vel` | `Vector3` | 机器人当前角速度 | 弧度/秒 |
| `orientation_euler` | `Vector3` | 机器人当前欧拉角 | 弧度 |

 ```cpp
 struct OdomInfo {
   PoseWithCovariance pose{};    ///< robot current pose
   TwistWithCovariance twist{};  ///< robot current twist
   bool is_stationary{};         ///< robot if stationary
   bool is_sliping{};            ///< robot if slipping
   int32_t loc_confidence{};     ///< robot location confidence
   int32_t loc_state{};          ///< robot location state
   Vector3 velocity{};           ///< robot current velocity
   Vector3 velocity_body{};      ///< robot current body velocity
   Vector3 acceleration{};       ///< robot current acceleration
   Vector3 ang_vel{};            ///< robot current angular velocity
   Vector3 orientation_euler{};  ///< robot current orientation euler
 };
 ```
**PoseWithCovariance结构体**：

| 成员名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `pose` | `Pose` | 位姿信息 |
| `covariance` | `std::vector<double>` | 协方差矩阵 |

 ```cpp
 struct PoseWithCovariance {
   Pose pose{};
   std::vector<double> covariance{};
 };
 ```

**TwistWithCovariance结构体**：

| 成员名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `twist` | `Twist` | 速度信息 |
| `covariance` | `std::vector<double>` | 协方差矩阵 |

 ```cpp
 struct TwistWithCovariance {
   Twist twist{};
   std::vector<double> covariance{};
 };
 ```

**Pose结构体**：

| 成员名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `position` | `Position` | 位置信息 |
| `orientation` | `Orientation` | 方向信息 |

 ```cpp
 struct Pose {
   Position position{};
   Orientation orientation{};
 };
 ```

**Position结构体**：

| 成员名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `x` | `double` | X坐标 | 米 |
| `y` | `double` | Y坐标 | 米 |
| `z` | `double` | Z坐标 | 米 |

**Orientation结构体**：

| 成员名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `x` | `double` | 四元数X分量 | 无单位 |
| `y` | `double` | 四元数Y分量 | 无单位 |
| `z` | `double` | 四元数Z分量 | 无单位 |
| `w` | `double` | 四元数W分量 | 无单位 |

**Twist结构体**：

| 成员名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `linear` | `Vector3` | 线速度 |
| `angular` | `Vector3` | 角速度 |

 ```cpp
 struct Twist {minear{};   ///< linear velocity (m/s)
   Vector3 angular{};  ///< angular velocity (rad/s)
 };
 ```

**Vector3结构体**：

| 成员名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `x` | `double` | X轴分量 | 米/秒或弧度/秒 |
| `y` | `double` | Y轴分量 | 米/秒或弧度/秒 |
| `z` | `double` | Z轴分量 | 米/秒或弧度/秒 |

- **示例**：

  ```cpp
    #include <chrono>
    #include <iostream>
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

        agibot::gdk::Slam slam;
        std::cout << "Slam init" << std::endl;
        std::this_thread::sleep_for(std::chrono::seconds(2)); // 等待slam初始化完成

        slam.StartMapping();
        std::cout << "Start mapping" << std::endl;
        for(int i = 0; i < 10; i++)
        {
            agibot::gdk::OdomInfo odom;
            if (slam.GetOdomInfo(odom) != agibot::gdk::GDKRes::kSuccess) {
                std::cout << "Failed to get odom info" << std::endl;
            } else {
                std::cout << "pose: (" << odom.pose.pose.position.x << ", " << odom.pose.pose.position.y << ", " << odom.pose.pose.position.z << ")" << std::endl;
                std::cout << "orientation (quaternion): x=" << odom.pose.pose.orientation.x 
                        << ", y=" << odom.pose.pose.orientation.y 
                        << ", z=" << odom.pose.pose.orientation.z 
                        << ", w=" << odom.pose.pose.orientation.w << std::endl;
            }
            std::this_thread::sleep_for(std::chrono::seconds(1));
        }
        slam.StopMapping();

        // 释放GDK系统资源
        if (agibot::gdk::GDKRelease() != agibot::gdk::GDKRes::kSuccess) {
            std::cout << "GDK释放失败" << std::endl;
            return -1;
        }
        std::cout << "GDK释放成功" << std::endl;
        
        return 0;
    }
  ```

#### 6. `RecordSpecLoc()`

- **功能**：记录当前位置为特定位置
- **参数**：无

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`

- **示例**：

  ```cpp
  #include "gdk/gdk.h"
  #include <iostream>
  #include <chrono>
  #include <thread>
  using namespace agibot::gdk;

  int main() {
      // 初始化GDK系统
      if (agibot::gdk::GDKInit() != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "GDK初始化失败" << std::endl;
          return -1;
      }
      std::cout << "GDK初始化成功" << std::endl;

      Slam slam;
      std::this_thread::sleep_for(std::chrono::seconds(1)); // 等待1秒以确保DDS连接建立
      GDKRes result = slam.RecordSpecLoc();
      
      if (result == GDKRes::kSuccess) {
          std::cout << "记录特定位置成功" << std::endl;
      } else {
          std::cout << "记录特定位置失败" << std::endl;
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

#### 7. `GetCurrPose()`

- **功能**：获取机器人当前位置
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `pose` | `Pose&` | 输出参数，机器人当前位姿 |

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`，`pose`参数包含机器人当前位姿

- **示例**：

  ```cpp
  #include "gdk/gdk.h"
  #include <iostream>
  #include <chrono>
  #include <thread>
  using namespace agibot::gdk;

  int main() {
      // 初始化GDK系统
      if (agibot::gdk::GDKInit() != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "GDK初始化失败" << std::endl;
          return -1;
      }
      std::cout << "GDK初始化成功" << std::endl;

      Slam slam;
      std::this_thread::sleep_for(std::chrono::seconds(1)); // 等待1秒以确保DDS连接建立
      
      Pose current_pose;
      GDKRes result = slam.GetCurrPose(current_pose);
      
      if (result == GDKRes::kSuccess) {
          std::cout << "当前位置: (" << current_pose.position.x 
                    << ", " << current_pose.position.y 
                    << ", " << current_pose.position.z << ")" << std::endl;
          std::cout << "当前方向: x=" << current_pose.orientation.x 
                    << ", y=" << current_pose.orientation.y 
                    << ", z=" << current_pose.orientation.z 
                    << ", w=" << current_pose.orientation.w << std::endl;
      } else {
          std::cout << "获取当前位置失败" << std::endl;
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

#### 8. 完整使用示例

- **功能**：演示SLAM模块的完整使用流程
- **示例**：

  ```cpp
    #include <chrono>
    #include <iostream>
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

        agibot::gdk::Slam slam;
        agibot::gdk::Map map;
        std::cout << "Slam init" << std::endl;
        std::this_thread::sleep_for(std::chrono::seconds(2)); // 等待slam初始化完成

        slam.StartMapping();
        std::cout << "Start mapping" << std::endl;
        for(int i = 0; i < 10; i++)
        {
            agibot::gdk::OdomInfo odom;
            if (slam.GetOdomInfo(odom) != agibot::gdk::GDKRes::kSuccess) {
                std::cout << "Failed to get odom info" << std::endl;
            } else {
                std::cout << "pose: (" << odom.pose.pose.position.x << ", " << odom.pose.pose.position.y << ", " << odom.pose.pose.position.z << ")" << std::endl;
                std::cout << "orientation (quaternion): x=" << odom.pose.pose.orientation.x 
                        << ", y=" << odom.pose.pose.orientation.y 
                        << ", z=" << odom.pose.pose.orientation.z 
                        << ", w=" << odom.pose.pose.orientation.w << std::endl;
            }
            uint32_t state;
            if (slam.GetSlamState(state) != agibot::gdk::GDKRes::kSuccess) {
                std::cout << "Failed to get slam state" << std::endl;
            } else {
                std::cout << "slam state: " << state << std::endl;
            }

            std::this_thread::sleep_for(std::chrono::seconds(1));
        }
        agibot::gdk::MapName map_name;
        map.GetCurrMap(map_name);
        std::cout << "Get current map: " << map_name.id << std::endl;

        std::vector<agibot::gdk::MapName> map_names;
        map.GetAllMap(map_names);
        for (const auto& name : map_names) {
            std::cout << "Map: " << name.id << ", " << name.name << ", is current: " << name.is_curr_map << std::endl;
        }
        slam.StopMapping();

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

1. **GDK初始化**：使用SLAM功能前必须先调用`agibot::gdk::GDKInit()`初始化GDK系统
2. **GDK释放**：程序结束前必须调用`agibot::gdk::GDKRelease()`释放GDK系统资源
3. **初始化等待**：创建Slam对象后，建议等待1秒以确保DDS连接建立
4. **建图顺序**：建议先开始建图，再进行其他操作
5. **状态检查**：操作前后建议检查SLAM状态确保操作成功
6. **里程计信息**：获取里程计信息时确保SLAM或PNC正在运行
7. **重定位**：全局重定位需要在地图构建完成后进行
8. **资源管理**：注意SLAM系统的资源使用，避免过度请求
9. **错误处理**：始终检查GDKRes返回值，确保操作成功

## 应用场景

- **环境建图**：构建机器人工作环境的地图
- **实时定位**：获取机器人在环境中的实时位置
- **导航支持**：为导航系统提供定位和地图数据
- **环境建模**：建立环境的空间模型
- **位置记录**：记录和标记重要位置点
- **多地图管理**：支持多个环境的地图构建和管理
