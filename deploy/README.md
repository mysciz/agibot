# Agibot G2 部署

动作是关节增量 \(\Delta\theta\)。`"unit": "rad"` 写弧度，`"unit": "norm"` 写 0–1，`0.5` 表示不动。顺序是左臂 7、右臂 7、左右夹爪。模式见 [docs/mode.md](../docs/mode.md)，今晚的命令在 [scripts.txt](../scripts.txt)。

连机器人的终端先执行。`serve` 不用。

```bash
export LOCATOR_IP=10.42.1.102
export AORTA_DISCOVERY_URI=http://10.42.1.101:2379
export AORTA_DISPATCHER_THREAD_NUM=6
```

先开 A，再开 B。`MOCK=1` 不连机器人。`NO_MOVE=1` 只计算、不下发。

```bash
python deploy/examples/nudge_left_wrist.py
bash deploy/serve.sh
MODE=serial_speed bash deploy/client.sh
MODE=async bash deploy/serve.sh
MODE=async bash deploy/client.sh
```

`SAVE_DIR=deploy/records` 加在 A 上，每次观测存成 `0001/head.png`、`left_wrist.png`、`right_wrist.png` 和 `proprio.json`。这时 B 不要加 `NO_CAMERA=1`。
