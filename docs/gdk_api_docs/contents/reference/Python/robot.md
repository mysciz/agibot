# GDK 机器人控制接口文档（Python）

## 概述

机器人控制模块为G02机器人提供了获取关节状态、控制机器人运动、获取全身状态等功能。通过Python接口，开发者可以方便地实现对机器人运动的精细化控制，适用于基础控制、状态检测、动作录制回放等多种场景。

## 接口说明

### Robot 类

该类封装了机器人控制的主要功能接口。

#### 1. `get_joint_states()`

- **注意事项**：使用motor_position和motor_velocity获取电机位置和速度，position和velocity为低速电机预留字段，当前版本无需关注
- **功能**：获取关节状态信息
- **参数**：无
- **返回值**：`dict`，包含以下属性：

| 属性名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `timestamp` | `int` | 时间戳 | 纳秒 |
| `nums` | `int` | 关节数量 | 整数 |
| `states` | `list[dict]` | 关节状态列表 | 字典列表 |

**states中每个关节状态结构**：

| 属性名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `name` | `str` | 关节名称 | 字符串 |
| `mode` | `int` | 关节模式 | 整数 |
| `position` | `float` | 关节位置 | 弧度 |
| `velocity` | `float` | 关节速度 | 弧度/秒 |
| `effort` | `float` | 关节力矩 | 牛顿·米 |
| `motor_position` | `float` | 电机位置 | 弧度 |
| `motor_velocity` | `float` | 电机速度 | 弧度/秒 |
| `motor_current` | `float` | 电机电流 | 安培 |
| `error_code` | `int` | 错误码 | 整数 |

- **示例**：

  ```python
  import agibot_gdk
  import time

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  robot = agibot_gdk.Robot()
  time.sleep(2)  # 等待机器人初始化

  # 获取关节状态
  joint_states = robot.get_joint_states()
  print(f"关节数量: {joint_states['nums']}")
  print(f"时间戳: {joint_states['timestamp']}")

  for state in joint_states['states']:
      print(f"关节: {state['name']}")
      print(f"  位置: {state['position']:.3f} 弧度")
      print(f"  速度: {state['velocity']:.3f} 弧度/秒")
      print(f"  力矩: {state['effort']:.3f} 牛顿·米")
      print(f"  电机位置: {state['motor_position']:.3f} 弧度")
      print(f"  电机电流: {state['motor_current']:.3f} 安培")
      print(f"  错误码: {state['error_code']}")

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

#### 2. `get_whole_body_status()`

- **功能**：获取全身状态信息
- **参数**：无
- **返回值**：`dict`，包含以下属性：

| 属性名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `timestamp` | `int` | 时间戳 | 纳秒 |
| `right_arm_error` | `int` | 右臂错误码 | 整数 |
| `left_arm_error` | `int` | 左臂错误码 | 整数 |
| `right_arm_control` | `bool` | 右臂控制状态 | 布尔值 |
| `left_arm_control` | `bool` | 左臂控制状态 | 布尔值 |
| `right_arm_estop` | `bool` | 右臂急停状态 | 布尔值 |
| `left_arm_estop` | `bool` | 左臂急停状态 | 布尔值 |
| `right_end_error` | `int` | 右执行器错误码 | 整数 |
| `left_end_error` | `int` | 左执行器错误码 | 整数 |
| `right_end_model` | `str` | 右执行器型号 | 字符串 |
| `left_end_model` | `str` | 左执行器型号 | 字符串 |
| `waist_error` | `int` | 腰部错误码 | 整数 |
| `lift_error` | `int` | 升降错误码 | 整数 |
| `neck_error` | `int` | 头部错误码 | 整数 |
| `chassis_error` | `int` | 底盘错误码 | 整数 |

**mode数值说明**：

| 数值 | 含义 |
| :--- | :--- |
| 0 | `停止` |
| 1 | `G1_伺服` |
| 2 | `路径规划` |
| 5 | `G2_伺服` |

- **示例**：

  ```python
  import agibot_gdk
  import time

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  robot = agibot_gdk.Robot()
  time.sleep(2)  # 等待机器人初始化

  # 获取全身状态
  status = robot.get_whole_body_status()

  # 打印基本信息
  print(f"时间戳: {status['timestamp']}")
  print(f"右执行器型号: {status['right_end_model']}")
  print(f"左执行器型号: {status['left_end_model']}")

  # 检查错误状态
  print("\n=== 错误状态检查 ===")
  if status['right_arm_error'] == 0:
      print("✅ 右臂正常")
  else:
      print(f"❌ 右臂错误码: {status['right_arm_error']}")

  if status['left_arm_error'] == 0:
      print("✅ 左臂正常")
  else:
      print(f"❌ 左臂错误码: {status['left_arm_error']}")

  if status['waist_error'] == 0:
      print("✅ 腰部正常")
  else:
      print(f"❌ 腰部错误码: {status['waist_error']}")

  if status['neck_error'] == 0:
      print("✅ 头部正常")
  else:
      print(f"❌ 头部错误码: {status['neck_error']}")

  if status['chassis_error'] == 0:
      print("✅ 底盘正常")
  else:
      print(f"❌ 底盘错误码: {status['chassis_error']}")

  # 检查控制状态
  print("\n=== 控制状态 ===")
  print(f"右臂控制: {'是' if status['right_arm_control'] else '否'}")
  print(f"左臂控制: {'是' if status['left_arm_control'] else '否'}")
  print(f"右臂急停: {'是' if status['right_arm_estop'] else '否'}")
  print(f"左臂急停: {'是' if status['left_arm_estop'] else '否'}")

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

#### 3. `get_motion_control_status()`

- **功能**：获取末端运动控制状态
- **参数**：无
- **返回值**：`MotionControlStatus`对象，包含以下属性：

| 属性名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `frame_names` | `list[str]` | 末端关节名称列表 | 字符串列表 |
| `frame_poses` | `list[Pose]` | 末端关节位姿列表 | 位姿列表 |
| `collision_pairs_1` | `list[str]` | 碰撞对列表1 | 字符串列表 |
| `collision_pairs_2` | `list[str]` | 碰撞对列表2 | 字符串列表 |
| `mode` | `int` | 运动模式 | 整数 |
| `error_code` | `int` | 错误码 | 整数 |
| `error_msg` | `str` | 错误信息 | 字符串 |
| `twists` | `list[Twist]` | 速度列表 | 速度列表 |
| `wrenches` | `list[Wrench]` | 力/力矩列表 | 力/力矩列表 |

**mode数值说明**：

| 数值 | 含义 |
| :--- | :--- |
| 0 | `停止` |
| 1 | `G1_伺服` |
| 2 | `路径规划` |
| 5 | `G2_伺服` |

- **示例**：

  ```python
  import agibot_gdk
  import time

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  robot = agibot_gdk.Robot()
  time.sleep(2)  # 等待机器人初始化

  # 获取运动控制状态
  status = robot.get_motion_control_status()
  print(f"运动模式: {status.mode}")
  print(f"错误码: {status.error_code}")
  print(f"错误信息: {status.error_msg}")
  print(f"关节数量: {len(status.frame_names)}")
  print(f"碰撞对数量: {len(status.collision_pairs_1)}")

  # 打印所有关节名称
  for i, frame_name in enumerate(status.frame_names):
      print(f"关节 {i}: {frame_name}")

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

#### 4. `get_end_state()`

- **功能**：获取末端执行器状态信息
- **参数**：无
- **返回值**：`dict`，包含以下属性：

| 属性名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `left_end_state` | `dict` | 左执行器状态信息 | 字典 |
| `right_end_state` | `dict` | 右执行器状态信息 | 字典 |

**left_end_state/right_end_state结构**：

| 属性名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `controlled` | `bool` | 是否被控制 | 布尔值 |
| `type` | `int` | 执行器类型 | 整数 |
| `names` | `list[str]` | 关节名称列表 | 字符串列表 |
| `end_states` | `list[dict]` | 关节状态列表 | 字典列表 |

**end_states中每个关节状态结构**：

| 属性名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `id` | `int` | 关节ID | 整数 |
| `enable` | `bool` | 是否启用 | 布尔值 |
| `position` | `float` | 关节位置 | 弧度 |
| `velocity` | `float` | 关节速度 | 弧度/秒 |
| `effort` | `float` | 关节力矩 | 牛顿·米 |
| `current` | `float` | 电机电流 | 安培 |
| `voltage` | `float` | 电机电压 | 伏特 |
| `temperature` | `float` | 电机温度 | 摄氏度 |
| `status` | `int` | 状态码 | 整数 |
| `err_code` | `int` | 错误码 | 整数 |

- **示例**：

  ```python
  import agibot_gdk
  import time

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  robot = agibot_gdk.Robot()
  time.sleep(2)  # 等待机器人初始化

  # 获取末端执行器状态
  end_state = robot.get_end_state()

  # 打印左执行器状态
  left_state = end_state['left_end_state']
  print(f"左执行器控制状态: {left_state['controlled']}")
  print(f"左执行器类型: {left_state['type']}")
  print(f"左执行器关节: {left_state['names']}")

  # 打印左执行器关节详细信息
  for i, joint_state in enumerate(left_state['end_states']):
      print(f"\n左执行器关节 {i+1}:")
      print(f"  关节ID: {joint_state['id']}")
      print(f"  启用状态: {joint_state['enable']}")
      print(f"  位置: {joint_state['position']:.3f} 行程值")
      print(f"  速度: {joint_state['velocity']:.3f} 行程值/秒")
      print(f"  力矩: {joint_state['effort']:.3f} 牛顿·米")
      print(f"  电流: {joint_state['current']:.3f} 安培")
      print(f"  电压: {joint_state['voltage']:.3f} 伏特")
      print(f"  温度: {joint_state['temperature']:.1f} 摄氏度")
      print(f"  状态码: {joint_state['status']}")
      print(f"  错误码: {joint_state['err_code']}")

  # 打印右执行器状态
  right_state = end_state['right_end_state']
  print(f"\n右执行器控制状态: {right_state['controlled']}")
  print(f"右执行器类型: {right_state['type']}")
  print(f"右执行器关节: {right_state['names']}")

  # 检查执行器状态
  print("\n=== 执行器状态检查 ===")
  for side in ['left', 'right']:
      state = end_state[f'{side}_end_state']
      if state['controlled']:
          print(f"✅ {side}执行器正在控制中")
      else:
          print(f"❌ {side}执行器未控制")

      for joint_state in state['end_states']:
          if joint_state['err_code'] == 0:
              print(f"✅ {side}执行器关节{joint_state['id']}正常")
          else:
              print(f"❌ {side}执行器关节{joint_state['id']}错误码: {joint_state['err_code']}")

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

#### 5. `get_chassis_power_state()`

- **功能**：获取底盘电源状态
- **返回值**：`ChassisPowerState`对象，包含以下属性：

| 属性名 | 类型 | 描述 | 单位 |
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
| `battery_states` | `list[BatteryState]` | 电池状态列表 | 电池状态列表 |
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

- **示例**：

  ```python

  import agibot_gdk
  import time

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  robot = agibot_gdk.Robot()
  time.sleep(2)  # 等待机器人初始化

  # 获取底盘电源状态
  chassis_power_state = robot.get_chassis_power_state()
  print(chassis_power_state)

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

#### 6. `get_chest_power_state()`

- **功能**：获取胸部电源状态
- **返回值**：`ChestPowerState`对象，包含以下属性：

| 属性名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `power_onoff_req` | `uint8_t` | 开关机请求 | 无单位 |
| `emergency_stop_button_req` | `uint8_t` | 急停按钮请求 | 无单位 |
| `power_switch_fault_state` | `uint8_t` | 电源开关故障状态 | 无单位 |
| `emergency_stop_button_fault_state` | `uint8_t` | 急停按钮故障状态 | 无单位 |
| `power_full_low_req` | `uint8_t` | 电源满低请求 | 无单位 |
| `chest_power_board_power_state` | `uint8_t` | 胸部电源板状态 | 无单位 |
| `domain_controller_power_state` | `uint8_t` | 域控制器电源状态 | 无单位 |
| `head_interactive_board_power_state` | `uint8_t` | 头部交互板电源状态 | 无单位 |
| `curved_screen_power_state` | `uint8_t` | 曲面屏电源状态 | 无单位 |
| `head_yaw_motor_power_state` | `uint8_t` | 头部偏航电机电源状态 | 无单位 |
| `head_pitch_motor_power_state` | `uint8_t` | 头部俯仰电机电源状态 | 无单位 |
| `head_roll_motor_power_state` | `uint8_t` | 头部滚转电机电源状态 | 无单位 |
| `fan_power_state` | `uint8_t` | 风扇电源状态 | 无单位 |
| `chest_power_board_fan_fault_state` | `uint8_t` | 胸部电源板风扇故障状态 | 无单位 |
| `body_fan1_fault_state` | `uint8_t` | 身体风扇1故障状态 | 无单位 |
| `body_fan2_fault_state` | `uint8_t` | 身体风扇2故障状态 | 无单位 |
| `body_fan3_fault_state` | `uint8_t` | 身体风扇3故障状态 | 无单位 |
| `body_fan4_fault_state` | `uint8_t` | 身体风扇4故障状态 | 无单位 |
| `upper_body_led_strip_power_state` | `uint8_t` | 上体LED灯带电源状态 | 无单位 |
| `poe_power_state` | `uint8_t` | PoE电源状态 | 无单位 |
| `ipad_power_state` | `uint8_t` | iPad电源状态 | 无单位 |
| `chest_reserved_lidar_power_state` | `uint8_t` | 胸部保留激光雷达电源状态 | 无单位 |
| `chest_power_board_temperature` | `float` | 胸部电源板温度 | °C |
| `chest_power_board_fault_state` | `uint32_t` | 胸部电源板故障状态 | 无单位 |

- **示例**：

  ```python
  import agibot_gdk
  import time

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  robot = agibot_gdk.Robot()
  time.sleep(2)  # 等待机器人初始化

  # 获取胸部电源状态
  chest_power_state = robot.get_chest_power_state()
  print(chest_power_state)

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```   

#### 7. `joint_control_request()`

- **功能**：关节位置规划控制接口，执行到目标位置后，接口返回。
- **参数**：`JointControlReq`对象，包含以下属性：

| 属性名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `life_time` | `float` | 生命周期 | 秒 |
| `joint_names` | `list[str]` | 关节名称列表 | 字符串列表 |
| `joint_positions` | `list[float]` | 关节位置列表 | 弧度 |
| `joint_velocities` | `list[float]` | 关节速度列表 | 弧度/秒 |
| `detail` | `str` | 详细信息 | 字符串 |

- **返回值**：`int`，0表示成功，失败时抛出异常

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

  ```python
  import agibot_gdk
  import time

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  robot = agibot_gdk.Robot()
  time.sleep(2)  # 等待机器人初始化

  # 创建关节控制请求
  joint_control_req = agibot_gdk.JointControlReq()
  joint_control_req.joint_names = ["idx01_body_joint1", "idx02_body_joint2"]
  joint_control_req.joint_positions = [0.0, 0.0]
  joint_control_req.joint_velocities = [0.1, 0.1]
  joint_control_req.life_time = 5.0
  joint_control_req.detail = "测试关节控制"

  try:
      result = robot.joint_control_request(joint_control_req)
      print("关节控制请求成功")
  except Exception as e:
      print(f"关节控制请求失败: {e}")

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

#### 8. `move_head_joint()`

- **功能**：头部关节位置规划控制接口，执行到目标位置后，接口返回。
- **参数**：
  - `positions`：`list[float]`，头部关节位置列表，按照"idx11_head_joint1", "idx12_head_joint2", "idx13_head_joint3"顺序
  - `velocities`：`list[float]`，头部关节速度列表（弧度/秒），按照"idx11_head_joint1", "idx12_head_joint2", "idx13_head_joint3"顺序
- **返回值**：`int`，0表示成功，失败时抛出异常

- **示例**：

  ```python
  import agibot_gdk
  import time

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  robot = agibot_gdk.Robot()
  time.sleep(2)  # 等待机器人初始化

  # 控制头部位置（按照关节顺序：idx11_head_joint1, idx12_head_joint2, idx13_head_joint3）
  head_positions = [0.0, 0.0, 0.0]  # 头部关节位置列表
  head_velocities = [0.3, 0.3, 0.3]  # 头部关节速度列表

  try:
      result = robot.move_head_joint(head_positions, head_velocities)
      print("头部控制成功")
  except Exception as e:
      print(f"头部控制失败: {e}")

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

#### 9. `move_waist_joint()`

- **功能**：腰部关节位置规划控制接口，执行到目标位置后，接口返回。
- **参数**：
  - `positions`：`list[float]`，腰部关节位置列表，按照"idx01_body_joint1", "idx02_body_joint2", "idx03_body_joint3", "idx04_body_joint4", "idx05_body_joint5"顺序
  - `velocities`：`list[float]`，腰部关节速度列表（弧度/秒），按照"idx01_body_joint1", "idx02_body_joint2", "idx03_body_joint3", "idx04_body_joint4", "idx05_body_joint5"顺序
- **返回值**：`int`，0表示成功，失败时抛出异常

- **示例**：

  ```python
  import agibot_gdk
  import time

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  robot = agibot_gdk.Robot()
  time.sleep(2)  # 等待机器人初始化

  # 控制腰部位置（按照关节顺序：idx01_body_joint1, idx02_body_joint2, idx03_body_joint3, idx04_body_joint4, idx05_body_joint5）
  waist_positions = [0.0, 0.0, 0.0, 0.0, 0.0]  # 腰部关节位置列表
  waist_velocities = [0.3, 0.3, 0.3, 0.3, 0.3]  # 腰部关节速度列表

  try:
      result = robot.move_waist_joint(waist_positions, waist_velocities)
      print("腰部控制成功")
  except Exception as e:
      print(f"腰部控制失败: {e}")

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

#### 10. `move_arm_joint()`

- **功能**：手臂关节位置规划控制接口，执行到目标位置后，接口返回。
- **参数**：
  - `positions`：`list[float]`，手臂关节位置列表，按照"idx21_arm_l_joint1", "idx22_arm_l_joint2", "idx23_arm_l_joint3", "idx24_arm_l_joint4", "idx25_arm_l_joint5", "idx26_arm_l_joint6", "idx27_arm_l_joint7", "idx61_arm_r_joint1", "idx62_arm_r_joint2", "idx63_arm_r_joint3", "idx64_arm_r_joint4", "idx65_arm_r_joint5", "idx66_arm_r_joint6", "idx67_arm_r_joint7"顺序
  - `velocities`：`list[float]`，手臂关节速度列表（弧度/秒），按照"idx21_arm_l_joint1", "idx22_arm_l_joint2", "idx23_arm_l_joint3", "idx24_arm_l_joint4", "idx25_arm_l_joint5", "idx26_arm_l_joint6", "idx27_arm_l_joint7", "idx61_arm_r_joint1", "idx62_arm_r_joint2", "idx63_arm_r_joint3", "idx64_arm_r_joint4", "idx65_arm_r_joint5", "idx66_arm_r_joint6", "idx67_arm_r_joint7"顺序
  - `control_group`：`int`，控制组，0表示控制左臂，1表示控制右臂，2表示控制双臂
- **返回值**：`int`，0表示成功，失败时抛出异常

- **示例**：

  ```python
  import agibot_gdk
  import time

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  robot = agibot_gdk.Robot()
  time.sleep(2)  # 等待机器人初始化

  # 控制手臂位置（按照关节顺序：左臂7个关节 + 右臂7个关节）
  arm_positions = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,  # 左臂7个关节
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # 右臂7个关节
  arm_velocities = [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3,  # 左臂7个关节速度
                    0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3]  # 右臂7个关节速度

  try:
      result = robot.move_arm_joint(arm_positions, arm_velocities, 2)
      print("手臂控制成功")
  except Exception as e:
      print(f"手臂控制失败: {e}")

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

#### 11. `joint_servo_control()`

- **功能**：关节位置伺服控制接口，需要以100hz的控制频率进行控制，支持正常模式和低延时模式，默认使用正常模式。
- **注意**：低延时模式无碰撞保护，使用时注意安全。如需同时控制末端执行器，需要使用该接口下发控制明令，具体参考以下示例。
- **参数**：
  - `joint_servo_control_req`：`JointServoControlReq`对象，包含以下属性：


| 属性名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `control_period` | `float` | 控制周期 | 秒 |
| `joint_names` | `list[str]` | 关节名称列表 | 字符串列表 |
| `joint_positions` | `list[float]` | 关节位置列表 | 弧度 |
| `joint_velocities` | `list[float]` | 关节速度列表 | 弧度/秒 |

  - `enable_low_latency`：`bool`，可选参数，默认为`False`。

**参数说明**：
- `control_period` 表示控制周期，单位为秒,建议比控制频率稍大
- `joint_names`、`joint_positions` 两个列表的长度必须相同
- `joint_positions` 中的值必须在对应关节的限位范围内（见下方关节限位值说明），否则将抛出异常
- `joint_names`、`joint_positions` 不能为空，否则将抛出异常
- `joint_velocities` 预留参数，目前不使用，可以为空
- `enable_low_latency` 用于选择控制通道，低延时模式适用于对实时性要求更高的场景

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

- **返回值**：`int`，0表示成功，失败时抛出异常

- **异常说明**：
  - 如果 `joint_names`、`joint_positions` 为空，底层将返回 `ErrorCode::kInvalidInput`，Python 将抛出 `std::runtime_error("JointServoControlRequest failed")`
  - 如果 `joint_positions` 中的值超出对应关节的限位范围，底层将返回 `ErrorCode::kInvalidInput`，Python 将抛出异常
  - 如果配置解析器获取失败，底层将返回 `ErrorCode::kRuntimeError`，Python 将抛出异常

- **示例**：

```python
import agibot_gdk
import time
import math

# 控制参数
CONTROL_PERIOD = 0.01  # 控制周期（秒）
RATE_HZ = 100.0        # 发送频率（Hz）
DURATION = 5.0         # 控制持续时间（秒）
MAX_POSITION_DELTA = 0.1  # 最大位置变化量（弧度）


class JointServoControlController:
    def __init__(self, robot):
        self.robot = robot

    def get_joint_position_by_name(self, joint_states, joint_name):
        """根据关节名称获取关节位置"""
        for state in joint_states['states']:
            if state['name'] == joint_name:
                return state['motor_position']
        raise RuntimeError(f"Joint name {joint_name} not found")

    def interpolate_position(self, start_pos, target_pos, t):
        """线性插值计算中间位置"""
        return start_pos + t * (target_pos - start_pos)

    def execute_joint_servo_control(self, target_joint_names, target_positions):
        """执行关节位置伺服控制"""
        time.sleep(1.0)  # 等待1秒

        # 获取当前关节状态
        current_joint_states = self.robot.get_joint_states()
        print(f"当前关节数量: {current_joint_states['nums']}")

        # 获取起始位置
        start_positions = []
        for joint_name in target_joint_names:
            try:
                pos = self.get_joint_position_by_name(current_joint_states, joint_name)
                start_positions.append(pos)
                print(f"关节 {joint_name} 当前位置: {pos:.3f} 弧度")
            except RuntimeError as e:
                print(f"错误: {e}")
                return

        # 计算步数
        n_steps = int(DURATION * RATE_HZ)
        print(f"总步数: {n_steps}, 持续时间: {DURATION} 秒")

        # 执行轨迹
        dt = 1.0 / RATE_HZ
        start_time = time.time()

        for i in range(n_steps):
            t = float(i) / (n_steps - 1) if n_steps > 1 else 0.0

            # 创建关节位置伺服请求
            joint_servo_control_req = agibot_gdk.JointServoControlReq()
            joint_servo_control_req.control_period = CONTROL_PERIOD

            # 计算当前目标位置（线性插值）
            current_positions = []
            for j, joint_name in enumerate(target_joint_names):
                interp_pos = self.interpolate_position(
                    start_positions[j], target_positions[j], t
                )
                current_positions.append(interp_pos)

            joint_servo_control_req.joint_names = target_joint_names
            joint_servo_control_req.joint_positions = current_positions

            try:
                # 使用普通模式（enable_low_latency=False，默认值）
                result = self.robot.joint_servo_control(joint_servo_control_req)
                # 如需使用低延时模式，可传入 enable_low_latency=True：
                # result = self.robot.joint_servo_control(joint_servo_control_req, enable_low_latency=True)
                if result != 0:
                    print(f"控制命令发送失败，步数: {i}")
                    return
            except Exception as e:
                print(f"控制命令发送异常，步数: {i}, 错误: {e}")
                return

            # 控制发送频率
            elapsed = time.time() - start_time
            expected_time = (i + 1) * dt
            sleep_time = expected_time - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)

        print("关节位置伺服控制完成")

        # 保持最终位置
        print("进入最终位置保持（Ctrl+C 结束）...")
        try:
            while True:
                joint_servo_control_req = agibot_gdk.JointServoControlReq()
                joint_servo_control_req.control_period = CONTROL_PERIOD
                joint_servo_control_req.joint_names = target_joint_names
                joint_servo_control_req.joint_positions = target_positions

                try:
                    # 使用普通模式（enable_low_latency=False，默认值）
                    result = self.robot.joint_servo_control(joint_servo_control_req)
                    # 如需使用低延时模式，可传入 enable_low_latency=True：
                    # result = self.robot.joint_servo_control(joint_servo_control_req, enable_low_latency=True)
                    if result != 0:
                        print("保持位置失败")
                        break
                except Exception as e:
                    print(f"保持位置异常: {e}")
                    break

                time.sleep(dt)
        except KeyboardInterrupt:
            print("\n已中断保持")


def main():
    # 初始化GDK系统
    if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
        print("GDK初始化失败")
        return

    print("GDK初始化成功")

    try:
        robot = agibot_gdk.Robot()
        time.sleep(2)  # 等待机器人初始化

        # 获取当前关节状态
        current_joint_states = robot.get_joint_states()
        print(f"当前关节数量: {current_joint_states['nums']}")

        # 定义要控制的关节（示例：左臂前3个关节）
        target_joint_names = [
            "idx21_arm_l_joint1",
            "idx22_arm_l_joint2",
            "idx23_arm_l_joint3"
        ]

        # 获取当前位置作为起始位置（用于插值）
        controller = JointServoControlController(robot)
        start_positions = []
        for joint_name in target_joint_names:
            pos = controller.get_joint_position_by_name(current_joint_states, joint_name)
            start_positions.append(pos)
            print(f"关节 {joint_name} 当前位置: {pos:.3f} 弧度")

        # 设置目标角度（直接指定目标角度值，单位：弧度）
        target_positions = [
            0.0,  # idx21_arm_l_joint1: 目标角度 0.0 弧度
            0.0,  # idx22_arm_l_joint2: 目标角度 0.0 弧度
            0.0   # idx23_arm_l_joint3: 目标角度 0.0 弧度
        ]

        print(f"\n目标角度:")
        for i, joint_name in enumerate(target_joint_names):
            print(f"  {joint_name}: {target_positions[i]:.3f} 弧度")

        # 执行关节位置伺服控制
        controller.execute_joint_servo_control(
            target_joint_names, target_positions)

    except Exception as e:
        print(f"执行过程中发生错误: {e}")
    finally:
        # 释放GDK系统资源
        if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
            print("GDK释放失败")
        else:
            print("GDK释放成功")


if __name__ == "__main__":
    main()
```

- **同时控制机械臂与末端的示例**：

```python
import agibot_gdk
import time

# 控制参数
CONTROL_PERIOD = 0.01  # 控制周期（秒）
RATE_HZ = 100.0        # 发送频率（Hz）
DURATION = 3.0         # 单次移动持续时间（秒）
HOLD_DURATION = 0.5    # 在 0 或 1 处保持的时间（秒）
NUM_CYCLES = 3         # 往复运动次数

# 左臂 7 个关节名称（与 get_joint_states 中一致）
ARM_L_JOINT_NAMES = [
    "idx21_arm_l_joint1", "idx22_arm_l_joint2", "idx23_arm_l_joint3",
    "idx24_arm_l_joint4", "idx25_arm_l_joint5", "idx26_arm_l_joint6",
    "idx27_arm_l_joint7",
]

def get_arm_positions_by_name(joint_states, joint_names):
    """从 get_joint_states 的返回中按关节名取出位置列表"""
    name_to_pos = {s["name"]: s["motor_position"] for s in joint_states["states"]}
    return [name_to_pos[name] for name in joint_names]

def get_ee_names_and_positions(end_state, side="left"):
    """从 get_end_state 的返回中取出指定侧末端的关节名列表和位置列表"""
    key = f"{side}_end_state"
    if key not in end_state:
        raise RuntimeError(f"get_end_state 中未找到 {key}")
    state = end_state[key]
    names = state.get("names", [])
    positions = [s["position"] for s in state.get("end_states", [])]
    if len(names) != len(positions):
        raise RuntimeError(f"{key} 中 names 与 end_states 长度不一致")
    return names, positions

def main():
    if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
        print("GDK初始化失败")
        return
    print("GDK初始化成功")

    try:
        robot = agibot_gdk.Robot()
        time.sleep(2)

        # 1) 从 get_joint_states 获取全身关节（含机械臂）
        joint_states = robot.get_joint_states()
        # 2) 从 get_end_state 获取末端关节名与当前位置（如左夹爪/左手）
        end_state = robot.get_end_state()
        ee_names, ee_positions = get_ee_names_and_positions(end_state, "left")

        # 合并：机械臂关节 + 末端关节
        all_names = ARM_L_JOINT_NAMES + ee_names
        arm_positions = get_arm_positions_by_name(joint_states, ARM_L_JOINT_NAMES)

        # 机械臂小幅运动，末端关节在 -0.785 和 0 之间往复运动(omnipicker)
        arm_start = arm_positions[:]                           # 机械臂初始姿态
        arm_target = [p + 0.05 for p in arm_positions]         # 机械臂目标姿态（小幅偏移）
        ee_low = -0.785                                        # 末端下限
        ee_high = 0.0                                          # 末端上限

        print(f"控制关节数: 机械臂 {len(ARM_L_JOINT_NAMES)} + 末端 {len(ee_names)} = {len(all_names)}")
        print(f"机械臂将在关节空间 arm_start ↔ arm_target 之间运动，末端关节在 {ee_low} 和 {ee_high} 之间往复 {NUM_CYCLES} 次")
        
        n_steps = int(DURATION * RATE_HZ)           # 单次移动的步数
        hold_steps = int(HOLD_DURATION * RATE_HZ)   # 保持阶段的步数
        dt = 1.0 / RATE_HZ

        def send_control_command(arm_target_values, ee_target_values):
            """发送控制命令的辅助函数"""
            current = arm_target_values + ee_target_values
            req = agibot_gdk.JointServoControlReq()
            req.control_period = CONTROL_PERIOD
            req.joint_names = all_names
            req.joint_positions = current
            return robot.joint_servo_control(req)

        for cycle in range(NUM_CYCLES):
            print(f"\n=== 周期 {cycle+1}/{NUM_CYCLES}: 机械臂 arm_start -> arm_target, 末端 {ee_low} -> {ee_high} ===")
            start_time = time.time()
            
            # 第一段：机械臂 arm_start -> arm_target，末端 ee_low -> ee_high
            for i in range(n_steps):
                t = float(i) / (n_steps - 1) if n_steps > 1 else 1.0
                current_arm = [
                    arm_start[j] + t * (arm_target[j] - arm_start[j])
                    for j in range(len(ARM_L_JOINT_NAMES))
                ]
                current_ee = [ee_low + t * (ee_high - ee_low) for _ in ee_names]
                
                result = send_control_command(current_arm, current_ee)
                if result != 0:
                    print(f"发送失败，周期={cycle+1}, 阶段=0->1, 步数={i}")
                    raise RuntimeError("joint_servo_control failed")
                
                elapsed = time.time() - start_time
                sleep_time = (i + 1) * dt - elapsed
                if sleep_time > 0:
                    time.sleep(sleep_time)

            # 第二段：在 arm_target / ee_high 处保持
            print(f"=== 周期 {cycle+1}/{NUM_CYCLES}: 在 arm_target / {ee_high} 处保持 {HOLD_DURATION} 秒 ===")
            start_time = time.time()
            current_arm = arm_target[:]
            current_ee = [ee_high for _ in ee_names]
            
            for i in range(hold_steps):
                result = send_control_command(current_arm, current_ee)
                if result != 0:
                    print(f"发送失败，周期={cycle+1}, 阶段=保持@1, 步数={i}")
                    raise RuntimeError("joint_servo_control failed")
                
                elapsed = time.time() - start_time
                sleep_time = (i + 1) * dt - elapsed
                if sleep_time > 0:
                    time.sleep(sleep_time)

            # 第三段：机械臂 arm_target -> arm_start，末端 ee_high -> ee_low
            print(f"=== 周期 {cycle+1}/{NUM_CYCLES}: 机械臂 arm_target -> arm_start, 末端 {ee_high} -> {ee_low} ===")
            start_time = time.time()
            
            for i in range(n_steps):
                t = float(i) / (n_steps - 1) if n_steps > 1 else 1.0
                current_arm = [
                    arm_target[j] + t * (arm_start[j] - arm_target[j])
                    for j in range(len(ARM_L_JOINT_NAMES))
                ]
                current_ee = [ee_high + t * (ee_low - ee_high) for _ in ee_names]
                
                result = send_control_command(current_arm, current_ee)
                if result != 0:
                    print(f"发送失败，周期={cycle+1}, 阶段=1->0, 步数={i}")
                    raise RuntimeError("joint_servo_control failed")
                
                elapsed = time.time() - start_time
                sleep_time = (i + 1) * dt - elapsed
                if sleep_time > 0:
                    time.sleep(sleep_time)

            # 第四段：在 arm_start / ee_low 处保持
            print(f"=== 周期 {cycle+1}/{NUM_CYCLES}: 在 arm_start / {ee_low} 处保持 {HOLD_DURATION} 秒 ===")
            start_time = time.time()
            current_arm = arm_start[:]
            current_ee = [ee_low for _ in ee_names]
            
            for i in range(hold_steps):
                result = send_control_command(current_arm, current_ee)
                if result != 0:
                    print(f"发送失败，周期={cycle+1}, 阶段=保持@0, 步数={i}")
                    raise RuntimeError("joint_servo_control failed")
                
                elapsed = time.time() - start_time
                sleep_time = (i + 1) * dt - elapsed
                if sleep_time > 0:
                    time.sleep(sleep_time)

        print(f"\n机械臂 arm_start↔arm_target、末端 {ee_low}↔{ee_high} 往复控制结束")
    except Exception as e:
        print(f"执行错误: {e}")
    finally:
        if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
            print("GDK释放失败")
        else:
            print("GDK释放成功")

if __name__ == "__main__":
    main()
```

#### 12. `move_head_joint_servo()`

- **功能**：头部关节位置伺服控制接口，需要以100hz的控制频率进行控制，支持正常模式和低延时模式，默认使用正常模式。
- **注意**：低延时模式无碰撞保护，使用时注意安全。
- **参数**：
  - `positions`：`list[float]`，头部关节位置列表（弧度），按照"idx11_head_joint1", "idx12_head_joint2", "idx13_head_joint3"顺序
  - `control_period`：`float`，控制周期（秒），建议比控制频率稍大
  - `enable_low_latency`：`bool`，可选参数，默认为`False`，用于选择控制通道

**参数说明**：
- `positions` 长度必须为3
- `positions` 中的值必须在对应关节的限位范围内（见下方关节限位值说明），否则将抛出异常
- `control_period` 表示控制周期，单位为秒，建议比控制频率稍大
- `enable_low_latency` 用于选择控制通道，低延时模式适用于对实时性要求更高的场景

#### 关节限位值说明

头部关节的限位值（单位：弧度）如下：

| 关节名称 | 最小值 | 最大值 |
| :--- | :--- | :--- |
| `idx11_head_joint1` | -1.570970 | 1.570970 |
| `idx12_head_joint2` | -0.349240 | 0.349240 |
| `idx13_head_joint3` | -0.534773 | 0.534773 |

- **返回值**：`int`，0表示成功，失败时抛出异常

- **异常说明**：
  - 如果 `positions` 的长度不为3，底层将返回 `ErrorCode::kInvalidInput`，Python 将抛出异常
  - 如果 `positions` 中的值超出对应关节的限位范围，底层将返回 `ErrorCode::kInvalidInput`，Python 将抛出异常

- **示例**：

```python
import agibot_gdk
import time
import math

# 控制参数
CONTROL_PERIOD = 0.01  # 控制周期（秒）
RATE_HZ = 100.0        # 发送频率（Hz）
DURATION = 5.0         # 控制持续时间（秒）

class HeadJointServoController:
    def __init__(self, robot):
        self.robot = robot

    def get_joint_position_by_name(self, joint_states, joint_name):
        """根据关节名称获取关节位置"""
        for state in joint_states['states']:
            if state['name'] == joint_name:
                return state['motor_position']
        raise RuntimeError(f"Joint name {joint_name} not found")

    def interpolate_position(self, start_pos, target_pos, t):
        """线性插值计算中间位置"""
        return start_pos + t * (target_pos - start_pos)

    def execute_head_joint_servo_control(self, target_positions):
        """执行头部关节位置伺服控制"""
        time.sleep(1.0)  # 等待1秒

        # 获取当前关节状态
        current_joint_states = self.robot.get_joint_states()

        # 获取起始位置
        head_joint_names = ["idx11_head_joint1", "idx12_head_joint2", "idx13_head_joint3"]
        start_positions = []
        for joint_name in head_joint_names:
            try:
                pos = self.get_joint_position_by_name(current_joint_states, joint_name)
                start_positions.append(pos)
                print(f"关节 {joint_name} 当前位置: {pos:.3f} 弧度")
            except RuntimeError as e:
                print(f"错误: {e}")
                return

        # 计算步数
        n_steps = int(DURATION * RATE_HZ)
        print(f"总步数: {n_steps}, 持续时间: {DURATION} 秒")

        # 执行轨迹
        dt = 1.0 / RATE_HZ
        start_time = time.time()

        for i in range(n_steps):
            t = float(i) / (n_steps - 1) if n_steps > 1 else 0.0

            # 计算当前目标位置（线性插值）
            current_positions = []
            for j in range(3):
                interp_pos = self.interpolate_position(
                    start_positions[j], target_positions[j], t
                )
                current_positions.append(interp_pos)

            try:
                # 使用普通模式（enable_low_latency=False，默认值）
                result = self.robot.move_head_joint_servo(
                    current_positions, CONTROL_PERIOD)
                # 如需使用低延时模式，可传入 enable_low_latency=True：
                # result = self.robot.move_head_joint_servo(
                #     current_positions, CONTROL_PERIOD, enable_low_latency=True
                # )
                if result != 0:
                    print(f"控制命令发送失败，步数: {i}")
                    return
            except Exception as e:
                print(f"控制命令发送异常，步数: {i}, 错误: {e}")
                return

            # 控制发送频率
            elapsed = time.time() - start_time
            expected_time = (i + 1) * dt
            sleep_time = expected_time - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)

        print("头部关节位置伺服控制完成")

        # 保持最终位置
        print("进入最终位置保持（Ctrl+C 结束）...")
        try:
            while True:
                try:
                    # 使用普通模式（enable_low_latency=False，默认值）
                    result = self.robot.move_head_joint_servo(
                        target_positions, CONTROL_PERIOD
                    )
                    # 如需使用低延时模式，可传入 enable_low_latency=True：
                    # result = self.robot.move_head_joint_servo(
                    #     target_positions, CONTROL_PERIOD, enable_low_latency=True
                    # )
                    if result != 0:
                        print("保持位置失败")
                        break
                except Exception as e:
                    print(f"保持位置异常: {e}")
                    break

                time.sleep(dt)
        except KeyboardInterrupt:
            print("\n已中断保持")


def main():
    # 初始化GDK系统
    if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
        print("GDK初始化失败")
        return

    print("GDK初始化成功")

    try:
        robot = agibot_gdk.Robot()
        time.sleep(2)  # 等待机器人初始化

        # 获取当前关节状态
        current_joint_states = robot.get_joint_states()

        # 定义目标位置（示例：头部关节）
        target_positions = [
            0.0,  # idx11_head_joint1: 目标角度 0.0 弧度
            0.0,  # idx12_head_joint2: 目标角度 0.0 弧度
            0.0   # idx13_head_joint3: 目标角度 0.0 弧度
        ]

        print(f"\n目标角度:")
        head_joint_names = ["idx11_head_joint1", "idx12_head_joint2", "idx13_head_joint3"]
        for i, joint_name in enumerate(head_joint_names):
            print(f"  {joint_name}: {target_positions[i]:.3f} 弧度")

        # 执行头部关节位置伺服控制
        controller = HeadJointServoController(robot)
        controller.execute_head_joint_servo_control(target_positions)

    except Exception as e:
        print(f"执行过程中发生错误: {e}")
    finally:
        # 释放GDK系统资源
        if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
            print("GDK释放失败")
        else:
            print("GDK释放成功")


if __name__ == "__main__":
    main()
```

#### 13. `move_waist_joint_servo()`

- **功能**：腰部关节位置伺服控制接口，需要以100hz的控制频率进行控制，支持正常模式和低延时模式，默认使用正常模式。
- **注意**：低延时模式无碰撞保护，使用时注意安全。
- **参数**：
  - `positions`：`list[float]`，腰部关节位置列表（弧度），按照"idx01_body_joint1", "idx02_body_joint2", "idx03_body_joint3", "idx04_body_joint4", "idx05_body_joint5"顺序
  - `control_period`：`float`，控制周期（秒），建议比控制频率稍大
  - `enable_low_latency`：`bool`，可选参数，默认为`False`，用于选择控制通道

**参数说明**：
- `positions` 长度必须为5
- `positions` 中的值必须在对应关节的限位范围内（见下方关节限位值说明），否则将抛出异常
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

- **返回值**：`int`，0表示成功，失败时抛出异常

- **异常说明**：
  - 如果 `positions` 的长度不为5，底层将返回 `ErrorCode::kInvalidInput`，Python 将抛出异常
  - 如果 `positions` 中的值超出对应关节的限位范围，底层将返回 `ErrorCode::kInvalidInput`，Python 将抛出异常

- **示例**：

```python
import agibot_gdk
import time
import math

# 控制参数
CONTROL_PERIOD = 0.01  # 控制周期（秒）
RATE_HZ = 100.0        # 发送频率（Hz）
DURATION = 5.0         # 控制持续时间（秒）

class WaistJointServoController:
    def __init__(self, robot):
        self.robot = robot

    def get_joint_position_by_name(self, joint_states, joint_name):
        """根据关节名称获取关节位置"""
        for state in joint_states['states']:
            if state['name'] == joint_name:
                return state['motor_position']
        raise RuntimeError(f"Joint name {joint_name} not found")

    def interpolate_position(self, start_pos, target_pos, t):
        """线性插值计算中间位置"""
        return start_pos + t * (target_pos - start_pos)

    def execute_waist_joint_servo_control(self, target_positions):
        """执行腰部关节位置伺服控制"""
        time.sleep(1.0)  # 等待1秒

        # 获取当前关节状态
        current_joint_states = self.robot.get_joint_states()

        # 获取起始位置
        waist_joint_names = [
            "idx01_body_joint1", "idx02_body_joint2", "idx03_body_joint3",
            "idx04_body_joint4", "idx05_body_joint5"
        ]
        start_positions = []
        for joint_name in waist_joint_names:
            try:
                pos = self.get_joint_position_by_name(current_joint_states, joint_name)
                start_positions.append(pos)
                print(f"关节 {joint_name} 当前位置: {pos:.3f} 弧度")
            except RuntimeError as e:
                print(f"错误: {e}")
                return

        # 计算步数
        n_steps = int(DURATION * RATE_HZ)
        print(f"总步数: {n_steps}, 持续时间: {DURATION} 秒")

        # 执行轨迹
        dt = 1.0 / RATE_HZ
        start_time = time.time()

        for i in range(n_steps):
            t = float(i) / (n_steps - 1) if n_steps > 1 else 0.0

            # 计算当前目标位置（线性插值）
            current_positions = []
            for j in range(5):
                interp_pos = self.interpolate_position(
                    start_positions[j], target_positions[j], t
                )
                current_positions.append(interp_pos)

            try:
                # 使用普通模式（enable_low_latency=False，默认值）
                result = self.robot.move_waist_joint_servo(
                    current_positions, CONTROL_PERIOD
                )
                # 如需使用低延时模式，可传入 enable_low_latency=True：
                # result = self.robot.move_waist_joint_servo(
                #     current_positions, CONTROL_PERIOD, enable_low_latency=True
                # )
                if result != 0:
                    print(f"控制命令发送失败，步数: {i}")
                    return
            except Exception as e:
                print(f"控制命令发送异常，步数: {i}, 错误: {e}")
                return

            # 控制发送频率
            elapsed = time.time() - start_time
            expected_time = (i + 1) * dt
            sleep_time = expected_time - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)

        print("腰部关节位置伺服控制完成")

        # 保持最终位置
        print("进入最终位置保持（Ctrl+C 结束）...")
        try:
            while True:
                try:
                    # 使用普通模式（enable_low_latency=False，默认值）
                    result = self.robot.move_waist_joint_servo(
                        target_positions, CONTROL_PERIOD
                    )
                    # 如需使用低延时模式，可传入 enable_low_latency=True：
                    # result = self.robot.move_waist_joint_servo(
                    #     target_positions, CONTROL_PERIOD, enable_low_latency=True
                    # )
                    if result != 0:
                        print("保持位置失败")
                        break
                except Exception as e:
                    print(f"保持位置异常: {e}")
                    break

                time.sleep(dt)
        except KeyboardInterrupt:
            print("\n已中断保持")


def main():
    # 初始化GDK系统
    if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
        print("GDK初始化失败")
        return

    print("GDK初始化成功")

    try:
        robot = agibot_gdk.Robot()
        time.sleep(2)  # 等待机器人初始化

        # 获取当前关节状态
        current_joint_states = robot.get_joint_states()

        # 定义目标位置（示例：腰部关节）
        target_positions = [
            0.0,  # idx01_body_joint1: 目标角度 0.0 弧度
            0.0,  # idx02_body_joint2: 目标角度 0.0 弧度
            0.0,  # idx03_body_joint3: 目标角度 0.0 弧度
            0.0,  # idx04_body_joint4: 目标角度 0.0 弧度
            0.0   # idx05_body_joint5: 目标角度 0.0 弧度
        ]

        print(f"\n目标角度:")
        waist_joint_names = [
            "idx01_body_joint1", "idx02_body_joint2", "idx03_body_joint3",
            "idx04_body_joint4", "idx05_body_joint5"
        ]
        for i, joint_name in enumerate(waist_joint_names):
            print(f"  {joint_name}: {target_positions[i]:.3f} 弧度")

        # 执行腰部关节位置伺服控制
        controller = WaistJointServoController(robot)
        controller.execute_waist_joint_servo_control(target_positions)

    except Exception as e:
        print(f"执行过程中发生错误: {e}")
    finally:
        # 释放GDK系统资源
        if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
            print("GDK释放失败")
        else:
            print("GDK释放成功")


if __name__ == "__main__":
    main()
```

#### 14. `move_arm_joint_servo()`

- **功能**：手臂关节位置伺服控制接口，需要以100hz的控制频率进行控制，支持正常模式和低延时模式，默认使用正常模式。
- **注意**：低延时模式无碰撞保护，使用时注意安全。
- **参数**：
  - `positions`：`list[float]`，手臂关节位置列表（弧度），按照"idx21_arm_l_joint1", "idx22_arm_l_joint2", "idx23_arm_l_joint3", "idx24_arm_l_joint4", "idx25_arm_l_joint5", "idx26_arm_l_joint6", "idx27_arm_l_joint7", "idx61_arm_r_joint1", "idx62_arm_r_joint2", "idx63_arm_r_joint3", "idx64_arm_r_joint4", "idx65_arm_r_joint5", "idx66_arm_r_joint6", "idx67_arm_r_joint7"顺序
  - `control_period`：`float`，控制周期（秒），建议比控制频率稍大
  - `control_group`：`int`，控制组，0表示控制左臂，1表示控制右臂，2表示控制双臂
  - `enable_low_latency`：`bool`，可选参数，默认为`False`，用于选择控制通道

**参数说明**：
- `positions` 长度必须为7(左臂或右臂)或14(双臂)
- `positions` 中的值必须在对应关节的限位范围内（见下方关节限位值说明），否则将抛出异常
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

- **返回值**：`int`，0表示成功，失败时抛出异常

- **异常说明**：
  - 如果 `positions` 的长度不为7(左臂或右臂)或14(双臂)，底层将返回 `ErrorCode::kInvalidInput`，Python 将抛出异常
  - 如果 `positions` 中的值超出对应关节的限位范围，底层将返回 `ErrorCode::kInvalidInput`，Python 将抛出异常

- **示例**：

```python
import agibot_gdk
import time
import math

# 控制参数
CONTROL_PERIOD = 0.01  # 控制周期（秒）
RATE_HZ = 100.0        # 发送频率（Hz）
DURATION = 5.0         # 控制持续时间（秒）

class ArmJointServoController:
    def __init__(self, robot):
        self.robot = robot

    def get_joint_position_by_name(self, joint_states, joint_name):
        """根据关节名称获取关节位置"""
        for state in joint_states['states']:
            if state['name'] == joint_name:
                return state['motor_position']
        raise RuntimeError(f"Joint name {joint_name} not found")

    def interpolate_position(self, start_pos, target_pos, t):
        """线性插值计算中间位置"""
        return start_pos + t * (target_pos - start_pos)

    def execute_arm_joint_servo_control(self, target_positions, control_group):
        """执行手臂关节位置伺服控制"""
        time.sleep(1.0)  # 等待1秒

        # 获取当前关节状态
        current_joint_states = self.robot.get_joint_states()

        # 获取起始位置
        arm_joint_names = [
            "idx21_arm_l_joint1", "idx22_arm_l_joint2", "idx23_arm_l_joint3",
            "idx24_arm_l_joint4", "idx25_arm_l_joint5", "idx26_arm_l_joint6",
            "idx27_arm_l_joint7",  # 左臂7个关节
            "idx61_arm_r_joint1", "idx62_arm_r_joint2", "idx63_arm_r_joint3",
            "idx64_arm_r_joint4", "idx65_arm_r_joint5", "idx66_arm_r_joint6",
            "idx67_arm_r_joint7"   # 右臂7个关节
        ]
        start_positions = []
        for joint_name in arm_joint_names:
            try:
                pos = self.get_joint_position_by_name(current_joint_states, joint_name)
                start_positions.append(pos)
                print(f"关节 {joint_name} 当前位置: {pos:.3f} 弧度")
            except RuntimeError as e:
                print(f"错误: {e}")
                return

        # 计算步数
        n_steps = int(DURATION * RATE_HZ)
        print(f"总步数: {n_steps}, 持续时间: {DURATION} 秒")

        # 执行轨迹
        dt = 1.0 / RATE_HZ
        start_time = time.time()

        for i in range(n_steps):
            t = float(i) / (n_steps - 1) if n_steps > 1 else 0.0

            # 计算当前目标位置（线性插值）
            current_positions = []
            for j in range(14):
                interp_pos = self.interpolate_position(
                    start_positions[j], target_positions[j], t
                )
                current_positions.append(interp_pos)

            try:
                # 使用普通模式（enable_low_latency=False，默认值）
                result = self.robot.move_arm_joint_servo(
                    current_positions, CONTROL_PERIOD, control_group
                )
                # 如需使用低延时模式，可传入 enable_low_latency=True：
                # result = self.robot.move_arm_joint_servo(
                #     current_positions, CONTROL_PERIOD, control_group, enable_low_latency=True
                # )
                if result != 0:
                    print(f"控制命令发送失败，步数: {i}")
                    return
            except Exception as e:
                print(f"控制命令发送异常，步数: {i}, 错误: {e}")
                return

            # 控制发送频率
            elapsed = time.time() - start_time
            expected_time = (i + 1) * dt
            sleep_time = expected_time - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)

        print("手臂关节位置伺服控制完成")

        # 保持最终位置
        print("进入最终位置保持（Ctrl+C 结束）...")
        try:
            while True:
                try:
                    # 使用普通模式（enable_low_latency=False，默认值）
                    result = self.robot.move_arm_joint_servo(
                        target_positions, CONTROL_PERIOD, control_group
                    )
                    # 如需使用低延时模式，可传入 enable_low_latency=True：
                    # result = self.robot.move_arm_joint_servo(
                    #     target_positions, CONTROL_PERIOD, control_group, enable_low_latency=True
                    # )
                    if result != 0:
                        print("保持位置失败")
                        break
                except Exception as e:
                    print(f"保持位置异常: {e}")
                    break

                time.sleep(dt)
        except KeyboardInterrupt:
            print("\n已中断保持")


def main():
    # 初始化GDK系统
    if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
        print("GDK初始化失败")
        return

    print("GDK初始化成功")

    try:
        robot = agibot_gdk.Robot()
        time.sleep(2)  # 等待机器人初始化

        # 获取当前关节状态
        current_joint_states = robot.get_joint_states()

        # 定义目标位置（示例：手臂关节）
        target_positions = [
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,  # 左臂7个关节
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0   # 右臂7个关节
        ]

        print(f"\n目标角度:")
        arm_joint_names = [
            "idx21_arm_l_joint1", "idx22_arm_l_joint2", "idx23_arm_l_joint3",
            "idx24_arm_l_joint4", "idx25_arm_l_joint5", "idx26_arm_l_joint6",
            "idx27_arm_l_joint7",  # 左臂7个关节
            "idx61_arm_r_joint1", "idx62_arm_r_joint2", "idx63_arm_r_joint3",
            "idx64_arm_r_joint4", "idx65_arm_r_joint5", "idx66_arm_r_joint6",
            "idx67_arm_r_joint7"   # 右臂7个关节
        ]
        for i, joint_name in enumerate(arm_joint_names):
            print(f"  {joint_name}: {target_positions[i]:.3f} 弧度")

        # 执行手臂关节位置伺服控制
        controller = ArmJointServoController(robot)
        controller.execute_arm_joint_servo_control(target_positions, 2)

    except Exception as e:
        print(f"执行过程中发生错误: {e}")
    finally:
        # 释放GDK系统资源
        if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
            print("GDK释放失败")
        else:
            print("GDK释放成功")


if __name__ == "__main__":
    main()
```

#### 15. `move_ee_pos()`

- **功能**：控制末端执行器位置（夹爪开合）
- **参数**：`JointStates` 对象

**JointStates对象结构**：

| 属性名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `group` | `str` | 控制组，必须为 "left_tool"、"right_tool" 或 "dual_tool" | 字符串 |
| `target_type` | `str` | 目标类型，支持的值见下表 | 字符串 |
| `states` | `list[JointState]` | 关节状态列表（必需） | JointState列表 |
| `nums` | `int` | 关节数量，应等于 `len(states)` | 无单位 |


**target_type 支持的值及对应的关节数量要求**：

| target_type 值 | 关节数量要求 | 说明 |
| :--- | :--- | :--- |
| `"omnipicker"` | 1 | 全向抓取器，需要1个关节 |
| `"dahuan"` | 1 | 大寰末端执行器，需要1个关节 |
| `"ctek90d"` | 1 | CTEK90D末端执行器，需要1个关节 |
| `"o10_t2"` | 10 | O10灵巧手末端执行器，需要10个关节 |
| `"o12_t2"` | 12 | O12灵巧手节末端执行器，需要12个关节 |

**各末端类型的关节位置取值范围**：

- **注意**：关节取值范围与版本绑定，使用时注意当前版本的取值范围，当前版本取值范围以文档为主
- **omnipicker**：`position` 取值范围为 `[-0.785, 0]`，其中 `-0.785` 表示打开，`0` 表示关闭
- **dahuan**：`position` 取值范围为 `[0, 0.025]`，其中 `0` 表示打开，`0.025` 表示关闭
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

**JointState对象结构**：

| 属性名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `position` | `float` | 关节位置（必需） | 开合度 |


**参数说明**：
- `group` 必须为 "left_tool"（左末端执行器）、"right_tool"（右末端执行器）或 "dual_tool"（双末端执行器）
  - 当 `group` 为 "left_tool" 或 "right_tool" 时，`states` 列表的长度必须与 `target_type` 对应的关节数量要求完全匹配
  - 当 `group` 为 "dual_tool" 时，`states` 列表的长度必须为 `target_type` 对应的关节数量要求的 2 倍（前半部分用于左末端执行器，后半部分用于右末端执行器）
- `target_type` 必须为上述支持的值之一，其他值将返回错误
- `states` 是一个 `JointState` 对象列表，每个 `JointState` 只需要设置 `position` 字段
- `nums` 必须等于 `len(states)`

- **返回值**：`int`，0表示成功，失败时抛出异常

- **异常说明**：
  - 如果 `target_type` 不是支持的值（"omnipicker", "dahuan", "ctek90d", "o10_t2", "o12_t2"），底层将返回 `ErrorCode::kInvalidInput`
  - 如果 `states` 的长度与 `target_type` 要求的关节数量不匹配（对于 "dual_tool"，必须是 2 倍），底层将返回 `ErrorCode::kInvalidInput`
  - 如果 `group` 不是 "left_tool"、"right_tool" 或 "dual_tool"，底层将返回 `ErrorCode::kInvalidInput`
  - 如果 `states` 为空，底层将返回 `ErrorCode::kInvalidInput`
  - 如果关节位置值超出对应末端类型的取值范围，底层将返回 `ErrorCode::kInvalidInput`
  - 如果控制命令执行失败，抛出 `std::runtime_error("Failed to move end effector position")`

- **示例**：

  **示例1：控制左夹爪（omnipicker类型，需要1个关节）**

  ```python
  import agibot_gdk
  import time

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  robot = agibot_gdk.Robot()
  time.sleep(2)  # 等待机器人初始化

  # 控制左夹爪（omnipicker类型，需要1个关节）
  joint_states_left = agibot_gdk.JointStates()
  joint_states_left.group = "left_tool"
  joint_states_left.target_type = "omnipicker"
  
  joint_state = agibot_gdk.JointState()
  joint_state.position = 0  # 取值范围 [-0.785, 0]  
  joint_states_left.states = [joint_state]
  joint_states_left.nums = len(joint_states_left.states)

  try:
      result = robot.move_ee_pos(joint_states_left)
      print("左夹爪控制成功")
  except Exception as e:
      print(f"左夹爪控制失败: {e}")

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

  **示例2：控制右夹爪（dahuan类型，需要1个关节）**

  ```python
  import agibot_gdk
  import time

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  robot = agibot_gdk.Robot()
  time.sleep(2)  # 等待机器人初始化

  # 控制右夹爪（dahuan类型，需要1个关节）
  joint_states_right = agibot_gdk.JointStates()
  joint_states_right.group = "right_tool"
  joint_states_right.target_type = "dahuan"
  
  joint_state = agibot_gdk.JointState()
  joint_state.position = 0  # 右手夹爪位置，取值范围 [0, 0.025]
  joint_states_right.states = [joint_state]
  joint_states_right.nums = len(joint_states_right.states)

  try:
      result = robot.move_ee_pos(joint_states_right)
      print("右夹爪控制成功")
  except Exception as e:
      print(f"右夹爪控制失败: {e}")

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

  **示例3：控制左夹爪（ctek90d类型，需要1个关节）**

  ```python
  import agibot_gdk
  import time

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  robot = agibot_gdk.Robot()
  time.sleep(2)  # 等待机器人初始化

  # 控制左夹爪（ctek90d类型，需要1个关节）
  joint_states_left = agibot_gdk.JointStates()
  joint_states_left.group = "left_tool"
  joint_states_left.target_type = "ctek90d"
  
  joint_state = agibot_gdk.JointState()
  joint_state.position = 0.5  # 取值范围 [-0.91, 0]
  joint_states_left.states = [joint_state]
  joint_states_left.nums = len(joint_states_left.states)

  try:
      result = robot.move_ee_pos(joint_states_left)
      print("左夹爪（ctek90d）控制成功")
  except Exception as e:
      print(f"左夹爪控制失败: {e}")

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

  **示例4：控制左末端执行器（o10_t2类型，需要10个关节）**

  ```python
  import agibot_gdk
  import time

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  robot = agibot_gdk.Robot()
  time.sleep(2)  # 等待机器人初始化

  # 控制左末端执行器（o10_t2类型，需要10个关节）
  joint_states_left_o10 = agibot_gdk.JointStates()
  joint_states_left_o10.group = "left_tool"
  joint_states_left_o10.target_type = "o10_t2"
  
  # 创建关节状态列表
  positions = [-0.2, 1.45, -0.75, 0, 1, 1, 0, 1, 0, 1]
  states_list = []
  for i in range(10):
      joint_state = agibot_gdk.JointState()
      joint_state.position = positions[i]
      states_list.append(joint_state)
  # 直接赋值整个列表
  joint_states_left_o10.states = states_list
  joint_states_left_o10.nums = len(joint_states_left_o10.states)

  try:
      result = robot.move_ee_pos(joint_states_left_o10)
      print("左末端执行器（o10_t2）控制成功")
  except Exception as e:
      print(f"左末端执行器控制失败: {e}")

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

  **示例5：控制右末端执行器（o12_t2类型，需要12个关节）**

  ```python
  import agibot_gdk
  import time

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  robot = agibot_gdk.Robot()
  time.sleep(2)  # 等待机器人初始化

  # 控制右末端执行器（o12_t2类型，需要12个关节）
  joint_states_right_o12 = agibot_gdk.JointStates()
  joint_states_right_o12.group = "right_tool"
  joint_states_right_o12.target_type = "o12_t2"
  
  # 创建关节状态列表
  states_list = []
  for i in range(12):
      joint_state = agibot_gdk.JointState()
      joint_state.position = 0
      states_list.append(joint_state)
  # 直接赋值整个列表
  joint_states_right_o12.states = states_list
  joint_states_right_o12.nums = len(joint_states_right_o12.states)

  try:
      result = robot.move_ee_pos(joint_states_right_o12)
      print("右末端执行器（o12_t2）控制成功")
  except Exception as e:
      print(f"右末端执行器控制失败: {e}")

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

  **示例6：控制双末端执行器（dual_tool，需要2倍关节数量）**

  ```python
  import agibot_gdk
  import time

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  robot = agibot_gdk.Robot()
  time.sleep(2)  # 等待机器人初始化

  # 控制双末端执行器（dual_tool，需要2倍关节数量）
  # 例如：使用 omnipicker 类型，需要 2 个关节（左1个 + 右1个）
  joint_states_dual = agibot_gdk.JointStates()
  joint_states_dual.group = "dual_tool"
  joint_states_dual.target_type = "omnipicker"
  
  # 前半部分用于左末端执行器
  joint_state_left = agibot_gdk.JointState()
  joint_state_left.position = 0
  # 后半部分用于右末端执行器
  joint_state_right = agibot_gdk.JointState()
  joint_state_right.position = 0
  # 直接赋值整个列表
  joint_states_dual.states = [joint_state_left, joint_state_right]
  joint_states_dual.nums = len(joint_states_dual.states)

  try:
      result = robot.move_ee_pos(joint_states_dual)
      print("双末端执行器控制成功")
  except Exception as e:
      print(f"双末端执行器控制失败: {e}")

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

#### 16. `end_effector_pose_control()`

- **功能**：末端执行器位姿控制
- **注意**：该接口要求发送端以50hz频率发布控制命令，不允许阶越信号；该接口无碰撞检测，注意使用时环境。
- **参数**：`EndEffectorPose`对象，包含以下属性：

| 属性名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `life_time` | `float` | 生命周期 | 秒 |
| `group` | `int` | 控制组 | 整数 |
| `left_end_effector_pose` | `Pose` | 左末端执行器位姿（base_link坐标系下） | 位姿 |
| `right_end_effector_pose` | `Pose` | 右末端执行器位姿（base_link坐标系下）| 位姿 |

- **返回值**：`int`，0表示成功，失败时抛出异常

- **示例**：（注意：为保证安全，该示例会将机器移动到初始位姿（站立），再调用末端位姿控制，请在确保机器人周围空间安全的情况下运行）

```python
import agibot_gdk
import time
import math


# 常量定义
LEFT_NAME = "arm_l_end_link"
RIGHT_NAME = "arm_r_end_link"

# 目标位姿（位置和四元数）
TARGET_LEFT_POSITION = [0.626755,0.301127306,1.08398]
TARGET_LEFT_ORIENTATION =  [0.5858436, -0.02614889,0.80973243,0.02089957]

TARGET_RIGHT_POSITION = [0.6099763,-0.3903393, 1.050190472]
TARGET_RIGHT_ORIENTATION =  [0.648815,-0.001096,0.76094223696, 0.0020416]

# 控制参数
MAX_STEP_CM = 0.1  # 最大步长（厘米）
LIFETIME = 0.02    # 生命周期（秒）
RATE_HZ = 50.0     # 发送频率（Hz）
HOLD_FINAL = True  # 是否保持最终位姿


class EndEffectorController:
    def __init__(self, robot):
        self.robot = robot

    def slerp(self, q0, q1, t):
        """
        四元数球面线性插值
        q0, q1: 四元数 [x, y, z, w]
        t: 插值参数 [0, 1]
        返回: 插值后的四元数 [x, y, z, w]
        """
        # 计算点积
        dot = q0[0]*q1[0] + q0[1]*q1[1] + q0[2]*q1[2] + q0[3]*q1[3]

        # 如果点积为负，取反q1以确保最短路径
        if dot < 0.0:
            dot = -dot
            q1_neg = [-q1[0], -q1[1], -q1[2], -q1[3]]
            result = [q0[i] + t * (q1_neg[i] - q0[i]) for i in range(4)]
        else:
            result = [q0[i] + t * (q1[i] - q0[i]) for i in range(4)]

        # 限制点积范围
        dot = max(-1.0, min(1.0, dot))

        if dot > 0.9995:
            # 线性插值
            norm = math.sqrt(sum(r*r for r in result))
            if norm > 0.0:
                result = [r / norm for r in result]
        else:
            # 球面线性插值
            theta_0 = math.acos(dot)
            sin_theta_0 = math.sin(theta_0)
            theta = theta_0 * t
            sin_theta = math.sin(theta)
            s0 = math.cos(theta) - dot * sin_theta / sin_theta_0
            s1 = sin_theta / sin_theta_0

            result = [s0 * q0[i] + s1 * q1[i] for i in range(4)]

        return result

    def distance_between_points(self, p1, p2):
        """计算两点之间的距离"""
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        dz = p2[2] - p1[2]
        return math.sqrt(dx*dx + dy*dy + dz*dz)

    def calculate_n_steps(self, start_pos, goal_pos, max_step_cm):
        """计算需要的步数"""
        dist_cm = self.distance_between_points(start_pos, goal_pos) * 100.0
        return max(int(math.ceil(dist_cm / max_step_cm)), 1)

    def plan_trajectory(self, start_pose, goal_pose, n_steps):
        """
        规划轨迹
        start_pose, goal_pose: 包含position和orientation的字典
        n_steps: 步数
        返回: 轨迹列表
        """
        trajectory = []

        for i in range(n_steps):
            t = float(i) / (n_steps - 1) if n_steps > 1 else 0.0

            # 位置线性插值
            pos = [
                start_pose['position'][0] + t * (goal_pose['position'][0] - start_pose['position'][0]),
                start_pose['position'][1] + t * (goal_pose['position'][1] - start_pose['position'][1]),
                start_pose['position'][2] + t * (goal_pose['position'][2] - start_pose['position'][2])
            ]

            # 四元数SLERP插值
            q0 = start_pose['orientation']
            q1 = goal_pose['orientation']
            quat = self.slerp(q0, q1, t)

            trajectory.append({
                'position': pos,
                'orientation': quat
            })

        return trajectory

    def find_pose_by_name(self, status, target_name):
        """根据名称查找位姿"""
        for i, frame_name in enumerate(status.frame_names):
            if frame_name == target_name:
                pose = status.frame_poses[i]
                # 提取位置和四元数
                position = [pose.position.x, pose.position.y, pose.position.z]
                orientation = [pose.orientation.x, pose.orientation.y,
                              pose.orientation.z, pose.orientation.w]
                return {'position': position, 'orientation': orientation}
        raise RuntimeError(f"Frame name {target_name} not found")

    def execute_end_pose_control(self):
        """执行末端位姿控制"""
        time.sleep(1.0)  # 等待1秒

        # 获取当前状态
        status = self.robot.get_motion_control_status()

        # 获取起始位姿
        start_left_pose = self.find_pose_by_name(status, LEFT_NAME)
        start_right_pose = self.find_pose_by_name(status, RIGHT_NAME)

        # 目标位姿
        goal_left_pose = {
            'position': TARGET_LEFT_POSITION,
            'orientation': TARGET_LEFT_ORIENTATION
        }
        goal_right_pose = {
            'position': TARGET_RIGHT_POSITION,
            'orientation': TARGET_RIGHT_ORIENTATION
        }

        # 计算步数
        n_left = self.calculate_n_steps(start_left_pose['position'],
                                        goal_left_pose['position'],
                                        MAX_STEP_CM)
        n_right = self.calculate_n_steps(start_right_pose['position'],
                                        goal_right_pose['position'],
                                        MAX_STEP_CM)
        n_steps = max(n_left, n_right)

        print(f"左臂步数: {n_left}, 右臂步数: {n_right}, 总步数: {n_steps}")
        # 规划轨迹
        traj_left = self.plan_trajectory(start_left_pose, goal_left_pose, n_steps)
        traj_right = self.plan_trajectory(start_right_pose, goal_right_pose, n_steps)

        # 执行轨迹
        dt = 1.0 / RATE_HZ
        for i in range(n_steps):
            # 创建末端执行器位姿控制请求
            end_pose = agibot_gdk.EndEffectorPose()
            end_pose.life_time = LIFETIME
            end_pose.group = agibot_gdk.EndEffectorControlGroup.kBothArms

            # 设置左臂位姿
            end_pose.left_end_effector_pose.position.x = traj_left[i]['position'][0]
            end_pose.left_end_effector_pose.position.y = traj_left[i]['position'][1]
            end_pose.left_end_effector_pose.position.z = traj_left[i]['position'][2]
            end_pose.left_end_effector_pose.orientation.x = traj_left[i]['orientation'][0]
            end_pose.left_end_effector_pose.orientation.y = traj_left[i]['orientation'][1]
            end_pose.left_end_effector_pose.orientation.z = traj_left[i]['orientation'][2]
            end_pose.left_end_effector_pose.orientation.w = traj_left[i]['orientation'][3]

            # 设置右臂位姿
            end_pose.right_end_effector_pose.position.x = traj_right[i]['position'][0]
            end_pose.right_end_effector_pose.position.y = traj_right[i]['position'][1]
            end_pose.right_end_effector_pose.position.z = traj_right[i]['position'][2]
            end_pose.right_end_effector_pose.orientation.x = traj_right[i]['orientation'][0]
            end_pose.right_end_effector_pose.orientation.y = traj_right[i]['orientation'][1]
            end_pose.right_end_effector_pose.orientation.z = traj_right[i]['orientation'][2]
            end_pose.right_end_effector_pose.orientation.w = traj_right[i]['orientation'][3]

            try:
                result = self.robot.end_effector_pose_control(end_pose)
                if result != 0:
                    print(f"控制命令发送失败，步数: {i}")
                    return
                print(f"控制命令发送成功，步数: {i}")
            except Exception as e:
                print(f"控制命令发送异常，步数: {i}, 错误: {e}")
                return

            time.sleep(dt)

        # 保持最终位姿
        if HOLD_FINAL:
            print("进入末端位姿保持（Ctrl+C 结束）...")
            try:
                final_left = traj_left[-1]
                final_right = traj_right[-1]

                while True:
                    end_pose = agibot_gdk.EndEffectorPose()
                    end_pose.life_time = LIFETIME
                    end_pose.group = agibot_gdk.EndEffectorControlGroup.kBothArms

                    # 设置左臂位姿
                    end_pose.left_end_effector_pose.position.x = final_left['position'][0]
                    end_pose.left_end_effector_pose.position.y = final_left['position'][1]
                    end_pose.left_end_effector_pose.position.z = final_left['position'][2]
                    end_pose.left_end_effector_pose.orientation.x = final_left['orientation'][0]
                    end_pose.left_end_effector_pose.orientation.y = final_left['orientation'][1]
                    end_pose.left_end_effector_pose.orientation.z = final_left['orientation'][2]
                    end_pose.left_end_effector_pose.orientation.w = final_left['orientation'][3]

                    # 设置右臂位姿
                    end_pose.right_end_effector_pose.position.x = final_right['position'][0]
                    end_pose.right_end_effector_pose.position.y = final_right['position'][1]
                    end_pose.right_end_effector_pose.position.z = final_right['position'][2]
                    end_pose.right_end_effector_pose.orientation.x = final_right['orientation'][0]
                    end_pose.right_end_effector_pose.orientation.y = final_right['orientation'][1]
                    end_pose.right_end_effector_pose.orientation.z = final_right['orientation'][2]
                    end_pose.right_end_effector_pose.orientation.w = final_right['orientation'][3]

                    try:
                        result = self.robot.end_effector_pose_control(end_pose)
                        if result != 0:
                            print("保持位姿失败")
                            break
                    except Exception as e:
                        print(f"保持位姿异常: {e}")
                        break

                    time.sleep(dt)
            except KeyboardInterrupt:
                print("\n已中断保持")


def main():
    # 初始化GDK系统
    if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
        print("GDK初始化失败")
        return

    print("GDK初始化成功")

    try:
        robot = agibot_gdk.Robot()
        time.sleep(2)  # 等待机器人初始化

        print("正在移动到初始位姿...")
        joint_control_req = agibot_gdk.JointControlReq()
        joint_control_req.joint_names = [
            "idx01_body_joint1", "idx02_body_joint2", "idx03_body_joint3", "idx04_body_joint4", "idx05_body_joint5",
            "idx11_head_joint1", "idx12_head_joint2", "idx13_head_joint3",
            "idx21_arm_l_joint1", "idx22_arm_l_joint2", "idx23_arm_l_joint3",
            "idx24_arm_l_joint4", "idx25_arm_l_joint5", "idx26_arm_l_joint6",
            "idx27_arm_l_joint7",  # 左臂7个关节
            "idx61_arm_r_joint1", "idx62_arm_r_joint2", "idx63_arm_r_joint3",
            "idx64_arm_r_joint4", "idx65_arm_r_joint5", "idx66_arm_r_joint6",
            "idx67_arm_r_joint7"   # 右臂7个关节
        ]
        joint_control_req.joint_positions = [-0.12526109443163597,
                                            0.8407635483115572,
                                            -0.971927299903638,
                                            0, 
                                            0,
                                            0,
                                            0,
                                            0.0036426282540360732,
                                            1.7301117664332919,
                                            -1.1500181062743811,
                                            -1.5999388458662482,
                                            -1.79993398793182,
                                            -0.41992232715148303, 
                                            5.8962386534354331e-05, 
                                            3.8709046444301724e-05, 
                                            -1.7301030279359648, 
                                            -1.1500377304426637, 
                                            1.5999483134039236, 
                                            -1.6252835640650924, 
                                            0.42000178256260562, 
                                            1.3781858641160056e-05, 
                                            3.7151097206605374e-06]
        joint_control_req.joint_velocities = [0.3] * 22 # 设置速度
        joint_control_req.life_time = 5.0

        result = robot.joint_control_request(joint_control_req)
        if result != 0:
            print("移动到初始位姿失败")
            return
        print("移动到初始位姿成功，等待到位...")
        time.sleep(2)  

        controller = EndEffectorController(robot)
        controller.execute_end_pose_control()

    except Exception as e:
        print(f"执行过程中发生错误: {e}")
    finally:
        # 释放GDK系统资源
        if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
            print("GDK释放失败")
        else:
            print("GDK释放成功")


if __name__ == "__main__":
    main()
```

## 使用注意事项

1. **GDK初始化**：使用机器人控制功能前必须先调用`agibot_gdk.gdk_init()`初始化GDK系统
2. **GDK释放**：程序结束前必须调用`agibot_gdk.gdk_release()`释放GDK系统资源
3. **初始化等待**：创建Robot对象后，建议等待2秒以确保DDS连接建立
4. **关节名称**：使用前请确认关节名称的正确性，可通过`get_motion_control_status()`获取
5. **位置范围**：关节位置应在安全范围内，避免超出机械限制
6. **速度限制**：设置合理的关节速度，避免过快运动造成危险
7. **生命周期**：合理设置请求生命周期，避免命令过期
8. **异常处理**：所有接口在失败时会抛出`std::runtime_error`异常，需要适当处理
9. **数据类型**：位置参数使用弧度单位，速度参数使用弧度/秒单位
10. **时间戳精度**：时间戳单位为纳秒，可用于精确的时间同步

## 应用场景

- **基础控制**：实现机器人的基本运动控制
- **状态监控**：实时监控机器人各关节状态
- **动作录制**：录制和回放机器人动作序列
- **精确控制**：实现高精度的关节位置控制
- **安全检测**：监控机器人异常状态，确保安全运行
- **末端执行器控制**：控制夹爪等末端执行器的开合
- **多关节协调**：实现多个关节的协调运动
- **位姿控制**：基于笛卡尔坐标系的末端执行器位姿控制
