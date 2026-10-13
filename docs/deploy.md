# 使用说明

代码在仓库根目录 `agibot/`（里面有 `deploy/`）。下面的命令都在这个目录执行。

现在没有 WAM 模型。想让机器人动，有两条路：

1. 直接跑示例脚本，只转一侧手腕，用来确认关节接口通不通。
2. 开两个端口。A 用文件或终端代替模型，给出每一步的关节增量；B 读机器人，把观测发给 A，再取回动作并执行。

## 连机器人之前

开发机网口是 `10.42.1.102`，机器人是 `10.42.1.101`。每次新开终端先执行：

```bash
export LOCATOR_IP=10.42.1.102
export AORTA_DISCOVERY_URI=http://10.42.1.101:2379
export AORTA_DISPATCHER_THREAD_NUM=6
```

没设置这两个地址时，程序不会去连 `127.0.0.1:2379`。急停放在手边，周围留出空位。

当前终端如果提示 `python: 未找到`，先 `conda activate base`。`serve.sh` / `client.sh` 也会在找不到 `python` 时改用 `~/miniconda3/bin/python`。不连机器人、只在本机走通端口时，用 `MOCK=1`，不需要上面三个环境变量。

## 1. 直接转手腕

不经过端口 A/B，脚本自己读当前角度、转一点、再转回去。

```bash
python deploy/examples/nudge_left_wrist.py
python deploy/examples/nudge_right_wrist.py
```

| 脚本 | 动的关节 | 默认幅度 |
|---|---|---|
| `nudge_left_wrist.py` | 左腕末关节 `idx27_arm_l_joint7` | `0.05` rad，约 3° |
| `nudge_right_wrist.py` | 右腕末关节 `idx67_arm_r_joint7` | `0.05` rad，约 3° |

幅度用 `--delta` 改，绝对值不能超过 `0.15` rad：

```bash
python deploy/examples/nudge_left_wrist.py --delta 0.03
```

打印目标角度后会停 2 秒，这时 `Ctrl+C` 可以取消。转完会回到原来的角度。

## 2. 两个端口

| | 端口 A | 端口 B |
|---|---|---|
| 默认地址 | `127.0.0.1:8800` | `127.0.0.1:8801` |
| 启动 | `bash deploy/serve.sh` | `bash deploy/client.sh` |
| 角色 | 模型侧。现在从文件或终端拿动作 | 机器人侧。读关节和相机，执行动作 |
| 数据 | B 把观测 `POST /observation` 过来；B 再 `GET /actions` 取走动作块 | 收到的是归一化 \(\Delta\theta\)，加到当前关节角上再下发 |

先开 A，再开 B。B 发现 A 没起来会直接退出。默认是位置串行。换成速度串行：`MODE=serial_speed bash deploy/client.sh`。异步播放要两边都带 `MODE=async`，说明见 [mode.md](mode.md)。

不连机器人、只在内存里走一遍：

```bash
bash deploy/serve.sh
MOCK=1 bash deploy/client.sh
```

连上机器人后，建议先只打印、不下发：

```bash
bash deploy/serve.sh
NO_MOVE=1 NO_CAMERA=1 bash deploy/client.sh
```

确认打印出的角度增量是你要的，再真正运动。只测关节、不打开相机时用 `NO_CAMERA=1`。要留下相机画面时不要加它，并让 A 带上 `SAVE_DIR`：

```bash
SAVE_DIR=deploy/records bash deploy/serve.sh
bash deploy/client.sh
```

每次观测存成 `SAVE_DIR/0001/` 这一类目录，里面是 `head.png`、`left_wrist.png`、`right_wrist.png` 和 `proprio.json`。

执行过程中看 B 的状态：

```bash
curl http://127.0.0.1:8801/status
```

`Ctrl+C` 停止对应终端。急停或手臂、夹爪错误码不是 0 时，B 会停止下发。

### 动作格式

每一步 16 个数，顺序固定：

| 下标 | 关节 |
|---|---|
| 0–6 | 左臂 `idx21` … `idx27`（6 是左腕末关节） |
| 7–13 | 右臂 `idx61` … `idx67`（13 是右腕末关节） |
| 14 | 左夹爪 |
| 15 | 右夹爪 |

这 16 个数是**相对当前角度的增量**，不是要去的绝对角度。

文件和终端里可以写弧度。端口之间传的是归一化值，范围 `[0, 1]`：

| 归一化值 | 含义 |
|---|---|
| `0.5` | 这个关节不动 |
| `1` | 正向转一步上限 |
| `0` | 反向转一步上限 |

手臂一步上限默认 `0.10` rad，夹爪默认 `0.30`。文件里写了 `0.05` rad 时，线上大约是 `0.75`。写得比上限还大，会被裁到上限再执行。正增量让关节值变大；`omnipicker` 变大是在闭合。

B 每一轮做完这四步才进入下一轮：读当前姿态，POST 给 A，GET 动作，逐步执行。`move_arm_joint` 返回之后才发下一步。

## 文件输入

这是默认方式，`deploy/config/common.env` 里 `ACTION_SOURCE=file`。

默认文件是 `deploy/examples/joint0_wiggle.json`，左臂第 1 关节走 `+0.05、+0.05、-0.05、-0.05` rad，其余关节为 0，最后回到原位。

换文件：

```bash
ACTIONS_FILE=deploy/examples/你的文件.json bash deploy/serve.sh
```

`unit` 用 `rad` 时，数字是弧度增量：

```json
{
  "unit": "rad",
  "steps": [
    [0.05, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0.05, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  ]
}
```

第二行下标 5 是左臂第 6 关节，转 `+0.05` rad。

`unit` 用 `norm` 时，数字已经是 `0–1`，`0.5` 表示不动：

```json
{
  "unit": "norm",
  "steps": [
    [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.75, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
  ]
}
```

这一步只让左腕末关节正向转半个上限（默认 `0.05` rad）。

也可以写成多段 `chunks`，程序会按顺序拼成一条时间序列：

```json
{
  "unit": "rad",
  "chunks": [
    [[0.05, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
    [[-0.05, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
  ]
}
```

文件在 A 启动时一次读完。B 每来要一次，就按 `OPEN_LOOP_HORIZON` 取走后面几步。步数用完后 B 停止。改文件后要重启 A。

## 终端输入

A 不读文件，改由你在 A 的终端里逐行输入。B 每次来取动作时，A 才会出现提示符。

```bash
ACTION_SOURCE=stdin bash deploy/serve.sh
```

另一个终端照常启动 B。A 上会看到类似：

```text
[A] 观测 #1 j0=+0.0123 rad  grip=(-0.3925, -0.3925)
Δθ>  16 个数，默认弧度；或 `norm ...` / `hold` / `quit`
```

在这个提示后面输入一行：

| 输入 | 作用 |
|---|---|
| `0.05 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0` | 16 个弧度增量。不写前缀时默认是弧度 |
| `rad 0.05 0 0 0 0 0 0 0 0 0 0 0 0 0 0` | 同上，显式标明弧度 |
| `norm 0.75 0.5 0.5 0.5 0.5 0.5 0.5 0.5 0.5 0.5 0.5 0.5 0.5 0.5 0.5 0.5` | 16 个 `0–1` 归一化值 |
| `hold` 或直接回车 | 16 个关节都不动 |
| `quit`、`q`、`done` | 结束，B 不再收到新动作 |

必须是 16 个数。`OPEN_LOOP_HORIZON` 是几，A 就会连续问几行，然后 B 把这几步做完，再来要下一批。默认是 1，所以每输入一行，机器人动一步。

## 参数

写在 `deploy/config/common.env`。临时改动放在命令前面，不必改文件：

```bash
MAX_STEPS=2 OPEN_LOOP_HORIZON=2 bash deploy/client.sh
```

| 参数 | 默认 | 作用 |
|---|---|---|
| `MODEL_HOST` / `MODEL_PORT` | `127.0.0.1` / `8800` | 端口 A |
| `ROBOT_HOST` / `ROBOT_PORT` | `127.0.0.1` / `8801` | 端口 B，提供 `/health` 和 `/status` |
| `MODEL_URL` | `http://127.0.0.1:8800` | B 连接 A 的地址 |
| `ACTION_SOURCE` | `file` | `file` 或 `stdin` |
| `ACTIONS_FILE` | `deploy/examples/joint0_wiggle.json` | 文件模式下的动作 |
| `GRIPPER` | `omnipicker` | 也可选 `dahuan`、`ctek90d` |
| `MAX_JOINT_STEP` | `0.10` | 手臂一步最大弧度，也是归一化 `0/1` 对应的幅度 |
| `MAX_GRIPPER_STEP` | `0.30` | 夹爪一步最大行程 |
| `LIMIT_MARGIN` | `0.02` | 手臂目标离硬限位保留的弧度 |
| `MODE` | `serial` | `serial`、`serial_speed` 或 `async`。见 [mode.md](mode.md) |
| `JOINT_VELOCITY` | `0.20` | `serial` 模式下发给规划器的关节速度，rad/s |
| `STEP_DURATION` | `0.50` | `serial_speed` 的步长时间，秒。速度 = Δθ / 这个时间 |
| `MAX_JOINT_VEL` | `0.20` | `serial_speed` 手臂速度上限，rad/s |
| `MAX_GRIPPER_VEL` | `0.40` | `serial_speed` 和 `async` 的夹爪速度上限 |
| `INFER_DELAY` | `0`，`async` 为 `0.40` | 端口 A 在发出动作前等待的秒数，用来模拟推理 |
| `PREFETCH_MARGIN` | `0.05` | `async` 在推理时间之外再提前这么多秒去要下一块 |
| `SERVO_HZ` | `100` | `async` 的播放频率 |
| `CONTROL_PERIOD` | `0.012` | 传给 `joint_servo_control` 的控制周期，秒 |
| `MAX_STEPS` | `4` | B 最多执行多少步 |
| `OPEN_LOOP_HORIZON` | `1` | 每向 A 要一次，连续执行几步 |
| `MOCK` | `0` | `1` 时不连机器人，关节只存在内存里 |
| `NO_MOVE` | `0` | `1` 时读真机关节并打印指令，不下发 |
| `NO_CAMERA` | `0` | `1` 时不打开相机，用空白图 |
| `SAVE_DIR` | 空 | 端口 A 把每次观测的三路图和关节角写到这个目录 |
| `PYTHON` | `python` | 解释器。环境不在默认 `python` 上时写成绝对路径 |

`MAX_JOINT_STEP` 和 `MAX_GRIPPER_STEP` 在 A、B 两侧要一致，否则同一句弧度增量会被编成不同的 `0–1`。用 `serve.sh` / `client.sh` 时两边读的是同一份配置。
