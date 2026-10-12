# GDK 通用接口文档（Python）

## 概述

GDK（Genie Development Kit）通用接口提供了系统初始化和资源释放的核心功能。通过Python接口，开发者可以方便地管理GDK系统的生命周期，确保所有GDK功能正常使用。

## 接口说明

### 1. `gdk_init()`

- **功能**：初始化GDK系统
- **参数**：无
- **返回值**：`GDKRes`，操作结果状态码

#### GDKRes状态码说明

| 状态码 | 描述 |
| :--- | :--- |
| `kSuccess` | 操作成功 |
| `kInvalidInput` | 输入参数无效 |
| `kInvalidOutput` | 输出参数无效 |
| `kRuntimeError` | 运行时错误 |
| `kUnknown` | 未知错误 |

- **示例**：

  ```python
  import agibot_gdk

  # 初始化GDK系统
  result = agibot_gdk.gdk_init()
  if result == agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化成功")
  else:
      print(f"GDK初始化失败，错误码: {result}")
      exit(1)
  ```

### 2. `gdk_release()`

- **功能**：释放GDK系统资源
- **参数**：无
- **返回值**：`GDKRes`，操作结果状态码

- **示例**：

  ```python
  import agibot_gdk

  # 使用GDK功能...
  
  # 释放GDK系统资源
  result = agibot_gdk.gdk_release()
  if result == agibot_gdk.GDKRes.kSuccess:
      print("GDK释放成功")
  else:
      print(f"GDK释放失败，错误码: {result}")
  ```

## 完整使用示例

```python
import agibot_gdk
import time

def main():
    # 1. 初始化GDK系统
    print("正在初始化GDK系统...")
    init_result = agibot_gdk.gdk_init()
    if init_result != agibot_gdk.GDKRes.kSuccess:
        print(f"GDK初始化失败，错误码: {init_result}")
        return -1
    print("GDK初始化成功")
    
    try:
        # 2. 使用GDK功能
        print("开始使用GDK功能...")
        
        # 创建相机对象
        camera = agibot_gdk.Camera()
        time.sleep(1)  # 等待相机初始化
        
        # 获取图像
        image = camera.get_latest_image(agibot_gdk.CameraType.kHeadStereoLeft, 1000.0)
        if image is not None:
            print(f"成功获取图像: {image.width}x{image.height}")
        else:
            print("未获取到图像")
        
        # 关闭相机
        camera.close_camera()
        
        print("GDK功能使用完成")
        
    except Exception as e:
        print(f"使用GDK功能时发生错误: {e}")
        return -1
    
    finally:
        # 3. 释放GDK系统资源
        print("正在释放GDK系统资源...")
        release_result = agibot_gdk.gdk_release()
        if release_result != agibot_gdk.GDKRes.kSuccess:
            print(f"GDK释放失败，错误码: {release_result}")
            return -1
        print("GDK释放成功")
    
    return 0

if __name__ == "__main__":
    exit(main())
```

## 使用注意事项

1. **必须初始化**：使用任何GDK功能前必须先调用`gdk_init()`初始化系统
2. **必须释放**：程序结束前必须调用`gdk_release()`释放系统资源
3. **资源管理**：确保在异常情况下也能正确释放资源
4. **错误处理**：始终检查返回值，确保操作成功
5. **初始化顺序**：先初始化GDK，再创建具体的功能对象（如Camera、Robot等）
6. **释放顺序**：先关闭具体功能对象，再释放GDK系统

## 应用场景

- **系统管理**：管理GDK系统的完整生命周期
- **资源控制**：确保系统资源的正确分配和释放
- **异常处理**：在异常情况下保证系统资源的清理
- **多模块开发**：为多个GDK模块提供统一的初始化入口

