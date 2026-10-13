#!/bin/bash
# 端口 B：机器人侧。先确认端口 A 的 /health，再串行执行。
#
#   bash deploy/client.sh
#   MOCK=1 bash deploy/client.sh
#   NO_MOVE=1 bash deploy/client.sh
#   MAX_STEPS=4 OPEN_LOOP_HORIZON=2 bash deploy/client.sh
set -eo pipefail
cd "$(dirname "$0")/.."
# shellcheck disable=SC1091
source deploy/config/resolve_config.sh
resolve_config
cd "${REPO_ROOT}"

if ! curl -sf --max-time 5 "${MODEL_URL}/health" >/dev/null; then
  echo "端口 A 不可达: ${MODEL_URL}/health"
  echo "先在另一个终端运行: bash deploy/serve.sh"
  exit 1
fi

ARGS=(
  --model-url "${MODEL_URL}"
  --host "${ROBOT_HOST}"
  --port "${ROBOT_PORT}"
  --max-steps "${MAX_STEPS}"
  --open-loop-horizon "${OPEN_LOOP_HORIZON}"
  --gripper "${GRIPPER}"
  --max-joint-step "${MAX_JOINT_STEP}"
  --max-gripper-step "${MAX_GRIPPER_STEP}"
  --limit-margin "${LIMIT_MARGIN}"
  --joint-velocity "${JOINT_VELOCITY}"
  --verbose
)
if [ "${MOCK}" = "1" ] || [ "${MOCK}" = "true" ]; then
  ARGS+=(--mock)
fi
if [ "${NO_MOVE}" = "1" ] || [ "${NO_MOVE}" = "true" ]; then
  ARGS+=(--no-move)
fi
if [ "${NO_CAMERA}" = "1" ] || [ "${NO_CAMERA}" = "true" ]; then
  ARGS+=(--no-camera)
fi

echo "=== 端口 B  robot:${ROBOT_PORT}  model=${MODEL_URL}  mode=${MODE_KEY}  python=${PYTHON} ==="
exec "${PYTHON}" -m deploy.g2.client_serial "${ARGS[@]}"
