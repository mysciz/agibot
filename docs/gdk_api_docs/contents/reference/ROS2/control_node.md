# Control Node
机器人控制器节点
## 末端控制信息获取

### Topic

/wbc/motion_control_status

### 消息类型

genie_msgs::msg::MotionControlStatus.msg

```
std_msgs/Header header  # frame id 默认填写base_link, timestamp发送时间

# 反馈末端位姿状态
string[] frame_names   #运控参数配置定义
geometry_msgs/Pose[] frame_poses

# 反馈自碰撞状态
# [collision_pair_1， collision_pair_2]组成一组碰撞对的frame名称
string[] collision_pairs_1
string[] collision_pairs_2

# 运控模式
uint8 MODE_STOP=0
uint8 MODE_SERVO=1
uint8 MODE_PLANNING=2
uint8 mode

# 实时控制的运控错误码
# 0: no error 
uint8 error_code
string error_msg

geometry_msgs/Twist[] frame_twists
geometry_msgs/Wrench[] frame_wrenchs
```

## 关节角度获取

### Topic

/hal/joint_state

### 消息类型

genie_msgs::msg::JointState

```
# The state of each joint (revolute or prismatic) is defined by:
#  * the control mode (csp 0, cst 1)
#  * the position of the joint (rad or m),
#  * the velocity of the joint (rad/s or m/s),
#  * the effort that is applied in the joint (Nm or N),
#  * the position of the motor (rad or m),
#  * the velocity of the motor (rad/s or m/s),
#  * the current of the motor (A),
#  * the error_code of the joint.      
#
# TODO: Error code description or joint error code page

std_msgs/Header header

string[] name
uint32[] mode
float64[] position
float64[] velocity
float64[] effort
float64[] motor_position
float64[] motor_velocity
float64[] motor_current
uint32[] error_code
```

## 通过关节角度控制机器人

### Topic

/MotionControlService/JointPosition/request

### 消息类型

genie_msg::msg::CommonResponse.msg

```
# frame id 无用, timestamp发送时间
std_msgs/Header header
float64 lifetime

string[] joint_names
float64[] joint_positions
float64[] joint_velocities

string uuid
string details
```

## 关节角控制命令反馈

### Topic

/MotionControlService/JointPosition/response

### 消息类型

genie_msg::msg::CommonResponse.msg

```
# frame id 无用, timestamp发送时间
std_msgs/Header header

uint8 data

string uuid
string detail
```
## 启动ROS2转发节点

### 混合部署

```
source ~/.cache/agibot/app/gdk/scripts/ros_env.sh gdk_controller
ros2 launch gdk_controller controller.launch.py
```
