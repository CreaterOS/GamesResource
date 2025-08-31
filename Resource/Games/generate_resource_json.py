#!/usr/bin/env python3
import json
from pathlib import Path

root = Path(__file__).resolve().parent

# 动态获取一级目录并按字母序排序
categories = sorted([p.name for p in root.iterdir() if p.is_dir()])

# 组装结果
result = []
for cat in categories:
    subs = sorted([p.name for p in (root / cat).iterdir()
                   if p.is_dir()])  # 只取直接子目录
    result.append({cat: subs})

# 写出 JSON（紧凑，无多余空格）
with open("resource.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, separators=(",", ": "))

print("✅ resource.json 已生成")
