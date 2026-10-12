# GDK PNC 接口文档（C++）

## 概述

PNC（Planning and Control，规划与控制）模块为G02机器人提供了路径规划和导航控制功能。通过C++接口，开发者可以方便地实现机器人的自主导航、路径规划、任务状态管理等功能，适用于自主导航、路径规划、任务调度等多种场景。

## 接口说明

### Pnc 类

该类封装了机器人路径规划和导航控制的主要接口。

#### 1. `GetTaskState()`

- **功能**：获取当前任务状态
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `task_state` | `PNCTaskState&` | 输出参数，任务状态信息对象 |

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`，`task_state`参数包含任务状态信息

#### PNCTaskState对象详细说明

**PNCTaskState结构体包含以下成员**：

| 成员名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `id` | `uint32_t` | 任务ID | 无单位 |
| `state` | `uint32_t` | 任务状态码 | 无单位 |
| `type` | `uint32_t` | 任务类型 | 无单位 |
| `message` | `std::string` | 状态描述信息 | 字符串 |

**任务状态码说明**：
- `0`: 空闲
- `1`: 启动中
- `2`: 运行中
- `3`: 暂停中
- `4`: 已暂停
- `5`: 恢复中
- `6`: 取消中
- `7`: 已取消
- `8`: 失败
- `9`: 成功

**任务类型说明**：
- `0`: 空闲
- `1`: 正常导航
- `2`: 远程控制

- **示例**：

  ```cpp
  #include "gdk/gdk.h"
  #include <iostream>
  #include <chrono>
  #include <thread>
  using namespace agibot::gdk;

  int main() {
      Pnc pnc;
      std::this_thread::sleep_for(std::chrono::seconds(1)); // 等待1秒以确保DDS连接建立
      PNCTaskState task_state;
      GDKRes result = pnc.GetTaskState(task_state);

      if (result == GDKRes::kSuccess) {
        std::cout << "PNC任务状态: " << task_state.state << std::endl;
        std::cout << "PNC任务ID: " << task_state.id << std::endl;
        std::cout << "PNC任务内容: " << task_state.message << std::endl;
        std::cout << "PNC任务种类: " << task_state.type << std::endl;
      } else {
        std::cout << "获取任务状态失败" << std::endl;
      }

      return 0;
  }
  ```

#### 2. `NormalNavi()`

- **功能**：执行正常导航到指定目标点, 执行之前需要在G02 Pad上进行重定位
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `navi_req` | `const NaviReq&` | 导航请求对象 |

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`

#### NaviReq对象详细说明

**NaviReq结构体包含以下成员**：

| 成员名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `target` | `Pose` | 目标位姿 | 位姿 |
| `timestamp_ns` | `uint64_t` | 导航时间戳 | 纳秒 |

**Pose结构体**：

| 成员名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `position` | `Position` | 位置信息 |
| `orientation` | `Orientation` | 方向信息 |

**Position结构体**：

| 成员名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `x` | `double` | 目标位置X坐标 | 米 |
| `y` | `double` | 目标位置Y坐标 | 米 |
| `z` | `double` | 目标位置Z坐标 | 米 |

**Orientation结构体**：

| 成员名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `x` | `double` | 目标方向四元数X分量 | 无单位 |
| `y` | `double` | 目标方向四元数Y分量 | 无单位 |
| `z` | `double` | 目标方向四元数Z分量 | 无单位 |
| `w` | `double` | 目标方向四元数W分量 | 无单位 |

- **示例**：

  ```cpp
  #include "gdk/gdk.h"
  #include <iostream>
  #include <chrono>
  #include <thread>
  using namespace agibot::gdk;

  int main() {
      Pnc pnc;
      std::this_thread::sleep_for(std::chrono::seconds(1)); // 等待1秒以确保DDS连接建立
      NaviReq navi_req;
      navi_req.target.position.x = 2.0;  // 目标X坐标
      navi_req.target.position.y = 3.0;  // 目标Y坐标
      navi_req.target.position.z = 0.0;  // 目标Z坐标
      navi_req.target.orientation.x = 0.0;  // 目标方向四元数X
      navi_req.target.orientation.y = 0.0;  // 目标方向四元数Y
      navi_req.target.orientation.z = 0.0;  // 目标方向四元数Z
      navi_req.target.orientation.w = 1.0;  // 目标方向四元数W
      navi_req.timestamp_ns = 0;  // 时间戳

      GDKRes result = pnc.NormalNavi(navi_req);

      if (result == GDKRes::kSuccess) {
          std::cout << "正常导航启动成功" << std::endl;
      } else {
          std::cout << "正常导航启动失败" << std::endl;
      }

      return 0;
  }
  ```

#### 3. `HighPrecisionNavi()`

- **功能**：执行高精度导航到指定目标点, 执行之前需要在G02 Pad上进行重定位
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `navi_req` | `const NaviReq&` | 导航请求对象 |

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`

- **示例**：

  ```cpp
  #include "gdk/gdk.h"
  #include <iostream>

  using namespace agibot::gdk;

  int main() {
      Pnc pnc;

      NaviReq navi_req;
      navi_req.target.position.x = 1.5;  // 目标X坐标
      navi_req.target.position.y = 2.5;  // 目标Y坐标
      navi_req.target.position.z = 0.0;  // 目标Z坐标
      navi_req.target.orientation.x = 0.0;  // 目标方向四元数X
      navi_req.target.orientation.y = 0.0;  // 目标方向四元数Y
      navi_req.target.orientation.z = 0.0;  // 目标方向四元数Z
      navi_req.target.orientation.w = 1.0;  // 目标方向四元数W
      navi_req.timestamp_ns = 0;  // 时间戳

      GDKRes result = pnc.HighPrecisionNavi(navi_req);

      if (result == GDKRes::kSuccess) {
          std::cout << "高精度导航启动成功" << std::endl;
      } else {
          std::cout << "高精度导航启动失败" << std::endl;
      }

      return 0;
  }
  ```

#### 4. `RelativeMove()`

- **功能**：执行小范围平移, 简单停障，无避障，执行之前需要在G02 Pad上进行重定位
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `navi_req` | `const NaviReq&` | 导航请求对象 |

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`

- **示例**：

  ```cpp
  #include "gdk/gdk.h"
  #include <iostream>

  using namespace agibot::gdk;

  int main() {
      Pnc pnc;

      NaviReq navi_req;
      navi_req.target.position.x = 0.5;  // 相对X移动距离
      navi_req.target.position.y = 0.0;  // 相对Y移动距离
      navi_req.target.position.z = 0.0;  // 相对Z移动距离
      navi_req.target.orientation.x = 0.0;  // 相对旋转X
      navi_req.target.orientation.y = 0.0;  // 相对旋转Y
      navi_req.target.orientation.z = 0.0;  // 相对旋转Z
      navi_req.target.orientation.w = 1.0;  // 相对旋转W
      navi_req.timestamp_ns = 0;  // 时间戳

      GDKRes result = pnc.RelativeMove(navi_req);

      if (result == GDKRes::kSuccess) {
          std::cout << "相对移动启动成功" << std::endl;
      } else {
          std::cout << "相对移动启动失败" << std::endl;
      }

      return 0;
  }
  ```

#### 5. `CancelTask()`

- **功能**：取消指定ID的导航任务
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `task_id` | `uint32_t` | 要取消的任务ID |

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`

- **示例**：

  ```cpp
  #include "gdk/gdk.h"
  #include <iostream>

  using namespace agibot::gdk;

  int main() {
      Pnc pnc;
      std::this_thread::sleep_for(std::chrono::seconds(1));

      // 先获取当前任务状态以获取任务ID
      PNCTaskState task_state;
      if (pnc.GetTaskState(task_state) == GDKRes::kSuccess) {
          uint32_t task_id = task_state.id;
          GDKRes result = pnc.CancelTask(task_id);

          if (result == GDKRes::kSuccess) {
              std::cout << "任务取消成功" << std::endl;
          } else {
              std::cout << "任务取消失败" << std::endl;
          }
      }

      return 0;
  }
  ```

#### 6. `PauseTask()`

- **功能**：暂停指定ID的导航任务
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `task_id` | `uint32_t` | 要暂停的任务ID |

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`

- **示例**：

  ```cpp
  #include "gdk/gdk.h"
  #include <iostream>
  #include <thread>
  #include <chrono>

  using namespace agibot::gdk;

  int main() {
      Pnc pnc;
      std::this_thread::sleep_for(std::chrono::seconds(1));

      // 先获取当前任务状态以获取任务ID
      PNCTaskState task_state;
      if (pnc.GetTaskState(task_state) == GDKRes::kSuccess) {
          uint32_t task_id = task_state.id;
          GDKRes result = pnc.PauseTask(task_id);

          if (result == GDKRes::kSuccess) {
              std::cout << "任务暂停成功" << std::endl;
          } else {
              std::cout << "任务暂停失败" << std::endl;
          }
      }

      return 0;
  }
  ```

#### 7. `ResumeTask()`

- **功能**：恢复指定ID的导航任务
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `task_id` | `uint32_t` | 要恢复的任务ID |

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`

- **示例**：

  ```cpp
  #include "gdk/gdk.h"
  #include <iostream>
  #include <thread>
  #include <chrono>

  using namespace agibot::gdk;

  int main() {
      Pnc pnc;
      std::this_thread::sleep_for(std::chrono::seconds(1));

      // 先获取当前任务状态以获取任务ID
      PNCTaskState task_state;
      if (pnc.GetTaskState(task_state) == GDKRes::kSuccess) {
          uint32_t task_id = task_state.id;
          GDKRes result = pnc.ResumeTask(task_id);

          if (result == GDKRes::kSuccess) {
              std::cout << "任务恢复成功" << std::endl;
          } else {
              std::cout << "任务恢复失败" << std::endl;
          }
      }

      return 0;
  }
  ```

#### 8. `RequestChassisControl()`


- **功能**：请求底盘控制权限，用于远程控制模式
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `control_mode` | `int32_t` | 控制请求：0 |

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`

**控制模式说明**：
- **阿克曼模式**：适用于前轮转向的车辆运动学模型，通过线速度(`linear.x`)和角速度(`angular.z`)控制
- **蟹行模式**：支持全向移动，通过`linear.x`和`linear.y`分别控制前后和左右移动

- **示例**：

  ```cpp
  #include "gdk/gdk.h"
  #include <iostream>
  #include <thread>
  #include <chrono>

  using namespace agibot::gdk;

  int main() {
      Pnc pnc;
      std::this_thread::sleep_for(std::chrono::seconds(1));

      // 请求远程控制
      GDKRes res = pnc.RequestChassisControl(0);
      if (res == GDKRes::kSuccess) {
          std::cout << "远程控制请求成功" << std::endl;
      } else {
          std::cout << "控制请求失败" << std::endl;
          return 1;
      }

      // 等待控制权限生效
      std::this_thread::sleep_for(std::chrono::milliseconds(500));

      // 现在可以使用 MoveChassis() 控制底盘
      Twist twist;
      twist.linear.x = 0.3;
      twist.angular.z = 0.0;
      pnc.MoveChassis(twist);

      return 0;
  }
  ```

#### 9. `MoveChassis()`

- **功能**：移动底盘，用于远程控制模式下的底盘运动控制
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `twist` | `const Twist&` | 速度指令对象，包含线速度和角速度 |

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`

#### Twist对象详细说明

**Twist结构体包含以下成员**：

| 成员名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `linear` | `Vector3` | 线速度向量 | 米/秒 (m/s) |
| `angular` | `Vector3` | 角速度向量 | 弧度/秒 (rad/s) |

**Vector3结构体**：

| 成员名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `x` | `double` | X轴分量 | 根据上下文 |
| `y` | `double` | Y轴分量 | 根据上下文 |
| `z` | `double` | Z轴分量 | 根据上下文 |

**使用说明**：
- 在调用`MoveChassis()`之前，需要先调用`RequestChassisControl()`请求底盘控制权限
- `linear.x`：前进/后退速度（正值为前进，负值为后退）
- `linear.y`：左右平移速度（蟹行模式使用，正值为左移，负值为右移）
- `linear.z`：通常为0
- `angular.z`：绕Z轴旋转角速度（正值为逆时针，负值为顺时针）

- **示例**：

  ```cpp
  #include "gdk/gdk.h"
  #include <iostream>
  #include <thread>
  #include <chrono>

  using namespace agibot::gdk;

  int main() {
      Pnc pnc;
      std::this_thread::sleep_for(std::chrono::seconds(1));

      // 请求底盘控制权限
      GDKRes res = pnc.RequestChassisControl(0);
      if (res != GDKRes::kSuccess) {
          std::cout << "请求底盘控制失败" << std::endl;
          return 1;
      }
      std::this_thread::sleep_for(std::chrono::milliseconds(500));

      // 阿克曼模式：前进并右转
      Twist twist;
      twist.linear.x = 0.5;   // 前进速度 0.5 m/s
      twist.linear.y = 0.0;
      twist.linear.z = 0.0;
      twist.angular.x = 0.0;
      twist.angular.y = 0.0;
      twist.angular.z = -0.3; // 右转角速度 0.3 rad/s

      res = pnc.MoveChassis(twist);
      if (res == GDKRes::kSuccess) {
          std::cout << "底盘移动指令发送成功" << std::endl;
      }

      // 运行一段时间后停止
      std::this_thread::sleep_for(std::chrono::seconds(2));

      res = pnc.get_task_state(task_state);
      if (res == GDKRes::kSuccess) {
          std::cout << "任务状态: " << task_state.state << std::endl;
      } else {
          std::cout << "获取任务状态失败" << std::endl;
      }
      auto task_id = task_state.id;
      res = pnc.CancelTask(task_id);
      if (res != GDKRes::kSuccess) {
          std::cout << "任务取消失败" << std::endl;
      }

      // 蟹行模式：向左平移
      Twist twist;
      twist.linear.x = 0.0;
      twist.linear.y = 0.5; // 向左平移速度 0.5 m/s
      twist.linear.z = 0.0;
      twist.angular.x = 0.0;
      twist.angular.y = 0.0;
      twist.angular.z = 0.0;
      pnc.MoveChassis(twist);

      std::this_thread::sleep_for(std::chrono::seconds(2));
      res = pnc.get_task_state(task_state);
      if (res == GDKRes::kSuccess) {
          std::cout << "任务状态: " << task_state.state << std::endl;
      } else {
          std::cout << "获取任务状态失败" << std::endl;
      }
      auto task_id = task_state.id;
      res = pnc.CancelTask(task_id);
      if (res != GDKRes::kSuccess) {
          std::cout << "任务取消失败" << std::endl;
      }

      return 0;
  }
  ```

#### 10. 完整使用示例

- **功能**：演示PNC模块的完整使用流程
- **示例**：

  ```cpp
    #include <iostream>
    #include <chrono>
    #include <thread>
    #include <csignal>
    #include "gdk/gdk.h"

    void signal_handler(int signum) {
        std::cout << "Interrupt signal (" << signum << ") received." << std::endl;
        exit(signum);
    }

    int main(int argc, char** argv) {
        if (argc != 8) {
            std::cerr << "Usage: " << argv[0]
                    << " position_x position_y position_z orientation_x "
                        "orientation_y orientation_z orientation_w"
                    << std::endl;
            return 1;
        }
        double position_x = std::stod(argv[1]);
        double position_y = std::stod(argv[2]);
        double position_z = std::stod(argv[3]);
        double orientation_x = std::stod(argv[4]);
        double orientation_y = std::stod(argv[5]);
        double orientation_z = std::stod(argv[6]);
        double orientation_w = std::stod(argv[7]);
        agibot::gdk::Pnc pnc;
        std::cout << "Pnc init" << std::endl;
        agibot::gdk::NaviReq navi_req;
        navi_req.target.position.x = position_x;
        navi_req.target.position.y = position_y;
        navi_req.target.position.z = position_z;
        navi_req.target.orientation.x = orientation_x;
        navi_req.target.orientation.y = orientation_y;
        navi_req.target.orientation.z = orientation_z;
        navi_req.target.orientation.w = orientation_w;

        std::this_thread::sleep_for(std::chrono::seconds(1));

        auto res = pnc.NormalNavi(navi_req);
        if (res != agibot::gdk::GDKRes::kSuccess) {
            std::cerr << "NormalNavi failed" << std::endl;
            return 1;
        }
        // std::this_thread::sleep_for(std::chrono::seconds(1));

        // 获取任务ID
        agibot::gdk::PNCTaskState task_state;
        res = pnc.GetTaskState(task_state);
        if (res != agibot::gdk::GDKRes::kSuccess) {
            std::cerr << "GetTaskState failed" << std::endl;
            return 1;
        }
        uint32_t task_id = task_state.id;

        std::cout << "PauseTask" << std::endl;
        res = pnc.PauseTask(task_id);

        if (res != agibot::gdk::GDKRes::kSuccess) {
            std::cerr << "PauseTask failed" << std::endl;
            return 1;
        }
        std::cout << "ResumeTask" << std::endl;
        std::this_thread::sleep_for(std::chrono::milliseconds(200));
        res = pnc.ResumeTask(task_id);
        if (res != agibot::gdk::GDKRes::kSuccess) {
            std::cerr << "ResumeTask failed" << std::endl;
            return 1;
        }
        std::cout << "CancelTask" << std::endl;
        std::this_thread::sleep_for(std::chrono::milliseconds(200));
        res = pnc.CancelTask(task_id);
        if (res != agibot::gdk::GDKRes::kSuccess) {
            std::cerr << "CancelTask failed" << std::endl;
            return 1;
        }
        std::this_thread::sleep_for(std::chrono::seconds(1));
        if (res != agibot::gdk::GDKRes::kSuccess) {
            // until ctrl c to exit
            std::signal(SIGINT, signal_handler);
            while (true) {
            std::this_thread::sleep_for(std::chrono::seconds(1));
            }

            return 0;
        }
    }
  ```


## 使用注意事项

1. **初始化等待**：创建Pnc对象后，建议等待一段时间以确保系统初始化完成
2. **地图准备**：执行导航前确保已有可用的地图
3. **目标点设置**：设置目标点时注意坐标系的正确性
4. **任务状态监控**：建议定期检查任务状态以了解导航进度
5. **任务管理**：合理使用暂停、恢复、取消功能
6. **精度选择**：根据需求选择合适的导航精度（正常/高精度）
7. **相对移动**：使用相对移动时注意移动距离的合理性

## 应用场景

- **自主导航**：实现机器人的自主路径规划和导航
- **精确导航**：执行高精度的位置控制
- **相对移动**：执行基于当前位置的相对移动
- **任务调度**：管理多个导航任务的执行
- **路径规划**：为机器人规划最优路径
- **避障导航**：在复杂环境中进行安全导航
- **多目标导航**：实现多个目标点的连续导航
- **远程控制**：支持远程控制模式下的导航
