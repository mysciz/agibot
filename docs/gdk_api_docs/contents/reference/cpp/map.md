# GDK Map 接口文档（C++）

## 概述

Map（地图）模块为G02机器人提供了地图管理功能。通过C++接口，开发者可以方便地获取、切换、管理机器人构建的地图，适用于地图存储、地图切换、地图管理等多种场景。

## 接口说明

### Map 类

该类封装了地图管理的主要功能接口。

#### 1. `GetCurrMap()`

- **功能**：获取当前使用的地图信息
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `map_name` | `MapName&` | 输出参数，当前地图名称信息 |

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`，`map_name`参数包含当前地图信息

#### MapName对象详细说明

**MapName结构体包含以下成员**：

| 成员名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `id` | `uint32_t` | 地图ID | 无单位 |
| `name` | `std::string` | 地图名称 | 字符串 |
| `is_curr_map` | `bool` | 是否为当前地图 | 布尔值 |

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

      Map map_manager;
      std::this_thread::sleep_for(std::chrono::seconds(1)); // 等待1秒以确保DDS连接建立
      MapName current_map;
      GDKRes result = map_manager.GetCurrMap(current_map);
      
      if (result == GDKRes::kSuccess) {
          std::cout << "当前地图: " << std::endl;
          std::cout << "当前地图ID: " << current_map.id << std::endl;
          std::cout << "当前地图名称: " << current_map.name << std::endl;
          std::cout << "是否为当前地图: " << (current_map.is_curr_map ? "是" : "否") << std::endl;
      } else {
          std::cout << "获取当前地图失败" << std::endl;
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

#### 2. `GetAllMap()`

- **功能**：获取所有可用地图列表
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `map_names` | `std::vector<MapName>&` | 输出参数，地图名称列表 |

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`，`map_names`参数包含所有地图信息

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

      Map map_manager;
      std::this_thread::sleep_for(std::chrono::seconds(1)); // 等待1秒以确保DDS连接建立      
      std::vector<MapName> map_names;
      GDKRes result = map_manager.GetAllMap(map_names);
      
      if (result == GDKRes::kSuccess) {
          std::cout << "地图列表: " << std::endl;
          std::cout << "地图数量: " << map_names.size() << std::endl;
          
          for (const auto& map_name : map_names) {
              std::cout << "地图ID: " << map_name.id 
                        << ", 名称: " << map_name.name
                        << ", 当前地图: " << (map_name.is_curr_map ? "是" : "否") << std::endl;
          }
      } else {
          std::cout << "获取地图列表失败" << std::endl;
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

#### 3. `SwitchMap()`

- **功能**：切换到指定ID的地图
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `map_id` | `const uint8_t` | 地图ID |

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

      Map map_manager;
      std::this_thread::sleep_for(std::chrono::seconds(1)); // 等待1秒以确保DDS连接建立      
      // 切换到地图ID为1的地图
      GDKRes result = map_manager.SwitchMap(1);
      
      if (result == GDKRes::kSuccess) {
          std::cout << "地图切换成功" << std::endl;
          
          // 验证切换结果
          MapName current_map;
          result = map_manager.GetCurrMap(current_map);
          if (result == GDKRes::kSuccess) {
              std::cout << "当前地图ID: " << current_map.id << std::endl;
          }
      } else {
          std::cout << "地图切换失败" << std::endl;
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

#### 4. `RemoveMap()`

- **功能**：删除指定ID的地图
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `map_id` | `const uint8_t` | 地图ID |

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

      Map map_manager;
      std::this_thread::sleep_for(std::chrono::seconds(1)); // 等待1秒以确保DDS连接建立 
      // 删除地图ID为2的地图
      GDKRes result = map_manager.RemoveMap(2);
      
      if (result == GDKRes::kSuccess) {
          std::cout << "地图删除成功" << std::endl;
      } else {
          std::cout << "地图删除失败" << std::endl;
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

1. **GDK初始化**：使用Map功能前必须先调用`agibot::gdk::GDKInit()`初始化GDK系统
2. **GDK释放**：程序结束前必须调用`agibot::gdk::GDKRelease()`释放GDK系统资源
3. **初始化等待**：创建Map对象后，建议等待1秒以确保DDS连接建立
4. **地图ID有效性**：使用前请确保地图ID存在且有效
5. **返回值检查**：使用前请检查GDKRes返回值是否为kSuccess
6. **地图切换**：切换地图时确保当前没有正在进行的导航任务
7. **地图更新**：更新地图时注意数据格式的正确性
8. **资源管理**：注意地图数据的内存使用，特别是大型地图
9. **错误处理**：始终检查GDKRes返回值，确保操作成功

## 应用场景

- **地图存储**：管理和存储机器人构建的地图数据
- **地图切换**：在不同环境间切换使用不同的地图
- **地图管理**：添加、删除、更新地图信息
- **导航支持**：为导航系统提供地图数据支持
- **环境建模**：构建和维护环境的空间模型
- **路径规划**：为路径规划提供地图基础数据
- **引导点管理**：管理地图中的关键位置点
- **区域标记**：标记不可通行区域和特殊区域
