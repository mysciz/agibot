# Agibot G2 部署

动作是归一化的关节增量 \(\Delta\theta\)，每个数在 \([0, 1]\)，`0.5` 表示不动。左臂 7 关节、右臂 7 关节、左右夹爪。

## 先测能不能转关节

急停放在手边。下面两个脚本只动一侧手腕末关节 `0.05` rad（约 3°），然后转回。

```bash
export LOCATOR_IP=10.42.1.102
export AORTA_DISCOVERY_URI=http://10.42.1.101:2379
export AORTA_DISPATCHER_THREAD_NUM=6

python deploy/examples/nudge_left_wrist.py
python deploy/examples/nudge_right_wrist.py
```

幅度用 `--delta 0.03` 改，绝对值不超过 `0.15` rad。

## 串行闭环

端口 A（8800）给出动作，端口 B（8801）读机器人、POST 观测、GET 动作并执行。

```bash
bash deploy/serve.sh
MOCK=1 bash deploy/client.sh
```

连上机器人后先看指令、再真的动：

```bash
NO_MOVE=1 NO_CAMERA=1 bash deploy/client.sh
NO_CAMERA=1 bash deploy/client.sh
```

动作文件是 `deploy/examples/joint0_wiggle.json`。改从终端输入：`ACTION_SOURCE=stdin bash deploy/serve.sh`，一行 16 个弧度增量，或 `hold` / `quit`。
