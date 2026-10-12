# GDK Map 接口文档（Python）

## 概述

Map（地图）模块为G02机器人提供了地图管理功能。通过Python接口，开发者可以方便地获取、切换、管理机器人构建的地图，适用于地图存储、地图切换、地图管理等多种场景。

## 接口说明

### Map 类

该类封装了地图管理的主要功能接口。

#### 1. `get_curr_map()`

- **功能**：获取当前使用的地图信息
- **参数**：无

- **返回值**：`MapName`对象，包含以下属性：

| 属性名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `id` | `int` | 地图ID | 整数 |
| `name` | `str` | 地图名称 | 字符串 |
| `is_curr_map` | `bool` | 是否为当前地图 | 布尔值 |

- **示例**：

  ```python
  import agibot_gdk
  import time

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  map_manager = agibot_gdk.Map()
  time.sleep(2)  # 等待地图管理器初始化
  
  # 获取当前地图
  current_map = map_manager.get_curr_map()
  print(f"当前地图:")
  print(f"  地图ID: {current_map.id}")
  print(f"  地图名称: {current_map.name}")
  print(f"  是否为当前地图: {current_map.is_curr_map}")

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

#### 2. `get_all_map()`

- **功能**：获取所有可用地图列表
- **参数**：无

- **返回值**：`list[MapName]`，地图名称列表

- **示例**：

  ```python
  import agibot_gdk
  import time

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  map_manager = agibot_gdk.Map()
  time.sleep(2)  # 等待地图管理器初始化
  
  # 获取所有地图
  all_maps = map_manager.get_all_map()
  print(f"所有地图数量: {len(all_maps)}")
  
  for i, map_name in enumerate(all_maps):
      print(f"地图 {i+1}:")
      print(f"  ID: {map_name.id}")
      print(f"  名称: {map_name.name}")
      print(f"  是否为当前地图: {map_name.is_curr_map}")

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

#### 3. `switch_map()`

- **功能**：切换到指定地图
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `map_id` | `int` | 目标地图ID |

- **返回值**：无（成功时无返回值，失败时抛出异常）

- **示例**：

  ```python
  import agibot_gdk
  import time

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  map_manager = agibot_gdk.Map()
  time.sleep(2)  # 等待地图管理器初始化
  
  try:
      # 切换到指定地图
      map_manager.switch_map(1)
      print("地图切换成功")
      
      # 验证切换结果
      current_map = map_manager.get_curr_map()
      print(f"当前地图ID: {current_map.id}")
      print(f"当前地图名称: {current_map.name}")
  except Exception as e:
      print(f"地图切换失败: {e}")

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

#### 4. `remove_map()`

- **功能**：删除指定地图
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `map_id` | `int` | 要删除的地图ID |

- **返回值**：无（成功时无返回值，失败时抛出异常）

- **示例**：

  ```python
  import agibot_gdk
  import time

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  map_manager = agibot_gdk.Map()
  time.sleep(2)  # 等待地图管理器初始化
  
  try:
      # 删除指定地图
      map_manager.remove_map(2)
      print("地图删除成功")
      
      # 验证删除结果
      all_maps = map_manager.get_all_map()
      print(f"剩余地图数量: {len(all_maps)}")
  except Exception as e:
      print(f"地图删除失败: {e}")

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
  else:
      print("GDK释放成功")
  ```

## 使用注意事项

1. **GDK初始化**：使用地图功能前必须先调用`agibot_gdk.gdk_init()`初始化GDK系统
2. **GDK释放**：程序结束前必须调用`agibot_gdk.gdk_release()`释放GDK系统资源
3. **初始化等待**：创建Map对象后，建议等待2秒以确保系统初始化完成
4. **地图ID**：确保使用有效的地图ID，避免访问不存在的地图
5. **地图切换**：切换地图时确保当前没有正在进行的导航任务
6. **地图删除**：删除地图前确认该地图不再需要，删除操作不可逆
7. **存储空间**：注意地图文件占用的存储空间，及时清理不需要的地图
8. **异常处理**：所有接口在失败时会抛出`std::runtime_error`异常，需要适当处理
9. **数据类型**：地图ID使用`uint8_t`类型，范围为0-255
10. **时间戳精度**：时间戳单位为纳秒，可用于精确的时间同步

## 应用场景

- **地图管理**：管理机器人构建的多个地图
- **环境切换**：在不同工作环境间切换地图
- **地图备份**：保存和恢复重要地图数据
- **存储优化**：清理不需要的地图以节省存储空间
- **环境感知**：利用地图中的墙壁和不可行区域信息
- **引导点导航**：使用地图中的引导点进行精确导航
