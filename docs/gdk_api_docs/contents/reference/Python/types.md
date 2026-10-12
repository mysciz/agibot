# GDK 数据类型文档（Python）

## 概述

GDK（Genie Development Kit）提供了丰富的数据类型，用于处理机器人系统中的各种数据。通过Python接口，开发者可以方便地使用这些数据类型进行机器人控制、传感器数据处理、地图管理等功能。

## 枚举类型

### 1. GDKRes

GDK操作结果状态码。

| 枚举值 | 描述 |
| :--- | :--- |
| `kSuccess` | 操作成功 |
| `kInvalidInput` | 输入参数无效 |
| `kInvalidOutput` | 输出参数无效 |
| `kRuntimeError` | 运行时错误 |
| `kUnknown` | 未知错误 |

**示例**：
```python
import agibot_gdk

result = agibot_gdk.gdk_init()
if result == agibot_gdk.GDKRes.kSuccess:
    print("GDK初始化成功")
else:
    print(f"GDK初始化失败，错误码: {result}")
```

### 2. CameraType

相机类型枚举。

| 枚举值 | 描述 |
| :--- | :--- |
| `kCameraUnknown` | 未知相机 |
| `kHeadBackFisheye` | 头部后鱼眼相机 |
| `kHeadLeftFisheye` | 头部左鱼眼相机 |
| `kHeadRightFisheye` | 头部右鱼眼相机 |
| `kHeadStereoLeft` | 头部立体左相机 |
| `kHeadStereoRight` | 头部立体右相机 |
| `kHandLeftColor` | 左手相机 |
| `kHandRightColor` | 右手相机 |
| `kHeadColor` | 头部彩色相机 |
| `kHeadDepth` | 头部深度相机 |

**示例**：
```python
import agibot_gdk

camera_type = agibot_gdk.CameraType.kHeadStereoLeft
print(f"相机类型: {camera_type}")
```

### 3. LidarType

激光雷达类型枚举。

| 枚举值 | 描述 |
| :--- | :--- |
| `kLidarUnknown` | 未知激光雷达 |
| `kLidarFront` | 前激光雷达 |
| `kLidarBack` | 后激光雷达 |

**示例**：
```python
import agibot_gdk

lidar_type = agibot_gdk.LidarType.kLidarFront
print(f"激光雷达类型: {lidar_type}")
```

### 4. ImuType

IMU类型枚举。

| 枚举值 | 描述 |
| :--- | :--- |
| `kImuUnknown` | 未知IMU |
| `kImuFront` | 前IMU |
| `kImuBack` | 后IMU |
| `kImuChassis` | 底盘IMU |

**示例**：
```python
import agibot_gdk

imu_type = agibot_gdk.ImuType.kImuChassis
print(f"IMU类型: {imu_type}")
```

### 5. EndEffectorControlGroup

末端执行器控制组枚举。

| 枚举值 | 描述 |
| :--- | :--- |
| `kUnknown` | 未知组 |
| `kLeftArm` | 左臂 |
| `kRightArm` | 右臂 |
| `kBothArms` | 双臂 |
| `kLeftArmWaistLift` | 左臂+腰部+升降 |
| `kRightArmWaistLift` | 右臂+腰部+升降 |
| `kBothArmsWaistLift` | 双臂+腰部+升降 |
| `kLeftArmWaistPitch` | 左臂+腰部俯仰 |
| `kRightArmWaistPitch` | 右臂+腰部俯仰 |
| `kBothArmsWaistPitch` | 双臂+腰部俯仰 |
| `kLeftArmWaist` | 左臂+腰部 |
| `kRightArmWaist` | 右臂+腰部 |
| `kBothArmsWaist` | 双臂+腰部 |

**示例**：
```python
import agibot_gdk

control_group = agibot_gdk.EndEffectorControlGroup.kBothArms
print(f"控制组: {control_group}")
```

### 6. SensorExtrinsicType

传感器外参类型枚举。

| 枚举值 | 描述 |
| :--- | :--- |
| `kUnknown` | 未知类型 |
| `kHeadLeftStereoToHeadRightStereo` | 头部左立体相机到右立体相机 |
| `kLeftHandDepthToLeftHandColor` | 左手深度相机到彩色相机 |
| `kRightHandDepthToRightHandColor` | 右手深度相机到彩色相机 |
| `kHeadDepthToHeadColor` | 头部深度相机到彩色相机 |
| `kHeadLeftStereoToHeadLink3` | 头部左立体相机到头部链接3 |
| `kHeadRightStereoToHeadLink3` | 头部右立体相机到头部链接3 |
| `kHeadLeftFisheyeToHeadLink3` | 头部左鱼眼相机到头部链接3 |
| `kHeadRightFisheyeToHeadLink3` | 头部右鱼眼相机到头部链接3 |
| `kHeadBackFisheyeToHeadLink3` | 头部后鱼眼相机到头部链接3 |
| `kChassisFrontLidarToBaseLink` | 底盘前激光雷达到base_link |
| `kChassisBackLidarToBaseLink` | 底盘后激光雷达到base_link |
| `kChassisBackLidarToChassisFrontLidar` | 底盘后激光雷达到前激光雷达 |
| `kChassisMid360ImuToChassisMid360Lidar` | 底盘Mid360 IMU到激光雷达 |
| `kChassisImuToBaseLink` | 底盘IMU到base_link |
| `kLeftHandRGBDToArmLEndLink` | 左手RGBD到左臂末端链接 |
| `kRightHandRGBDToArmREndLink` | 右手RGBD到右臂末端链接 |
| `kHeadRGBDToHeadLink3` | 头部RGBD到头部链接3 |

**示例**：
```python
import agibot_gdk

sensor_type = agibot_gdk.SensorExtrinsicType.kHeadLeftStereoToHeadRightStereo
print(f"传感器外参类型: {sensor_type}")
```

## 基础数据类型

### 1. Vector3

3D向量结构。

| 属性名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `x` | `float` | X轴分量 | 米 |
| `y` | `float` | Y轴分量 | 米 |
| `z` | `float` | Z轴分量 | 米 |

**示例**：
```python
import agibot_gdk

vector = agibot_gdk.Vector3()
vector.x = 1.0
vector.y = 2.0
vector.z = 3.0
print(f"向量: {vector}")
```

### 2. Quaternion

四元数结构。

| 属性名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `x` | `float` | 四元数X分量 | 无单位 |
| `y` | `float` | 四元数Y分量 | 无单位 |
| `z` | `float` | 四元数Z分量 | 无单位 |
| `w` | `float` | 四元数W分量 | 无单位 |

**示例**：
```python
import agibot_gdk

quat = agibot_gdk.Quaternion()
quat.x = 0.0
quat.y = 0.0
quat.z = 0.0
quat.w = 1.0
print(f"四元数: {quat}")
```

### 3. Pose

位姿结构。

| 属性名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `position` | `Vector3` | 位置 | 米 |
| `orientation` | `Quaternion` | 方向 | 无单位 |

**示例**：
```python
import agibot_gdk

pose = agibot_gdk.Pose()
pose.position.x = 1.0
pose.position.y = 2.0
pose.position.z = 3.0
pose.orientation.w = 1.0
print(f"位姿: {pose}")
```

### 4. Twist

速度结构。

| 属性名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `linear` | `Vector3` | 线速度 | 米/秒 |
| `angular` | `Vector3` | 角速度 | 弧度/秒 |

**示例**：
```python
import agibot_gdk

twist = agibot_gdk.Twist()
twist.linear.x = 0.5
twist.angular.z = 0.1
print(f"速度: {twist}")
```

### 5. Wrench

力/力矩结构。

| 属性名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `force` | `Vector3` | 力 | 牛顿 |
| `torque` | `Vector3` | 力矩 | 牛顿·米 |

**示例**：
```python
import agibot_gdk

wrench = agibot_gdk.Wrench()
wrench.force.z = 10.0
wrench.torque.z = 5.0
print(f"力/力矩: {wrench}")
```

## 传感器数据类型

### 1. Image

图像数据结构。

| 属性名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `width` | `int` | 图像宽度 | 像素 |
| `height` | `int` | 图像高度 | 像素 |
| `timestamp_ns` | `int` | 时间戳 | 纳秒 |
| `data` | `numpy.ndarray` | 图像数据 | 字节 |
| `encoding` | `Encoding` | 编码格式 | 枚举 |
| `color_format` | `ColorFormat` | 颜色格式 | 枚举 |
| `bit_depth` | `int` | 位深度 | 位 |

**示例**：
```python
import agibot_gdk
import time

# 获取图像数据
camera = agibot_gdk.Camera()
time.sleep(1.0)
image = camera.get_latest_image(agibot_gdk.CameraType.kHeadStereoLeft, 1000.0)

if image is not None:
    print(f"图像尺寸: {image.width} x {image.height}")
    print(f"时间戳: {image.timestamp_ns}")
    print(f"数据大小: {image.data.size} 字节")
    print(f"编码格式: {image.encoding}")
    print(f"颜色格式: {image.color_format}")
    print(f"位深度: {image.bit_depth}")
```

### 2. PointCloud

点云数据结构。

| 属性名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `width` | `int` | 点云宽度 | 点 |
| `height` | `int` | 点云高度 | 点 |
| `fields` | `list[PointField]` | 点云字段 | 列表 |
| `point_step` | `int` | 点步长 | 字节 |
| `row_step` | `int` | 行步长 | 字节 |
| `is_bigendian` | `bool` | 是否大端序 | 布尔 |
| `is_dense` | `bool` | 是否稠密 | 布尔 |
| `data` | `numpy.ndarray` | 点云数据 | 字节 |
| `timestamp_ns` | `int` | 时间戳 | 纳秒 |

**示例**：
```python
import agibot_gdk
import time

# 获取点云数据
lidar = agibot_gdk.Lidar()
time.sleep(1.0)
pointcloud = lidar.get_latest_pointcloud(agibot_gdk.LidarType.kLidarFront, 1000.0)

if pointcloud is not None:
    print(f"点云尺寸: {pointcloud.width} x {pointcloud.height}")
    print(f"时间戳: {pointcloud.timestamp_ns}")
    print(f"数据大小: {pointcloud.data_size} 字节")
    print(f"字段数量: {len(pointcloud.fields)}")
    for field in pointcloud.fields:
        print(f"  字段: {field.name}, 偏移: {field.offset}, 类型: {field.datatype}")
```

### 3. ImuData

IMU数据结构。

| 属性名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `angular_velocity` | `Vector3` | 角速度 | 弧度/秒 |
| `linear_acceleration` | `Vector3` | 线加速度 | 米/秒² |
| `timestamp_ns` | `int` | 时间戳 | 纳秒 |

**示例**：
```python
import agibot_gdk
import time

# 获取IMU数据
imu = agibot_gdk.Imu()
time.sleep(1.0)
imu_data = imu.get_latest_imu(agibot_gdk.ImuType.kImuChassis, 1000.0)

if imu_data is not None:
    print(f"角速度: ({imu_data.angular_velocity.x}, {imu_data.angular_velocity.y}, {imu_data.angular_velocity.z})")
    print(f"线加速度: ({imu_data.linear_acceleration.x}, {imu_data.linear_acceleration.y}, {imu_data.linear_acceleration.z})")
    print(f"时间戳: {imu_data.timestamp_ns}")
```

### 4. CameraIntrinsic

相机内参结构。

| 属性名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `intrinsic` | `list[float]` | 内参 [fx, fy, cx, cy] | 像素 |
| `distortion` | `list[float]` | 畸变参数 [k1, k2, p1, p2, k3, k4, k5, k6] | 无单位 |

**示例**：
```python
import agibot_gdk
import time

# 获取相机内参
camera = agibot_gdk.Camera()
time.sleep(1.0)
intrinsic = camera.get_camera_intrinsic(agibot_gdk.CameraType.kHeadStereoLeft)

print(f"内参:")
print(f"  fx: {intrinsic.intrinsic[0]}")
print(f"  fy: {intrinsic.intrinsic[1]}")
print(f"  cx: {intrinsic.intrinsic[2]}")
print(f"  cy: {intrinsic.intrinsic[3]}")

print(f"畸变参数:")
for i, dist in enumerate(intrinsic.distortion):
    print(f"  k{i+1}: {dist}")
```

## 机器人控制数据类型

### 1. JointState

关节状态结构。

| 属性名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `name` | `str` | 关节名称 | 字符串 |
| `mode` | `int` | 关节模式 | 整数 |
| `position` | `float` | 关节位置 | 弧度 |
| `velocity` | `float` | 关节速度 | 弧度/秒 |
| `effort` | `float` | 关节力矩 | 牛顿·米 |
| `motor_position` | `float` | 电机位置 | 弧度 |
| `motor_velocity` | `float` | 电机速度 | 弧度/秒 |
| `motor_current` | `float` | 电机电流 | 安培 |
| `error_code` | `int` | 错误码 | 整数 |

**示例**：
```python
import agibot_gdk
import time

# 获取关节状态
robot = agibot_gdk.Robot()
time.sleep(1.0)
joint_states = robot.get_joint_states()

print(f"关节数量: {joint_states['nums']}")
for state in joint_states['states']:
    print(f"关节: {state['name']}")
    print(f"  位置: {state['position']}")
    print(f"  速度: {state['velocity']}")
    print(f"  力矩: {state['effort']}")
```

### 2. JointControlReq

关节控制请求结构。

| 属性名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `joint_names` | `list[str]` | 关节名称列表 | 字符串列表 |
| `joint_positions` | `list[float]` | 关节位置列表 | 弧度 |
| `joint_velocities` | `list[float]` | 关节速度列表 | 弧度/秒 |
| `life_time` | `float` | 生命周期 | 秒 |
| `detail` | `str` | 详细信息 | 字符串 |

**示例**：
```python
import agibot_gdk
import time

# 创建关节控制请求
joint_control_req = agibot_gdk.JointControlReq()
joint_control_req.joint_names = ["idx01_body_joint1", "idx02_body_joint2"]
joint_control_req.joint_positions = [0.0, 0.0]
joint_control_req.joint_velocities = [0.1, 0.1]
joint_control_req.life_time = 5.0

# 执行关节控制
robot = agibot_gdk.Robot()
time.sleep(1.0)
result = robot.joint_control_request(joint_control_req)
if result == agibot_gdk.GDKRes.kSuccess:
    print("关节控制成功")
```

### 3. EndEffectorPose

末端执行器位姿控制结构。

| 属性名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `group` | `int` | 控制组 | 整数 |
| `left_end_effector_pose` | `Pose` | 左末端执行器位姿 | 位姿 |
| `right_end_effector_pose` | `Pose` | 右末端执行器位姿 | 位姿 |
| `life_time` | `float` | 生命周期 | 秒 |

**示例**：

注意：end_effector_pose_control()需要对action进行插值处理才可正常响应，本示例仅说明EndEffectorPose的数据结构

```python
import agibot_gdk
import time

# 创建末端执行器位姿控制请求
# 该请求需要结合当前末端执行器位姿进行插补，本示例仅作说明
end_pose = agibot_gdk.EndEffectorPose()
end_pose.group = agibot_gdk.EndEffectorControlGroup.kBothArms
end_pose.left_end_effector_pose.position.x = 0.3
end_pose.left_end_effector_pose.position.y = 0.2
end_pose.left_end_effector_pose.position.z = 0.4
end_pose.left_end_effector_pose.orientation.x = 0.0
end_pose.left_end_effector_pose.orientation.y = 0.0
end_pose.left_end_effector_pose.orientation.z = 0.0
end_pose.left_end_effector_pose.orientation.w = 1.0
end_pose.right_end_effector_pose.position.x = 0.3
end_pose.right_end_effector_pose.position.y = 0.3
end_pose.right_end_effector_pose.position.z = -0.2
end_pose.right_end_effector_pose.orientation.x = 0.0
end_pose.right_end_effector_pose.orientation.y = 0.0
end_pose.right_end_effector_pose.orientation.z = 0.0
end_pose.right_end_effector_pose.orientation.w = 1.0
end_pose.life_time = 5.0

# 执行末端执行器位姿控制
robot = agibot_gdk.Robot()
time.sleep(1.0)
result = robot.end_effector_pose_control(end_pose)
if result == agibot_gdk.GDKRes.kSuccess:
    print("末端执行器位姿控制成功")
```

## 地图数据类型

### 1. MapInfo

地图信息结构。

| 属性名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `id` | `int` | 地图ID | 整数 |
| `name` | `str` | 地图名称 | 字符串 |
| `status` | `int` | 地图状态 | 整数 |
| `counter` | `int` | 地图计数器 | 整数 |
| `timestamp_ns` | `int` | 时间戳 | 纳秒 |
| `gravity` | `Vector3` | 重力向量 | 米/秒² |
| `cloud_map` | `PointCloud` | 点云地图 | 点云 |
| `grid_map` | `OccupancyGrid` | 栅格地图 | 栅格 |
| `walls` | `list[list[Point3d]]` | 墙壁 | 点列表 |
| `infeasible_areas` | `list[list[Point3d]]` | 不可行区域 | 点列表 |
| `guide_pts` | `list[GuidePtInfo]` | 引导点 | 引导点列表 |

**示例**：
```python
import agibot_gdk
import time

# 获取地图信息
map_manager = agibot_gdk.Map()
time.sleep(1.0)

# 获取地图信息前，先完成建图
try:
    map_info = map_manager.get_map(1)
except Exception as e:
    print(f"获取地图信息失败: {e}")
    exit(1)

print(f"地图名称: {map_info.name}")
print(f"地图ID: {map_info.id}")
print(f"地图状态: {map_info.status}")
print(f"重力向量: ({map_info.gravity.x}, {map_info.gravity.y}, {map_info.gravity.z})")
print(f"墙壁数量: {len(map_info.walls)}")
print(f"不可行区域数量: {len(map_info.infeasible_areas)}")
print(f"引导点数量: {len(map_info.guide_pts)}")
```

### 2. OccupancyGrid

占用栅格地图结构。

| 属性名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `width` | `int` | 地图宽度 | 栅格 |
| `height` | `int` | 地图高度 | 栅格 |
| `resolution` | `float` | 分辨率 | 米/栅格 |
| `origin` | `Pose` | 原点位姿 | 位姿 |
| `data` | `list[int]` | 栅格数据 | 整数列表 |
| `timestamp_ns` | `int` | 时间戳 | 纳秒 |

**示例**：
```python
import agibot_gdk
import time

# 获取栅格地图
map_manager = agibot_gdk.Map()
time.sleep(1.0)
map_info = map_manager.get_map(1)
grid_map = map_info.grid_map

print(f"栅格地图尺寸: {grid_map.width} x {grid_map.height}")
print(f"分辨率: {grid_map.resolution} 米/栅格")
print(f"原点位置: ({grid_map.origin.position.x}, {grid_map.origin.position.y}, {grid_map.origin.position.z})")
print(f"栅格数据大小: {len(grid_map.data)}")
```

## 坐标变换数据类型

### 1. Transform

坐标变换结构。

| 属性名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `translation` | `Vector3` | 平移向量 | 米 |
| `rotation` | `Quaternion` | 旋转四元数 | 无单位 |

**示例**：
```python
import agibot_gdk
import time

# 获取坐标变换
tf = agibot_gdk.TF()
time.sleep(1.0)
transform = tf.get_tf_from_base_link("arm_l_end_link")

print(f"平移: ({transform.translation.x}, {transform.translation.y}, {transform.translation.z})")
print(f"旋转: ({transform.rotation.x}, {transform.rotation.y}, {transform.rotation.z}, {transform.rotation.w})")
```

### 2. TransformStamped

带时间戳的坐标变换结构。

| 属性名 | 类型 | 描述 | 单位 |
| :--- | :--- | :--- | :--- |
| `frame_id` | `str` | 父坐标系ID | 字符串 |
| `child_frame_id` | `str` | 子坐标系ID | 字符串 |
| `transform` | `Transform` | 变换信息 | 变换 |
| `timestamp_ns` | `int` | 时间戳 | 纳秒 |

**示例**：
```python
import agibot_gdk
import time

# 获取所有坐标变换
tf = agibot_gdk.TF()
time.sleep(1.0)
transforms = tf.get_all_tf_from_base_link()

for transform_stamped in transforms:
    print(f"坐标系: {transform_stamped.frame_id} -> {transform_stamped.child_frame_id}")
    print(f"  平移: ({transform_stamped.transform.translation.x}, {transform_stamped.transform.translation.y}, {transform_stamped.transform.translation.z})")
    print(f"  时间戳: {transform_stamped.timestamp_ns}")
```

## 使用注意事项

1. **数据有效性**：使用前请检查返回的数据是否为None
2. **枚举值使用**：使用枚举值而不是整数值，提高代码可读性
3. **数组访问**：使用Python列表语法访问数组元素
4. **字符串编码**：字符串使用UTF-8编码

## 应用场景

- **机器人控制**：使用关节状态和控制请求进行机器人运动控制
- **传感器数据处理**：处理图像、点云、IMU等传感器数据
- **地图管理**：使用地图信息进行导航和路径规划
- **坐标变换**：处理不同坐标系之间的变换关系
- **状态监控**：监控机器人各部件的工作状态
- **数据融合**：融合多种传感器数据进行环境感知
- **路径规划**：基于地图数据进行路径规划
- **视觉处理**：使用相机内参进行图像校正和3D重建
