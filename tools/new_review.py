#!/usr/bin/env python3
"""Create a dated retrospective note without overwriting existing work."""

from __future__ import annotations

import argparse
from datetime import date, datetime
from pathlib import Path


def parse_date(value: str) -> date:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise argparse.ArgumentTypeError("日期格式应为 YYYY-MM-DD") from exc


def main() -> int:
    parser = argparse.ArgumentParser(description="创建一份带日期的复盘记录")
    parser.add_argument(
        "--date",
        type=parse_date,
        default=date.today(),
        help="复盘日期，格式 YYYY-MM-DD；默认使用本机日期",
    )
    args = parser.parse_args()

    repository_root = Path(__file__).resolve().parent.parent
    template_path = Path(__file__).resolve().parent / "review-template.md"
    target = (
        repository_root
        / "reviews"
        / str(args.date.year)
        / f"{args.date.isoformat()}-review.md"
    )
    content = template_path.read_text(encoding="utf-8").replace(
        "{{DATE}}", args.date.isoformat()
    )
    target.parent.mkdir(parents=True, exist_ok=True)

    try:
        with target.open("x", encoding="utf-8") as review_file:
            review_file.write(content)
    except FileExistsError:
        parser.error(f"目标文件已存在，不会覆盖：{target.relative_to(repository_root)}")

    print(f"已创建：{target.relative_to(repository_root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
