---
title: Ros2
order: 4
---

## 安装

将开发机与G02机器人通过网线直连，配置开发机的静态IP为10.42.1.102。确保ping 10.42.1.101通信正常。

在开发机环境安装GDK依赖：

```
curl -sSL http://10.42.1.101:8849/install.sh | bash
```

## 编译

```shell
cd <your_workspace>
cp -r ~/.cache/agibot/app/gdk/build_dep/ros/genie_msgs ./
colcon build 
```

## 运行示例

```shell
source ~/.cache/agibot/app/gdk/scripts/ros_env.sh gdk_controller
ros2 launch gdk_controller controller.launch.py
```

可订阅/hal/joint_state话题查看机器人关节状态。

```shell
#新建终端
source ~/.cache/agibot/app/gdk/scripts/ros_env.sh gdk_controller

ros2 topic list
#ros2 topic hz /hal/joint_state #查看发布频率
#ros2 topic echo /hal/joint_state #查看关节状态
```



