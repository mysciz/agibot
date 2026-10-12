---
title: ros2
order: 4
---

# GDK ROS2 humble版本使用说明
Genie 02使用高性能的DDS，默认不发送ROS2消息。如需使用ROS2，需要启动GDK的ROS2转发节点。
GDK在部署时会同时安装自定义的ROS消息，用户编译GDK自定义消息后即可使用ROS2来接收/发送GDK的消息。

## 启动转发节点来获取消息

### 查看消息（以运控节点为例）

#### 启动controller的ROS转发节点

```
source ~/.cache/agibot/app/gdk/scripts/ros_env.sh gdk_controller
ros2 launch gdk_controller controller.launch.py
```

#### 声明ros环境变量
新打开一个终端，在终端中声明环境变量
```
source ~/.cache/agibot/app/gdk/scripts/ros_env.sh gdk_controller
```

#### 查看节点消息

```
ros2 topic list # 查看当前所有topic
ros2 topic echo /hal/joint_state  # 读取topic数据
ros2 topic hz /hal/joint_state # 读取发送频率
```

## 编写程序（以控制关节为例）

### 引入需要用到的genie_msg消息头文件

```
#include "genie_msgs/msg/joint_position_requst.hpp"
#include "genie_msgs/msg/joint_state.hpp"
```

### 创建/hal/joint_state消息的subscriber获取机器人当前所有关节名称、关节角度、速度等信息

```
sub_joint_ = this->create_subscription<genie_msgs::msg::JointState>(
            "/hal/joint_state",  
            10,              
            std::bind(&ControlExampleNode::joint_state_callback, this, std::placeholders::_1)
);
```

### 创建/MotionControlService/JointPosition/request消息的publisher

```
pub_joint_position_ = create_publisher<genie_msgs::msg::JointPositionRequst>("/MotionControlService/JointPosition/request", 10);
```

### 设置uuid

gdk的控制命令需要设置uuid来唯一标识，你可以通过以下方法来创建uuid
```
#include <boost/uuid/uuid.hpp>
#include <boost/uuid/uuid_generators.hpp>
#include <boost/uuid/uuid_io.hpp>
inline std::string generate_uuid_boost()
{
    boost::uuids::random_generator gen;
    return boost::uuids::to_string(gen());
}
```

### 设置控制命令并发布，即可控制对应的关节

```
genie_msgs::msg::JointPositionRequst request;
request.lifetime = 1.0;
request.joint_names = joint_names_;
request.joint_positions = target_positions;
request.joint_velocities = {velocity_};
request.uuid = generate_uuid_boost();
pub_joint_position_->publish(request);      
```

## 获取genie_msgs消息包并编译

### 从部署包中获取编译需要用到的genie_msgs消息包到工作空间并编译
```
cd <your_workspace>
cp -r ~/.cache/agibot/app/gdk/build_dep/ros/genie_msgs ./
colcon build
```

## 运行程序
```
cd <your_workspace>
source install/setup.bash
ros2 launch <your_pkg> <your_launch>
```