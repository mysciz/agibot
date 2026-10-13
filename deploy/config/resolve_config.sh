# 被 serve.sh / client.sh source。
# 命令行里已经 export 的变量优先于 env 文件。
resolve_config() {
  local here
  here="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
  local _inline
  # export -p 在函数里是 declare -x，eval 后会变成局部变量，函数返回就丢了。
  _inline="$(export -p | sed -E 's/^declare -x /export /')"

  set -a
  # shellcheck disable=SC1091
  source "${here}/config/common.env"
  eval "${_inline}"

  local mode="${MODE:-serial}"
  if [ ! -f "${here}/config/modes/${mode}.env" ]; then
    echo "未知 MODE: ${mode}（见 deploy/config/modes/）"
    exit 1
  fi
  # shellcheck disable=SC1091
  source "${here}/config/modes/${mode}.env"
  if [ -f "${here}/config/run.env" ]; then
    # shellcheck disable=SC1091
    source "${here}/config/run.env"
  fi
  eval "${_inline}"
  set +a

  export MODE_KEY="${MODE:-serial}"
  export REPO_ROOT="$(cd "${here}/.." && pwd)"

  if ! command -v "${PYTHON}" >/dev/null 2>&1; then
    if [ -x "${HOME}/miniconda3/bin/python" ]; then
      PYTHON="${HOME}/miniconda3/bin/python"
    elif command -v python3 >/dev/null 2>&1; then
      PYTHON=python3
    else
      echo "找不到 python。请先 conda activate base，或设置 PYTHON=/绝对路径/python"
      exit 1
    fi
  fi
  export PYTHON
}
