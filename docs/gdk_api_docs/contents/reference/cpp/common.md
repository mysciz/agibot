# GDK Common 接口文档（C++）

## 概述

Common（通用）模块为G02机器人提供了GDK系统的初始化和释放功能。通过C++接口，开发者可以方便地管理GDK系统的生命周期，确保系统正确启动和资源正确释放。

## 接口说明

### 全局函数

#### 1. `GDKInit()`

- **功能**：初始化GDK系统
- **参数**：无
- **返回值**：`GDKRes`，操作结果状态码
  - `GDKRes::kSuccess`：初始化成功
  - 其他值：初始化失败

- **说明**：
  - 必须在调用其他GDK功能之前调用此函数
  - 初始化GDK内部系统、DDS连接、配置管理等
  - 建议在程序开始时调用一次

- **示例**：

  ```cpp
  #include <iostream>
  #include "gdk/gdk.h"

  int main() {
      // 初始化GDK系统
      agibot::gdk::GDKRes init_result = agibot::gdk::GDKInit();
      
      if (init_result != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "GDK初始化失败: " << static_cast<int>(init_result) << std::endl;
          return -1;
      }
      
      std::cout << "GDK初始化成功" << std::endl;
      
      // 使用GDK功能...
      
      return 0;
  }
  ```

#### 2. `GDKRelease()`

- **功能**：释放GDK系统资源
- **参数**：无
- **返回值**：`GDKRes`，操作结果状态码
  - `GDKRes::kSuccess`：释放成功
  - 其他值：释放失败

- **说明**：
  - 在程序结束前调用此函数释放GDK系统资源
  - 清理DDS连接、关闭文件句柄、释放内存等
  - 建议在程序退出前调用一次

- **示例**：

  ```cpp
  #include <iostream>
  #include "gdk/gdk.h"

  int main() {
      // 初始化GDK系统
      agibot::gdk::GDKRes init_result = agibot::gdk::GDKInit();
      
      if (init_result != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "GDK初始化失败" << std::endl;
          return -1;
      }
      
      std::cout << "GDK初始化成功" << std::endl;
      
      // 使用GDK功能...
      
      // 释放GDK系统资源
      agibot::gdk::GDKRes release_result = agibot::gdk::GDKRelease();
      
      if (release_result != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "GDK释放失败: " << static_cast<int>(release_result) << std::endl;
          return -1;
      }
      
      std::cout << "GDK释放成功" << std::endl;
      return 0;
  }
  ```

## 完整使用示例

```cpp
#include <iostream>
#include <thread>
#include "gdk/gdk.h"

int main() {
    std::cout << "GDK Common 示例程序" << std::endl;
    
    // 1. 初始化GDK系统
    std::cout << "正在初始化GDK系统..." << std::endl;
    agibot::gdk::GDKRes init_result = agibot::gdk::GDKInit();
    
    if (init_result != agibot::gdk::GDKRes::kSuccess) {
        std::cout << "❌ GDK初始化失败: " << static_cast<int>(init_result) << std::endl;
        return -1;
    }
    
    std::cout << "✅ GDK初始化成功" << std::endl;
    
    // 2. 使用GDK功能
    std::cout << "开始使用GDK功能..." << std::endl;
    
    // 创建相机对象
    agibot::gdk::Camera camera;
    std::this_thread::sleep_for(std::chrono::seconds(1));
    
    // 创建IMU对象
    agibot::gdk::Imu imu;
    std::this_thread::sleep_for(std::chrono::seconds(1));
    
    std::cout << "GDK功能使用完成" << std::endl;
    
    // 3. 释放GDK系统资源
    std::cout << "正在释放GDK系统资源..." << std::endl;
    agibot::gdk::GDKRes release_result = agibot::gdk::GDKRelease();
    
    if (release_result != agibot::gdk::GDKRes::kSuccess) {
        std::cout << "❌ GDK释放失败: " << static_cast<int>(release_result) << std::endl;
        return -1;
    }
    
    std::cout << "✅ GDK释放成功" << std::endl;
    std::cout << "程序正常结束" << std::endl;
    
    return 0;
}
```

## 使用注意事项

1. **初始化顺序**：必须在调用任何其他GDK功能之前调用`GDKInit()`
2. **释放顺序**：在程序结束前调用`GDKRelease()`释放资源
3. **错误处理**：始终检查返回值，确保操作成功
4. **单次调用**：通常只需要在程序开始时调用一次`GDKInit()`，结束时调用一次`GDKRelease()`
5. **异常安全**：在异常情况下也要确保调用`GDKRelease()`释放资源
6. **多线程**：GDK初始化是全局的，多线程环境下只需要一个线程调用即可

## 错误码说明

| 错误码 | 描述 | 可能原因 |
| :--- | :--- | :--- |
| `GDKRes::kSuccess` | 操作成功 | - |
| `GDKRes::kInvalidInput` | 无效输入 | 参数错误 |
| `GDKRes::kInvalidOutput` | 无效输出 | 输出参数错误 |
| `GDKRes::kTimeout` | 超时 | 操作超时 |
| `GDKRes::kNotInitialized` | 未初始化 | 系统未正确初始化 |
| `GDKRes::kAlreadyInitialized` | 已初始化 | 重复初始化 |
| `GDKRes::kInternalError` | 内部错误 | 系统内部错误 |

## 应用场景

- **系统启动**：在机器人系统启动时初始化GDK
- **资源管理**：确保GDK系统资源正确释放

