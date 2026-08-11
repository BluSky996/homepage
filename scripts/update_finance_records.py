from __future__ import annotations

import html
import re
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "datasets" / "finance" / "index.html"
FINANCE_DIR = ROOT / "datasets" / "finance"
LIMIT = 3
STRATEGIES = ("strategy_01", "strategy_02")
DATE_PATTERN = re.compile(
    r"(?<!\d)(20\d{2})[-_]?([01]\d)[-_]?([0-3]\d)(?:[-_]?([0-2]\d)([0-5]\d)([0-5]\d))?(?!\d)"
)


def file_date(path: Path) -> datetime:
    matches = list(DATE_PATTERN.finditer(path.stem))
    if matches:
        groups = matches[-1].groups(default="00")
        try:
            return datetime.strptime("".join(groups), "%Y%m%d%H%M%S")
        except ValueError:
            pass
    return datetime.fromtimestamp(path.stat().st_mtime)


def latest_files(directory: Path, suffixes: set[str]) -> list[tuple[datetime, Path]]:
    directory.mkdir(parents=True, exist_ok=True)
    records = [
        (file_date(path), path)
        for path in directory.iterdir()
        if path.is_file() and path.suffix.lower() in suffixes
    ]
    return sorted(records, key=lambda item: (item[0], item[1].name), reverse=True)[:LIMIT]


def rows(records: list[tuple[datetime, Path]], strategy: str, kind: str) -> str:
    if not records:
        label = "暂无真实 CSV 交易数据" if kind == "data" else "暂无真实分析报告"
        return f'<div class="history-empty">{label}</div>'

    rendered = []
    for date, path in records:
        name = html.escape(path.name)
        href = f"{kind}/{strategy}/{name}"
        if kind == "data":
            action = f'<a class="history-action" href="{href}" download>下载 CSV</a>'
        else:
            action = (
                f'<a class="history-action" href="{href}" target="_blank" '
                'rel="noreferrer">查看 / 下载</a>'
            )
        rendered.append(
            '<div class="history-row">'
            f'<span class="history-date">{date:%Y-%m-%d}</span>'
            f'<span class="history-file">{name}</span>'
            f'{action}'
            '</div>'
        )
    return "".join(rendered)


def replace_block(source: str, marker: str, content: str) -> str:
    start = f"<!-- {marker}_START -->"
    end = f"<!-- {marker}_END -->"
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    updated, count = pattern.subn(f"{start}{content}{end}", source, count=1)
    if count != 1:
        raise RuntimeError(f"Cannot find unique {marker} block in {PAGE}")
    return updated


def main() -> None:
    source = PAGE.read_text(encoding="utf-8")
    for strategy in STRATEGIES:
        data = latest_files(FINANCE_DIR / "data" / strategy, {".csv"})
        reports = latest_files(
            FINANCE_DIR / "reports" / strategy, {".png", ".pdf"}
        )
        prefix = strategy.upper()
        source = replace_block(source, f"{prefix}_DATA_RECORDS", rows(data, strategy, "data"))
        source = replace_block(
            source, f"{prefix}_REPORT_RECORDS", rows(reports, strategy, "reports")
        )
    PAGE.write_text(source, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
