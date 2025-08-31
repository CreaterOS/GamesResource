#!/usr/bin/env python3
import json
from pathlib import Path
from typing import List, Dict, Any

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "resource.json"

def load_game_cfg(game_dir: Path) -> Dict[str, str]:
    """读取单个游戏的 config.json；缺失字段用默认值填充。"""
    cfg_path = game_dir / "config.json"
    defaults = {
        "title": game_dir.name,
        "description": "(未找到描述)",
        "cover_image": "",
        "link": ""
    }
    if not cfg_path.is_file():
        return defaults
    try:
        with cfg_path.open(encoding="utf-8") as f:
            cfg = json.load(f)
    except Exception:
        cfg = {}
    # 只取需要的四个字段，其余忽略
    return {k: cfg.get(k, defaults[k]) for k in defaults}

def build_resource() -> List[Dict[str, Any]]:
    """构建最终 JSON 结构"""
    resource: List[Dict[str, Any]] = []
    # 动态一级目录并排序
    for cat in sorted(p.name for p in ROOT.iterdir() if p.is_dir()):
        cat_path = ROOT / cat
        items: List[Dict[str, str]] = []
        # 二级目录并排序
        for game_dir in sorted(cat_path.iterdir(), key=lambda p: p.name):
            if game_dir.is_dir():
                items.append(load_game_cfg(game_dir))
        resource.append({"name": cat, "items": items})
    return resource

if __name__ == "__main__":
    data = build_resource()
    with OUTPUT.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"✅ 已生成 {OUTPUT}")
