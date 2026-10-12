# GDK 交互接口文档（C++）

## 概述

交互模块为G02机器人提供了语音交互、显示控制、音频播放等功能。通过C++接口，开发者可以方便地实现对机器人的语音控制、TTS播放、音频视频播放、显示控制等功能，适用于语音交互、多媒体展示、人机交互等多种场景。

## 注意事项

交互接口依赖跨网段通信模块，因此如果在隔离环境中使用该类接口（如docker容器），需要确保容器可以修改宿主机的网络配置。（启动容器时添加参数‘--privileged’）

## 接口说明

### Interaction 类

该类封装了机器人交互的主要功能接口。

#### 1. `SetLanguage()`

- **功能**：设置语音语言
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `language` | `const Language&` | 语言类型，`Language::kLanguageChinese` 表示中文，`Language::kLanguageEnglish` 表示英文 |

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`

**Language枚举值**：

| 枚举值 | 描述 |
| :--- | :--- |
| `Language::kLanguageChinese` | 中文 |
| `Language::kLanguageEnglish` | 英文 |

```cpp
enum class Language {
  kLanguageChinese = 0,
  kLanguageEnglish = 1,
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

      agibot::gdk::Interaction interaction;
      std::cout << "Interaction init" << std::endl;
      std::this_thread::sleep_for(std::chrono::seconds(1));

      // 设置语言为中文
      if (interaction.SetLanguage(agibot::gdk::Language::kLanguageChinese) != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "设置语言失败" << std::endl;
      } else {
          std::cout << "设置语言成功" << std::endl;
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

#### 2. `SetCallMode()`

- **功能**：设置通话模式
- **参数**：
| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `is_on` | `const bool&` | `true` 表示开启通话模式，`false` 表示关闭通话模式 |
- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`

- **注意事项**：
  - 开启通话模式后，自动进入唤醒状态，关闭通话模式后，自动退出唤醒状态，无需唤醒词和结束词
  - 在通话模式下，可以获取用户输入的语音，并通过接口获取对应的语音文本
  - 在通话模式下，可以调用`GetAsrText()`或`RegisterCallback()`注册回调函数获取用户输入的语音文本
  
- **示例**：

  ```cpp
  #include "gdk/gdk.h"
  #include <iostream>
  #include <chrono>
  #include <thread>

  int main()
  {
      if (agibot::gdk::GDKInit() != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "GDK初始化失败" << std::endl;
          return -1;
      }
      std::cout << "GDK初始化成功" << std::endl;

      agibot::gdk::Interaction interaction;
      std::this_thread::sleep_for(std::chrono::seconds(1));

      // 开启通话模式
      bool is_on = true;
      if (interaction.SetCallMode(is_on) != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "开启通话模式失败" << std::endl;
      } else {
          std::cout << "开启通话模式成功" << std::endl;
      }

      is_on = false;
      if (interaction.SetCallMode(is_on) != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "关闭通话模式失败" << std::endl;
      } else {
          std::cout << "关闭通话模式成功" << std::endl;
      }

      agibot::gdk::GDKRelease();
      return 0;
  }
  ```

#### 3. `SetVolume()`

- **功能**：设置音量
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `volume` | `const int32_t&` | 音量值，范围通常为0-500 |

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`

- **示例**：

  ```cpp
  #include "gdk/gdk.h"
  #include <iostream>
  #include <chrono>
  #include <thread>

  int main()
  {
      if (agibot::gdk::GDKInit() != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "GDK初始化失败" << std::endl;
          return -1;
      }
      std::cout << "GDK初始化成功" << std::endl;

      agibot::gdk::Interaction interaction;
      std::this_thread::sleep_for(std::chrono::seconds(1));

      // 设置音量为50
      int32_t volume = 50;
      if (interaction.SetVolume(volume) != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "设置音量失败" << std::endl;
      } else {
          std::cout << "设置音量成功" << std::endl;
      }

      agibot::gdk::GDKRelease();
      return 0;
  }
  ```

#### 4. `SetWakeupSwitch()`

- **功能**：设置唤醒开关
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `is_on` | `const bool&` | `true` 表示开启唤醒，`false` 表示关闭唤醒 |

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`

- **示例**：

  ```cpp
  #include "gdk/gdk.h"
  #include <iostream>
  #include <chrono>
  #include <thread>

  int main()
  {
      if (agibot::gdk::GDKInit() != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "GDK初始化失败" << std::endl;
          return -1;
      }
      std::cout << "GDK初始化成功" << std::endl;

      agibot::gdk::Interaction interaction;
      std::this_thread::sleep_for(std::chrono::seconds(1));

      // 开启唤醒功能
      bool is_on = true;
      if (interaction.SetWakeupSwitch(is_on) != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "设置唤醒开关失败" << std::endl;
      } else {
          std::cout << "开启唤醒功能成功" << std::endl;
      }

      agibot::gdk::GDKRelease();
      return 0;
  }
  ```

#### 5. `SetAudioSwitch()`

- **功能**：设置音频开关
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `is_on` | `const bool&` | `true` 表示开启音频，`false` 表示关闭音频 |

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`

- **示例**：

  ```cpp
  #include "gdk/gdk.h"
  #include <iostream>
  #include <chrono>
  #include <thread>

  int main()
  {
      if (agibot::gdk::GDKInit() != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "GDK初始化失败" << std::endl;
          return -1;
      }
      std::cout << "GDK初始化成功" << std::endl;

      agibot::gdk::Interaction interaction;
      std::this_thread::sleep_for(std::chrono::seconds(1));

      // 开启音频功能
      bool is_on = true;
      if (interaction.SetAudioSwitch(is_on) != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "设置音频开关失败" << std::endl;
      } else {
          std::cout << "开启音频功能成功" << std::endl;
      }

      agibot::gdk::GDKRelease();
      return 0;
  }
  ```

#### 6. `SetDisplaySwitch()`

- **功能**：设置显示开关
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `is_on` | `const bool&` | `true` 表示开启显示，`false` 表示关闭显示 |

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`

- **示例**：

  ```cpp
  #include "gdk/gdk.h"
  #include <iostream>
  #include <chrono>
  #include <thread>

  int main()
  {
      if (agibot::gdk::GDKInit() != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "GDK初始化失败" << std::endl;
          return -1;
      }
      std::cout << "GDK初始化成功" << std::endl;

      agibot::gdk::Interaction interaction;
      std::this_thread::sleep_for(std::chrono::seconds(1));

      // 开启显示功能
      bool is_on = true;
      if (interaction.SetDisplaySwitch(is_on) != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "设置显示开关失败" << std::endl;
      } else {
          std::cout << "开启显示功能成功" << std::endl;
      }

      agibot::gdk::GDKRelease();
      return 0;
  }
  ```

#### 7. `PlayTts()`

- **功能**：播放TTS（文本转语音）
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `text` | `const std::string&` | 要播放的文本内容 |

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`

- **示例**：

  ```cpp
  #include "gdk/gdk.h"
  #include <iostream>
  #include <chrono>
  #include <thread>

  int main()
  {
      if (agibot::gdk::GDKInit() != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "GDK初始化失败" << std::endl;
          return -1;
      }
      std::cout << "GDK初始化成功" << std::endl;

      agibot::gdk::Interaction interaction;
      std::this_thread::sleep_for(std::chrono::seconds(1));

      // 播放TTS
      std::string text = "你好，我是精灵G2";
      if (interaction.PlayTts(text) != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "播放TTS失败" << std::endl;
      } else {
          std::cout << "TTS播放成功" << std::endl;
          std::this_thread::sleep_for(std::chrono::seconds(3));  // 等待播放完成
      }

      agibot::gdk::GDKRelease();
      return 0;
  }
  ```

#### 8. `PlayAudio()`

- **功能**：播放音频文件
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `audio_path` | `const std::string&` | 音频文件路径 |

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`

- **示例**：

  ```cpp
  #include "gdk/gdk.h"
  #include <iostream>
  #include <chrono>
  #include <thread>

  int main()
  {
      if (agibot::gdk::GDKInit() != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "GDK初始化失败" << std::endl;
          return -1;
      }
      std::cout << "GDK初始化成功" << std::endl;

      agibot::gdk::Interaction interaction;
      std::this_thread::sleep_for(std::chrono::seconds(1));

      // 播放音频文件
      std::string audio_path = "/path/to/audio.wav";
      if (interaction.PlayAudio(audio_path) != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "播放音频失败" << std::endl;
      } else {
          std::cout << "音频播放成功" << std::endl;
          std::this_thread::sleep_for(std::chrono::seconds(5));  // 等待播放完成
      }

      agibot::gdk::GDKRelease();
      return 0;
  }
  ```

#### 9. `PlayVideo()`

- **功能**：播放视频文件
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `video_path` | `const std::string&` | 视频文件路径 |
| `loop_count` | `const int32_t&` | 循环播放次数，-1表示无限循环 |

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`

- **示例**：

  ```cpp
  #include "gdk/gdk.h"
  #include <iostream>
  #include <chrono>
  #include <thread>

  int main()
  {
      if (agibot::gdk::GDKInit() != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "GDK初始化失败" << std::endl;
          return -1;
      }
      std::cout << "GDK初始化成功" << std::endl;

      agibot::gdk::Interaction interaction;
      std::this_thread::sleep_for(std::chrono::seconds(1));

      // 播放视频文件，循环1次
      std::string video_path = "/path/to/video.mp4";
      int32_t loop_count = 1;
      if (interaction.PlayVideo(video_path, loop_count) != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "播放视频失败" << std::endl;
      } else {
          std::cout << "视频播放成功" << std::endl;
          std::this_thread::sleep_for(std::chrono::seconds(10));  // 等待播放完成
      }

      // 无限循环播放
      loop_count = -1;
      if (interaction.PlayVideo(video_path, loop_count) != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "播放视频失败" << std::endl;
      } else {
          std::cout << "视频开始循环播放" << std::endl;
      }

      agibot::gdk::GDKRelease();
      return 0;
  }
  ```

#### 10. `GetFuncStatus()`

- **功能**：获取语音功能状态
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `func_status` | `VoiceFuncStatus&` | 输出参数，语音功能状态对象 |

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`，`func_status`参数包含功能状态信息

#### VoiceFuncStatus对象详细说明

**VoiceFuncStatus结构体包含以下成员**：

| 成员名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `func_status` | `uint32_t` | 功能状态 | 无单位 |
| `wakeup_status` | `uint32_t` | 唤醒状态 | 无单位 |
| `requester` | `std::string` | 请求者 | 字符串 |
| `wakeup_enabled` | `bool` | 唤醒功能是否启用 | 布尔值 |
| `display_enabled` | `bool` | 显示功能是否启用 | 布尔值 |
| `audio_enabled` | `bool` | 音频功能是否启用 | 布尔值 |
| `en_settings` | `VoiceSettings` | 英文语音设置 | 语音设置 |
| `cn_settings` | `VoiceSettings` | 中文语音设置 | 语音设置 |
| `timestamp` | `uint64_t` | 时间戳 | 纳秒 |

**func_status**：
| 值 | 描述 |
| :--- | :--- |
| 0 | 空闲 |
| 1 | 电话模式 |
| 2 | 语音唤醒 + 自由问答 |
| 3 | 语音唤醒 + ASR |
| 4 | 语音播报 |
| 5 | 多轮语音交互 |
| 6 | 音频播放 |
| 9 | 异常 |

**wakeup_status**：
| 值 | 描述 |
| :--- | :--- |
| 0 | 未唤醒 |
| 1 | 唤醒后倾听 |
| 2 | 唤醒后思考 |
| 4 | 唤醒后播报 |

```cpp
struct VoiceFuncStatus {
  uint32_t func_status{0};
  uint32_t wakeup_status{0};
  std::string requester{};
  bool wakeup_enabled{false};
  bool display_enabled{false};
  bool audio_enabled{false};
  VoiceSettings en_settings{};
  VoiceSettings cn_settings{};
  uint64_t timestamp{0};
};
```

**VoiceSettings结构体**：

| 成员名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `volume` | `uint32_t` | 音量 | 无单位 |
| `speech_rate` | `float` | 语速 | 无单位 |
| `voice_tone` | `std::string` | 音色 | 字符串 |
| `is_curr_setting` | `bool` | 是否为当前设置 | 布尔值 |

```cpp
struct VoiceSettings {
  uint32_t volume{0};
  float speech_rate{0.0};
  std::string voice_tone{};
  bool is_curr_setting{false};
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
      if (agibot::gdk::GDKInit() != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "GDK初始化失败" << std::endl;
          return -1;
      }
      std::cout << "GDK初始化成功" << std::endl;

      agibot::gdk::Interaction interaction;
      std::this_thread::sleep_for(std::chrono::seconds(1));

      agibot::gdk::VoiceFuncStatus func_status;
      if (interaction.GetFuncStatus(func_status) != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "获取功能状态失败" << std::endl;
      } else {
          std::cout << "功能状态信息:" << std::endl;
          std::cout << "  功能状态: " << func_status.func_status << std::endl;
          std::cout << "  唤醒状态: " << func_status.wakeup_status << std::endl;
          std::cout << "  请求者: " << func_status.requester << std::endl;
          std::cout << "  唤醒功能启用: " << (func_status.wakeup_enabled ? "是" : "否") << std::endl;
          std::cout << "  显示功能启用: " << (func_status.display_enabled ? "是" : "否") << std::endl;
          std::cout << "  音频功能启用: " << (func_status.audio_enabled ? "是" : "否") << std::endl;
          std::cout << "  中文设置 - 音量: " << func_status.cn_settings.volume
                    << ", 语速: " << func_status.cn_settings.speech_rate
                    << ", 音色: " << func_status.cn_settings.voice_tone << std::endl;
          std::cout << "  英文设置 - 音量: " << func_status.en_settings.volume
                    << ", 语速: " << func_status.en_settings.speech_rate
                    << ", 音色: " << func_status.en_settings.voice_tone << std::endl;
          std::cout << "  时间戳: " << func_status.timestamp << std::endl;
      }

      agibot::gdk::GDKRelease();
      return 0;
  }
  ```

#### 10. `GetAsrText()`

- **功能**：获取ASR（自动语音识别）文本
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `asr_text` | `std::string&` | 输出参数，识别到的文本内容 |

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`，`asr_text`参数包含识别到的文本

- **示例**：

  ```cpp
  #include "gdk/gdk.h"
  #include <iostream>
  #include <chrono>
  #include <thread>

  int main()
  {
      if (agibot::gdk::GDKInit() != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "GDK初始化失败" << std::endl;
          return -1;
      }
      std::cout << "GDK初始化成功" << std::endl;

      agibot::gdk::Interaction interaction;
      std::this_thread::sleep_for(std::chrono::seconds(1));

      std::string asr_text;
      if (interaction.GetAsrText(asr_text) != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "获取ASR文本失败" << std::endl;
      } else {
          std::cout << "识别到的文本: " << asr_text << std::endl;
      }

      agibot::gdk::GDKRelease();
      return 0;
  }
  ```

#### 11. `RegisterCallback()`
- **功能**：注册回调函数
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `type` | `const std::string&` | 回调类型 |
| `callback` | `std::function<void(const std::any&)>` | 回调函数 |

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`

- **当前支持的回调类型**：
  - `get_asr_text`：回调函数参数类型为`const std::string&`，唤醒状态下，识别到新的语音输入时，会调用回调函数，并传递识别到的文本内容
  - 其余功能回调暂不支持

#### 12. `UnregisterCallback()`

- **功能**：注销回调函数
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `type` | `const std::string&` | 回调类型 |

- **返回值**：`GDKRes`，操作结果状态码。成功时返回`GDKRes::kSuccess`

- **当前支持的回调类型**：
  - `get_asr_text`：注销回调函数，注销后，唤醒状态下，识别到新的语音输入时，不会调用回调函数
  - 其余功能回调暂不支持

- **示例**：

  ```cpp
  #include "gdk/gdk.h"
  #include <iostream>
  #include <chrono>
  #include <thread>
  #include <atomic>

  std::atomic<bool> g_running{true};

  void signal_handler(int signum) {
    std::cout << "收到中断信号" << std::endl;
    g_running = false;
  }
  
  int main()
  {
      signal(SIGINT, signal_handler);
      signal(SIGTERM, signal_handler);

      if (agibot::gdk::GDKInit() != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "GDK初始化失败" << std::endl;
          return -1;
      }
      std::cout << "GDK初始化成功" << std::endl;

      agibot::gdk::Interaction interaction;
      std::this_thread::sleep_for(std::chrono::seconds(1));

      // 开启通话模式
      if (interaction.SetCallMode(true) != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "开启通话模式失败" << std::endl;
      } else {
          std::cout << "开启通话模式成功" << std::endl;
      }

      std::string asr_text;
      if (interaction.RegisterCallback("get_asr_text", [&asr_text](const std::any& data) {
          asr_text = std::any_cast<const std::string&>(data);
          std::cout << "ASR文本: " << asr_text << std::endl;
      }) != agibot::gdk::GDKRes::kSuccess) {
          std::cout << "注册回调失败" << std::endl;
      } else {
          std::cout << "注册回调成功" << std::endl;
      }

      while (g_running) {
          std::this_thread::sleep_for(std::chrono::seconds(1));
      }

      interaction.SetCallMode(false);
      interaction.UnregisterCallback("get_asr_text");
      agibot::gdk::GDKRelease();
      return 0;
  }
  ```

## 使用注意事项

1. **GDK初始化**：使用Interaction功能前必须先调用`agibot::gdk::GDKInit()`初始化GDK系统
2. **GDK释放**：程序结束前必须调用`agibot::gdk::GDKRelease()`释放GDK系统资源
3. **初始化等待**：创建Interaction对象后，建议等待1秒以确保DDS连接建立
4. **返回值检查**：所有接口都会返回`GDKRes`状态码，请及时检查返回值，确保操作成功
5. **文件路径**：播放音频和视频时，确保文件路径正确且文件存在
6. **语言设置**：设置语言后会影响TTS的语言，请根据实际需求设置
7. **音量范围**：设置音量时注意合理范围，避免过大或过小
8. **循环播放**：视频循环播放时，使用-1表示无限循环，注意及时停止
9. **状态查询**：定期查询功能状态，确保各功能正常工作
10. **ASR文本**：获取ASR文本时，需要确保语音识别功能已启用
11. **字符串参数**：传递字符串参数时，确保字符串有效且不为空
12. **错误处理**：始终检查GDKRes返回值，确保操作成功
13. **通话模式**：在通话模式下，可以获取用户输入的语音，并通过接口获取对应的语音文本
14. **注册回调函数**：在通话模式下，可以调用`GetAsrText()`或`RegisterCallback()`注册回调函数获取用户输入的语音文本

## 应用场景

- **语音交互**：实现机器人的语音识别和语音合成功能
- **多媒体展示**：播放音频、视频内容，进行信息展示
- **人机交互**：通过语音和显示进行人机交互
- **状态监控**：监控语音功能状态，确保系统正常运行
- **多语言支持**：支持中英文切换，适应不同场景需求
- **音量控制**：动态调整音量，适应不同环境
- **功能开关**：灵活控制唤醒、音频、显示等功能开关

