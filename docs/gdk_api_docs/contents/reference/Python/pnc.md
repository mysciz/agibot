# GDK PNC 接口文档（Python）

## 概述

PNC（Planning and Control，规划与控制）模块为G02机器人提供了路径规划和导航控制功能。通过Python接口，开发者可以方便地实现机器人的自主导航、路径规划、任务状态管理等功能，适用于自主导航、路径规划、任务调度等多种场景。

## 接口说明

### Pnc 类

该类封装了机器人路径规划和导航控制的主要接口。

#### 1. `get_task_state()`

- **功能**：获取当前任务状态
- **参数**：无
- **返回值**：`PNCTaskState`对象，包含以下属性：

| 属性名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `state` | `int` | 任务状态码 | 整数 |
| `message` | `str` | 状态描述信息 | 字符串 |
| `id` | `int` | 任务ID | 整数 |
| `type` | `int` | 任务类型 | 整数 |

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

  ```python
  import agibot_gdk
  import time

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  pnc = agibot_gdk.Pnc()
  time.sleep(2)  # 等待PNC初始化

  # 获取任务状态
  task_state = pnc.get_task_state()
  print(f"PNC任务状态: {task_state.state}")
  print(f"PNC任务ID: {task_state.id}")
  print(f"PNC任务内容: {task_state.message}")
  print(f"PNC任务种类: {task_state.type}")

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

#### 2. `normal_navi()`

- **功能**：执行正常导航到指定目标点, 执行之前需要在G02 Pad上进行重定位
- **参数**：`NaviReq`对象(map坐标系下)，包含以下属性：

| 属性名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `target.position.x` | `float` | 目标位置X坐标 | 米 |
| `target.position.y` | `float` | 目标位置Y坐标 | 米 |
| `target.position.z` | `float` | 目标位置Z坐标 | 米 |
| `target.orientation.x` | `float` | 目标方向四元数X分量 | 无单位 |
| `target.orientation.y` | `float` | 目标方向四元数Y分量 | 无单位 |
| `target.orientation.z` | `float` | 目标方向四元数Z分量 | 无单位 |
| `target.orientation.w` | `float` | 目标方向四元数W分量 | 无单位 |

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

  pnc = agibot_gdk.Pnc()
  time.sleep(2)  # 等待PNC初始化

  # 创建导航目标
  target = agibot_gdk.NaviReq()
  target.target.position.x = -0.14157561800950003
  target.target.position.y = 0.015152394013126735
  target.target.position.z = 0.0040338473100211417
  target.target.orientation.x = 0.01146358383671978
  target.target.orientation.y = -0.01720065085681078
  target.target.orientation.z = 0.83847410642918951
  target.target.orientation.w = 0.54454926012574167

  # 执行导航
  try:
      pnc.normal_navi(target)
      print("正常导航请求发送成功")
  except Exception as e:
      print(f"正常导航失败: {e}")

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

#### 3. `high_precision_navi()` (该接口暂未上线)

- **功能**：执行高精度导航到指定目标点, 执行之前需要在G02 Pad上进行重定位
- **参数**：`NaviReq`对象(map坐标系下)
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

  pnc = agibot_gdk.Pnc()
  time.sleep(2)  # 等待PNC初始化

  # 创建高精度导航目标
  target = agibot_gdk.NaviReq()
  target.target.position.x = 1.0
  target.target.position.y = 2.0
  target.target.position.z = 0.0
  target.target.orientation.x = 0.0
  target.target.orientation.y = 0.0
  target.target.orientation.z = 0.0
  target.target.orientation.w = 1.0

  # 执行高精度导航
  try:
      pnc.high_precision_navi(target)
      print("高精度导航请求发送成功")
  except Exception as e:
      print(f"高精度导航失败: {e}")

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

#### 4. `relative_move()`

- **功能**：执行小范围平移, 简单停障，无避障，执行之前需要在G02 Pad上进行重定位
- **参数**：`NaviReq`对象(base_link坐标系下)
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

  pnc = agibot_gdk.Pnc()
  time.sleep(2)  # 等待PNC初始化

  # 创建相对移动目标
  target = agibot_gdk.NaviReq()
  target.target.position.x = 0.5  # 相对前进0.5米
  target.target.position.y = 0.0
  target.target.position.z = 0.0
  target.target.orientation.x = 0.0
  target.target.orientation.y = 0.0
  target.target.orientation.z = 0.0
  target.target.orientation.w = 1.0

  # 执行相对移动
  try:
      pnc.relative_move(target)
      print("相对移动请求发送成功")
  except Exception as e:
      print(f"相对移动失败: {e}")

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

#### 5. `cancel_task()`

- **功能**：取消指定ID的导航任务
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `task_id` | `int` | 要取消的任务ID |

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

  pnc = agibot_gdk.Pnc()
  time.sleep(2)  # 等待PNC初始化

  # 先获取当前任务状态以获取任务ID
  try:
      task_state = pnc.get_task_state()
      task_id = task_state.id

      # 取消指定ID的导航任务
      pnc.cancel_task(task_id)
      print("取消任务请求发送成功")
  except Exception as e:
      print(f"取消任务失败: {e}")

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

#### 6. `pause_task()`

- **功能**：暂停指定ID的导航任务
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `task_id` | `int` | 要暂停的任务ID |

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

  pnc = agibot_gdk.Pnc()
  time.sleep(2)  # 等待PNC初始化

  # 先获取当前任务状态以获取任务ID
  try:
      task_state = pnc.get_task_state()
      task_id = task_state.id

      # 暂停指定ID的任务
      pnc.pause_task(task_id)
      print("暂停任务请求发送成功")
  except Exception as e:
      print(f"暂停任务失败: {e}")

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

#### 7. `resume_task()`

- **功能**：恢复指定ID的导航任务
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `task_id` | `int` | 要恢复的任务ID |

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

  pnc = agibot_gdk.Pnc()
  time.sleep(2)  # 等待PNC初始化

  # 先获取当前任务状态以获取任务ID
  try:
      task_state = pnc.get_task_state()
      task_id = task_state.id

      # 恢复指定ID的任务
      pnc.resume_task(task_id)
      print("恢复任务请求发送成功")
  except Exception as e:
      print(f"恢复任务失败: {e}")

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

#### 8. `request_chassis_control()`

- **功能**：请求底盘控制权限，用于远程控制模式
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `control_mode` | `int` | 控制模式：0=阿克曼模式，1=蟹行模式 |

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

  pnc = agibot_gdk.Pnc()
  time.sleep(2)  # 等待PNC初始化

  # 请求底盘控制权限
  try:
      pnc.request_chassis_control(0)
      print("底盘控制权限请求发送成功")
  except Exception as e:
      print(f"底盘控制权限请求失败: {e}")

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

#### 9. `move_chassis()`

- **功能**：移动底盘，用于远程控制模式下的底盘运动控制
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `twist` | `Twist` | 速度指令对象，包含线速度和角速度 |

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

  pnc = agibot_gdk.Pnc()
  time.sleep(2)  # 等待PNC初始化

  # 请求底盘控制权限
  try:
      pnc.request_chassis_control(0)
      print("底盘控制权限请求发送成功")
  except Exception as e:
      print(f"底盘控制权限请求失败: {e}")

  # 创建速度指令(阿克曼行走)
  twist = agibot_gdk.Twist()
  twist.linear.x = 0.5  # 线速度0.5米/秒
  twist.angular.z = 0.1  # 角速度0.1弧度/秒

  # 移动底盘
  try:
      pnc.move_chassis(twist)
      print("底盘移动请求发送成功")
  except Exception as e:
      print(f"底盘移动失败: {e}")

  task_state = pnc.get_task_state()
  print(f"任务状态: {task_state.state}")
  task_id = task_state.id
  try:
      pnc.cancel_task(task_id)
      print("任务取消请求发送成功")
  except Exception as e:
      print(f"任务取消请求失败: {e}")

  # 创建速度指令（蟹行行走）
  twist = agibot_gdk.Twist()
  twist.linear.x = 0.0  # 线速度0米/秒
  twist.linear.y = 0.5 # 左平移速度0.5米/秒
  twist.angular.z = 0.0  # 角速度0弧度/秒

  # 移动底盘
  try:
      pnc.move_chassis(twist)
      print("底盘移动请求发送成功")
  except Exception as e:
      print(f"底盘移动失败: {e}")

  # 获取任务状态
  task_state = pnc.get_task_state()
  print(f"任务状态: {task_state.state}")
  task_id = task_state.id
  try:
      pnc.cancel_task(task_id)
      print("任务取消请求发送成功")
  except Exception as e:
      print(f"任务取消请求失败: {e}")

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

## 使用注意事项

1. **GDK初始化**：使用PNC功能前必须先调用`agibot_gdk.gdk_init()`初始化GDK系统
2. **GDK释放**：程序结束前必须调用`agibot_gdk.gdk_release()`释放GDK系统资源
3. **初始化等待**：创建Pnc对象后，建议等待2秒以确保系统初始化完成
4. **目标设置**：确保目标位置在机器人可达范围内
5. **坐标系**：注意使用正确的坐标系（通常是机器人本体坐标系）
6. **任务状态**：及时检查任务状态，处理可能的错误情况
7. **安全考虑**：在导航过程中注意周围环境安全
8. **异常处理**：所有接口在失败时会抛出`std::runtime_error`异常，需要适当处理
9. **资源管理**：在程序退出前确保调用`cancel_task()`停止正在进行的任务

## 应用场景

- **自主导航**：实现机器人在环境中的自主移动
- **路径规划**：规划从起点到终点的最优路径
- **任务调度**：管理多个导航任务的执行
- **位置控制**：精确控制机器人到达指定位置和姿态
- **避障导航**：在动态环境中实现安全导航
- **高精度导航**：需要精确定位的应用场景
- **相对移动**：基于当前位置的相对位移控制
- **任务控制**：动态暂停、恢复或取消导航任务
