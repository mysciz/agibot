---
title: C++
order: 2
---
# GDK C++ 使用说明

混合部署时，可以在x86平台上基于GDK C++接口二次开发。本文介绍如何在c++项目中使用GDK。

请确保编译/运行时链接动态库版本的一致性，如果编译/运行时链接的动态库版本不匹配，GDK会输出错误日志，例如：
”Version mismatch, runtime version: 2.2.0, build version: 2.2.1“;


## 基本开发（以运控为例）

### 引入头文件

```
#include "gdk/gdk.h"
```

### 初始化GDK

```
if (agibot::gdk::GDKInit() != agibot::gdk::GDKRes::kSuccess) {
    std::cout << "GDK初始化失败" << std::endl;
    return -1;
}
```

### 初始化机器人对象

```
agibot::gdk::Robot robot;
std::cout << "Robot init" << std::endl;
std::this_thread::sleep_for(std::chrono::seconds(1));
```

### 设置控制的关节与对应的关节角位置，执行速度

```
agibot::gdk::JointControlReq joint_control;
joint_control.life_time = 5.0;
joint_control.joint_names = {"arm_l_joint1", "arm_l_joint2", "arm_l_joint3"};
joint_control.joint_positions = {0.5, -0.3, 0.8};
joint_control.joint_velocities = {0.3, 0.3, 0.3};
```

### 发送关节控制命令

```
if (robot.JointControl(joint_control) != agibot::gdk::GDKRes::kSuccess) {
    std::cout << "Failed to control joints" << std::endl;
} else {
    std::cout << "关节控制指令发送成功" << std::endl;
}
```

## 编译
### CMake编译配置

GDK的头文件和动态库部署在GDK_HOME目录，混合部署下GDK_HOME默认在~/.cache/agibot。
将以下内容添加到你的CMakeLists.txt当中，来将你的程序与链接gdk链接库以及头文件，并使用该方法创建编译项目
```
if(NOT DEFINED ENV{GDK_HOME})  
    set(GDK_HOME_PATH ~/.cache/agibot)   
else()
    set(GDK_HOME_PATH $ENV{GDK_HOME})          
endif()

function(add_adapter name)
    add_executable(${name} src/${name}.cpp)

    if(CMAKE_SYSTEM_PROCESSOR STREQUAL "x86_64")
        target_include_directories(${name} PRIVATE ${GDK_HOME_PATH}/app/gdk/build_dep/cpp/x86_64/include)
        target_link_libraries(${name} PRIVATE ${GDK_HOME_PATH}/app/gdk/build_dep/cpp/x86_64/lib/libgdk_adapter.so)        
    elseif(CMAKE_SYSTEM_PROCESSOR STREQUAL "aarch64")
        target_include_directories(${name} PRIVATE ${GDK_HOME_PATH}/app/gdk/build_dep/cpp/aarch64/include)
        target_link_libraries(${name} PRIVATE ${GDK_HOME_PATH}/app/gdk/build_dep/cpp/aarch64/lib/libgdk_adapter.so)     
    endif()    
endfunction()

add_adapter(your_program)
```
### 声明编译链接库路径

```
source ~/.cache/agibot/app/env.sh
```

### 编译
```
cmake -B build
make -C build
```
编译产物可在build文件夹中查询

### 运行程序

```
./build/your_program
```