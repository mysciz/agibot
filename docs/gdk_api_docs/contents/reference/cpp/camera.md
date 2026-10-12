# GDK Camera 接口文档（C++）

## 概述

Camera（相机）模块为G02机器人提供了获取实时图像数据的功能。通过C++接口，开发者可以方便地获取机器人的视觉感知数据，适用于目标检测、图像识别、视觉导航、SLAM建图、环境监控等多种场景。

## 接口说明

### Camera 类

该类封装了相机传感器的主要数据获取接口。

#### 1. `GetLatestImage()`

- **功能**：获取最新的图像数据
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `camera_type` | `const CameraType&` | 相机类型枚举值 |
| `timeout_ms` | `const float` | 超时时间（毫秒） |
| `image` | `std::shared_ptr<Image>&` | 输出参数，图像数据指针 |

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`，`image`参数包含图像数据

#### Image对象详细说明

**Image结构体包含以下成员**：

| 成员名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `timestamp_ns` | `uint64_t` | 图像采集的时间戳 | 纳秒 |
| `width` | `uint32_t` | 图像的宽度（像素） | 像素 |
| `height` | `uint32_t` | 图像的高度（像素） | 像素 |
| `encoding` | `Encoding` | 图像的编码格式枚举 | 枚举值 |
| `color_format` | `ColorFormat` | 图像的颜色格式枚举 | 枚举值 |
| `bit_depth` | `uint8_t` | 每个像素的位数 | 位 |
| `data_view` | `DataView` | 图像的原始像素数据视图 | 数据视图 |

  ```cpp
  struct Image {
    uint32_t width{0};   ///< image width
    uint32_t height{0};  ///< image height

    enum class Encoding : uint8_t {
      UNCOMPRESSED,  ///< uncompressed
      JPEG,          ///< JPEG
      PNG            ///< PNG
    } encoding{Encoding::UNCOMPRESSED};

    enum class ColorFormat : uint8_t {
      RGB,
      BGR,
      RGBA,
      BGRA,

      YUV420,
      YUV422,
      YUV444,
      NV12,
      NV21,

      GRAY8,
      GRAY16,

      BAYER_RGGB,
      BAYER_BGGR,
      BAYER_GBRG,
      BAYER_GRBG,

      RS2_FORMAT_Z16
    } color_format{ColorFormat::RGB};

    uint8_t bit_depth{8};  ///< bit depth

    DataView data_view{};      ///< image data view
    uint64_t timestamp_ns{0};  ///< image timestamp(ns)
  };
  ```
**encoding (编码格式)**：

- **类型**：`Encoding`枚举
- **常见值**：
  - `Encoding::UNCOMPRESSED`: 未压缩
  - `Encoding::JPEG`: JPEG压缩
  - `Encoding::PNG`: PNG压缩

 ```cpp
  enum class Encoding : uint8_t {
    UNCOMPRESSED,  ///< uncompressed
    JPEG,          ///< JPEG
    PNG            ///< PNG
  } encoding{Encoding::UNCOMPRESSED};
 ```
**color_format (颜色格式)**：

- **类型**：`ColorFormat`枚举
- **常见值**：
  - `ColorFormat::RGB`: 红绿蓝
  - `ColorFormat::BGR`: 蓝绿红
  - `ColorFormat::RGBA`: 红绿蓝透明度
  - `ColorFormat::BGRA`: 蓝绿红透明度
  - `ColorFormat::GRAY8`: 8位灰度
  - `ColorFormat::GRAY16`: 16位灰度
  - `ColorFormat::YUV420`: YUV420格式
  - `ColorFormat::YUV422`: YUV422格式
  - `ColorFormat::YUV444`: YUV444格式
  - `ColorFormat::NV12`: NV12格式
  - `ColorFormat::NV21`: NV21格式
  - `ColorFormat::BAYER_RGGB`: RGGB拜耳模式
  - `ColorFormat::BAYER_BGGR`: BGGR拜耳模式
  - `ColorFormat::BAYER_GBRG`: GBRG拜耳模式
  - `ColorFormat::BAYER_GRBG`: GRBG拜耳模式
  - `ColorFormat::RS2_FORMAT_Z16`: RealSense Z16深度格式

 ```cpp
  enum class ColorFormat : uint8_t {
    RGB,
    BGR,
    RGBA,
    BGRA,

    YUV420,
    YUV422,
    YUV444,
    NV12,
    NV21,

    GRAY8,
    GRAY16,

    BAYER_RGGB,
    BAYER_BGGR,
    BAYER_GBRG,
    BAYER_GRBG,

    RS2_FORMAT_Z16
  } color_format{ColorFormat::RGB};
 ```

**bit_depth (位深度)**：

- **类型**：`uint8_t`
- **常见值**：
  - `8`: 8位（0-255）
  - `16`: 16位（0-65535）
  - `32`: 32位（浮点）

**data_view (图像数据)**：

- **类型**：`DataView`
- **描述**：图像的原始像素数据视图
- **用途**：图像处理、显示、保存
- **注意**：需要根据encoding和尺寸进行解析

**相机类型**：
- `CameraType::kHeadBackFisheye`: 头部背部鱼眼相机
- `CameraType::kHeadLeftFisheye`: 头部左侧鱼眼相机
- `CameraType::kHeadRightFisheye`: 头部右侧鱼眼相机
- `CameraType::kHeadStereoLeft`: 头部立体左相机
- `CameraType::kHeadStereoRight`: 头部立体右相机
- `CameraType::kHandLeftColor`: 左手彩色相机
- `CameraType::kHandRightColor`: 右手彩色相机
- `CameraType::kHeadColor`: 头部彩色相机
- `CameraType::kHeadDepth`: 头部深度相机（输出为深度图）
- `CameraType::kHandLeftDepth`: 左手深度相机（输出为深度图）
- `CameraType::kHandRightDepth`: 右手深度相机（输出为深度图）

- `CameraType::kHandLeftUpperColor`: 左手上部彩色相机 (预留)
- `CameraType::kHandRightUpperColor`: 右手上部彩色相机 (预留)
- `CameraType::kHandLeftLowerColor`: 左手下部彩色相机 (预留)
- `CameraType::kHandRightLowerColor`: 右手下部彩色相机 (预留)
- `CameraType::kHandLeftUpperDepth`: 左手上部深度相机（输出为深度图） (预留)
- `CameraType::kHandRightUpperDepth`: 右手上部深度相机（输出为深度图） (预留)
- `CameraType::kHandLeftLowerDepth`: 左手下部深度相机（输出为深度图） (预留)
- `CameraType::kHandRightLowerDepth`: 右手下部深度相机（输出为深度图） (预留)

- 在常规模式下，默认打开头部立体左相机，头部立体右相机，左右彩色相机，右手彩色相机，头部彩色相机，头部深度相机，其余相机默认关闭，且不建议在常规模式下打开其余相机
- 可以在develop模式下开启或关闭其余相机

- **示例**：

  ```cpp
  #include <iostream>
  #include <thread>
  #include "gdk/gdk.h"

  int main() {
      // 初始化GDK系统
      if (agibot::gdk::GDKInit() != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "GDK初始化失败" << std::endl;
          return -1;
      }
      std::cout << "GDK初始化成功" << std::endl;

      agibot::gdk::Camera gdk_camera;
      std::cout << "Camera init" << std::endl;

      std::this_thread::sleep_for(std::chrono::seconds(1));

      std::shared_ptr<agibot::gdk::Image> image = std::make_shared<agibot::gdk::Image>();

      agibot::gdk::CameraType camera_type = agibot::gdk::CameraType::kHandLeftColor;

      if (gdk_camera.GetLatestImage(camera_type, 500, image) != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "Failed to get latest image" << std::endl;
      } else {
          std::cout << "Image shape: " << image->width << "x" << image->height << std::endl;
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

#### 2. `GetNearestImage()`

- **功能**：获取指定时间戳附近最近的图像数据
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `camera_type` | `const CameraType&` | 相机类型枚举值 |
| `timestamp_ns` | `const uint64_t` | 目标时间戳（纳秒） |
| `timeout_ms` | `const float` | 超时时间（毫秒） |
| `image` | `std::shared_ptr<Image>&` | 输出参数，图像数据指针 |

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`，`image`参数包含图像数据，结构与`GetLatestImage()`相同

- **示例**：

  ```cpp
  #include <iostream>
  #include <thread>
  #include "gdk/gdk.h"

  int main() {
      // 初始化GDK系统
      if (agibot::gdk::GDKInit() != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "GDK初始化失败" << std::endl;
          return -1;
      }
      std::cout << "GDK初始化成功" << std::endl;

      agibot::gdk::Camera gdk_camera;
      std::cout << "Camera init" << std::endl;

      std::this_thread::sleep_for(std::chrono::seconds(1));

      std::shared_ptr<agibot::gdk::Image> image = std::make_shared<agibot::gdk::Image>();

      agibot::gdk::CameraType camera_type = agibot::gdk::CameraType::kHandLeftColor;

      if(gdk_camera.GetNearestImage(camera_type, 0, 2000.0, image) != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "GetNearestImage failed" << std::endl;
          return -1;
      } else {
          std::cout << "Image shape: " << image->width << " x " << image->height << std::endl;
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

#### 3. `GetImageShape()`

- **功能**：获取图像数据大小
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `camera_type` | `const CameraType&` | 相机类型枚举值 |
| `shape` | `std::tuple<int, int>&` | 输出参数，图像宽度和高度的元组 |

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`，`shape`参数包含图像尺寸

- **示例**：

  ```cpp
  #include <iostream>
  #include <thread>
  #include "gdk/gdk.h"

  int main() {
      // 初始化GDK系统
      if (agibot::gdk::GDKInit() != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "GDK初始化失败" << std::endl;
          return -1;
      }
      std::cout << "GDK初始化成功" << std::endl;

      agibot::gdk::Camera gdk_camera;
      std::cout << "Camera init" << std::endl;

      std::this_thread::sleep_for(std::chrono::seconds(1));

      std::shared_ptr<agibot::gdk::Image> image = std::make_shared<agibot::gdk::Image>();

      agibot::gdk::CameraType camera_type = agibot::gdk::CameraType::kHandRightColor;

      std::tuple<int, int> shape;
      if (gdk_camera.GetImageShape(camera_type, shape) != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "Failed to get image shape" << std::endl;
      } else {
          std::cout << "Image shape: " << std::get<0>(shape) << "x" << std::get<1>(shape) << std::endl;
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

#### 4. `GetImageFps()`

- **功能**：获取图像捕获帧率
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `camera_type` | `const CameraType&` | 相机类型枚举值 |
| `fps` | `float&` | 输出参数，图像帧率（FPS） |

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`，`fps`参数包含帧率值

- **示例**：

  ```cpp
  #include <iostream>
  #include <thread>
  #include "gdk/gdk.h"

  int main() {
      // 初始化GDK系统
      if (agibot::gdk::GDKInit() != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "GDK初始化失败" << std::endl;
          return -1;
      }
      std::cout << "GDK初始化成功" << std::endl;

      agibot::gdk::Camera gdk_camera;
      std::cout << "Camera init" << std::endl;

      std::this_thread::sleep_for(std::chrono::seconds(1));

      std::shared_ptr<agibot::gdk::Image> image = std::make_shared<agibot::gdk::Image>();

      agibot::gdk::CameraType camera_type = agibot::gdk::CameraType::kHandLeftColor;

      float fps;
      if (gdk_camera.GetImageFps(camera_type, fps) != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "Failed to get image fps" << std::endl;
      } else {
          std::cout << "Image fps: " << fps << std::endl;
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

#### 5. `GetImageLatency()`

- **注意事项**：获取图像延迟统计信息前，需要先进行时间同步，否则延迟统计结果不准确
- **功能**：获取图像延迟统计信息
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `camera_type` | `const CameraType&` | 相机类型枚举值 |
| `window_seconds` | `const float` | 统计窗口时间（秒） |
| `latency` | `LatencyStats&` | 输出参数，延迟统计信息 |

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`，`latency`参数包含延迟统计信息

- **示例**：

  ```cpp
  #include <iostream>
  #include <thread>
  #include "gdk/gdk.h"

  int main() {
      // 初始化GDK系统
      if (agibot::gdk::GDKInit() != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "GDK初始化失败" << std::endl;
          return -1;
      }
      std::cout << "GDK初始化成功" << std::endl;

      agibot::gdk::Camera gdk_camera;
      std::cout << "Camera init" << std::endl;

      std::this_thread::sleep_for(std::chrono::seconds(1));

      std::shared_ptr<agibot::gdk::Image> image = std::make_shared<agibot::gdk::Image>();

      agibot::gdk::CameraType camera_type = agibot::gdk::CameraType::kHandLeftColor;

      agibot::gdk::LatencyStats latency;
      if (gdk_camera.GetImageLatency(agibot::gdk::CameraType::kHeadStereoLeft, 1.0, latency) != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "Failed to get image latency" << std::endl;
      } else {
          std::cout << "Image latency: " << latency.max_latency_ms << "ms" << std::endl;
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

#### 6. `GetCameraIntrinsic()`

- **功能**：获取相机内参信息
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `camera_type` | `const CameraType&` | 相机类型枚举值 |
| `intrinsic` | `CameraIntrinsic&` | 输出参数，相机内参信息 |

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`，`intrinsic`参数包含相机内参

- **注意**：并非所有相机类型都支持内参获取。支持内参的相机类型包括：`kHeadBackFisheye`、`kHeadLeftFisheye`、`kHeadRightFisheye`、`kHeadStereoLeft`、`kHeadStereoRight`、`kHandLeftColor`、`kHandRightColor`、`kHeadColor`、`kHeadDepth`、`kHandLeftDepth`、`kHandRightDepth`。对于不支持的相机类型，调用此接口将返回错误。

- **CameraIntrinsic结构体说明**：

```cpp
struct CameraIntrinsic {
  std::vector<double> intrinsic{};  ///< camera intrinsic, fx, fy, cx, cy
  std::vector<double> distortion{}; ///< camera distortion, k1, k2, p1, p2, k3, k4, k5, k6
};
```

| 成员名 | 类型 | 描述 | 索引 | 单位 |
| :--- | :--- | :--- | :--- | :--- |
| `intrinsic[0]` | `double` | 焦距x方向 (fx) | 0 | 像素 |
| `intrinsic[1]` | `double` | 焦距y方向 (fy) | 1 | 像素 |
| `intrinsic[2]` | `double` | 主点x坐标 (cx) | 2 | 像素 |
| `intrinsic[3]` | `double` | 主点y坐标 (cy) | 3 | 像素 |
| `distortion[0]` | `double` | 径向畸变系数1 (k1) | 0 | 无量纲 |
| `distortion[1]` | `double` | 径向畸变系数2 (k2) | 1 | 无量纲 |
| `distortion[2]` | `double` | 切向畸变系数1 (p1) | 2 | 无量纲 |
| `distortion[3]` | `double` | 切向畸变系数2 (p2) | 3 | 无量纲 |
| `distortion[4]` | `double` | 径向畸变系数3 (k3) | 4 | 无量纲 |
| `distortion[5]` | `double` | 径向畸变系数4 (k4) | 5 | 无量纲 |
| `distortion[6]` | `double` | 径向畸变系数5 (k5) | 6 | 无量纲 |
| `distortion[7]` | `double` | 径向畸变系数6 (k6) | 7 | 无量纲 |

- **不同相机类型的内参支持**：

| 相机类型 | intrinsic向量大小 | distortion向量大小 | 说明 |
| :--- | :--- | :--- | :--- |
| **双目相机** | 4 (fx, fy, cx, cy) | 8 (k1, k2, p1, p2, k3, k4, k5, k6) | 完整的12参数畸变模型 |
| **RGBD相机** | 4 (fx, fy, cx, cy) | 5 (k1, k2, p1, p2, k3) | 9参数畸变模型 |
| **鱼眼相机** | 4 (fx, fy, cx, cy) | 6 (k1, k2, p1, p2, k3, k4) | 10参数畸变模型 |

- **畸变模型说明**：
  - **径向畸变**：`k1, k2, k3, k4, k5, k6` - 用于校正镜头径向畸变
  - **切向畸变**：`p1, p2` - 用于校正镜头切向畸变
  - **不同相机类型**：根据镜头特性使用不同数量的畸变参数

- **示例**：

  ```cpp
  #include <iostream>
  #include <thread>
  #include "gdk/gdk.h"

  void printCameraIntrinsic(const agibot::gdk::CameraType& camera_type,
                           const agibot::gdk::CameraIntrinsic& intrinsic) {
      std::cout << "Camera intrinsic for " << static_cast<int>(camera_type) << ":" << std::endl;

      // 显示内参矩阵 (fx, fy, cx, cy)
      if (intrinsic.intrinsic.size() >= 4) {
          std::cout << "  fx: " << intrinsic.intrinsic[0] << ", fy: " << intrinsic.intrinsic[1] << std::endl;
          std::cout << "  cx: " << intrinsic.intrinsic[2] << ", cy: " << intrinsic.intrinsic[3] << std::endl;
      }

      // 显示畸变参数
      if (intrinsic.distortion.size() > 0) {
          std::cout << "  k1: " << intrinsic.distortion[0];
          if (intrinsic.distortion.size() > 1) std::cout << ", k2: " << intrinsic.distortion[1];
          if (intrinsic.distortion.size() > 2) std::cout << ", p1: " << intrinsic.distortion[2];
          if (intrinsic.distortion.size() > 3) std::cout << ", p2: " << intrinsic.distortion[3];
          if (intrinsic.distortion.size() > 4) std::cout << ", k3: " << intrinsic.distortion[4];
          std::cout << std::endl;

          // 根据相机类型显示额外的畸变参数
          if (camera_type == agibot::gdk::CameraType::kHeadStereoLeft ||
              camera_type == agibot::gdk::CameraType::kHeadStereoRight) {
              // 双目相机：显示 k4, k5, k6
              if (intrinsic.distortion.size() > 5) std::cout << "  k4: " << intrinsic.distortion[5];
              if (intrinsic.distortion.size() > 6) std::cout << ", k5: " << intrinsic.distortion[6];
              if (intrinsic.distortion.size() > 7) std::cout << ", k6: " << intrinsic.distortion[7];
              std::cout << " (双目相机，12参数畸变模型)" << std::endl;
          } else if (camera_type == agibot::gdk::CameraType::kHeadDepth) {
              // RGBD相机：只显示 k1, k2, k3
              std::cout << "  (RGBD相机，9参数畸变模型)" << std::endl;
          } else if (camera_type == agibot::gdk::CameraType::kHeadBackFisheye ||
                     camera_type == agibot::gdk::CameraType::kHandLeftColor ||
                     camera_type == agibot::gdk::CameraType::kHandRightColor) {
              // 鱼眼相机：显示 k4
              if (intrinsic.distortion.size() > 5) {
                  std::cout << "  k4: " << intrinsic.distortion[5] << " (鱼眼相机，10参数畸变模型)" << std::endl;
              }
          }
      }
  }

  int main() {
      // 初始化GDK系统
      if (agibot::gdk::GDKInit() != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "GDK初始化失败" << std::endl;
          return -1;
      }
      std::cout << "GDK初始化成功" << std::endl;

      agibot::gdk::Camera gdk_camera;
      std::cout << "Camera init" << std::endl;

      std::this_thread::sleep_for(std::chrono::seconds(1));

      // 获取不同相机类型的内参
      std::vector<agibot::gdk::CameraType> camera_types = {
          agibot::gdk::CameraType::kHeadStereoLeft,    // 双目相机
          agibot::gdk::CameraType::kHeadDepth,         // RGBD相机
          agibot::gdk::CameraType::kHeadBackFisheye  // 鱼眼相机
      };

      for (auto camera_type : camera_types) {
          agibot::gdk::CameraIntrinsic intrinsic;
          if (gdk_camera.GetCameraIntrinsic(camera_type, intrinsic) != agibot::gdk::GDKRes::kSuccess) {
              std::cout << "Failed to get camera intrinsic for type " << static_cast<int>(camera_type) << std::endl;
          } else {
              printCameraIntrinsic(camera_type, intrinsic);
          }
          std::cout << std::endl;
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

#### 7. `SetDevCameraConfig()`

- **功能**：相机客制化功能(开关相机、设置帧率)
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `cam_conf_path` | `const std::string&` | 相机配置文件路径 |



- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`

- **注意**：
  - 配置文件路径必须存在，否则返回`GDKRes::kInvalidInput`
  - 每次修改客制化相机配置文件且调用接口后，需要重新切换模式至develop模式

##### 配置选项
GDK支持配置相机的开关与设置的帧率，相机客制化的配置文件在部署包下，其绝对路径通常为 `~/.cache/agibot/app/gdk/config/r1_camera_conf.json`或`~/.cache/agibot/app/gdk/config/thor_camera_conf.json`（其中 `~` 表示用户主目录，如 `/home/your_name`）
r1机器的配置文件为r1_camera_conf.json，thor机器的配置文件为thor_camera_conf.json，使用时注意文件名称
设置publish为true开启相机，false关闭相机，设置fps来控制相机帧率

相机具体配置形式如下
```json
{
    "cam0": {
        "fps": "30",
        "name": "head_stereo_right",
        "publish": true
    },
    "cam3": {
        "fps": "30",
        "name": "head_stereo_left",
        "publish": true
    },
    "cam4": {
        "fps": "30",
        "name": "hand_left_depth",
        "publish": false
    },
    "cam5": {
        "fps": "30",
        "name": "hand_left_color",
        "publish": true
    },
    "cam6": {
        "fps": "30",
        "name": "hand_right_depth",
        "publish": false
    },
    "cam7": {
        "fps": "30",
        "name": "hand_right_color",
        "publish": true
    },
    "cam10": {
        "fps": "30",
        "name": "head_right_fisheye",
        "publish": false
    },
    "cam11": {
        "fps": "30",
        "name": "head_left_fisheye",
        "publish": false
    },
    "cam12": {
        "fps": "30",
        "name": "head_back_fisheye",
        "publish": false
    },
    "cam14": {
        "fps": "30",
        "name": "head_depth",
        "publish": true
    },
    "cam15": {
        "fps": "30",
        "name": "head_color",
        "publish": true
    }
}
```
##### 模式切换
```bash
./mode_switch --mode develop # 切换到develop模式
```
如需切换回之前base模式，则执行
```bash
./mode_switch --mode base # 切换到base模式
```


- **示例**：

  ```cpp
  #include <iostream>
  #include <thread>
  #include "gdk/gdk.h"

  int main() {
      // 初始化GDK系统
      if (agibot::gdk::GDKInit() != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "GDK初始化失败" << std::endl;
          return -1;
      }
      std::cout << "GDK初始化成功" << std::endl;

      agibot::gdk::Camera gdk_camera;
      std::cout << "Camera init" << std::endl;

      std::this_thread::sleep_for(std::chrono::seconds(1));

      // 设置相机配置
      std::string config_path = "/home/<your_name>/.cache/agibot/app/gdk/config/r1_camera_conf.json";
      if (gdk_camera.SetDevCameraConfig(config_path) != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "Failed to set camera config" << std::endl;
      } else {
          std::cout << "Camera config set successfully" << std::endl;
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

#### 8. `CloseCamera()`

- **功能**：关闭相机DDS连接
- **参数**：无
- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`

- **示例**：

  ```cpp
  #include <iostream>
  #include <thread>
  #include "gdk/gdk.h"

  int main() {
      // 初始化GDK系统
      if (agibot::gdk::GDKInit() != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "GDK初始化失败" << std::endl;
          return -1;
      }
      std::cout << "GDK初始化成功" << std::endl;

      agibot::gdk::Camera gdk_camera;
      std::cout << "Camera init" << std::endl;

      // 使用相机...

      // 关闭相机
      if (gdk_camera.CloseCamera() != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "Failed to close camera" << std::endl;
      } else {
          std::cout << "Camera closed successfully" << std::endl;
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

1. **GDK初始化**：使用Camera功能前必须先调用`agibot::gdk::GDKInit()`初始化GDK系统
2. **GDK释放**：程序结束前必须调用`agibot::gdk::GDKRelease()`释放GDK系统资源
3. **初始化等待**：创建Camera对象后，建议等待1秒以确保相机初始化完成
4. **超时设置**：根据实际需求设置合适的超时时间，避免长时间阻塞
5. **数据有效性**：使用前请检查返回的图像数据是否为nullptr
6. **时间戳精度**：时间戳单位为纳秒，可用于精确的时间同步
7. **图像处理**：图像数据量较大，处理时注意内存使用
8. **相机选择**：根据应用场景选择合适的相机类型（鱼眼/立体/深度等）
9. **帧率控制**：注意相机的帧率限制，避免过度请求
10. **相机配置**：使用`SetDevCameraConfig()`设置相机配置时，确保配置文件路径有效
11. **错误处理**：始终检查GDKRes返回值，确保操作成功
12. **相机开关**：在常规模式/develop模式下，若打开更多相机，存在性能风险

## 应用场景

- **目标检测**：利用图像数据进行目标识别和检测
- **视觉导航**：为机器人导航提供视觉信息
- **SLAM建图**：结合图像数据进行同时定位与地图构建
- **环境监控**：实时监控周围环境变化
- **深度感知**：使用深度相机获取3D环境信息
- **立体视觉**：利用双目相机进行距离测量
- **图像识别**：进行物体分类和识别
- **数据融合**：与其他传感器数据进行融合，提高感知精度
- **相机标定**：使用相机内参进行图像校正和畸变补偿
- **3D重建**：结合相机内参进行三维点云重建
- **视觉测量**：利用相机内参进行精确的尺寸测量
