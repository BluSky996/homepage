from __future__ import annotations

import html
import json
import re
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "datasets" / "environment.html"
ENVIRONMENT_DIR = ROOT / "datasets" / "environment"
DATA_DIR = ENVIRONMENT_DIR / "data"
REPORT_DIR = ENVIRONMENT_DIR / "reports"
MANIFEST = ENVIRONMENT_DIR / "records.json"
LIMIT = 5


def load_batches() -> list[dict[str, str | None]]:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    batches: list[dict[str, str | None]] = []
    used_data: set[str] = set()
    used_reports: set[str] = set()

    for item in manifest.get("experiments", []):
        csv_name = item.get("csv")
        report_name = item.get("report") or item.get("png")
        if csv_name and not (DATA_DIR / csv_name).is_file():
            csv_name = None
        if report_name and not (REPORT_DIR / report_name).is_file():
            report_name = None
        if not csv_name and not report_name:
            continue
        if csv_name:
            used_data.add(csv_name)
        if report_name:
            used_reports.add(report_name)
        batches.append(
            {
                "date": item["date"],
                "project": item.get("project", "ESP32 温度与光照环境监测实验"),
                "csv": csv_name,
                "report": report_name,
            }
        )

    # Unregistered files remain visible as incomplete batches until paired in records.json.
    for path in DATA_DIR.iterdir():
        if path.is_file() and path.suffix.lower() == ".csv" and path.name not in used_data:
            batches.append(
                {
                    "date": datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d"),
                    "project": "ESP32 温度与光照环境监测实验",
                    "csv": path.name,
                    "report": None,
                }
            )
    for path in REPORT_DIR.iterdir():
        if path.is_file() and path.suffix.lower() in {".png", ".pdf"} and path.name not in used_reports:
            batches.append(
                {
                    "date": datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d"),
                    "project": "ESP32 温度与光照环境监测实验",
                    "csv": None,
                    "report": path.name,
                }
            )

    return sorted(
        batches,
        key=lambda item: (str(item["date"]), str(item.get("csv") or item.get("report") or "")),
        reverse=True,
    )[:LIMIT]


def file_row(label: str, filename: str | None, kind: str) -> str:
    if not filename:
        return (
            '<div class="experiment-file-row missing">'
            f'<span class="experiment-file-label">{label}</span>'
            '<span class="experiment-file-name">暂未上传</span>'
            '</div>'
        )
    name = html.escape(filename)
    if kind == "data":
        action = f'<a class="record-action" href="environment/data/{name}" download>下载 CSV</a>'
    else:
        extension = Path(filename).suffix.upper().lstrip(".")
        action = (
            f'<a class="record-action" href="environment/reports/{name}" target="_blank" '
            f'rel="noreferrer">查看 {extension}</a>'
        )
    return (
        '<div class="experiment-file-row">'
        f'<span class="experiment-file-label">{label}</span>'
        f'<span class="experiment-file-name">{name}</span>'
        f'{action}'
        '</div>'
    )


def batch_rows(records: list[dict[str, str | None]]) -> str:
    if not records:
        return '<div class="archive-empty">暂无实验历史记录</div>'
    rows: list[str] = []
    for item in records:
        rows.append(
            '<article class="experiment-record">'
            '<div class="experiment-record-head">'
            f'<span class="archive-date">{html.escape(str(item["date"]))}</span>'
            f'<strong>{html.escape(str(item["project"]))}</strong>'
            '</div>'
            '<div class="experiment-files">'
            f'{file_row("原始数据", item.get("csv"), "data")}'
            f'{file_row("分析报告", item.get("report"), "reports")}'
            '</div>'
            '</article>'
        )
    return "\n".join(rows)


def replace_block(source: str, content: str) -> str:
    start = "<!-- EXPERIMENT_RECORDS_START -->"
    end = "<!-- EXPERIMENT_RECORDS_END -->"
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    updated, count = pattern.subn(f"{start}\n{content}\n{end}", source, count=1)
    if count != 1:
        raise RuntimeError(f"Cannot find unique experiment records block in {PAGE}")
    return updated


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    source = PAGE.read_text(encoding="utf-8")
    PAGE.write_text(replace_block(source, batch_rows(load_batches())), encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
