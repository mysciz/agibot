# 控制模式

端口 B 用 `MODE` 选择怎么把动作变成机器人指令。端口 A 不变，给出的仍是归一化 \(\Delta\theta\)。

```bash
bash deploy/serve.sh
MODE=serial bash deploy/client.sh
MODE=serial_speed bash deploy/client.sh
```

`MODE` 对应 `deploy/config/modes/` 里的一个文件。客户端目前只会真正跑下面两个。`smooth` 的配置文件先留着，选它会退出并提示还没实现。

| MODE | 状态 | 做法 |
|---|---|---|
| `serial` | 可用，默认 | 转角增量加到当前角度上，用固定速度走到那个角度 |
| `serial_speed` | 可用 | 转角增量先除以步长时间，得到关节速度，再乘回时间得到这一步的目标角度 |
| `smooth` | 未实现 | 预备给以后的轨迹平滑。现在不要用 |

两种可用模式都是串行的：`move_arm_joint` 返回之后才执行下一步。区别只在速度怎么来。

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

## 以后加模式

1. 在 `deploy/config/modes/` 增加一个 env 文件，文件名就是 `MODE` 的值。
2. 在 `deploy/g2/lib/` 写这个模式自己的 `execute_...`，输入仍是归一化 \(\Delta\theta\) 和当前关节角。
3. 把模式名加进 `deploy/g2/client_serial.py` 的 `IMPLEMENTED_MODES`，并在那里选中对应的执行函数。

没做第 3 步时，客户端会拒绝启动，不会悄悄退回 `serial`。
