#!/bin/bash
# 端口 A：模型侧。默认从文件读 Δθ，也可以 ACTION_SOURCE=stdin 从终端读。
#
#   bash deploy/serve.sh
#   ACTION_SOURCE=stdin bash deploy/serve.sh
#   ACTIONS_FILE=deploy/examples/joint0_wiggle.json bash deploy/serve.sh
set -eo pipefail
cd "$(dirname "$0")/.."
# shellcheck disable=SC1091
source deploy/config/resolve_config.sh
resolve_config
cd "${REPO_ROOT}"

ARGS=(
  --host "${MODEL_HOST}"
  --port "${MODEL_PORT}"
  --source "${ACTION_SOURCE}"
  --gripper "${GRIPPER}"
  --max-joint-step "${MAX_JOINT_STEP}"
  --max-gripper-step "${MAX_GRIPPER_STEP}"
)
if [ -n "${INFER_DELAY:-}" ]; then
  ARGS+=(--infer-delay "${INFER_DELAY}")
fi
if [ "${ACTION_SOURCE}" = "file" ]; then
  ARGS+=(--actions "${ACTIONS_FILE}")
fi
if [ -n "${SAVE_DIR:-}" ]; then
  ARGS+=(--save-dir "${SAVE_DIR}")
fi

echo "=== 端口 A  model:${MODEL_PORT}  source=${ACTION_SOURCE}  mode=${MODE_KEY}  python=${PYTHON} ==="
exec "${PYTHON}" -m deploy.g2.server "${ARGS[@]}"
