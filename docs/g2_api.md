# 部署里用到的 G2 API

只列当前代码真正调用的 `agibot_gdk` 接口。封装在 `deploy/g2/lib/gdk_session.py`、`robot.py`、`camera.py`。手腕示例 `deploy/examples/nudge_wrist.py` 只通过 `GdkRobot` 间接调用其中的读关节、读状态和 `move_arm_joint`。

完整接口说明见 [gdk_api_docs](gdk_api_docs/contents/reference/Python/robot.md) 和 [相机文档](gdk_api_docs/contents/reference/Python/camera.md)。

调用前需要：

```bash
export LOCATOR_IP=10.42.1.102
export AORTA_DISCOVERY_URI=http://10.42.1.101:2379
export AORTA_DISPATCHER_THREAD_NUM=6
```

## 初始化

| 函数 | 作用 |
|---|---|
| `gdk_init()` | 初始化 GDK。返回值必须等于 `GDKRes.kSuccess`，否则视为失败。整个进程只调用一次，机器人和相机共用。 |
| `gdk_release()` | 进程结束时释放。由 `GdkRobot.close()` 调用。 |
| `Robot()` | 机器人控制对象。创建后等待约 1 秒再读状态。 |
| `Camera()` | 相机对象。和 `Robot()` 共用同一次 `gdk_init()`。 |

## 读状态

### `Robot.get_joint_states()`

读取全身关节。代码只用返回字典里的 `states`，并按名字取出 14 个手臂关节：

`idx21_arm_l_joint1` … `idx27_arm_l_joint7`，`idx61_arm_r_joint1` … `idx67_arm_r_joint7`。

每个关节优先读 `motor_position`（弧度）。没有该字段时才用 `position`。

### `Robot.get_end_state()`

读取左右夹爪。使用：

- `left_end_state["end_states"][0]["position"]`
- `right_end_state["end_states"][0]["position"]`

### `Robot.get_whole_body_status()`

下发运动前检查。下面任一项不满足就不再发指令：

| 字段 | 要求 |
|---|---|
| `left_arm_error`、`right_arm_error` | `0` |
| `left_end_error`、`right_end_error` | `0` |
| `left_arm_estop`、`right_arm_estop` | 假 |

## 控制手臂

### `Robot.move_arm_joint(positions, velocities, control_group)`

阻塞规划接口：臂运动到目标后函数才返回。

| 参数 | 代码里的取值 |
|---|---|
| `positions` | 14 个弧度。前 7 个左臂 `idx21`–`idx27`，后 7 个右臂 `idx61`–`idx67` |
| `velocities` | 14 个速度，单位 rad/s，默认每个都是 `0.20` |
| `control_group` | 固定为 `2`，表示同时控制双臂 |

手腕示例也是这条接口：只改 14 维里的一个数（左腕下标 6，右腕下标 13），其余关节保持当前角度。

没有使用 `joint_servo_control`。那条通道要按约 100Hz 连续发送，低延时模式没有碰撞保护。

## 控制夹爪

### `Robot.move_ee_pos(joint_states)`

`joint_states` 是 `JointStates`：

| 字段 | 取值 |
|---|---|
| `group` | `"dual_tool"`，一次下发左右夹爪 |
| `target_type` | 默认 `"omnipicker"`，也可为 `"dahuan"`、`"ctek90d"` |
| `states` | 两个 `JointState`，只设置 `position`。顺序是左、右 |
| `nums` | `2` |

`omnipicker` 的 `position` 范围是 `[-0.785, 0]`，下界打开，上界闭合。

## 相机

### `Camera.get_latest_image(camera_type, timeout_ms)`

`timeout_ms` 为 `1000`。三路相机：

| 代码里的名字 | `CameraType` |
|---|---|
| `head` | `kHeadColor` |
| `left_wrist` | `kHandLeftColor` |
| `right_wrist` | `kHandRightColor` |

返回图像使用这些字段：`data`、`encoding`、`height`、`width`、`color_format`。JPEG/PNG 用 OpenCV 解码后转成 RGB。`NO_CAMERA=1` 或 `MOCK=1` 时不调用这个接口。

如果相机对象有 `close()`，结束时会调用。这不是控制所必需的接口。
