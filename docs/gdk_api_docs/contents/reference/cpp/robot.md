# GDK Robot 接口文档（C++）

## 概述

Robot（机器人）模块为G02机器人提供了统一的机器人控制接口，集成了机器人本体状态获取、运动控制、关节控制、末端执行器控制等功能。通过C++接口，开发者可以方便地实现对机器人的全面控制，适用于机器人控制、状态监控、动作执行、路径规划等多种场景。

## 接口说明

### Robot 类

该类封装了机器人的主要控制接口，集成了HAL（硬件抽象层）和运动控制功能。

#### 1. `GetJointStates()`

- **注意事项**：使用motor_position和motor_velocity获取电机位置和速度，position和velocity为低速电机预留字段，当前版本无需关注
- **功能**：获取机器人关节状态信息
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `joint_states` | `JointStates&` | 输出参数，关节状态信息对象 |

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`，`joint_states`参数包含关节状态信息

#### JointStates对象详细说明

**JointStates结构体包含以下成员**：

| 成员名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `nums` | `size_t` | 关节数量 | 无单位 |
| `states` | `std::vector<JointState>` | 关节状态列表 | 关节状态列表 |
| `timestamp` | `uint64_t` | 时间戳 | 纳秒 |

```cpp
struct JointStates {
  size_t nums{};                     ///< number of joint states
  std::vector<JointState> states{};  ///< joint states
  uint64_t timestamp{};              ///< joint states timestamp(ns)
};
```

**JointState结构体**：

| 成员名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `name` | `std::string` | 关节名称 | 字符串 |
| `mode` | `uint32_t` | 关节模式 | 无单位 |
| `position` | `double` | 关节位置 | 弧度 |
| `velocity` | `double` | 关节速度 | 弧度/秒 |
| `effort` | `double` | 关节力矩 | N·m |
| `motor_position` | `double` | 电机位置 | 弧度 |
| `motor_velocity` | `double` | 电机速度 | 弧度/秒 |
| `motor_current` | `double` | 电机电流 | A |
| `error_code` | `uint32_t` | 错误码，0表示正常 | 无单位 |

```cpp
struct JointState {
  std::string name{};
  uint32_t mode{};
  double position{};
  double velocity{};
  double effort{};
  double motor_position{};
  double motor_velocity{};
  double motor_current{};
  uint32_t error_code{};
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

      agibot::gdk::Robot robot;
      std::cout << "Robot init" << std::endl;
      std::this_thread::sleep_for(std::chrono::seconds(1));

      agibot::gdk::JointStates joint_states;
      if (robot.GetJointStates(joint_states) != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "Failed to get joint states" << std::endl;
      } else {
          std::cout << "关节数量: " << joint_states.nums << std::endl;
          std::cout << "时间戳: " << joint_states.timestamp << std::endl;
          for (const auto& joint_state : joint_states.states) {
              std::cout << "关节: " << joint_state.name
                        << ", 位置: " << joint_state.position
                        << ", 速度: " << joint_state.velocity
                        << ", 力矩: " << joint_state.effort
                        << ", 错误码: " << joint_state.error_code << std::endl;
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

#### 2. `GetEndState()`

- **功能**：获取末端执行器状态信息
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `end_state` | `DualEndState&` | 输出参数，双末端执行器状态信息对象 |

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`，`end_state`参数包含末端执行器状态信息

#### DualEndState对象详细说明

**DualEndState结构体包含以下成员**：

| 成员名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `left_end_state` | `EndState` | 左末端执行器状态 | 末端状态 |
| `right_end_state` | `EndState` | 右末端执行器状态 | 末端状态 |

```cpp
struct DualEndState {
  EndState left_end_state{};
  EndState right_end_state{};
};
```

**EndState结构体**：

| 成员名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `controlled` | `bool` | 是否被控制 | 布尔值 |
| `type` | `uint32_t` | 末端执行器类型 | 无单位 |
| `names` | `std::vector<std::string>` | 关节名称列表 | 字符串列表 |
| `end_states` | `std::vector<MotorState>` | 电机状态列表 | 电机状态列表 |

```cpp
struct EndState {
  bool controlled{};
  uint32_t type{};
  std::vector<std::string> names{};
  std::vector<MotorState> end_states{};
};
```

**MotorState结构体**：

| 成员名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `id` | `uint32_t` | 电机ID | 无单位 |
| `enable` | `bool` | 是否使能 | 布尔值 |
| `position` | `double` | 电机位置 | 弧度 |
| `velocity` | `double` | 电机速度 | 弧度/秒 |
| `effort` | `double` | 电机力矩 | N·m |
| `current` | `float` | 电机电流 | A |
| `voltage` | `float` | 电机电压 | V |
| `temperature` | `float` | 电机温度 | °C |
| `status` | `uint32_t` | 电机状态 | 无单位 |
| `err_code` | `uint32_t` | 错误码 | 无单位 |

```cpp
struct MotorState {
  uint32_t id = 0;
  bool enable = false;
  double position = 0.0;
  double velocity = 0.0;
  double effort = 0.0;
  float current = 0.0f;
  float voltage = 0.0f;
  float temperature = 0.0f;
  uint32_t status = 0;
  uint32_t err_code = 0;
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

      agibot::gdk::Robot robot;
      std::cout << "Robot init" << std::endl;
      std::this_thread::sleep_for(std::chrono::seconds(1));

      agibot::gdk::DualEndState end_state;
      if (robot.GetEndState(end_state) != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "Failed to get end state" << std::endl;
      } else {
          std::cout << "左末端执行器状态:" << std::endl;
          std::cout << "  控制状态: " << (end_state.left_end_state.controlled ? "是" : "否") << std::endl;
          std::cout << "  类型: " << end_state.left_end_state.type << std::endl;
          for (const auto& motor_state : end_state.left_end_state.end_states) {
              std::cout << "  电机ID: " << motor_state.id
                        << ", 位置: " << motor_state.position
                        << ", 电流: " << motor_state.current
                        << ", 温度: " << motor_state.temperature << std::endl;
          }

          std::cout << "右末端执行器状态:" << std::endl;
          std::cout << "  控制状态: " << (end_state.right_end_state.controlled ? "是" : "否") << std::endl;
          std::cout << "  类型: " << end_state.right_end_state.type << std::endl;
          for (const auto& motor_state : end_state.right_end_state.end_states) {
              std::cout << "  电机ID: " << motor_state.id
                        << ", 位置: " << motor_state.position
                        << ", 电流: " << motor_state.current
                        << ", 温度: " << motor_state.temperature << std::endl;
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

#### 3. `GetWholeBodyStatus()`

- **功能**：获取机器人全身状态信息
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `whole_body_status` | `WholeBodyStatus&` | 输出参数，全身状态信息对象 |

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`，`whole_body_status`参数包含全身状态信息

#### WholeBodyStatus对象详细说明

**WholeBodyStatus结构体包含以下成员**：

| 成员名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `right_arm_error` | `uint32_t` | 右臂错误码 | 无单位 |
| `left_arm_error` | `uint32_t` | 左臂错误码 | 无单位 |
| `right_arm_control` | `bool` | 右臂控制状态 | 布尔值 |
| `left_arm_control` | `bool` | 左臂控制状态 | 布尔值 |
| `right_arm_estop` | `bool` | 右臂急停状态 | 布尔值 |
| `left_arm_estop` | `bool` | 左臂急停状态 | 布尔值 |
| `right_end_error` | `uint32_t` | 右末端执行器错误码 | 无单位 |
| `left_end_error` | `uint32_t` | 左末端执行器错误码 | 无单位 |
| `right_end_model` | `std::string` | 右末端执行器型号 | 字符串 |
| `left_end_model` | `std::string` | 左末端执行器型号 | 字符串 |
| `waist_error` | `uint32_t` | 腰部错误码 | 无单位 |
| `lift_error` | `uint32_t` | 升降错误码 | 无单位 |
| `neck_error` | `uint32_t` | 颈部错误码 | 无单位 |
| `chassis_error` | `uint32_t` | 底盘错误码 | 无单位 |
| `timestamp` | `uint64_t` | 时间戳 | 纳秒 |

```cpp
struct WholeBodyStatus {
  uint32_t right_arm_error{0};
  uint32_t left_arm_error{0};
  bool right_arm_control{false};
  bool left_arm_control{false};
  bool right_arm_estop{false};
  bool left_arm_estop{false};
  uint32_t right_end_error{0};
  uint32_t left_end_error{0};
  std::string right_end_model{};
  std::string left_end_model{};
  uint32_t waist_error{0};
  uint32_t lift_error{0};
  uint32_t neck_error{0};
  uint32_t chassis_error{0};
  uint64_t timestamp{};
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

      agibot::gdk::Robot robot;
      std::cout << "Robot init" << std::endl;
      std::this_thread::sleep_for(std::chrono::seconds(1));

      agibot::gdk::WholeBodyStatus whole_body_status;
      if (robot.GetWholeBodyStatus(whole_body_status) != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "Failed to get whole body status" << std::endl;
      } else {
          std::cout << "全身状态信息:" << std::endl;
          std::cout << "右臂错误码: " << whole_body_status.right_arm_error << std::endl;
          std::cout << "左臂错误码: " << whole_body_status.left_arm_error << std::endl;
          std::cout << "右臂控制状态: " << (whole_body_status.right_arm_control ? "是" : "否") << std::endl;
          std::cout << "左臂控制状态: " << (whole_body_status.left_arm_control ? "是" : "否") << std::endl;
          std::cout << "右臂急停状态: " << (whole_body_status.right_arm_estop ? "是" : "否") << std::endl;
          std::cout << "左臂急停状态: " << (whole_body_status.left_arm_estop ? "是" : "否") << std::endl;
          std::cout << "右末端执行器型号: " << whole_body_status.right_end_model << std::endl;
          std::cout << "左末端执行器型号: " << whole_body_status.left_end_model << std::endl;
          std::cout << "腰部错误码: " << whole_body_status.waist_error << std::endl;
          std::cout << "升降错误码: " << whole_body_status.lift_error << std::endl;
          std::cout << "颈部错误码: " << whole_body_status.neck_error << std::endl;
          std::cout << "底盘错误码: " << whole_body_status.chassis_error << std::endl;
          std::cout << "时间戳: " << whole_body_status.timestamp << std::endl;
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

#### 4. `GetMotionControlStatus()`

- **功能**：获取末端控制状态信息
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `status` | `MotionControlStatus&` | 输出参数，末端控制状态对象 |

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`，`status`参数包含运动控制状态信息

#### MotionControlStatus对象详细说明

**MotionControlStatus结构体包含以下成员**：

| 成员名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `frame_names` | `std::vector<std::string>` | 末端关节名称列表 | 字符串列表 |
| `frame_poses` | `std::vector<Pose>` | 末端关节位姿列表 | 位姿列表 |
| `collision_pairs_1` | `std::vector<std::string>` | 碰撞对列表1 | 字符串列表 |
| `collision_pairs_2` | `std::vector<std::string>` | 碰撞对列表2 | 字符串列表 |
| `mode` | `uint8_t` | 运动模式 | 无单位 |
| `error_code` | `uint8_t` | 错误码，0表示正常 | 无单位 |
| `error_msg` | `std::string` | 错误信息 | 字符串 |
| `twists` | `std::vector<Twist>` | 速度信息列表 | 速度列表 |
| `wrenches` | `std::vector<Wrench>` | 力/力矩信息列表 | 力/力矩列表 |

**mode数值说明**：

| 数值 | 含义 |
| :--- | :--- |
| 0 | `停止` |
| 1 | `G1_伺服` |
| 2 | `路径规划` |
| 5 | `G2_伺服` |
```cpp
struct MotionControlStatus {
  std::vector<std::string> frame_names{};
  std::vector<Pose> frame_poses{};
  std::vector<std::string> collision_pairs_1{};
  std::vector<std::string> collision_pairs_2{};
  uint8_t mode{};
  uint8_t error_code{};
  std::string error_msg{};
  std::vector<Twist> twists{};
  std::vector<Wrench> wrenches{};
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

      agibot::gdk::Robot robot;
      std::cout << "Robot init" << std::endl;
      std::this_thread::sleep_for(std::chrono::seconds(1));

      agibot::gdk::MotionControlStatus status;
      if (robot.GetMotionControlStatus(status) != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "Failed to get motion control status" << std::endl;
      } else {
          std::cout << "末端控制状态:" << std::endl;
          std::cout << "模式: " << status.mode << std::endl;
          std::cout << "错误码: " << status.error_code << std::endl;
          std::cout << "错误信息: " << status.error_msg << std::endl;
          std::cout << "关节数量: " << status.frame_names.size() << std::endl;
          for (size_t i = 0; i < status.frame_names.size(); i++) {
              std::cout << "关节: " << status.frame_names[i]
                        << ", 位置: x=" << status.frame_poses[i].position.x
                        << ", y=" << status.frame_poses[i].position.y
                        << ", z=" << status.frame_poses[i].position.z << std::endl;
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

#### 5. `GetChassisPowerState()`

- **功能**：获取底盘电源状态
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `chassis_power_state` | `ChassisPowerState&` | 底盘电源状态对象 |

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`

#### ChassisPowerState对象详细说明

**ChassisPowerState结构体包含以下成员**：

| 成员名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `battery_main_power_switch_state` | `uint8_t` | 电池主电源开关状态 | 无单位 |
| `emergency_stop_pedal_state` | `uint8_t` | 急停踏板状态 | 无单位 |
| `battery_main_power_switch_fault_state` | `uint8_t` | 电池主电源开关故障状态 | 无单位 |
| `emergency_stop_pedal_fault_state` | `uint8_t` | 急停踏板故障状态 | 无单位 |
| `chassis_power_board_state` | `uint8_t` | 底盘电源板状态 | 无单位 |
| `chassis_left_traction_motor_power_state` | `uint8_t` | 底盘左牵引电机电源状态 | 无单位 |
| `chassis_right_traction_motor_power_state` | `uint8_t` | 底盘右牵引电机电源状态 | 无单位 |
| `chassis_left_steering_motor_power_state` | `uint8_t` | 底盘左转向电机电源状态 | 无单位 |
| `chassis_right_steering_motor_power_state` | `uint8_t` | 底盘右转向电机电源状态 | 无单位 |
| `chassis_lidar1_power_state` | `uint8_t` | 底盘激光雷达1电源状态 | 无单位 |
| `chassis_lidar2_power_state` | `uint8_t` | 底盘激光雷达2电源状态 | 无单位 |
| `chassis_ultrasonic_radar_power_state` | `uint8_t` | 底盘超声波雷达电源状态 | 无单位 |
| `chassis_tof_camera_power_state` | `uint8_t` | 底盘ToF相机电源状态 | 无单位 |
| `chassis_ethernet_switch_power_state` | `uint8_t` | 底盘以太网交换机电源状态 | 无单位 |
| `chassis_external_power_output_state` | `uint8_t` | 底盘外部电源输出状态 | 无单位 |
| `battery_main_power_output_switch_state` | `uint8_t` | 电池主电源输出开关状态 | 无单位 |
| `battery_states` | `std::vector<BatteryState>` | 电池状态列表 | 电池状态列表 |
| `charge_plug_insert_state` | `uint8_t` | 充电插头插入状态 | 无单位 |
| `charge_plug_input_voltage` | `float` | 充电插头输入电压 | V |
| `charge_plug_input_current` | `float` | 充电插头输入电流 | A |
| `charge_plug_input_short_circuit_fault_state` | `uint8_t` | 充电插头输入短路故障状态 | 无单位 |
| `charge_plug_input_open_circuit_fault_state` | `uint8_t` | 充电插头输入开路故障状态 | 无单位 |
| `chassis_led_strip_power_state` | `uint8_t` | 底盘LED灯带电源状态 | 无单位 |
| `chassis_power_board_temperature` | `float` | 底盘电源板温度 | °C |
| `power_48v_bus_power_on_fault_state` | `uint8_t` | 48V总线电源故障状态 | 无单位 |
| `power_poe_bus_power_on_fault_state` | `uint8_t` | PoE总线电源故障状态 | 无单位 |
| `chassis_board_12v_output_fault_state` | `uint8_t` | 底盘板12V输出故障状态 | 无单位 |
| `chassis_board_5v_output_fault_state` | `uint8_t` | 底盘板5V输出故障状态 | 无单位 |
| `chassis_power_board_fault_state` | `uint32_t` | 底盘电源板故障状态 | 无单位 |
| `timestamp` | `uint64_t` | 时间戳 | 纳秒 |

```cpp
struct ChassisPowerState {
  uint8_t battery_main_power_switch_state{0};
  uint8_t emergency_stop_pedal_state{0};
  uint8_t battery_main_power_switch_fault_state{0};
  uint8_t emergency_stop_pedal_fault_state{0};
  uint8_t chassis_power_board_state{0};
  uint8_t chassis_left_traction_motor_power_state{0};
  uint8_t chassis_right_traction_motor_power_state{0};
  uint8_t chassis_left_steering_motor_power_state{0};
  uint8_t chassis_right_steering_motor_power_state{0};
  uint8_t chassis_lidar1_power_state{0};
  uint8_t chassis_lidar2_power_state{0};
  uint8_t chassis_ultrasonic_radar_power_state{0};
  uint8_t chassis_tof_camera_power_state{0};
  uint8_t chassis_ethernet_switch_power_state{0};
  uint8_t chassis_external_power_output_state{0};
  uint8_t battery_main_power_output_switch_state{0};
  std::vector<BatteryState> battery_states{};
  uint8_t charge_plug_insert_state{0};
  float charge_plug_input_voltage{0.0};
  float charge_plug_input_current{0.0};
  uint8_t charge_plug_input_short_circuit_fault_state{0};
  uint8_t charge_plug_input_open_circuit_fault_state{0};
  uint8_t chassis_led_strip_power_state{0};
  float chassis_power_board_temperature{0.0};
  uint8_t power_48v_bus_power_on_fault_state{0};
  uint8_t power_poe_bus_power_on_fault_state{0};
  uint8_t chassis_board_12v_output_fault_state{0};
  uint8_t chassis_board_5v_output_fault_state{0};
  uint32_t chassis_power_board_fault_state{0};
  uint64_t timestamp{0};
};
```

**BatteryState结构体**：

| 成员名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `battery_charging_status` | `uint8_t` | 电池充电状态 | 无单位 |
| `battery_output_voltage` | `float` | 电池输出电压 | V |
| `battery_output_current` | `float` | 电池输出电流 | A |
| `battery_charging_current` | `float` | 电池充电电流 | A |
| `battery_temperature` | `float` | 电池温度 | °C |
| `battery_soc` | `float` | 电池电量百分比 (State of Charge) | % |
| `battery_soh` | `uint8_t` | 电池健康度 (State of Health) | % |
| `battery_short_circuit_fault_state` | `uint8_t` | 电池短路故障状态 | 无单位 |
| `battery_open_circuit_fault_state` | `uint8_t` | 电池开路故障状态 | 无单位 |
| `battery_other_fault_state` | `uint8_t` | 电池其他故障状态 | 无单位 |
| `battery_outside_output_voltage` | `float` | 电池外部输出电压 | V |
| `battery_outside_connection` | `uint8_t` | 电池外部连接状态 | 无单位 |
| `battery_outside_open_circuit_fault_state` | `uint8_t` | 电池外部开路故障状态 | 无单位 |
| `battery_switch_state` | `uint8_t` | 电池开关状态 | 无单位 |
| `battery_unlock_state` | `uint8_t` | 电池解锁状态 | 无单位 |
| `battery_input_fault_state` | `uint8_t` | 电池输入故障状态 | 无单位 |
| `battery_charging_mos_switch_state` | `uint8_t` | 电池充电MOS开关状态 | 无单位 |

```cpp
struct BatteryState {
  uint8_t battery_charging_status{0};
  float battery_output_voltage{0.0};
  float battery_output_current{0.0};
  float battery_charging_current{0.0};
  float battery_temperature{0.0};
  float battery_soc{0.0};
  uint8_t battery_soh{0};
  uint8_t battery_short_circuit_fault_state{0};
  uint8_t battery_open_circuit_fault_state{0};
  uint8_t battery_other_fault_state{0};
  float battery_outside_output_voltage{0.0};
  uint8_t battery_outside_connection{0};
  uint8_t battery_outside_open_circuit_fault_state{0};
  uint8_t battery_switch_state{0};
  uint8_t battery_unlock_state{0};
  uint8_t battery_input_fault_state{0};
  uint8_t battery_charging_mos_switch_state{0};
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

      agibot::gdk::Robot robot;
      std::cout << "Robot init" << std::endl;
      std::this_thread::sleep_for(std::chrono::seconds(1));

      agibot::gdk::ChassisPowerState chassis_power_state;
      if (robot.GetChassisPowerState(chassis_power_state) != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "Failed to get chassis power state" << std::endl;
      } else {
          std::cout << "底盘电源状态信息:" << std::endl;
          std::cout << "  电池主电源开关: " << (int)chassis_power_state.battery_main_power_switch_state << std::endl;
          std::cout << "  急停踏板状态: " << (int)chassis_power_state.emergency_stop_pedal_state << std::endl;
          std::cout << "  底盘电源板状态: " << (int)chassis_power_state.chassis_power_board_state << std::endl;
          std::cout << "  底盘电源板温度: " << chassis_power_state.chassis_power_board_temperature << "°C" << std::endl;
          std::cout << "  充电插头输入电压: " << chassis_power_state.charge_plug_input_voltage << "V" << std::endl;
          std::cout << "  充电插头输入电流: " << chassis_power_state.charge_plug_input_current << "A" << std::endl;
          std::cout << "  电池数量: " << chassis_power_state.battery_states.size() << std::endl;

          for (size_t i = 0; i < chassis_power_state.battery_states.size(); i++) {
              const auto& battery = chassis_power_state.battery_states[i];
              std::cout << "  电池 " << i << ":" << std::endl;
              std::cout << "    电量: " << battery.battery_soc << "%" << std::endl;
              std::cout << "    健康度: " << (int)battery.battery_soh << "%" << std::endl;
              std::cout << "    电压: " << battery.battery_output_voltage << "V" << std::endl;
              std::cout << "    电流: " << battery.battery_output_current << "A" << std::endl;
              std::cout << "    温度: " << battery.battery_temperature << "°C" << std::endl;
          }

          std::cout << "  时间戳: " << chassis_power_state.timestamp << std::endl;
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

#### 6. `GetChestPowerState()`

- **功能**：获取胸部电源状态
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `chest_power_state` | `ChestPowerState&` | 输出参数，胸部电源状态对象 |

- **返回值**：`GDKRes`，操作结果状态码。

#### ChestPowerState对象详细说明

**ChestPowerState结构体包含以下成员**：

| 成员名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `power_onoff_req` | `uint8_t` | 开关机请求 | 无单位 |
| `emergency_stop_button_req` | `uint8_t` | 急停按钮请求 | 无单位 |
| `power_switch_fault_state` | `uint8_t` | 电源开关故障状态 | 无单位 |
| `emergency_stop_button_fault_state` | `uint8_t` | 急停按钮故障状态 | 无单位 |
| `power_full_low_req` | `uint8_t` | 电源全/低请求 | 无单位 |
| `chest_power_board_power_state` | `uint8_t` | 胸部电源板电源状态 | 无单位 |
| `domain_controller_power_state` | `uint8_t` | 域控制器电源状态 | 无单位 |
| `head_interactive_board_power_state` | `uint8_t` | 头部交互板电源状态 | 无单位 |
| `curved_screen_power_state` | `uint8_t` | 曲面屏电源状态 | 无单位 |
| `head_yaw_motor_power_state` | `uint8_t` | 头部偏航电机电源状态 | 无单位 |
| `head_pitch_motor_power_state` | `uint8_t` | 头部俯仰电机电源状态 | 无单位 |
| `head_roll_motor_power_state` | `uint8_t` | 头部滚转电机电源状态 | 无单位 |
| `waist_yaw_motor_power_state` | `uint8_t` | 腰部偏航电机电源状态 | 无单位 |
| `head_motor_short_circuit_fault_state` | `uint8_t` | 头部电机短路故障状态 | 无单位 |
| `waist_pitch_motor_power_state` | `uint8_t` | 腰部俯仰电机电源状态 | 无单位 |
| `leg_bending1_motor_power_state` | `uint8_t` | 腿部弯曲1电机电源状态 | 无单位 |
| `leg_bending2_motor_power_state` | `uint8_t` | 腿部弯曲2电机电源状态 | 无单位 |
| `leg_bending3_motor_power_state` | `uint8_t` | 腿部弯曲3电机电源状态 | 无单位 |
| `waist_motor_short_circuit_fault_state` | `uint8_t` | 腰部电机短路故障状态 | 无单位 |
| `left_arm_power_state` | `uint8_t` | 左臂电源状态 | 无单位 |
| `left_arm_motor_short_circuit_fault_state` | `uint8_t` | 左臂电机短路故障状态 | 无单位 |
| `left_arm_brake_enable_state` | `uint8_t` | 左臂刹车使能状态 | 无单位 |
| `right_arm_power_state` | `uint8_t` | 右臂电源状态 | 无单位 |
| `right_arm_motor_short_circuit_fault_state` | `uint8_t` | 右臂电机短路故障状态 | 无单位 |
| `right_arm_brake_enable_state` | `uint8_t` | 右臂刹车使能状态 | 无单位 |
| `fan_power_state` | `uint8_t` | 风扇电源状态 | 无单位 |
| `chest_power_board_fan_fault_state` | `uint8_t` | 胸部电源板风扇故障状态 | 无单位 |
| `body_fan1_fault_state` | `uint8_t` | 身体风扇1故障状态 | 无单位 |
| `body_fan2_fault_state` | `uint8_t` | 身体风扇2故障状态 | 无单位 |
| `body_fan3_fault_state` | `uint8_t` | 身体风扇3故障状态 | 无单位 |
| `body_fan4_fault_state` | `uint8_t` | 身体风扇4故障状态 | 无单位 |
| `upper_body_led_strip_power_state` | `uint8_t` | 上身LED灯带电源状态 | 无单位 |
| `poe_power_state` | `uint8_t` | PoE电源状态 | 无单位 |
| `ipad_power_state` | `uint8_t` | iPad电源状态 | 无单位 |
| `chest_reserved_lidar_power_state` | `uint8_t` | 胸部预留激光雷达电源状态 | 无单位 |
| `chest_power_board_temperature` | `float` | 胸部电源板温度 | °C |
| `chest_power_board_fault_state` | `uint32_t` | 胸部电源板故障状态 | 无单位 |
| `timestamp` | `uint64_t` | 时间戳 | 纳秒 |

```cpp
struct ChestPowerState {
  uint8_t power_onoff_req{0};
  uint8_t emergency_stop_button_req{0};
  uint8_t power_switch_fault_state{0};
  uint8_t emergency_stop_button_fault_state{0};
  uint8_t power_full_low_req{0};
  uint8_t chest_power_board_power_state{0};
  uint8_t domain_controller_power_state{0};
  uint8_t head_interactive_board_power_state{0};
  uint8_t curved_screen_power_state{0};
  uint8_t head_yaw_motor_power_state{0};
  uint8_t head_pitch_motor_power_state{0};
  uint8_t head_roll_motor_power_state{0};
  uint8_t waist_yaw_motor_power_state{0};
  uint8_t head_motor_short_circuit_fault_state{0};
  uint8_t waist_pitch_motor_power_state{0};
  uint8_t leg_bending1_motor_power_state{0};
  uint8_t leg_bending2_motor_power_state{0};
  uint8_t leg_bending3_motor_power_state{0};
  uint8_t waist_motor_short_circuit_fault_state{0};
  uint8_t left_arm_power_state{0};
  uint8_t left_arm_motor_short_circuit_fault_state{0};
  uint8_t left_arm_brake_enable_state{0};
  uint8_t right_arm_power_state{0};
  uint8_t right_arm_motor_short_circuit_fault_state{0};
  uint8_t right_arm_brake_enable_state{0};
  uint8_t fan_power_state{0};
  uint8_t chest_power_board_fan_fault_state{0};
  uint8_t body_fan1_fault_state{0};
  uint8_t body_fan2_fault_state{0};
  uint8_t body_fan3_fault_state{0};
  uint8_t body_fan4_fault_state{0};
  uint8_t upper_body_led_strip_power_state{0};
  uint8_t poe_power_state{0};
  uint8_t ipad_power_state{0};
  uint8_t chest_reserved_lidar_power_state{0};
  float chest_power_board_temperature{0.0};
  uint32_t chest_power_board_fault_state{0};
  uint64_t timestamp{0};
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

      agibot::gdk::Robot robot;
      std::cout << "Robot init" << std::endl;
      std::this_thread::sleep_for(std::chrono::seconds(1));

      agibot::gdk::ChestPowerState chest_state;
      if (robot.GetChestPowerState(chest_state) == agibot::gdk::GDKRes::kSuccess) {
          std::cout << "胸部电源状态信息:" << std::endl;
          std::cout << "  开关机请求: " << (int)chest_state.power_onoff_req << std::endl;
          std::cout << "  急停按钮请求: " << (int)chest_state.emergency_stop_button_req << std::endl;
          std::cout << "  胸部电源板状态: " << (int)chest_state.chest_power_board_power_state << std::endl;
          std::cout << "  胸部电源板温度: " << chest_state.chest_power_board_temperature << "°C" << std::endl;
          std::cout << "  域控制器电源: " << (int)chest_state.domain_controller_power_state << std::endl;
          std::cout << "  左臂电源: " << (int)chest_state.left_arm_power_state << std::endl;
          std::cout << "  右臂电源: " << (int)chest_state.right_arm_power_state << std::endl;
          std::cout << "  左臂刹车使能: " << (int)chest_state.left_arm_brake_enable_state << std::endl;
          std::cout << "  右臂刹车使能: " << (int)chest_state.right_arm_brake_enable_state << std::endl;
          std::cout << "  头部偏航电机电源: " << (int)chest_state.head_yaw_motor_power_state << std::endl;
          std::cout << "  头部俯仰电机电源: " << (int)chest_state.head_pitch_motor_power_state << std::endl;
          std::cout << "  头部滚转电机电源: " << (int)chest_state.head_roll_motor_power_state << std::endl;
          std::cout << "  风扇电源: " << (int)chest_state.fan_power_state << std::endl;
          std::cout << "  时间戳: " << chest_state.timestamp << std::endl;
      } else {
          std::cout << "Failed to get chest power state" << std::endl;
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

#### 7. `JointControl()`

- **功能**：关节控制接口（路径规划控制），执行到目标位置后，接口返回。
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `joint_control_req` | `const JointControlReq&` | 关节控制请求对象 |

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`

#### JointControlReq对象详细说明

**JointControlReq结构体包含以下成员**：

| 成员名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `uuid` | `std::string` | 请求唯一标识 | 字符串 |
| `life_time` | `double` | 请求生命周期 | 秒 |
| `joint_names` | `std::vector<std::string>` | 关节名称列表 | 字符串列表 |
| `joint_positions` | `std::vector<double>` | 关节位置列表 | 弧度 |
| `joint_velocities` | `std::vector<double>` | 关节速度列表 | 弧度/秒 |
| `detail` | `std::string` | 详细信息 | 字符串 |

```cpp
struct JointControlReq {
  double life_time{0.0};
  std::vector<std::string> joint_names{};
  std::vector<double> joint_positions{};
  std::vector<double> joint_velocities{};
  std::string uuid{};
  std::string detail{};
};
```

#### 关节限位值说明

各关节的限位值（单位：弧度）如下：

| 关节名称 | 最小值 | 最大值 |
| :--- | :--- | :--- |
| `idx01_body_joint1` | -1.082104 | 0.000174 |
| `idx02_body_joint2` | -0.000174 | 2.652900 |
| `idx03_body_joint3` | -1.919862 | 1.570970 |
| `idx04_body_joint4` | -0.436332 | 0.436332 |
| `idx05_body_joint5` | -3.045599 | 3.045599 |
| `idx11_head_joint1` | -1.570970 | 1.570970 |
| `idx12_head_joint2` | -0.349240 | 0.349240 |
| `idx13_head_joint3` | -0.534773 | 0.534773 |
| `idx21_arm_l_joint1` | -3.071796 | 3.071796 |
| `idx22_arm_l_joint2` | -2.059505 | 2.059505 |
| `idx23_arm_l_joint3` | -3.071796 | 3.071796 |
| `idx24_arm_l_joint4` | -2.495838 | 1.012308 |
| `idx25_arm_l_joint5` | -3.071796 | 3.071796 |
| `idx26_arm_l_joint6` | -1.012308 | 1.012308 |
| `idx27_arm_l_joint7` | -1.535907 | 1.535907 |
| `idx61_arm_r_joint1` | -3.071796 | 3.071796 |
| `idx62_arm_r_joint2` | -2.059505 | 2.059505 |
| `idx63_arm_r_joint3` | -3.071796 | 3.071796 |
| `idx64_arm_r_joint4` | -2.495838 | 1.012308 |
| `idx65_arm_r_joint5` | -3.071796 | 3.071796 |
| `idx66_arm_r_joint6` | -1.012308 | 1.012308 |
| `idx67_arm_r_joint7` | -1.535907 | 1.535907 |

- **示例**：

  ```cpp
  #include "gdk/gdk.h"
  #include <iostream>
  #include <chrono>
  #include <thread>
  #include <random>
  #include <sstream>

  std::string generate_uuid() {
      std::random_device rd;
      std::mt19937 gen(rd());
      std::uniform_int_distribution<uint32_t> dis(0, 0xFFFFFFFF);
      std::stringstream ss;
      ss << std::hex << dis(gen) << "-" << dis(gen) << "-" << dis(gen) << "-" << dis(gen);
      return ss.str();
  }

  int main()
  {
      // 初始化GDK系统
      if (agibot::gdk::GDKInit() != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "GDK初始化失败" << std::endl;
          return -1;
      }
      std::cout << "GDK初始化成功" << std::endl;

      agibot::gdk::Robot robot;
      std::cout << "Robot init" << std::endl;
      std::this_thread::sleep_for(std::chrono::seconds(1));

      agibot::gdk::JointControlReq joint_control;
      joint_control.life_time = 5.0;
      joint_control.joint_names = {"idx21_arm_l_joint1","idx22_arm_l_joint2","idx23_arm_l_joint3"};
      joint_control.joint_positions = {0.0, 0.0, 0.0};
      joint_control.joint_velocities = {0.0, 0.0, 0.0};
      joint_control.detail = "左臂关节控制";

      if (robot.JointControl(joint_control) != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "Failed to control joints" << std::endl;
      } else {
          std::cout << "关节控制指令发送成功" << std::endl;
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

#### 8. `MoveHeadJoint()`

- **功能**：头部关节位置规划控制接口，执行到目标位置后，接口返回。
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `positions` | `std::vector<double>&` | 头部关节位置列表, 按照"idx11_head_joint1", "idx12_head_joint2", "idx13_head_joint3"填写目标关节角|
| `velocities` | `const std::vector<double>&` | 头部关节速度列表, 按照"idx11_head_joint1", "idx12_head_joint2", "idx13_head_joint3"填写目标关节速度|

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`

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

      agibot::gdk::Robot robot;
      std::cout << "Robot init" << std::endl;
      std::this_thread::sleep_for(std::chrono::seconds(1));

      std::vector<double> head_positions = {0.0, 0.0, 0.0};  // 头部关节位置
      std::vector<double> head_velocities = {0.3, 0.3, 0.3};  // 头部关节速度

      if (robot.MoveHeadJoint(head_positions, head_velocities) != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "Failed to move head position" << std::endl;
      } else {
          std::cout << "头部位置控制成功" << std::endl;
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

#### 9. `MoveWaistJoint()`

- **功能**：腰部关节位置规划控制接口，执行到目标位置后，接口返回。
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `positions` | `std::vector<double>&` | 腰部关节位置列表, 按照"idx01_body_joint1", "idx02_body_joint2", "idx03_body_joint3", "idx04_body_joint4", "idx05_body_joint5"填写目标关节角|
| `velocities` | `const std::vector<double>&` | 腰部关节速度列表, 按照"idx01_body_joint1", "idx02_body_joint2", "idx03_body_joint3", "idx04_body_joint4", "idx05_body_joint5"填写目标关节速度|

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`

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

      agibot::gdk::Robot robot;
      std::cout << "Robot init" << std::endl;
      std::this_thread::sleep_for(std::chrono::seconds(1));

      std::vector<double> waist_positions = {0.0, 0.0, 0.0, 0.0, 0.0};  // 腰部关节位置
      std::vector<double> waist_velocities = {0.3, 0.3, 0.3, 0.3, 0.3};  // 腰部关节速度

      if (robot.MoveWaistJoint(waist_positions, waist_velocities) != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "Failed to move waist position" << std::endl;
      } else {
          std::cout << "腰部位置控制成功" << std::endl;
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

#### 10. `MoveArmJoint()`

- **功能**：手臂关节位置规划控制接口，执行到目标位置后，接口返回。
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `positions` | `std::vector<double>&` | 手臂关节位置列表, 按照"idx21_arm_l_joint1", "idx22_arm_l_joint2", "idx23_arm_l_joint3",
      "idx24_arm_l_joint4", "idx25_arm_l_joint5", "idx26_arm_l_joint6",
      "idx27_arm_l_joint7", "idx61_arm_r_joint1", "idx62_arm_r_joint2",
      "idx63_arm_r_joint3", "idx64_arm_r_joint4", "idx65_arm_r_joint5",
      "idx66_arm_r_joint6", "idx67_arm_r_joint7"填写目标关节角 |
| `velocities` | `const std::vector<double>&` | 手臂关节速度列表, 按照"idx21_arm_l_joint1", "idx22_arm_l_joint2", "idx23_arm_l_joint3",
      "idx24_arm_l_joint4", "idx25_arm_l_joint5", "idx26_arm_l_joint6",
      "idx27_arm_l_joint7", "idx61_arm_r_joint1", "idx62_arm_r_joint2",
      "idx63_arm_r_joint3", "idx64_arm_r_joint4", "idx65_arm_r_joint5",
      "idx66_arm_r_joint6", "idx67_arm_r_joint7"填写目标关节速度 |
| `control_group` | `const int` | 控制组，0表示控制左臂，1表示控制右臂，2表示控制双臂 |
- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`

- **示例**：

  ```cpp
  #include "gdk/gdk.h"
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

      agibot::gdk::Robot robot;
      std::cout << "Robot init" << std::endl;
      std::this_thread::sleep_for(std::chrono::seconds(1));

      std::vector<double> arm_positions = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0};  // 手臂关节位置
      std::vector<double> arm_velocities = {0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3};  // 手臂关节速度

      if (robot.MoveArmJoint(arm_positions, arm_velocities, 2) != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "Failed to move arm position" << std::endl;
      } else {
          std::cout << "手臂位置控制成功" << std::endl;
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

#### 11. `JointServoControl()`

- **功能**：关节位置伺服控制接口，需要以100hz的控制频率进行控制，支持正常模式和低延时模式，默认使用正常模式。
- **注意**：低延时模式无碰撞保护，使用时注意安全。如需同时控制末端执行器，需要使用该接口下发控制明令，具体参考以下示例。
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `joint_servo_control_req` | `const JointServoControlReq&` | 关节位置伺服请求对象 |
| `enable_low_latency` | `bool` | 是否启用低延时模式，默认为`false` ｜

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`

#### JointServoControlReq对象详细说明

**JointServoControlReq结构体包含以下成员**：

| 成员名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `control_period` | `double` | 控制周期 | 秒 |
| `joint_names` | `std::vector<std::string>` | 关节名称列表 | 字符串列表 |
| `joint_positions` | `std::vector<double>` | 关节位置列表 | 弧度 |
| `joint_velocities` | `std::vector<double>` | 关节速度列表 | 弧度/秒 |

```cpp
struct JointServoControlReq {
  double control_period{0.0};
  std::vector<std::string> joint_names{};
  std::vector<double> joint_positions{};
  std::vector<double> joint_velocities{};
};
```

**参数说明**：
- `control_period` 表示控制周期，单位为秒，建议比当前控制频率稍大
- `joint_names`、`joint_positions`、`joint_velocities` 三个列表的长度必须相同
- `joint_positions` 中的值必须在对应关节的限位范围内（见下方关节限位值说明），否则返回 `ErrorCode::kInvalidInput`
- `joint_names`、`joint_positions`、`joint_velocities` 不能为空，否则返回 `ErrorCode::kInvalidInput`
- `joint_velocities` 预留参数，目前不使用，可以为空

#### 关节限位值说明

各关节的限位值（单位：弧度）如下：

| 关节名称 | 最小值 | 最大值 |
| :--- | :--- | :--- |
| `idx01_body_joint1` | -1.082104 | 0.000174 |
| `idx02_body_joint2` | -0.000174 | 2.652900 |
| `idx03_body_joint3` | -1.919862 | 1.570970 |
| `idx04_body_joint4` | -0.436332 | 0.436332 |
| `idx05_body_joint5` | -3.045599 | 3.045599 |
| `idx11_head_joint1` | -1.570970 | 1.570970 |
| `idx12_head_joint2` | -0.349240 | 0.349240 |
| `idx13_head_joint3` | -0.534773 | 0.534773 |
| `idx21_arm_l_joint1` | -3.071796 | 3.071796 |
| `idx22_arm_l_joint2` | -2.059505 | 2.059505 |
| `idx23_arm_l_joint3` | -3.071796 | 3.071796 |
| `idx24_arm_l_joint4` | -2.495838 | 1.012308 |
| `idx25_arm_l_joint5` | -3.071796 | 3.071796 |
| `idx26_arm_l_joint6` | -1.012308 | 1.012308 |
| `idx27_arm_l_joint7` | -1.535907 | 1.535907 |
| `idx61_arm_r_joint1` | -3.071796 | 3.071796 |
| `idx62_arm_r_joint2` | -2.059505 | 2.059505 |
| `idx63_arm_r_joint3` | -3.071796 | 3.071796 |
| `idx64_arm_r_joint4` | -2.495838 | 1.012308 |
| `idx65_arm_r_joint5` | -3.071796 | 3.071796 |
| `idx66_arm_r_joint6` | -1.012308 | 1.012308 |
| `idx67_arm_r_joint7` | -1.535907 | 1.535907 |
| **末端执行器（omnipicker）** | | |
| `idx31_gripper_l_inner_joint1` | -0.785 | 0 |
| `idx71_gripper_r_inner_joint1` | -0.785 | 0 |
| **末端执行器（dahuan）** | | |
| `idx31_gripper_l_inner_joint1` | 0 | 0.025 |
| `idx71_gripper_r_inner_joint1` | 0 | 0.025 |
| **末端执行器（ctek90d）** | | |
| `idx31_gripper_l_inner_joint1` | -0.91 | 0 |
| `idx71_gripper_r_inner_joint1` | -0.91 | 0 |
| **末端执行器（灵巧手 o10_t2 左手）** | | |
| `idx31_hand_l_thumb_roll_joint` | -1.1213740444063567 | 0.029670597283903602 |
| `idx32_hand_l_thumb_abad_joint` | -0.04537856055185257 | 1.642354826126664 |
| `idx33_hand_l_thumb_mcp_joint` | -0.8415977653116657 | 0.0 |
| `idx36_hand_l_index_abad_joint` | 0.0 | 0.16406094968746698 |
| `idx37_hand_l_index_pip_joint` | 0.0 | 1.4835298641951802 |
| `idx39_hand_l_middle_pip_joint` | 0.0 | 1.4835298641951802 |
| `idx41_hand_l_ring_abad_joint` | -0.16929693744344995 | 0.0 |
| `idx42_hand_l_ring_pip_joint` | 0.0 | 1.4835298641951802 |
| `idx44_hand_l_pinky_abad_joint` | -0.1850049007113989 | 0.0 |
| `idx45_hand_l_pinky_pip_joint` | 0.0 | 1.4835298641951802 |
| **末端执行器（灵巧手 o10_t2 右手）** | | |
| `idx71_hand_r_thumb_roll_joint` | -0.029670597283903602 | 1.1213740444063567 |
| `idx72_hand_r_thumb_abad_joint` | -1.642354826126664 | 0.04537856055185257 |
| `idx73_hand_r_thumb_mcp_joint` | 0.0 | 0.8415977653116657 |
| `idx76_hand_r_index_abad_joint` | -0.16406094968746698 | 0.0 |
| `idx77_hand_r_index_pip_joint` | 0.0 | 1.4835298641951802 |
| `idx79_hand_r_middle_pip_joint` | 0.0 | 1.4835298641951802 |
| `idx81_hand_r_ring_abad_joint` | 0.0 | 0.16929693744344995 |
| `idx82_hand_r_ring_pip_joint` | 0.0 | 1.4835298641951802 |
| `idx84_hand_r_pinky_abad_joint` | 0.0 | 0.1850049007113989 |
| `idx85_hand_r_pinky_pip_joint` | 0.0 | 1.4835298641951802 |
| **末端执行器（灵巧手 o12_t2 左手）** | | |
| `idx31_hand_l_thumb_roll_joint` | -0.9425 | 0.0 |
| `idx32_hand_l_thumb_abad_joint` | 0.0 | 1.3875 |
| `idx33_hand_l_thumb_mcp_joint` | -0.8273 | 0.0 |
| `idx34_hand_l_thumb_pip_joint` | -1.2915 | 0.0 |
| `idx36_hand_l_index_abad_joint` | -0.2618 | 0.2618 |
| `idx37_hand_l_index_mcp_joint` | 0.0 | 1.3526 |
| `idx38_hand_l_index_pip_joint` | 0.0 | 1.5307 |
| `idx40_hand_l_middle_abad_joint` | -0.2618 | 0.2618 |
| `idx41_hand_l_middle_mcp_joint` | 0.0 | 1.3579 |
| `idx42_hand_l_middle_pip_joint` | 0.0 | 1.8151 |
| `idx44_hand_l_ring_mcp_joint` | 0.0 | 1.5359 |
| `idx47_hand_l_pinky_mcp_joint` | 0.0 | 1.5359 |
**末端执行器（灵巧手 o12_t2 右手）** | | |
| `idx71_hand_r_thumb_roll_joint` | 0.0 | 0.9425 |
| `idx72_hand_r_thumb_abad_joint` | -1.3875 | 0.0 |
| `idx73_hand_r_thumb_mcp_joint` | -0.8273 | 0.0 |
| `idx74_hand_r_thumb_pip_joint` | -1.2915 | 0.0 |
| `idx76_hand_r_index_abad_joint` | -0.2618 | 0.2618 |
| `idx77_hand_r_index_mcp_joint` | 0.0 | 1.3526 |
| `idx78_hand_r_index_pip_joint` | 0.0 | 1.5307 |
| `idx80_hand_r_middle_abad_joint` | -0.2618 | 0.2618 |
| `idx81_hand_r_middle_mcp_joint` | 0.0 | 1.3579 |
| `idx82_hand_r_middle_pip_joint` | 0.0 | 1.8151 |
| `idx84_hand_r_ring_mcp_joint` | 0.0 | 1.5359 |
| `idx87_hand_r_pinky_mcp_joint` | 0.0 | 1.5359 |

- **错误处理**：
  - 如果 `joint_names`、`joint_positions`为空，返回 `ErrorCode::kInvalidInput`
  - 如果 `joint_positions` 中的值超出对应关节的限位范围，返回 `ErrorCode::kInvalidInput`
  - 如果配置解析器获取失败，返回 `ErrorCode::kRuntimeError`
  - 其他错误情况返回相应的错误码

- **示例**：

  ```cpp
  #include "gdk/gdk.h"
  #include <iostream>
  #include <chrono>
  #include <thread>
  #include <vector>
  #include <algorithm>

  using namespace agibot::gdk;

  // 控制参数
  const double CONTROL_PERIOD = 0.01;  // 控制周期（秒）
  const double RATE_HZ = 100.0;        // 发送频率（Hz）
  const double DURATION = 5.0;         // 控制持续时间（秒）

  class JointServoControlController {
  private:
      Robot robot_;

      double getJointPositionByName(const JointStates& joint_states, const std::string& joint_name) {
          for (const auto& state : joint_states.states) {
              if (state.name == joint_name) {
                  return state.motor_position;
              }
          }
          throw std::runtime_error("Joint name " + joint_name + " not found");
      }

      double interpolatePosition(double start_pos, double target_pos, double t) {
          return start_pos + t * (target_pos - start_pos);
      }

  public:
      void executeJointServoControl(const std::vector<std::string>& target_joint_names,
                                     const std::vector<double>& target_positions) {
          std::this_thread::sleep_for(std::chrono::seconds(1));  // 等待1秒

          // 获取当前关节状态
          JointStates current_joint_states;
          if (robot_.GetJointStates(current_joint_states) != GDKRes::kSuccess) {
              std::cout << "获取关节状态失败" << std::endl;
              return;
          }
          std::cout << "当前关节数量: " << current_joint_states.nums << std::endl;

          // 获取起始位置
          std::vector<double> start_positions;
          for (const auto& joint_name : target_joint_names) {
              try {
                  double pos = getJointPositionByName(current_joint_states, joint_name);
                  start_positions.push_back(pos);
                  std::cout << "关节 " << joint_name << " 当前位置: " << pos << " 弧度" << std::endl;
              } catch (const std::exception& e) {
                  std::cout << "错误: " << e.what() << std::endl;
                  return;
              }
          }

          // 计算步数
          int n_steps = static_cast<int>(DURATION * RATE_HZ);
          std::cout << "总步数: " << n_steps << ", 持续时间: " << DURATION << " 秒" << std::endl;

          // 执行轨迹
          double dt = 1.0 / RATE_HZ;
          auto start_time = std::chrono::steady_clock::now();

          for (int i = 0; i < n_steps; i++) {
              double t = static_cast<double>(i) / (n_steps - 1);

              // 创建关节位置伺服请求
              JointServoControlReq joint_position_servo_req;
              joint_position_servo_req.control_period = CONTROL_PERIOD;

              // 计算当前目标位置（线性插值）
              std::vector<double> current_positions;
              for (size_t j = 0; j < target_joint_names.size(); j++) {
                  double interp_pos = interpolatePosition(
                      start_positions[j], target_positions[j], t
                  );
                  current_positions.push_back(interp_pos);
              }

              joint_position_servo_req.joint_names = target_joint_names;
              joint_position_servo_req.joint_positions = current_positions;

              // 使用普通模式（enable_low_latency=false，默认值）
              auto res = robot_.JointServoControl(joint_position_servo_req);
              // 如需使用低延时模式，可传入 enable_low_latency=true：
              // auto res = robot_.JointServoControl(joint_position_servo_req, true);
              if (res != GDKRes::kSuccess) {
                  std::cout << "控制命令发送失败，步数: " << i << std::endl;
                  return;
              }

              // 控制发送频率
              auto elapsed = std::chrono::steady_clock::now() - start_time;
              auto expected_time = std::chrono::milliseconds(static_cast<int>((i + 1) * dt * 1000));
              auto sleep_time = expected_time - elapsed;
              if (sleep_time.count() > 0) {
                  std::this_thread::sleep_for(sleep_time);
              }
          }

          std::cout << "关节位置伺服控制完成" << std::endl;

          // 保持最终位置
          std::cout << "进入最终位置保持（Ctrl+C 结束）..." << std::endl;
          try {
              while (true) {
                  JointServoControlReq joint_position_servo_req;
                  joint_position_servo_req.control_period = CONTROL_PERIOD;
                  joint_position_servo_req.joint_names = target_joint_names;
                  joint_position_servo_req.joint_positions = target_positions;

                  // 使用普通模式（enable_low_latency=false，默认值）
                  auto res = robot_.JointServoControl(joint_position_servo_req);
                  // 如需使用低延时模式，可传入 enable_low_latency=true：
                  // auto res = robot_.JointServoControl(joint_position_servo_req, true);
                  if (res != GDKRes::kSuccess) {
                      std::cout << "保持位置失败" << std::endl;
                      break;
                  }

                  std::this_thread::sleep_for(std::chrono::milliseconds(static_cast<int>(dt * 1000)));
              }
          } catch (const std::exception& e) {
              std::cout << "已中断保持: " << e.what() << std::endl;
          }
      }
  };

  int main() {
      // 初始化GDK系统
      if (GDKInit() != GDKRes::kSuccess) {
          std::cout << "GDK初始化失败" << std::endl;
          return -1;
      }
      std::cout << "GDK初始化成功" << std::endl;

      Robot robot;
      std::cout << "Robot init" << std::endl;
      std::this_thread::sleep_for(std::chrono::seconds(2));

      // 获取当前关节状态
      JointStates current_joint_states;
      if (robot.GetJointStates(current_joint_states) != GDKRes::kSuccess) {
          std::cout << "获取关节状态失败" << std::endl;
          GDKRelease();
          return -1;
      }
      std::cout << "当前关节数量: " << current_joint_states.nums << std::endl;

      // 定义要控制的关节（示例：左臂前3个关节）
      std::vector<std::string> target_joint_names = {
          "idx21_arm_l_joint1",
          "idx22_arm_l_joint2",
          "idx23_arm_l_joint3"
      };

      // 获取当前位置作为起始位置（用于插值）
      std::vector<double> start_positions;
      for (const auto& joint_name : target_joint_names) {
          bool found = false;
          for (const auto& state : current_joint_states.states) {
              if (state.name == joint_name) {
                  start_positions.push_back(state.motor_position);
                  std::cout << "关节 " << joint_name << " 当前位置: " << state.motor_position << " 弧度" << std::endl;
                  found = true;
                  break;
              }
          }
          if (!found) {
              std::cout << "错误: 关节 " << joint_name << " 未找到" << std::endl;
              GDKRelease();
              return -1;
          }
      }

      // 设置目标角度（直接指定目标角度值，单位：弧度）
      std::vector<double> target_positions = {
          0.0,  // idx21_arm_l_joint1: 目标角度 0.0 弧度
          0.0,  // idx22_arm_l_joint2: 目标角度 0.0 弧度
          0.0   // idx23_arm_l_joint3: 目标角度 0.0 弧度
      };

      std::cout << "\n目标角度:" << std::endl;
      for (size_t i = 0; i < target_joint_names.size(); i++) {
          std::cout << "  " << target_joint_names[i] << ": " << target_positions[i] << " 弧度" << std::endl;
      }

      // 执行关节位置伺服控制
      JointServoControlController controller;
      controller.executeJointServoControl(
          target_joint_names, target_positions);

      // 释放GDK系统资源
      if (GDKRelease() != GDKRes::kSuccess) {
          std::cout << "GDK释放失败" << std::endl;
          return -1;
      }
      std::cout << "GDK释放成功" << std::endl;

      return 0;
  }
  ```

- **同时控制机械臂与末端的示例**：

  ```cpp
  #include "gdk/gdk.h"
  #include <iostream>
  #include <chrono>
  #include <thread>
  #include <vector>

  using namespace agibot::gdk;

  const double CONTROL_PERIOD = 0.01;
  const double RATE_HZ = 100.0;
  const double DURATION = 3.0;
  const double HOLD_DURATION = 0.5;    // 在 -0.785 或 0 处保持的时间（秒）
  const int NUM_CYCLES = 3;            // 往复运动次数

  static const std::vector<std::string> ARM_L_JOINT_NAMES = {
      "idx21_arm_l_joint1", "idx22_arm_l_joint2", "idx23_arm_l_joint3",
      "idx24_arm_l_joint4", "idx25_arm_l_joint5", "idx26_arm_l_joint6",
      "idx27_arm_l_joint7",
  };

  // 从 GetJointStates 的返回中按关节名取出位置列表
  std::vector<double> getArmPositionsByName(const JointStates& joint_states,
                                            const std::vector<std::string>& joint_names) {
      std::vector<double> positions;
      for (const auto& name : joint_names) {
          for (const auto& state : joint_states.states) {
              if (state.name == name) {
                  positions.push_back(state.motor_position);
                  break;
              }
          }
      }
      return positions;
  }

  // 从 GetEndState 的返回中取出指定侧末端的关节名列表和位置列表
  // use_left 为 true 取 left_end_state，为 false 取 right_end_state
  void getEENamesAndPositions(const DualEndState& end_state,
                              bool use_left,
                              std::vector<std::string>& names,
                              std::vector<double>& positions) {
      const EndState& state = use_left ? end_state.left_end_state : end_state.right_end_state;
      names = state.names;
      positions.clear();
      for (const auto& motor : state.end_states) {
          positions.push_back(motor.position);
      }
  }

  int main() {
      if (GDKInit() != GDKRes::kSuccess) {
          std::cout << "GDK初始化失败" << std::endl;
          return -1;
      }
      std::cout << "GDK初始化成功" << std::endl;

      Robot robot;
      std::this_thread::sleep_for(std::chrono::seconds(2));

      JointStates joint_states;
      if (robot.GetJointStates(joint_states) != GDKRes::kSuccess) {
          std::cout << "获取关节状态失败" << std::endl;
          GDKRelease();
          return -1;
      }

      DualEndState end_state;
      if (robot.GetEndState(end_state) != GDKRes::kSuccess) {
          std::cout << "获取末端状态失败" << std::endl;
          GDKRelease();
          return -1;
      }

      std::vector<std::string> ee_names;
      std::vector<double> ee_positions;
      getEENamesAndPositions(end_state, true, ee_names, ee_positions);  // 左侧末端

      std::vector<std::string> all_names = ARM_L_JOINT_NAMES;
      all_names.insert(all_names.end(), ee_names.begin(), ee_names.end());

      std::vector<double> arm_positions = getArmPositionsByName(joint_states, ARM_L_JOINT_NAMES);
      if (arm_positions.size() != ARM_L_JOINT_NAMES.size()) {
          std::cout << "左臂关节数量不匹配" << std::endl;
          GDKRelease();
          return -1;
      }

      // 机械臂按之前方式做小幅关节空间运动（来回），末端关节在 -0.785 和 0 之间往复运动
      std::vector<double> arm_start = arm_positions;                    // 机械臂初始姿态
      std::vector<double> arm_target = arm_positions;                   // 机械臂目标姿态（小幅偏移）
      for (auto& v : arm_target) v += 0.05;
      const double ee_low = -0.785;                                     // 末端下限
      const double ee_high = 0.0;                                       // 末端上限

      std::cout << "控制关节数: 机械臂 " << ARM_L_JOINT_NAMES.size()
                << " + 末端 " << ee_names.size() << " = " << all_names.size() << std::endl;
      std::cout << "机械臂将在关节空间 arm_start ↔ arm_target 之间运动，末端关节在 "
                << ee_low << " 和 " << ee_high << " 之间往复 " << NUM_CYCLES << " 次" << std::endl;

      int n_steps = static_cast<int>(DURATION * RATE_HZ);           // 单次移动的步数
      int hold_steps = static_cast<int>(HOLD_DURATION * RATE_HZ);   // 保持阶段的步数
      double dt = 1.0 / RATE_HZ;

      // 辅助函数：发送控制命令
      auto sendControlCommand = [&](const std::vector<double>& arm_vals, const std::vector<double>& ee_vals) -> bool {
          std::vector<double> current = arm_vals;
          current.insert(current.end(), ee_vals.begin(), ee_vals.end());
          JointServoControlReq req;
          req.control_period = CONTROL_PERIOD;
          req.joint_names = all_names;
          req.joint_positions = current;
          req.joint_velocities = std::vector<double>(current.size(), 0.0);
          return robot.JointServoControl(req) == GDKRes::kSuccess;
      };

      for (int cycle = 0; cycle < NUM_CYCLES; cycle++) {
          std::cout << "\n=== 周期 " << (cycle + 1) << "/" << NUM_CYCLES
                    << ": 机械臂 arm_start -> arm_target, 末端 " << ee_low << " -> " << ee_high << " ===" << std::endl;
          auto start_time = std::chrono::steady_clock::now();

          // 第一段：机械臂 arm_start -> arm_target，末端 ee_low -> ee_high
          for (int i = 0; i < n_steps; i++) {
              double t = (n_steps > 1) ? static_cast<double>(i) / (n_steps - 1) : 1.0;
              std::vector<double> current_arm;
              for (size_t j = 0; j < arm_start.size(); j++) {
                  current_arm.push_back(arm_start[j] + t * (arm_target[j] - arm_start[j]));
              }
              std::vector<double> current_ee(ee_names.size(), ee_low + t * (ee_high - ee_low));

              if (!sendControlCommand(current_arm, current_ee)) {
                  std::cout << "发送失败，周期=" << (cycle + 1) << ", 阶段=0->1, 步数=" << i << std::endl;
                  GDKRelease();
                  return -1;
              }

              auto elapsed = std::chrono::steady_clock::now() - start_time;
              auto expected_ms = static_cast<int>((i + 1) * dt * 1000);
              auto sleep_time = std::chrono::milliseconds(expected_ms) - elapsed;
              if (sleep_time.count() > 0) {
                  std::this_thread::sleep_for(sleep_time);
              }
          }

          // 第二段：在 arm_target / ee_high 处保持
          std::cout << "=== 周期 " << (cycle + 1) << "/" << NUM_CYCLES
                    << ": 在 arm_target / " << ee_high << " 处保持 " << HOLD_DURATION << " 秒 ===" << std::endl;
          start_time = std::chrono::steady_clock::now();
          std::vector<double> current_arm = arm_target;
          std::vector<double> current_ee(ee_names.size(), ee_high);

          for (int i = 0; i < hold_steps; i++) {
              if (!sendControlCommand(current_arm, current_ee)) {
                  std::cout << "发送失败，周期=" << (cycle + 1) << ", 阶段=保持@1, 步数=" << i << std::endl;
                  GDKRelease();
                  return -1;
              }

              auto elapsed = std::chrono::steady_clock::now() - start_time;
              auto expected_ms = static_cast<int>((i + 1) * dt * 1000);
              auto sleep_time = std::chrono::milliseconds(expected_ms) - elapsed;
              if (sleep_time.count() > 0) {
                  std::this_thread::sleep_for(sleep_time);
              }
          }

          // 第三段：机械臂 arm_target -> arm_start，末端 ee_high -> ee_low
          std::cout << "=== 周期 " << (cycle + 1) << "/" << NUM_CYCLES
                    << ": 机械臂 arm_target -> arm_start, 末端 " << ee_high << " -> " << ee_low << " ===" << std::endl;
          start_time = std::chrono::steady_clock::now();

          for (int i = 0; i < n_steps; i++) {
              double t = (n_steps > 1) ? static_cast<double>(i) / (n_steps - 1) : 1.0;
              std::vector<double> current_arm;
              for (size_t j = 0; j < arm_target.size(); j++) {
                  current_arm.push_back(arm_target[j] + t * (arm_start[j] - arm_target[j]));
              }
              std::vector<double> current_ee(ee_names.size(), ee_high + t * (ee_low - ee_high));

              if (!sendControlCommand(current_arm, current_ee)) {
                  std::cout << "发送失败，周期=" << (cycle + 1) << ", 阶段=1->0, 步数=" << i << std::endl;
                  GDKRelease();
                  return -1;
              }

              auto elapsed = std::chrono::steady_clock::now() - start_time;
              auto expected_ms = static_cast<int>((i + 1) * dt * 1000);
              auto sleep_time = std::chrono::milliseconds(expected_ms) - elapsed;
              if (sleep_time.count() > 0) {
                  std::this_thread::sleep_for(sleep_time);
              }
          }

          // 第四段：在 arm_start / ee_low 处保持
          std::cout << "=== 周期 " << (cycle + 1) << "/" << NUM_CYCLES
                    << ": 在 arm_start / " << ee_low << " 处保持 " << HOLD_DURATION << " 秒 ===" << std::endl;
          start_time = std::chrono::steady_clock::now();
          current_arm = arm_start;
          current_ee = std::vector<double>(ee_names.size(), ee_low);

          for (int i = 0; i < hold_steps; i++) {
              if (!sendControlCommand(current_arm, current_ee)) {
                  std::cout << "发送失败，周期=" << (cycle + 1) << ", 阶段=保持@0, 步数=" << i << std::endl;
                  GDKRelease();
                  return -1;
              }

              auto elapsed = std::chrono::steady_clock::now() - start_time;
              auto expected_ms = static_cast<int>((i + 1) * dt * 1000);
              auto sleep_time = std::chrono::milliseconds(expected_ms) - elapsed;
              if (sleep_time.count() > 0) {
                  std::this_thread::sleep_for(sleep_time);
              }
          }
      }

      std::cout << "\n机械臂 arm_start↔arm_target、末端 " << ee_low << "↔" << ee_high << " 往复控制结束" << std::endl;

      if (GDKRelease() != GDKRes::kSuccess) {
          std::cout << "GDK释放失败" << std::endl;
          return -1;
      }
      std::cout << "GDK释放成功" << std::endl;
      return 0;
  }
  ```

#### 12. `MoveHeadJointServo()`

- **功能**：头部关节位置伺服控制接口，需要以100hz的控制频率进行控制，支持正常模式和低延时模式，默认使用正常模式。
- **注意**：低延时模式无碰撞保护，使用时注意安全。
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `positions` | `const std::vector<double>&` | 头部关节位置列表（弧度），按照"idx11_head_joint1", "idx12_head_joint2", "idx13_head_joint3"顺序 |
| `control_period` | `const double` | 控制周期（秒），建议比控制频率稍大 |
| `enable_low_latency` | `const bool` | 是否启用低延时模式，默认为`false` |

**参数说明**：
- `positions` 长度必须为3
- `positions` 中的值必须在对应关节的限位范围内（见下方关节限位值说明），否则返回 `ErrorCode::kInvalidInput`
- `control_period` 表示控制周期，单位为秒，建议比控制频率稍大
- `enable_low_latency` 用于选择控制通道，低延时模式适用于对实时性要求更高的场景

#### 关节限位值说明

头部关节的限位值（单位：弧度）如下：

| 关节名称 | 最小值 | 最大值 |
| :--- | :--- | :--- |
| `idx11_head_joint1` | -1.570970 | 1.570970 |
| `idx12_head_joint2` | -0.349240 | 0.349240 |
| `idx13_head_joint3` | -0.534773 | 0.534773 |

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`

- **错误处理**：
  - 如果 `positions` 的长度不为3，返回 `ErrorCode::kInvalidInput`
  - 如果 `positions` 中的值超出对应关节的限位范围，返回 `ErrorCode::kInvalidInput`
  - 其他错误情况返回相应的错误码

- **示例**：

  ```cpp
  #include "gdk/gdk.h"
  #include <iostream>
  #include <chrono>
  #include <thread>
  #include <vector>
  #include <algorithm>

  using namespace agibot::gdk;

  // 控制参数
  const double CONTROL_PERIOD = 0.01;  // 控制周期（秒）
  const double RATE_HZ = 100.0;        // 发送频率（Hz）
  const double DURATION = 5.0;         // 控制持续时间（秒）

  class HeadJointServoController {
  private:
      Robot robot_;

      double getJointPositionByName(const JointStates& joint_states, const std::string& joint_name) {
          for (const auto& state : joint_states.states) {
              if (state.name == joint_name) {
                  return state.motor_position;
              }
          }
          throw std::runtime_error("Joint name " + joint_name + " not found");
      }

      double interpolatePosition(double start_pos, double target_pos, double t) {
          return start_pos + t * (target_pos - start_pos);
      }

  public:
      void executeHeadJointServoControl(const std::vector<double>& target_positions) {
          std::this_thread::sleep_for(std::chrono::seconds(1));  // 等待1秒

          // 获取当前关节状态
          JointStates current_joint_states;
          if (robot_.GetJointStates(current_joint_states) != GDKRes::kSuccess) {
              std::cout << "获取关节状态失败" << std::endl;
              return;
          }

          // 获取起始位置
          std::vector<std::string> head_joint_names = {
              "idx11_head_joint1", "idx12_head_joint2", "idx13_head_joint3"
          };
          std::vector<double> start_positions;
          for (const auto& joint_name : head_joint_names) {
              try {
                  double pos = getJointPositionByName(current_joint_states, joint_name);
                  start_positions.push_back(pos);
                  std::cout << "关节 " << joint_name << " 当前位置: " << pos << " 弧度" << std::endl;
              } catch (const std::exception& e) {
                  std::cout << "错误: " << e.what() << std::endl;
                  return;
              }
          }

          // 计算步数
          int n_steps = static_cast<int>(DURATION * RATE_HZ);
          std::cout << "总步数: " << n_steps << ", 持续时间: " << DURATION << " 秒" << std::endl;

          // 执行轨迹
          double dt = 1.0 / RATE_HZ;
          auto start_time = std::chrono::steady_clock::now();

          for (int i = 0; i < n_steps; i++) {
              double t = static_cast<double>(i) / (n_steps - 1);

              // 计算当前目标位置（线性插值）
              std::vector<double> current_positions;
              for (size_t j = 0; j < 3; j++) {
                  double interp_pos = interpolatePosition(
                      start_positions[j], target_positions[j], t
                  );
                  current_positions.push_back(interp_pos);
              }

              // 使用普通模式（enable_low_latency=false，默认值）
              auto res = robot_.MoveHeadJointServo(
                  current_positions, CONTROL_PERIOD);
              // 如需使用低延时模式，可传入 enable_low_latency=true：
              // auto res = robot_.MoveHeadJointServo(
              //     current_positions, target_velocities, CONTROL_PERIOD, true
              // );
              if (res != GDKRes::kSuccess) {
                  std::cout << "控制命令发送失败，步数: " << i << std::endl;
                  return;
              }

              // 控制发送频率
              auto elapsed = std::chrono::steady_clock::now() - start_time;
              auto expected_time = std::chrono::milliseconds(static_cast<int>((i + 1) * dt * 1000));
              auto sleep_time = expected_time - elapsed;
              if (sleep_time.count() > 0) {
                  std::this_thread::sleep_for(sleep_time);
              }
          }

          std::cout << "头部关节位置伺服控制完成" << std::endl;

          // 保持最终位置
          std::cout << "进入最终位置保持（Ctrl+C 结束）..." << std::endl;
          try {
              while (true) {
                  // 使用普通模式（enable_low_latency=false，默认值）
                  auto res = robot_.MoveHeadJointServo(
                      target_positions, CONTROL_PERIOD);
                  // 如需使用低延时模式，可传入 enable_low_latency=true：
                  // auto res = robot_.MoveHeadJointServo(
                  //     target_positions, target_velocities, CONTROL_PERIOD, true
                  // );
                  if (res != GDKRes::kSuccess) {
                      std::cout << "保持位置失败" << std::endl;
                      break;
                  }

                  std::this_thread::sleep_for(std::chrono::milliseconds(static_cast<int>(dt * 1000)));
              }
          } catch (const std::exception& e) {
              std::cout << "已中断保持: " << e.what() << std::endl;
          }
      }
  };

  int main() {
      // 初始化GDK系统
      if (GDKInit() != GDKRes::kSuccess) {
          std::cout << "GDK初始化失败" << std::endl;
          return -1;
      }
      std::cout << "GDK初始化成功" << std::endl;

      Robot robot;
      std::cout << "Robot init" << std::endl;
      std::this_thread::sleep_for(std::chrono::seconds(2));

      // 获取当前关节状态
      JointStates current_joint_states;
      if (robot.GetJointStates(current_joint_states) != GDKRes::kSuccess) {
          std::cout << "获取关节状态失败" << std::endl;
          GDKRelease();
          return -1;
      }

      // 定义目标位置（示例：头部关节）
      std::vector<double> target_positions = {
          0.0,  // idx11_head_joint1: 目标角度 0.0 弧度
          0.0,  // idx12_head_joint2: 目标角度 0.0 弧度
          0.0   // idx13_head_joint3: 目标角度 0.0 弧度
      };

      std::cout << "\n目标角度:" << std::endl;
      std::vector<std::string> head_joint_names = {
          "idx11_head_joint1", "idx12_head_joint2", "idx13_head_joint3"
      };
      for (size_t i = 0; i < head_joint_names.size(); i++) {
          std::cout << "  " << head_joint_names[i] << ": " << target_positions[i] << " 弧度" << std::endl;
      }

      // 执行头部关节位置伺服控制
      HeadJointServoController controller;
      controller.executeHeadJointServoControl(target_positions);

      // 释放GDK系统资源
      if (GDKRelease() != GDKRes::kSuccess) {
          std::cout << "GDK释放失败" << std::endl;
          return -1;
      }
      std::cout << "GDK释放成功" << std::endl;

      return 0;
  }
  ```

#### 13. `MoveWaistJointServo()`

- **功能**：腰部关节位置伺服控制接口，需要以100hz的控制频率进行控制，支持正常模式和低延时模式，默认使用正常模式。
- **注意**：低延时模式无碰撞保护，使用时注意安全。
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `positions` | `const std::vector<double>&` | 腰部关节位置列表（弧度），按照"idx01_body_joint1", "idx02_body_joint2", "idx03_body_joint3", "idx04_body_joint4", "idx05_body_joint5"顺序 |
| `control_period` | `const double` | 控制周期（秒），建议比控制频率稍大 |
| `enable_low_latency` | `const bool` | 是否启用低延时模式，默认为`false` |

**参数说明**：
- `positions` 的长度必须为5
- `positions` 中的值必须在对应关节的限位范围内（见下方关节限位值说明），否则返回 `ErrorCode::kInvalidInput`
- `control_period` 表示控制周期，单位为秒，建议比控制频率稍大
- `enable_low_latency` 用于选择控制通道，低延时模式适用于对实时性要求更高的场景

#### 关节限位值说明

腰部关节的限位值（单位：弧度）如下：

| 关节名称 | 最小值 | 最大值 |
| :--- | :--- | :--- |
| `idx01_body_joint1` | -1.082104 | 0.000174 |
| `idx02_body_joint2` | -0.000174 | 2.652900 |
| `idx03_body_joint3` | -1.919862 | 1.570970 |
| `idx04_body_joint4` | -0.436332 | 0.436332 |
| `idx05_body_joint5` | -3.045599 | 3.045599 |

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`

- **错误处理**：
  - 如果 `positions` 的长度不为5，返回 `ErrorCode::kInvalidInput`
  - 如果 `positions` 中的值超出对应关节的限位范围，返回 `ErrorCode::kInvalidInput`
  - 其他错误情况返回相应的错误码

- **示例**：

  ```cpp
  #include "gdk/gdk.h"
  #include <iostream>
  #include <chrono>
  #include <thread>
  #include <vector>
  #include <algorithm>

  using namespace agibot::gdk;

  // 控制参数
  const double CONTROL_PERIOD = 0.01;  // 控制周期（秒）
  const double RATE_HZ = 100.0;        // 发送频率（Hz）
  const double DURATION = 5.0;         // 控制持续时间（秒）

  class WaistJointServoController {
  private:
      Robot robot_;

      double getJointPositionByName(const JointStates& joint_states, const std::string& joint_name) {
          for (const auto& state : joint_states.states) {
              if (state.name == joint_name) {
                  return state.motor_position;
              }
          }
          throw std::runtime_error("Joint name " + joint_name + " not found");
      }

      double interpolatePosition(double start_pos, double target_pos, double t) {
          return start_pos + t * (target_pos - start_pos);
      }

  public:
      void executeWaistJointServoControl(const std::vector<double>& target_positions) {
          std::this_thread::sleep_for(std::chrono::seconds(1));  // 等待1秒

          // 获取当前关节状态
          JointStates current_joint_states;
          if (robot_.GetJointStates(current_joint_states) != GDKRes::kSuccess) {
              std::cout << "获取关节状态失败" << std::endl;
              return;
          }

          // 获取起始位置
          std::vector<std::string> waist_joint_names = {
              "idx01_body_joint1", "idx02_body_joint2", "idx03_body_joint3",
              "idx04_body_joint4", "idx05_body_joint5"
          };
          std::vector<double> start_positions;
          for (const auto& joint_name : waist_joint_names) {
              try {
                  double pos = getJointPositionByName(current_joint_states, joint_name);
                  start_positions.push_back(pos);
                  std::cout << "关节 " << joint_name << " 当前位置: " << pos << " 弧度" << std::endl;
              } catch (const std::exception& e) {
                  std::cout << "错误: " << e.what() << std::endl;
                  return;
              }
          }

          // 计算步数
          int n_steps = static_cast<int>(DURATION * RATE_HZ);
          std::cout << "总步数: " << n_steps << ", 持续时间: " << DURATION << " 秒" << std::endl;

          // 执行轨迹
          double dt = 1.0 / RATE_HZ;
          auto start_time = std::chrono::steady_clock::now();

          for (int i = 0; i < n_steps; i++) {
              double t = static_cast<double>(i) / (n_steps - 1);

              // 计算当前目标位置（线性插值）
              std::vector<double> current_positions;
              for (size_t j = 0; j < 5; j++) {
                  double interp_pos = interpolatePosition(
                      start_positions[j], target_positions[j], t
                  );
                  current_positions.push_back(interp_pos);
              }

              // 使用普通模式（enable_low_latency=false，默认值）
              auto res = robot_.MoveWaistJointServo(
                  current_positions, CONTROL_PERIOD);
              // 如需使用低延时模式，可传入 enable_low_latency=true：
              // auto res = robot_.MoveWaistJointServo(
              //     current_positions, target_velocities, CONTROL_PERIOD, true
              // );
              if (res != GDKRes::kSuccess) {
                  std::cout << "控制命令发送失败，步数: " << i << std::endl;
                  return;
              }

              // 控制发送频率
              auto elapsed = std::chrono::steady_clock::now() - start_time;
              auto expected_time = std::chrono::milliseconds(static_cast<int>((i + 1) * dt * 1000));
              auto sleep_time = expected_time - elapsed;
              if (sleep_time.count() > 0) {
                  std::this_thread::sleep_for(sleep_time);
              }
          }

          std::cout << "腰部关节位置伺服控制完成" << std::endl;

          // 保持最终位置
          std::cout << "进入最终位置保持（Ctrl+C 结束）..." << std::endl;
          try {
              while (true) {
                  // 使用普通模式（enable_low_latency=false，默认值）
                  auto res = robot_.MoveWaistJointServo(
                      target_positions, CONTROL_PERIOD);
                  // 如需使用低延时模式，可传入 enable_low_latency=true：
                  // auto res = robot_.MoveWaistJointServo(
                  //     target_positions, target_velocities, CONTROL_PERIOD, true
                  // );
                  if (res != GDKRes::kSuccess) {
                      std::cout << "保持位置失败" << std::endl;
                      break;
                  }

                  std::this_thread::sleep_for(std::chrono::milliseconds(static_cast<int>(dt * 1000)));
              }
          } catch (const std::exception& e) {
              std::cout << "已中断保持: " << e.what() << std::endl;
          }
      }
  };

  int main() {
      // 初始化GDK系统
      if (GDKInit() != GDKRes::kSuccess) {
          std::cout << "GDK初始化失败" << std::endl;
          return -1;
      }
      std::cout << "GDK初始化成功" << std::endl;

      Robot robot;
      std::cout << "Robot init" << std::endl;
      std::this_thread::sleep_for(std::chrono::seconds(2));

      // 获取当前关节状态
      JointStates current_joint_states;
      if (robot.GetJointStates(current_joint_states) != GDKRes::kSuccess) {
          std::cout << "获取关节状态失败" << std::endl;
          GDKRelease();
          return -1;
      }

      // 定义目标位置（示例：腰部关节）
      std::vector<double> target_positions = {
          0.0,  // idx01_body_joint1: 目标角度 0.0 弧度
          0.0,  // idx02_body_joint2: 目标角度 0.0 弧度
          0.0,  // idx03_body_joint3: 目标角度 0.0 弧度
          0.0,  // idx04_body_joint4: 目标角度 0.0 弧度
          0.0   // idx05_body_joint5: 目标角度 0.0 弧度
      };

      std::cout << "\n目标角度:" << std::endl;
      std::vector<std::string> waist_joint_names = {
          "idx01_body_joint1", "idx02_body_joint2", "idx03_body_joint3",
          "idx04_body_joint4", "idx05_body_joint5"
      };
      for (size_t i = 0; i < waist_joint_names.size(); i++) {
          std::cout << "  " << waist_joint_names[i] << ": " << target_positions[i] << " 弧度" << std::endl;
      }

      // 执行腰部关节位置伺服控制
      WaistJointServoController controller;
      controller.executeWaistJointServoControl(target_positions);

      // 释放GDK系统资源
      if (GDKRelease() != GDKRes::kSuccess) {
          std::cout << "GDK释放失败" << std::endl;
          return -1;
      }
      std::cout << "GDK释放成功" << std::endl;

      return 0;
  }
  ```

#### 14. `MoveArmJointServo()`

- **功能**：手臂关节位置伺服控制接口，需要以100hz的控制频率进行控制，支持正常模式和低延时模式，默认使用正常模式。
- **注意**：低延时模式无碰撞保护，使用时注意安全。
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `positions` | `const std::vector<double>&` | 手臂关节位置列表（弧度），按照"idx21_arm_l_joint1", "idx22_arm_l_joint2", "idx23_arm_l_joint3", "idx24_arm_l_joint4", "idx25_arm_l_joint5", "idx26_arm_l_joint6", "idx27_arm_l_joint7", "idx61_arm_r_joint1", "idx62_arm_r_joint2", "idx63_arm_r_joint3", "idx64_arm_r_joint4", "idx65_arm_r_joint5", "idx66_arm_r_joint6", "idx67_arm_r_joint7"顺序 |
| `control_period` | `const double` | 控制周期（秒），建议比控制频率稍大 |
| `control_group` | `const int` | 控制组，0表示控制左臂，1表示控制右臂，2表示控制双臂 |
| `enable_low_latency` | `const bool` | 是否启用低延时模式，默认为`false` |

**参数说明**：
- `positions` 的长度为7(左臂或右臂)或14(双臂)
- `positions` 中的值必须在对应关节的限位范围内（见下方关节限位值说明），否则返回 `ErrorCode::kInvalidInput`
- `control_period` 表示控制周期，单位为秒，建议比控制频率稍大
- `control_group` 表示控制组，0表示控制左臂，1表示控制右臂，2表示控制双臂
- `enable_low_latency` 用于选择控制通道，低延时模式适用于对实时性要求更高的场景

#### 关节限位值说明

手臂关节的限位值（单位：弧度）如下：

| 关节名称 | 最小值 | 最大值 |
| :--- | :--- | :--- |
| `idx21_arm_l_joint1` | -3.071796 | 3.071796 |
| `idx22_arm_l_joint2` | -2.059505 | 2.059505 |
| `idx23_arm_l_joint3` | -3.071796 | 3.071796 |
| `idx24_arm_l_joint4` | -2.495838 | 1.012308 |
| `idx25_arm_l_joint5` | -3.071796 | 3.071796 |
| `idx26_arm_l_joint6` | -1.012308 | 1.012308 |
| `idx27_arm_l_joint7` | -1.535907 | 1.535907 |
| `idx61_arm_r_joint1` | -3.071796 | 3.071796 |
| `idx62_arm_r_joint2` | -2.059505 | 2.059505 |
| `idx63_arm_r_joint3` | -3.071796 | 3.071796 |
| `idx64_arm_r_joint4` | -2.495838 | 1.012308 |
| `idx65_arm_r_joint5` | -3.071796 | 3.071796 |
| `idx66_arm_r_joint6` | -1.012308 | 1.012308 |
| `idx67_arm_r_joint7` | -1.535907 | 1.535907 |

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`

- **错误处理**：
  - 如果 `positions` 的长度不为7(左臂或右臂)或14(双臂)，返回 `ErrorCode::kInvalidInput`
  - 如果 `positions` 中的值超出对应关节的限位范围，返回 `ErrorCode::kInvalidInput`
  - 其他错误情况返回相应的错误码

- **示例**：

  ```cpp
  #include "gdk/gdk.h"
  #include <iostream>
  #include <chrono>
  #include <thread>
  #include <vector>
  #include <algorithm>

  using namespace agibot::gdk;

  // 控制参数
  const double CONTROL_PERIOD = 0.01;  // 控制周期（秒）
  const double RATE_HZ = 100.0;        // 发送频率（Hz）
  const double DURATION = 5.0;         // 控制持续时间（秒）

  class ArmJointServoController {
  private:
      Robot robot_;

      double getJointPositionByName(const JointStates& joint_states, const std::string& joint_name) {
          for (const auto& state : joint_states.states) {
              if (state.name == joint_name) {
                  return state.motor_position;
              }
          }
          throw std::runtime_error("Joint name " + joint_name + " not found");
      }

      double interpolatePosition(double start_pos, double target_pos, double t) {
          return start_pos + t * (target_pos - start_pos);
      }

  public:
      void executeArmJointServoControl(const std::vector<double>& target_positions, const int control_group) {
          std::this_thread::sleep_for(std::chrono::seconds(1));  // 等待1秒

          // 获取当前关节状态
          JointStates current_joint_states;
          if (robot_.GetJointStates(current_joint_states) != GDKRes::kSuccess) {
              std::cout << "获取关节状态失败" << std::endl;
              return;
          }

          // 获取起始位置
          std::vector<std::string> arm_joint_names = {
              "idx21_arm_l_joint1", "idx22_arm_l_joint2", "idx23_arm_l_joint3",
              "idx24_arm_l_joint4", "idx25_arm_l_joint5", "idx26_arm_l_joint6",
              "idx27_arm_l_joint7",  // 左臂7个关节
              "idx61_arm_r_joint1", "idx62_arm_r_joint2", "idx63_arm_r_joint3",
              "idx64_arm_r_joint4", "idx65_arm_r_joint5", "idx66_arm_r_joint6",
              "idx67_arm_r_joint7"   // 右臂7个关节
          };
          std::vector<double> start_positions;
          for (const auto& joint_name : arm_joint_names) {
              try {
                  double pos = getJointPositionByName(current_joint_states, joint_name);
                  start_positions.push_back(pos);
                  std::cout << "关节 " << joint_name << " 当前位置: " << pos << " 弧度" << std::endl;
              } catch (const std::exception& e) {
                  std::cout << "错误: " << e.what() << std::endl;
                  return;
              }
          }

          // 计算步数
          int n_steps = static_cast<int>(DURATION * RATE_HZ);
          std::cout << "总步数: " << n_steps << ", 持续时间: " << DURATION << " 秒" << std::endl;

          // 执行轨迹
          double dt = 1.0 / RATE_HZ;
          auto start_time = std::chrono::steady_clock::now();

          for (int i = 0; i < n_steps; i++) {
              double t = static_cast<double>(i) / (n_steps - 1);

              // 计算当前目标位置（线性插值）
              std::vector<double> current_positions;
              for (size_t j = 0; j < 14; j++) {
                  double interp_pos = interpolatePosition(
                      start_positions[j], target_positions[j], t
                  );
                  current_positions.push_back(interp_pos);
              }

              // 使用普通模式（enable_low_latency=false，默认值）
              auto res = robot_.MoveArmJointServo(
                  current_positions, CONTROL_PERIOD, control_group
              );
              // 如需使用低延时模式，可传入 enable_low_latency=true：
              // auto res = robot_.MoveArmJointServo(
              //     current_positions, CONTROL_PERIOD, control_group, true
              // );
              if (res != GDKRes::kSuccess) {
                  std::cout << "控制命令发送失败，步数: " << i << std::endl;
                  return;
              }

              // 控制发送频率
              auto elapsed = std::chrono::steady_clock::now() - start_time;
              auto expected_time = std::chrono::milliseconds(static_cast<int>((i + 1) * dt * 1000));
              auto sleep_time = expected_time - elapsed;
              if (sleep_time.count() > 0) {
                  std::this_thread::sleep_for(sleep_time);
              }
          }

          std::cout << "手臂关节位置伺服控制完成" << std::endl;

          // 保持最终位置
          std::cout << "进入最终位置保持（Ctrl+C 结束）..." << std::endl;
          try {
              while (true) {
                  // 使用普通模式（enable_low_latency=false，默认值）
                  auto res = robot_.MoveArmJointServo(
                      target_positions, CONTROL_PERIOD, control_group
                  );
                  // 如需使用低延时模式，可传入 enable_low_latency=true：
                  // auto res = robot_.MoveArmJointServo(
                  //     target_positions, CONTROL_PERIOD, control_group, true
                  // );
                  if (res != GDKRes::kSuccess) {
                      std::cout << "保持位置失败" << std::endl;
                      break;
                  }

                  std::this_thread::sleep_for(std::chrono::milliseconds(static_cast<int>(dt * 1000)));
              }
          } catch (const std::exception& e) {
              std::cout << "已中断保持: " << e.what() << std::endl;
          }
      }
  };

  int main() {
      // 初始化GDK系统
      if (GDKInit() != GDKRes::kSuccess) {
          std::cout << "GDK初始化失败" << std::endl;
          return -1;
      }
      std::cout << "GDK初始化成功" << std::endl;

      Robot robot;
      std::cout << "Robot init" << std::endl;
      std::this_thread::sleep_for(std::chrono::seconds(2));

      // 获取当前关节状态
      JointStates current_joint_states;
      if (robot.GetJointStates(current_joint_states) != GDKRes::kSuccess) {
          std::cout << "获取关节状态失败" << std::endl;
          GDKRelease();
          return -1;
      }

      // 定义目标位置（示例：手臂关节）
      std::vector<double> target_positions = {
          0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,  // 左臂7个关节
          0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0   // 右臂7个关节
      };

      std::cout << "\n目标角度:" << std::endl;
      std::vector<std::string> arm_joint_names = {
          "idx21_arm_l_joint1", "idx22_arm_l_joint2", "idx23_arm_l_joint3",
          "idx24_arm_l_joint4", "idx25_arm_l_joint5", "idx26_arm_l_joint6",
          "idx27_arm_l_joint7",  // 左臂7个关节
          "idx61_arm_r_joint1", "idx62_arm_r_joint2", "idx63_arm_r_joint3",
          "idx64_arm_r_joint4", "idx65_arm_r_joint5", "idx66_arm_r_joint6",
          "idx67_arm_r_joint7"   // 右臂7个关节
      };
      for (size_t i = 0; i < arm_joint_names.size(); i++) {
          std::cout << "  " << arm_joint_names[i] << ": " << target_positions[i] << " 弧度" << std::endl;
      }

      // 执行手臂关节位置伺服控制
      ArmJointServoController controller;
      controller.executeArmJointServoControl(target_positions, 2);

      // 释放GDK系统资源
      if (GDKRelease() != GDKRes::kSuccess) {
          std::cout << "GDK释放失败" << std::endl;
          return -1;
      }
      std::cout << "GDK释放成功" << std::endl;

      return 0;
  }
  ```

#### 15. `EndEffectorPoseControl()`

- **功能**：末端执行器位姿控制接口
- **注意**：该接口要求发送端以50hz频率发布控制命令，不允许阶越信号；该接口无碰撞检测，注意使用时环境。
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `end_pose` | `const EndEffectorPose&` | 末端执行器位姿控制对象 |

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`

#### EndEffectorPose对象详细说明

**EndEffectorPose结构体包含以下成员**：

| 成员名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `life_time` | `double` | 控制生命周期 | 秒 |
| `group` | `int32_t` | 控制组，0: 未知，4: 左臂，8: 右臂，12: 双臂 | 无单位 |
| `left_end_effector_pose` | `Pose` | 左末端执行器位姿（base_link坐标系下） | 位姿 |
| `right_end_effector_pose` | `Pose` | 右末端执行器位姿（base_link坐标系下） | 位姿 |

```cpp
struct EndEffectorPose {
  double life_time{0.0};
  int32_t group{0};
  Pose left_end_effector_pose{};
  Pose right_end_effector_pose{};
};
```

**Pose结构体**：

| 成员名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `position` | `Position` | 位置信息 | 米 |
| `orientation` | `Orientation` | 方向信息 | 四元数 |

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

- **示例**：

  ```cpp
  #include "gdk/gdk.h"
  #include <iostream>
  #include <chrono>
  #include <thread>
  #include <cmath>
  #include <vector>
  #include <algorithm>

  using namespace agibot::gdk;

  const std::string LEFT_NAME = "arm_l_end_link";
  const std::string RIGHT_NAME = "arm_r_end_link";
  const int32_t CONTROL_GROUP = 12;  // kBothArms

  const Pose TARGET_LEFT = {
      {0.516, 0.433, 1.081},  // position
      {0.382, -0.146, 0.663, 0.626}  // orientation
  };

  const Pose TARGET_RIGHT = {
      {0.579, -0.306, 1.158},  // position
      {0.320, 0.655, 0.651, 0.206}  // orientation
  };

  const double MAX_STEP_CM = 0.1;  // 最大步长（厘米）
  const double LIFETIME = 0.02;    // 生命周期（秒）
  const double RATE_HZ = 50.0;     // 发送频率（Hz）
  const bool HOLD_FINAL = true;    // 是否保持最终位姿

  class EndEffectorController {
  private:
      Robot robot_;

      void slerp(const double q0[4], const double q1[4], double t, double result[4]) {
          double dot = q0[0]*q1[0] + q0[1]*q1[1] + q0[2]*q1[2] + q0[3]*q1[3];

          // 如果点积为负，取反q1以确保最短路径
          if (dot < 0.0) {
              dot = -dot;
              for (int i = 0; i < 4; i++) {
                  result[i] = q0[i] + t * (-q1[i] - q0[i]);
              }
          } else {
              for (int i = 0; i < 4; i++) {
                  result[i] = q0[i] + t * (q1[i] - q0[i]);
              }
          }

          // 限制点积范围
          dot = std::clamp(dot, -1.0, 1.0);

          if (dot > 0.9995) {
              // 线性插值
              double norm = 0.0;
              for (int i = 0; i < 4; i++) {
                  norm += result[i] * result[i];
              }
              norm = std::sqrt(norm);
              if (norm > 0.0) {
                  for (int i = 0; i < 4; i++) {
                      result[i] /= norm;
                  }
              }
          } else {
              // 球面线性插值
              double theta_0 = std::acos(dot);
              double sin_theta_0 = std::sin(theta_0);
              double theta = theta_0 * t;
              double sin_theta = std::sin(theta);
              double s0 = std::cos(theta) - dot * sin_theta / sin_theta_0;
              double s1 = sin_theta / sin_theta_0;

              for (int i = 0; i < 4; i++) {
                  result[i] = s0 * q0[i] + s1 * q1[i];
              }
          }
      }

      double distanceBetweenPoints(const Vector3& p1, const Vector3& p2) {
          double dx = p2.x - p1.x;
          double dy = p2.y - p1.y;
          double dz = p2.z - p1.z;
          return std::sqrt(dx*dx + dy*dy + dz*dz);
      }

      int calculateNSteps(const Vector3& start, const Vector3& goal, double max_step_cm) {
          double dist_cm = distanceBetweenPoints(start, goal) * 100.0;
          return std::max(static_cast<int>(std::ceil(dist_cm / max_step_cm)), 1);
      }

      std::vector<Pose> planTrajectory(const Pose& start, const Pose& goal, int n_steps) {
          std::vector<Pose> trajectory;

          for (int i = 0; i < n_steps; i++) {
              double t = static_cast<double>(i) / (n_steps - 1);
              Pose pose;

              // 位置线性插值
              pose.position.x = start.position.x + t * (goal.position.x - start.position.x);
              pose.position.y = start.position.y + t * (goal.position.y - start.position.y);
              pose.position.z = start.position.z + t * (goal.position.z - start.position.z);

              // 四元数SLERP插值
              double q0[4] = {start.orientation.x, start.orientation.y, start.orientation.z, start.orientation.w};
              double q1[4] = {goal.orientation.x, goal.orientation.y, goal.orientation.z, goal.orientation.w};
              double result[4];
              slerp(q0, q1, t, result);

              pose.orientation.x = result[0];
              pose.orientation.y = result[1];
              pose.orientation.z = result[2];
              pose.orientation.w = result[3];

              trajectory.push_back(pose);
          }

          return trajectory;
      }

      Pose findPoseByName(const std::vector<std::string>& frame_names,
                         const std::vector<Pose>& frame_poses,
                         const std::string& target_name) {
          for (size_t i = 0; i < frame_names.size(); i++) {
              if (frame_names[i] == target_name) {
                  return frame_poses[i];
              }
          }
          throw std::runtime_error("Frame name " + target_name + " not found");
      }

  public:
      void executeEndPoseControl() {
          std::this_thread::sleep_for(std::chrono::milliseconds(1000));  // 等待1秒

          // 获取当前状态
          MotionControlStatus status;
          GDKRes result = robot_.GetMotionControlStatus(status);
          if (result != GDKRes::kSuccess) {
              std::cout << "获取运动控制状态失败" << std::endl;
              return;
          }

          // 获取起始位姿
          Pose start_left_pose = findPoseByName(status.frame_names, status.frame_poses, LEFT_NAME);
          Pose start_right_pose = findPoseByName(status.frame_names, status.frame_poses, RIGHT_NAME);

          // 计算步数
          int n_left = calculateNSteps(start_left_pose.position, TARGET_LEFT.position, MAX_STEP_CM);
          int n_right = calculateNSteps(start_right_pose.position, TARGET_RIGHT.position, MAX_STEP_CM);
          int n_steps = std::max(n_left, n_right);

          std::cout << "左臂步数: " << n_left << ", 右臂步数: " << n_right << ", 总步数: " << n_steps << std::endl;

          // 规划轨迹
          std::vector<Pose> traj_left = planTrajectory(start_left_pose, TARGET_LEFT, n_steps);
          std::vector<Pose> traj_right = planTrajectory(start_right_pose, TARGET_RIGHT, n_steps);

          // 执行轨迹
          double dt = 1.0 / RATE_HZ;
          for (int i = 0; i < n_steps; i++) {
              EndEffectorPose end_pose;
              end_pose.life_time = LIFETIME;
              end_pose.group = CONTROL_GROUP;
              end_pose.left_end_effector_pose = traj_left[i];
              end_pose.right_end_effector_pose = traj_right[i];

              result = robot_.EndEffectorPoseControl(end_pose);
              if (result != GDKRes::kSuccess) {
                  std::cout << "控制命令发送失败，步数: " << i << std::endl;
                  return;
              }

              std::this_thread::sleep_for(std::chrono::milliseconds(static_cast<int>(dt * 1000)));
          }

          // 保持最终位姿（对应Python版本）
          if (HOLD_FINAL) {
              std::cout << "进入末端位姿保持（Ctrl+C 结束）..." << std::endl;
              try {
                  while (true) {
                      EndEffectorPose end_pose;
                      end_pose.life_time = LIFETIME;
                      end_pose.group = CONTROL_GROUP;
                      end_pose.left_end_effector_pose = traj_left.back();
                      end_pose.right_end_effector_pose = traj_right.back();

                      result = robot_.EndEffectorPoseControl(end_pose);
                      if (result != GDKRes::kSuccess) {
                          std::cout << "保持位姿失败" << std::endl;
                          break;
                      }

                      std::this_thread::sleep_for(std::chrono::milliseconds(static_cast<int>(dt * 1000)));
                  }
              } catch (const std::exception& e) {
                  std::cout << "已中断保持: " << e.what() << std::endl;
              }
          }
      }
  };

  int main() {
      EndEffectorController controller;
      controller.executeEndPoseControl();
      return 0;
  }
  ```
  
#### 16. `MoveEEPos()`

- **功能**：控制末端执行器位置
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `joint_states` | `const JointStates&` | 关节状态控制参数 |

#### JointStates对象详细说明（用于MoveEEPos）

**JointStates结构体包含以下成员**：

| 成员名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `nums` | `size_t` | 关节数量，应等于 `states.size()` | 无单位 |
| `group` | `std::string` | 控制组，必须为 "left_tool"、"right_tool" 或 "dual_tool" | 字符串 |
| `target_type` | `std::string` | 目标类型，支持的值见下表 | 字符串 |
| `states` | `std::vector<JointState>` | 关节状态列表（必需） | 关节状态列表 |

**target_type 支持的值及对应的关节数量要求**：

| target_type 值 | 关节数量要求 | 说明 |
| :--- | :--- | :--- |
| `"omnipicker"` | 1 | 全向抓取器，需要1个关节 |
| `"dahuan"` | 1 | 大环末端执行器，需要1个关节 |
| `"ctek90d"` | 1 | CTEK90D末端执行器，需要1个关节 |
| `"o10_t2"` | 10 | O10灵巧手末端执行器，需要10个关节 |
| `"o12_t2"` | 12 | O12灵巧手节末端执行器，需要12个关节 |

**各末端类型的关节位置取值范围**：

- **注意**：关节取值范围与版本绑定，使用时注意当前版本的取值范围，当前版本取值范围以文档为主
- **omnipicker**：`position` 取值范围为 `[-0.785,0]`，其中 `-0.785` 表示打开，`0` 表示关闭
- **dahuan**：`position` 取值范围为 `[0,0.025]`，其中 `0` 表示打开，`0.025` 表示关闭
- **ctek90d**：`position` 取值范围为 `[-0.91, 0]`，其中 `-0.91` 表示打开，`0` 表示关闭
- **o10_t2**：各关节位置取值范围如下（单位：弧度）

  **左手关节限位值**：

  | 关节索引 | 关节名称 | 最小值 | 最大值 |
  | :--- | :--- | :--- | :--- |
  | 0 | `idx31_hand_l_thumb_roll_joint` | -1.1213740444063567 | 0.029670597283903602 |
  | 1 | `idx32_hand_l_thumb_abad_joint` | -0.04537856055185257 | 1.642354826126664 |
  | 2 | `idx33_hand_l_thumb_mcp_joint` | -0.8415977653116657 | 0.0 |
  | 3 | `idx36_hand_l_index_abad_joint` | 0.0 | 0.16406094968746698 |
  | 4 | `idx37_hand_l_index_pip_joint` | 0.0 | 1.4835298641951802 |
  | 5 | `idx39_hand_l_middle_pip_joint` | 0.0 | 1.4835298641951802 |
  | 6 | `idx41_hand_l_ring_abad_joint` | -0.16929693744344995 | 0.0 |
  | 7 | `idx42_hand_l_ring_pip_joint` | 0.0 | 1.4835298641951802 |
  | 8 | `idx44_hand_l_pinky_abad_joint` | -0.1850049007113989 | 0.0 |
  | 9 | `idx45_hand_l_pinky_pip_joint` | 0.0 | 1.4835298641951802 |

  **右手关节限位值**：

  | 关节索引 | 关节名称 | 最小值 | 最大值 |
  | :--- | :--- | :--- | :--- |
  | 0 | `idx71_hand_r_thumb_roll_joint` | -0.029670597283903602 | 1.1213740444063567 |
  | 1 | `idx72_hand_r_thumb_abad_joint` | -1.642354826126664 | 0.04537856055185257 |
  | 2 | `idx73_hand_r_thumb_mcp_joint` | 0.0 | 0.8415977653116657 |
  | 3 | `idx76_hand_r_index_abad_joint` | -0.16406094968746698 | 0.0 |
  | 4 | `idx77_hand_r_index_pip_joint` | 0.0 | 1.4835298641951802 |
  | 5 | `idx79_hand_r_middle_pip_joint` | 0.0 | 1.4835298641951802 |
  | 6 | `idx81_hand_r_ring_abad_joint` | 0.0 | 0.16929693744344995 |
  | 7 | `idx82_hand_r_ring_pip_joint` | 0.0 | 1.4835298641951802 |
  | 8 | `idx84_hand_r_pinky_abad_joint` | 0.0 | 0.1850049007113989 |
  | 9 | `idx85_hand_r_pinky_pip_joint` | 0.0 | 1.4835298641951802 |

  **典型状态值**：
  - **左手开**：`[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
  - **左手握**：`[-0.2, 1.45, -0.75, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0]`
  - **右手开**：`[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
  - **右手握**：`[0.2, -1.45, 0.75, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0]`

- **o12_t2**：各关节位置取值范围如下（单位：弧度）

  **左手关节限位值**：

  | 关节索引 | 关节名称 | 最小值 | 最大值 |
  | :--- | :--- | :--- | :--- |
  | 0 | `idx31_hand_l_thumb_roll_joint` | -0.9425 | 0.0 |
  | 1 | `idx32_hand_l_thumb_abad_joint` | 0.0 | 1.3875 |
  | 2 | `idx33_hand_l_thumb_mcp_joint` | -0.8273 | 0.0 |
  | 3 | `idx34_hand_l_thumb_pip_joint` | -1.2915 | 0.0 |
  | 4 | `idx36_hand_l_index_abad_joint` | -0.2618 | 0.2618 |
  | 5 | `idx37_hand_l_index_mcp_joint` | 0.0 | 1.3526 |
  | 6 | `idx38_hand_l_index_pip_joint` | 0.0 | 1.5307 |
  | 7 | `idx40_hand_l_middle_abad_joint` | -0.2618 | 0.2618 |
  | 8 | `idx41_hand_l_middle_mcp_joint` | 0.0 | 1.3579 |
  | 9 | `idx42_hand_l_middle_pip_joint` | 0.0 | 1.8151 |
  | 10 | `idx44_hand_l_ring_mcp_joint` | 0.0 | 1.5359 |
  | 11 | `idx47_hand_l_pinky_mcp_joint` | 0.0 | 1.5359 |

  **右手关节限位值**：

  | 关节索引 | 关节名称 | 最小值 | 最大值 |
  | :--- | :--- | :--- | :--- |
  | 0 | `idx71_hand_r_thumb_roll_joint` | 0.0 | 0.9425 |
  | 1 | `idx72_hand_r_thumb_abad_joint` | -1.3875 | 0.0 |
  | 2 | `idx73_hand_r_thumb_mcp_joint` | -0.8273 | 0.0 |
  | 3 | `idx74_hand_r_thumb_pip_joint` | -1.2915 | 0.0 |
  | 4 | `idx76_hand_r_index_abad_joint` | -0.2618 | 0.2618 |
  | 5 | `idx77_hand_r_index_mcp_joint` | 0.0 | 1.3526 |
  | 6 | `idx78_hand_r_index_pip_joint` | 0.0 | 1.5307 |
  | 7 | `idx80_hand_r_middle_abad_joint` | -0.2618 | 0.2618 |
  | 8 | `idx81_hand_r_middle_mcp_joint` | 0.0 | 1.3579 |
  | 9 | `idx82_hand_r_middle_pip_joint` | 0.0 | 1.8151 |
  | 10 | `idx84_hand_r_ring_mcp_joint` | 0.0 | 1.5359 |
  | 11 | `idx87_hand_r_pinky_mcp_joint` | 0.0 | 1.5359 |

  **典型状态值**：
  - **左手开**：`[-0.53, 0.42, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
  - **左手握**：`[-0.77, 0.5, -0.4, -0.36, -0.12, 0.69, 0.46, 0.0, 0.72, 0.5, 0.63, 0.63]`
  - **右手开**：`[0.53, -0.42, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
  - **右手握**：`[0.77, -0.5, -0.4, -0.36, 0.12, 0.69, 0.46, 0.0, 0.72, 0.5, 0.63, 0.63]`

**参数说明**：
- `group` 必须为 "left_tool"（左末端执行器）、"right_tool"（右末端执行器）或 "dual_tool"（双末端执行器），其他值将返回 `ErrorCode::kInvalidInput`
  - 当 `group` 为 "left_tool" 或 "right_tool" 时，`states.size()` 必须与 `target_type` 对应的关节数量要求完全匹配
  - 当 `group` 为 "dual_tool" 时，`states.size()` 必须为 `target_type` 对应的关节数量要求的 2 倍（前半部分用于左末端执行器，后半部分用于右末端执行器）
- `target_type` 必须为上述支持的值之一，其他值将返回 `ErrorCode::kInvalidInput`
- `nums` 必须等于 `states` 向量的大小
- `states` 不能为空，`states.size()` 必须大于0，否则返回 `ErrorCode::kInvalidInput`

**JointState结构体**：

| 成员名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `position` | `double` | 关节位置（必需） | 开合度 |


- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`

- **错误处理**：
  - 如果 `joint_states.states.size() <= 0`，返回 `ErrorCode::kInvalidInput`
  - 如果 `target_type` 不是支持的值（"omnipicker", "dahuan", "ctek90d", "o10_t2", "o12_t2"），返回 `ErrorCode::kInvalidInput`
  - 如果 `joint_states.states.size()` 与 `target_type` 对应的关节数量要求不匹配（对于 "dual_tool"，必须是 2 倍），返回 `ErrorCode::kInvalidInput`
  - 如果 `group` 不是 "left_tool"、"right_tool" 或 "dual_tool"，返回 `ErrorCode::kInvalidInput`
  - 如果关节位置值超出对应末端类型的取值范围，返回 `ErrorCode::kInvalidInput`
  - 其他错误情况返回相应的错误码

- **示例**：

  **示例1：控制左夹爪（omnipicker类型，需要1个关节）**

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

      agibot::gdk::Robot robot;
      std::cout << "Robot init" << std::endl;
      std::this_thread::sleep_for(std::chrono::seconds(1));

      // 控制左夹爪（omnipicker类型，需要1个关节）
      agibot::gdk::JointStates left_joint_states;
      left_joint_states.group = "left_tool";
      left_joint_states.target_type = "omnipicker";
      left_joint_states.states.resize(1);
      left_joint_states.states[0].position = 0;  // 取值范围 [-0.785, 0]
      left_joint_states.nums = left_joint_states.states.size();

      if (robot.MoveEEPos(left_joint_states) != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "Failed to move left end effector position" << std::endl;
      } else {
          std::cout << "左末端执行器位置控制成功" << std::endl;
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

  **示例2：控制右夹爪（dahuan类型，需要1个关节）**

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

      agibot::gdk::Robot robot;
      std::cout << "Robot init" << std::endl;
      std::this_thread::sleep_for(std::chrono::seconds(1));

      // 控制右夹爪（dahuan类型，需要1个关节）
      agibot::gdk::JointStates right_joint_states;
      right_joint_states.group = "right_tool";
      right_joint_states.target_type = "dahuan";
      right_joint_states.states.resize(1);
      right_joint_states.states[0].position = 0;  // 取值范围 [0, 0.025]
      right_joint_states.nums = right_joint_states.states.size();

      if (robot.MoveEEPos(right_joint_states) != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "Failed to move right end effector position" << std::endl;
      } else {
          std::cout << "右末端执行器位置控制成功" << std::endl;
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

  **示例3：控制左夹爪（ctek90d类型，需要1个关节）**

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

      agibot::gdk::Robot robot;
      std::cout << "Robot init" << std::endl;
      std::this_thread::sleep_for(std::chrono::seconds(1));

      // 控制左夹爪（ctek90d类型，需要1个关节）
      agibot::gdk::JointStates left_joint_states;
      left_joint_states.group = "left_tool";
      left_joint_states.target_type = "ctek90d";
      left_joint_states.states.resize(1);
      left_joint_states.states[0].position = 0;  // 取值范围 [-0.91, 0]
      left_joint_states.nums = left_joint_states.states.size();

      if (robot.MoveEEPos(left_joint_states) != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "Failed to move left end effector position" << std::endl;
      } else {
          std::cout << "左末端执行器位置控制成功" << std::endl;
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

  **示例4：控制左末端执行器（o10_t2类型，需要10个关节）**

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

      agibot::gdk::Robot robot;
      std::cout << "Robot init" << std::endl;
      std::this_thread::sleep_for(std::chrono::seconds(1));

      // 控制左末端执行器（o10_t2类型，需要10个关节）
      agibot::gdk::JointStates left_o10_states;
      left_o10_states.group = "left_tool";
      left_o10_states.target_type = "o10_t2";
      left_o10_states.states.resize(10);
      for (size_t i = 0; i < 10; ++i) {
          left_o10_states.states[i].position = 0.0;
      }
      left_o10_states.nums = left_o10_states.states.size();

      if (robot.MoveEEPos(left_o10_states) != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "Failed to move left end effector (o10_t2)" << std::endl;
      } else {
          std::cout << "左末端执行器（o10_t2）位置控制成功" << std::endl;
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

  **示例5：控制右末端执行器（o12_t2类型，需要12个关节）**

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

      agibot::gdk::Robot robot;
      std::cout << "Robot init" << std::endl;
      std::this_thread::sleep_for(std::chrono::seconds(1));

      // 控制右末端执行器（o12_t2类型，需要12个关节）
      agibot::gdk::JointStates right_o12_states;
      right_o12_states.group = "right_tool";
      right_o12_states.target_type = "o12_t2";
      right_o12_states.states.resize(12);
      for (size_t i = 0; i < 12; ++i) {
          right_o12_states.states[i].position = 0.0;
      }
      right_o12_states.nums = right_o12_states.states.size();

      if (robot.MoveEEPos(right_o12_states) != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "Failed to move right end effector (o12_t2)" << std::endl;
      } else {
          std::cout << "右末端执行器（o12_t2）位置控制成功" << std::endl;
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

  **示例6：控制双末端执行器（dual_tool，需要2倍关节数量）**

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

      agibot::gdk::Robot robot;
      std::cout << "Robot init" << std::endl;
      std::this_thread::sleep_for(std::chrono::seconds(1));

      // 控制双末端执行器（dual_tool，需要2倍关节数量）
      // 例如：使用 omnipicker 类型，需要 2 个关节（左1个 + 右1个）
      agibot::gdk::JointStates dual_states;
      dual_states.group = "dual_tool";
      dual_states.target_type = "omnipicker";
      dual_states.states.resize(2);
      // 前半部分用于左末端执行器
      dual_states.states[0].position = 0.0;
      // 后半部分用于右末端执行器
      dual_states.states[1].position = 0.0;
      dual_states.nums = dual_states.states.size();

      if (robot.MoveEEPos(dual_states) != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "Failed to move dual end effector" << std::endl;
      } else {
          std::cout << "双末端执行器位置控制成功" << std::endl;
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

1. **GDK初始化**：使用Robot功能前必须先调用`agibot::gdk::GDKInit()`初始化GDK系统
2. **GDK释放**：程序结束前必须调用`agibot::gdk::GDKRelease()`释放GDK系统资源
3. **初始化等待**：创建Robot对象后，建议等待1秒以确保DDS连接建立
4. **关节名称**：使用前请确认关节名称的正确性，可通过`GetJointStates()`获取
5. **位置范围**：关节位置应在安全范围内，避免超出机械限制
6. **速度限制**：设置合理的关节速度，避免过快运动造成危险
7. **生命周期**：合理设置请求生命周期，避免命令过期
8. **错误处理**：及时检查返回值，处理可能的错误情况
9. **控制组选择**：末端执行器控制时选择合适的控制组（左臂/右臂/双臂）
10. **位姿设置**：设置末端执行器位姿时注意坐标系的正确性
11. **状态监控**：定期检查错误码，确保机器人安全运行
12. **温度监控**：注意电机温度，避免过热损坏
13. **急停状态**：检查急停状态，确保机器人可以正常控制
14. **数据同步**：基于时间戳进行多传感器数据同步
15. **错误处理**：始终检查GDKRes返回值，确保操作成功

## 应用场景

- **机器人控制**：实现机器人的全面运动控制
- **状态监控**：实时监控机器人各部件状态
- **动作执行**：执行复杂的机器人动作序列
- **路径规划**：结合状态信息进行路径规划
- **安全检测**：监控机器人异常状态，确保安全运行
- **末端控制**：精确控制末端执行器的位姿
- **双臂协调**：实现双臂机器人的协调控制
- **关节控制**：实现高精度的关节位置控制
- **故障诊断**：通过错误码进行故障诊断和处理
- **数据融合**：结合多传感器数据进行机器人控制
