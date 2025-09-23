#!/usr/bin/env python3
import json
from pathlib import Path
from typing import List, Dict, Any
import re

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "resource.json"

def load_game_cfg(game_dir: Path) -> Dict[str, str]:
    """读取单个游戏的 config.json；缺失字段用默认值填充。"""
    cfg_path = game_dir / "config.json"
    defaults = {
        "title": game_dir.name,
        "rating": "",
        "released": "",
        "description": "",
        "cover_image": "",
        "thumbnail_cover_image": "",
        "url": "",
        "link": "",
        "rotation_required": False
    }
    if not cfg_path.is_file():
        # 目录名也做首字母大写
        defaults["title"] = defaults["title"][:1].upper() + defaults["title"][1:]
        return defaults

    try:
        with cfg_path.open(encoding="utf-8") as f:
            cfg = json.load(f)
    except Exception:
        cfg = {}

    # 合并配置，并把 title 首字母大写
    merged = {k: cfg.get(k, defaults[k]) for k in defaults}
    merged["title"] = merged["title"][:1].upper() + merged["title"][1:]
    merged["link"] = merged["link"].replace("&skipPrerollFirstSession=true&", "&")
    merged["link"] = merged["link"].replace("v=1.340", "v=1.339")
    merged["thumbnail_cover_image"] = merged["cover_image"]
    merged["thumbnail_cover_image"] = re.sub(
        r'\bwidth=1200&height=630\b', 'width=240&height=126',
        merged["thumbnail_cover_image"]
    )
    
    return merged
    
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
