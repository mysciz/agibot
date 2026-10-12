# GDK 交互接口文档（Python）

## 概述

交互模块为G02机器人提供了语音交互、显示控制、音频播放等功能。通过Python接口，开发者可以方便地实现对机器人的语音控制、TTS播放、音频视频播放、显示控制等功能，适用于语音交互、多媒体展示、人机交互等多种场景。

## 注意事项

交互接口依赖跨网段通信模块，因此如果在隔离环境中使用该类接口（如docker容器），需要确保容器可以修改宿主机的网络配置。（启动容器时添加参数‘--privileged’）

## 接口说明

### Interaction 类

该类封装了机器人交互的主要功能接口。

#### 1. `set_language(language)`

- **功能**：设置语音语言
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `language` | `Language` | 语言类型，`Language.kLanguageChinese` 表示中文，`Language.kLanguageEnglish` 表示英文 |

- **返回值**：无，失败时抛出异常

**Language枚举值**：

| 枚举值 | 描述 |
| :--- | :--- |
| `Language.kLanguageChinese` | 中文 |
| `Language.kLanguageEnglish` | 英文 |

- **示例**：

  ```python
  import agibot_gdk
  import time

  # 初始化GDK系统
  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)
  print("GDK初始化成功")

  interaction = agibot_gdk.Interaction()
  time.sleep(1)  # 等待初始化完成

  # 设置语言为中文
  try:
      interaction.set_language(agibot_gdk.Language.kLanguageChinese)
      print("设置语言成功")
  except Exception as e:
      print(f"设置语言失败: {e}")

  # 释放GDK系统资源
  if agibot_gdk.gdk_release() != agibot_gdk.GDKRes.kSuccess:
      print("GDK释放失败")
      exit(1)
  print("GDK释放成功")
  ```

#### 2. `set_call_mode(is_on)`

- **功能**：设置通话模式
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `is_on` | `bool` | `True` 表示开启通话模式，`False` 表示关闭通话模式 |

- **返回值**：无，失败时抛出异常

- **注意事项**：
  - 开启通话模式后，自动进入唤醒状态，关闭通话模式后，自动退出唤醒状态，无需唤醒词和结束词
  - 在通话模式下，可以获取用户输入的语音，并通过接口获取对应的语音文本
  - 在通话模式下，可以调用`get_asr_text()`或`register_callback()`注册回调函数获取用户输入的语音文本

- **示例**：

  ```python
  import agibot_gdk
  import time

  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)

  interaction = agibot_gdk.Interaction()
  time.sleep(1)

  # 开启通话模式
  try:
      interaction.set_call_mode(True)
      print("开启通话模式成功")
  except Exception as e:
      print(f"开启通话模式失败: {e}")

  # 关闭通话模式
  try:
      interaction.set_call_mode(False)
      print("关闭通话模式成功")
  except Exception as e:
      print(f"关闭通话模式失败: {e}")

  agibot_gdk.gdk_release()
  ```

#### 3. `set_volume(volume)`

- **功能**：设置音量
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `volume` | `int` | 音量值，范围通常为0-100 |

- **返回值**：无，失败时抛出异常

- **示例**：

  ```python
  import agibot_gdk
  import time

  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)

  interaction = agibot_gdk.Interaction()
  time.sleep(1)

  # 设置音量为50
  try:
      interaction.set_volume(50)
      print("设置音量成功")
  except Exception as e:
      print(f"设置音量失败: {e}")

  agibot_gdk.gdk_release()
  ```

#### 4. `set_wakeup_switch(is_on)`

- **功能**：设置唤醒开关
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `is_on` | `bool` | `True` 表示开启唤醒，`False` 表示关闭唤醒 |

- **返回值**：无，失败时抛出异常

- **示例**：

  ```python
  import agibot_gdk
  import time

  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)

  interaction = agibot_gdk.Interaction()
  time.sleep(1)

  # 开启唤醒功能
  try:
      interaction.set_wakeup_switch(True)
      print("开启唤醒功能成功")
  except Exception as e:
      print(f"设置唤醒开关失败: {e}")

  agibot_gdk.gdk_release()
  ```

#### 5. `set_audio_switch(is_on)`

- **功能**：设置音频开关
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `is_on` | `bool` | `True` 表示开启音频，`False` 表示关闭音频 |

- **返回值**：无，失败时抛出异常

- **示例**：

  ```python
  import agibot_gdk
  import time

  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)

  interaction = agibot_gdk.Interaction()
  time.sleep(1)

  # 开启音频功能
  try:
      interaction.set_audio_switch(True)
      print("开启音频功能成功")
  except Exception as e:
      print(f"设置音频开关失败: {e}")

  agibot_gdk.gdk_release()
  ```

#### 6. `set_display_switch(is_on)`

- **功能**：设置显示开关
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `is_on` | `bool` | `True` 表示开启显示，`False` 表示关闭显示 |

- **返回值**：无，失败时抛出异常

- **示例**：

  ```python
  import agibot_gdk
  import time

  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)

  interaction = agibot_gdk.Interaction()
  time.sleep(1)

  # 开启显示功能
  try:
      interaction.set_display_switch(True)
      print("开启显示功能成功")
  except Exception as e:
      print(f"设置显示开关失败: {e}")

  agibot_gdk.gdk_release()
  ```

#### 7. `play_tts(text)`

- **功能**：播放TTS（文本转语音）
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `text` | `str` | 要播放的文本内容 |

- **返回值**：无，失败时抛出异常

- **示例**：

  ```python
  import agibot_gdk
  import time

  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)

  interaction = agibot_gdk.Interaction()
  time.sleep(1)

  # 播放TTS
  try:
      interaction.play_tts("你好，我是精灵G2")
      print("TTS播放成功")
      time.sleep(3)  # 等待播放完成
  except Exception as e:
      print(f"播放TTS失败: {e}")

  agibot_gdk.gdk_release()
  ```

#### 8. `play_audio(audio_path)`

- **功能**：播放音频文件
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `audio_path` | `str` | 音频文件路径 |

- **返回值**：无，失败时抛出异常

- **示例**：

  ```python
  import agibot_gdk
  import time

  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)

  interaction = agibot_gdk.Interaction()
  time.sleep(1)

  # 播放音频文件
  try:
      interaction.play_audio("/path/to/audio.wav")
      print("音频播放成功")
      time.sleep(5)  # 等待播放完成
  except Exception as e:
      print(f"播放音频失败: {e}")

  agibot_gdk.gdk_release()
  ```

#### 9. `play_video(video_path, loop_count)`

- **功能**：播放视频文件
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `video_path` | `str` | 视频文件路径 |
| `loop_count` | `int` | 循环播放次数，-1表示无限循环 |

- **返回值**：无，失败时抛出异常

- **示例**：

  ```python
  import agibot_gdk
  import time

  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)

  interaction = agibot_gdk.Interaction()
  time.sleep(1)

  # 播放视频文件，循环1次
  try:
      interaction.play_video("/path/to/video.mp4", 1)
      print("视频播放成功")
      time.sleep(10)  # 等待播放完成
  except Exception as e:
      print(f"播放视频失败: {e}")

  # 无限循环播放
  try:
      interaction.play_video("/path/to/video.mp4", -1)
      print("视频开始循环播放")
  except Exception as e:
      print(f"播放视频失败: {e}")

  agibot_gdk.gdk_release()
  ```

#### 10. `get_func_status()`

- **功能**：获取语音功能状态
- **参数**：无
- **返回值**：`VoiceFuncStatus` 对象，包含以下属性：

| 属性名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `func_status` | `int` | 功能状态 |
| `wakeup_status` | `int` | 唤醒状态 |
| `requester` | `str` | 请求者 |
| `wakeup_enabled` | `bool` | 唤醒功能是否启用 |
| `display_enabled` | `bool` | 显示功能是否启用 |
| `audio_enabled` | `bool` | 音频功能是否启用 |
| `en_settings` | `VoiceSettings` | 英文语音设置 |
| `cn_settings` | `VoiceSettings` | 中文语音设置 |
| `timestamp` | `int` | 时间戳（纳秒） |

**VoiceSettings对象属性**：

| 属性名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `volume` | `int` | 音量 |
| `speech_rate` | `float` | 语速 |
| `voice_tone` | `str` | 音色 |
| `is_curr_setting` | `bool` | 是否为当前设置 |

- **示例**：

  ```python
  import agibot_gdk
  import time

  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)

  interaction = agibot_gdk.Interaction()
  time.sleep(1)

  # 获取功能状态
  try:
      func_status = interaction.get_func_status()
      print("功能状态信息:")
      print(f"  功能状态: {func_status.func_status}")
      print(f"  唤醒状态: {func_status.wakeup_status}")
      print(f"  请求者: {func_status.requester}")
      print(f"  唤醒功能启用: {func_status.wakeup_enabled}")
      print(f"  显示功能启用: {func_status.display_enabled}")
      print(f"  音频功能启用: {func_status.audio_enabled}")
      print(f"  中文设置 - 音量: {func_status.cn_settings.volume}, "
            f"语速: {func_status.cn_settings.speech_rate}, "
            f"音色: {func_status.cn_settings.voice_tone}")
      print(f"  英文设置 - 音量: {func_status.en_settings.volume}, "
            f"语速: {func_status.en_settings.speech_rate}, "
            f"音色: {func_status.en_settings.voice_tone}")
      print(f"  时间戳: {func_status.timestamp}")
  except Exception as e:
      print(f"获取功能状态失败: {e}")

  agibot_gdk.gdk_release()
  ```

#### 11. `get_asr_text()`

- **功能**：获取ASR（自动语音识别）文本
- **参数**：无
- **返回值**：`str`，识别到的文本内容，失败时抛出异常

- **示例**：

  ```python
  import agibot_gdk
  import time

  if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
      print("GDK初始化失败")
      exit(1)

  interaction = agibot_gdk.Interaction()
  time.sleep(1)

  # 获取ASR文本
  try:
      asr_text = interaction.get_asr_text()
      print(f"识别到的文本: {asr_text}")
  except Exception as e:
      print(f"获取ASR文本失败: {e}")

  agibot_gdk.gdk_release()
  ```

#### 12. `register_callback(type, callback)`

- **功能**：注册回调函数
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `type` | `str` | 回调类型 |
| `callback` | `function` | 回调函数 |

- **返回值**：无，失败时抛出异常

- **当前支持的回调类型**：
  - `get_asr_text`：回调函数参数类型为`str`，唤醒状态下，识别到新的语音输入时，会调用回调函数，并传递识别到的文本内容
  - 其余功能回调暂不支持

#### 13. `unregister_callback(type)`

- **功能**：注销回调函数
- **参数**：

| 参数名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `type` | `str` | 回调类型 |

- **返回值**：无，失败时抛出异常

- **当前支持的回调类型**：
  - `get_asr_text`：注销回调函数，注销后，唤醒状态下，识别到新的语音输入时，不会调用回调函数
  - 其余功能回调暂不支持

- **示例**：

  ```python
    import agibot_gdk
    import time

    class ASRHandler:
        def __init__(self, interaction):
            self.interaction = interaction
    
        def callback(self, text):
            print(f"callback text: {text}")

    if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
        print("GDK初始化失败")
        exit(1)

    interaction = agibot_gdk.Interaction()
    time.sleep(1)

    # 开启通话模式
    try:
        interaction.set_call_mode(True)
        print("开启通话模式成功")
    except Exception as e:
        print(f"开启通话模式失败: {e}")

    asr_handler = ASRHandler(interaction)

    # 注册回调函数
    try:
        interaction.register_callback("get_asr_text", asr_handler.callback)
        print("注册回调函数成功")
    except Exception as e:
        print(f"注册回调函数失败: {e}")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        interaction.set_call_mode(False)
        interaction.unregister_callback("get_asr_text")
        agibot_gdk.gdk_release()

  ```

## 使用注意事项

1. **GDK初始化**：使用Interaction功能前必须先调用`agibot_gdk.gdk_init()`初始化GDK系统
2. **GDK释放**：程序结束前必须调用`agibot_gdk.gdk_release()`释放GDK系统资源
3. **初始化等待**：创建Interaction对象后，建议等待1秒以确保DDS连接建立
4. **异常处理**：所有接口在失败时会抛出异常，请使用try-except进行异常处理
5. **文件路径**：播放音频和视频时，确保文件路径正确且文件存在
6. **语言设置**：设置语言后会影响TTS的语言，请根据实际需求设置
7. **音量范围**：设置音量时注意合理范围，避免过大或过小
8. **循环播放**：视频循环播放时，使用-1表示无限循环，注意及时停止
9. **状态查询**：定期查询功能状态，确保各功能正常工作
10. **ASR文本**：获取ASR文本时，需要确保语音识别功能已启用
11. **通话模式**：在通话模式下，可以获取用户输入的语音，并通过接口获取对应的语音文本
12. **注册回调函数**：在通话模式下，可以调用`get_asr_text()`或`register_callback()`注册回调函数获取用户输入的语音文本

## 应用场景

- **语音交互**：实现机器人的语音识别和语音合成功能
- **多媒体展示**：播放音频、视频内容，进行信息展示
- **人机交互**：通过语音和显示进行人机交互
- **状态监控**：监控语音功能状态，确保系统正常运行
- **多语言支持**：支持中英文切换，适应不同场景需求
- **音量控制**：动态调整音量，适应不同环境
- **功能开关**：灵活控制唤醒、音频、显示等功能开关

