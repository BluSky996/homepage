from __future__ import annotations

import html
import json
import re
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "datasets" / "environment.html"
DATA_DIR = ROOT / "datasets" / "environment" / "data"
REPORT_DIR = ROOT / "datasets" / "environment" / "reports"
MANIFEST = ROOT / "datasets" / "environment" / "records.json"
LIMIT = 5

DATA_PATTERN = re.compile(r"^esp32_environment_(\d{8})\.csv$", re.IGNORECASE)
REPORT_PATTERN = re.compile(r"^environment_report_(\d{8})\.png$", re.IGNORECASE)


def dated_files(directory: Path, pattern: re.Pattern[str]) -> list[tuple[datetime, Path]]:
    records: list[tuple[datetime, Path]] = []
    for path in directory.iterdir():
        if not path.is_file():
            continue
        match = pattern.match(path.name)
        if not match:
            continue
        try:
            date = datetime.strptime(match.group(1), "%Y%m%d")
        except ValueError:
            continue
        records.append((date, path))
    return sorted(records, key=lambda item: (item[0], item[1].name), reverse=True)[:LIMIT]


def format_size(size: int) -> str:
    if size < 1024:
        return f"{size} B"
    if size < 1024 * 1024:
        return f"{size / 1024:.1f} KB"
    return f"{size / (1024 * 1024):.1f} MB"


def manifest_records(kind: str) -> list[tuple[datetime, Path, str]]:
    if not MANIFEST.exists():
        return []
    records = []
    for item in json.loads(MANIFEST.read_text(encoding="utf-8")).get("experiments", []):
        filename = item.get(kind)
        if not filename:
            continue
        directory = DATA_DIR if kind == "csv" else REPORT_DIR
        path = directory / filename
        if not path.is_file():
            continue
        date = datetime.strptime(item["date"], "%Y-%m-%d")
        title_key = "project" if kind == "csv" else "report"
        records.append((date, path, item[title_key]))
    return records


def latest_records(kind: str) -> list[tuple[datetime, Path, str]]:
    directory = DATA_DIR if kind == "csv" else REPORT_DIR
    pattern = DATA_PATTERN if kind == "csv" else REPORT_PATTERN
    default_title = "ESP32 环境采集数据" if kind == "csv" else "环境温度光照综合分析报告"
    combined = manifest_records(kind)
    known_paths = {path.resolve() for _, path, _ in combined}
    combined.extend(
        (date, path, default_title)
        for date, path in dated_files(directory, pattern)
        if path.resolve() not in known_paths
    )
    return sorted(combined, key=lambda item: (item[0], item[1].name), reverse=True)[:LIMIT]


def data_rows(records: list[tuple[datetime, Path, str]]) -> str:
    if not records:
        return '        <div class="archive-empty">暂无真实 CSV 数据记录</div>'
    rows = []
    for date, path, title in records:
        name = html.escape(path.name)
        rows.append(
            '        <div class="archive-row">'
            f'<span class="archive-date">{date:%Y-%m-%d}</span>'
            f'<span class="archive-title">{html.escape(title)}</span>'
            f'<span class="archive-file">{name}</span>'
            f'<span class="archive-size">{format_size(path.stat().st_size)}</span>'
            f'<a class="record-action" href="environment/data/{name}" download>下载 CSV</a>'
            '</div>'
        )
    return "\n".join(rows)


def report_rows(records: list[tuple[datetime, Path, str]]) -> str:
    if not records:
        return '        <div class="archive-empty">暂无真实 PNG 分析报告</div>'
    rows = []
    for date, path, title in records:
        name = html.escape(path.name)
        rows.append(
            '        <div class="archive-row">'
            f'<span class="archive-date">{date:%Y-%m-%d}</span>'
            f'<span class="archive-title">{html.escape(title)}</span>'
            f'<a class="record-action" href="environment/reports/{name}" target="_blank" rel="noreferrer">查看 PNG</a>'
            '</div>'
        )
    return "\n".join(rows)


def replace_block(source: str, marker: str, content: str) -> str:
    start = f"        <!-- {marker}_START -->"
    end = f"        <!-- {marker}_END -->"
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    replacement = f"{start}\n{content}\n{end}"
    updated, count = pattern.subn(replacement, source, count=1)
    if count != 1:
        raise RuntimeError(f"Cannot find unique {marker} block in {PAGE}")
    return updated


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    source = PAGE.read_text(encoding="utf-8")
    source = replace_block(source, "DATA_RECORDS", data_rows(latest_records("csv")))
    source = replace_block(source, "REPORT_RECORDS", report_rows(latest_records("png")))
    PAGE.write_text(source, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
