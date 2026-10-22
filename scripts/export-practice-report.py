#!/usr/bin/env python3
"""Convert a practice-record JSON file into a readable Markdown report.

Usage:
  python export-practice-report.py records.json report.md

Expected input: either a list of record objects or {"records": [...]}.
"""
import json
import sys
from pathlib import Path


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: export-practice-report.py records.json report.md")
    source, target = map(Path, sys.argv[1:])
    data = json.loads(source.read_text(encoding="utf-8"))
    records = data.get("records", data) if isinstance(data, dict) else data
    if not isinstance(records, list):
        raise SystemExit("records.json must contain a list or a records list")

    lines = ["# 面试练习报告", ""]
    for i, record in enumerate(records, 1):
        if not isinstance(record, dict):
            continue
        lines += [f"## 练习 {i}", ""]
        for key, label in [
            ("stage", "阶段"), ("question", "题目"), ("framework", "框架"),
            ("good", "做得好的地方"), ("blocker", "最主要的卡点"),
            ("next_action", "下一轮修改动作"), ("self_check", "用户自查"),
        ]:
            value = record.get(key, "")
            if value:
                lines += [f"**{label}**：{value}", ""]
        answer = record.get("answer", "")
        if answer:
            lines += ["**用户回答**", "", answer, ""]
    target.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
