"""GDK 只初始化一次，供机器人和相机共用。"""

from __future__ import annotations

import os

_ready = False


def ensure_gdk():
    """导入并初始化 agibot_gdk。未配置发现服务时直接失败，避免误连 127.0.0.1:2379。"""
    global _ready
    if not os.environ.get("LOCATOR_IP") and not os.environ.get("AORTA_DISCOVERY_URI"):
        raise RuntimeError(
            "未设置 LOCATOR_IP 或 AORTA_DISCOVERY_URI。"
            "请先执行: "
            "export LOCATOR_IP=10.42.1.102 "
            "AORTA_DISCOVERY_URI=http://10.42.1.101:2379 "
            "AORTA_DISPATCHER_THREAD_NUM=6"
        )
    import agibot_gdk

    if not _ready:
        if agibot_gdk.gdk_init() != agibot_gdk.GDKRes.kSuccess:
            raise RuntimeError("GDK 初始化失败")
        _ready = True
    return agibot_gdk


def release_gdk() -> None:
    global _ready
    if not _ready:
        return
    import agibot_gdk

    agibot_gdk.gdk_release()
    _ready = False
