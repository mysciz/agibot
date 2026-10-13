# 控制模式

端口 B 用 `MODE` 选择怎么把动作变成机器人指令。端口 A 不变，给出的仍是归一化 \(\Delta\theta\)。

```bash
bash deploy/serve.sh
MODE=serial bash deploy/client.sh
MODE=serial_speed bash deploy/client.sh
MODE=async bash deploy/serve.sh
MODE=async bash deploy/client.sh
```

`MODE` 对应 `deploy/config/modes/` 里的一个文件。`smooth` 的配置文件先留着，选它会退出并提示还没实现。

| MODE | 状态 | 做法 |
|---|---|---|
| `serial` | 可用，默认 | 转角增量加到当前角度上，用固定速度走到那个角度 |
| `serial_speed` | 可用 | 转角增量先除以步长时间，得到关节速度，再乘回时间得到这一步的目标角度 |
| `async` | 可用 | 一次取 `n` 步，插成 100Hz 位置流。下一块在播放还没结束时就去要 |
| `smooth` | 未实现 | 预备给以后的轨迹平滑。现在不要用 |

`serial` 和 `serial_speed` 都等 `move_arm_joint` 返回再执行下一步。`async` 用 `joint_servo_control`，播放线程不跟着推理停。

## serial

这一步的目标角度是：

```text
θ_cmd = θ_now + Δθ
```

然后交给 `move_arm_joint(θ_cmd, velocities, 2)`。14 个关节的速度都是同一个数，默认 `JOINT_VELOCITY=0.20` rad/s。转 `0.05` rad 和转 `0.10` rad 用的是一样的速度，只是路程不同。

单步转角仍受 `MAX_JOINT_STEP`（默认 `0.10` rad）限制。

## serial_speed

先把这一步要转的角度换成速度：

```text
ω = clip(Δθ / T, -ωmax, ωmax)
θ_cmd = θ_now + ω · T
```

`T` 是 `STEP_DURATION`，默认 `0.50` 秒。手臂 `ωmax` 是 `MAX_JOINT_VEL`，默认 `0.20` rad/s。夹爪用 `MAX_GRIPPER_VEL`，默认 `0.40`。

算完后再做原来的限位和单步限制。真正发给 `move_arm_joint` 的速度是每个关节自己的 \(|ω|\)，方向由目标角度决定。接口要的是正速度。

举例：`T = 0.5` s，`ωmax = 0.20` rad/s。

| 这一步 Δθ | 速度 | 实际转动 |
|---|---|---|
| `0.05` rad | `0.10` rad/s | `0.05` rad |
| `0.10` rad | `0.20` rad/s | `0.10` rad |
| `0.20` rad | 被裁成 `0.20` rad/s | 只有 `0.10` rad |

第三行就是这个模式和 `serial` 的差别：增量很大时，不会按那个大角度去追，而是按速度上限只走 `ωmax · T`。

夹爪没有单独的速度参数，`move_ee_pos` 仍下发位置。位置同样是 `ω · T` 积分出来的。

本地先看速度打印、不连机器人：

```bash
bash deploy/serve.sh
MODE=serial_speed MOCK=1 bash deploy/client.sh
```

日志里的 `v0` 是第 0 个关节这一步的速度，单位 rad/s。

## async

模型一次给出 `n` 步，但推理要花 `t` 秒。若等这 `n` 步全部走完再去要下一块，中间就会停住。这个模式把取动作和播放拆开。

端口 A 在 `GET /actions` 里先等待 `INFER_DELAY` 秒，用来假装推理。本地没有真模型时，延迟就是这个数。端口 B 用 `OPEN_LOOP_HORIZON` 作为一次取的步数 `n`。

每一块的处理是：

```text
ω = clip(Δθ / T, -ωmax, ωmax)
θ_next = limit(θ_anchor + ω · T)
```

`T` 是 `STEP_DURATION`，默认 `0.50` 秒。速度上限和 `serial_speed` 相同。`θ_anchor` 是这条队列里最后一个还没播完的点；队列空时就是上次发出去的角度。这样下一块接在上一块末尾，不会从实测角度另起一段。

然后把 `θ_anchor` 到 `θ_next` 按 `SERVO_HZ`（默认 100）线性插值。这些点交给 `joint_servo_control`：16 个关节名（14 个手臂 + 2 个夹爪），只填位置。`joint_velocities` 留空，接口目前不用它。`control_period` 默认 `0.012` 秒，比 100Hz 的周期略大。不打开 `enable_low_latency`。

播放线程大约每 0.01 秒发一个点。缓冲区里剩下的时间降到 `INFER_DELAY + PREFETCH_MARGIN` 时，主线程再去要下一块，播放不中断。下一块来晚了，就按同样的频率重复最后一个角度，把机器人留在原地。

要中途不空缓冲，一块的播放时间得长于推理时间：

```text
n × T > t
```

默认 `n = 4`，`T = 0.50` 秒，一块有 2 秒。默认 `t = 0.40` 秒，提前量 `0.05` 秒。第一块到来之前仍会停在当前姿态上等 `t` 秒，这是第一次推理的等待。

本地看播放、不连机器人。`visible_multi_joint.json` 有 6 步，默认 `MAX_STEPS` 只有 4，要改成 6 才播完夹爪：

```bash
MODE=async ACTIONS_FILE=deploy/examples/visible_multi_joint.json bash deploy/serve.sh
MODE=async MAX_STEPS=6 MOCK=1 bash deploy/client.sh
```

两边都要带 `MODE=async`，这样 A 才会等待 `INFER_DELAY`。结束时 B 打印 `servo`（真正播出去的点数）和 `hold`（缓冲区空着、重复最后一个点的次数）。`hold` 里包含第一块到来前的等待。中途如果 `hold` 还在涨，就是 `n × T` 不够盖住 `t`。

## 以后加模式

1. 在 `deploy/config/modes/` 增加一个 env 文件，文件名就是 `MODE` 的值。
2. 在 `deploy/g2/` 写这个模式怎么把归一化 \(\Delta\theta\) 变成关节指令。
3. 串行模式把名字加进 `deploy/g2/client_serial.py`。异步这一类单独写一个 `client_*.py`，并让 `deploy/client.sh` 在对应 `MODE` 下启动它。

没做第 3 步时，客户端会拒绝启动，不会悄悄退回 `serial`。
