from __future__ import annotations

import html
import json
import re
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "datasets" / "finance" / "index.html"
FINANCE_DIR = ROOT / "datasets" / "finance"
MANIFEST = FINANCE_DIR / "records.json"
LIMIT = 3
STRATEGIES = ("strategy_01", "strategy_02")


def load_batches(strategy: str) -> list[dict[str, str | None]]:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    batches: list[dict[str, str | None]] = []
    used_data: set[str] = set()
    used_reports: set[str] = set()

    for item in manifest.get("strategies", {}).get(strategy, []):
        csv_name = item.get("csv")
        report_name = item.get("report")
        csv_path = FINANCE_DIR / "data" / strategy / csv_name if csv_name else None
        report_path = FINANCE_DIR / "reports" / strategy / report_name if report_name else None

        if csv_path and not csv_path.is_file():
            csv_name = None
        if report_path and not report_path.is_file():
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
                "title": item.get("title", "本次交易记录"),
                "csv": csv_name,
                "report": report_name,
            }
        )

    # Files not yet listed in the manifest remain visible as incomplete batches.
    data_dir = FINANCE_DIR / "data" / strategy
    report_dir = FINANCE_DIR / "reports" / strategy
    for path in data_dir.iterdir():
        if path.is_file() and path.suffix.lower() == ".csv" and path.name not in used_data:
            batches.append(
                {
                    "date": datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d"),
                    "title": "本次交易记录",
                    "csv": path.name,
                    "report": None,
                }
            )
    for path in report_dir.iterdir():
        if path.is_file() and path.suffix.lower() in {".pdf", ".png"} and path.name not in used_reports:
            batches.append(
                {
                    "date": datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d"),
                    "title": "本次交易记录",
                    "csv": None,
                    "report": path.name,
                }
            )

    return sorted(
        batches,
        key=lambda item: (str(item["date"]), str(item.get("csv") or item.get("report") or "")),
        reverse=True,
    )[:LIMIT]


def file_row(label: str, filename: str | None, strategy: str, kind: str) -> str:
    if not filename:
        return (
            '<div class="batch-file-row missing">'
            f'<span class="batch-file-label">{label}</span>'
            '<span class="batch-file-name">暂未上传</span>'
            '</div>'
        )

    name = html.escape(filename)
    href = f"{kind}/{strategy}/{name}"
    if kind == "data":
        action = f'<a class="history-action" href="{href}" download>下载 CSV</a>'
    else:
        action = (
            f'<a class="history-action" href="{href}" target="_blank" '
            'rel="noreferrer">查看 / 下载</a>'
        )
    return (
        '<div class="batch-file-row">'
        f'<span class="batch-file-label">{label}</span>'
        f'<span class="batch-file-name">{name}</span>'
        f'{action}'
        '</div>'
    )


def batch_rows(records: list[dict[str, str | None]], strategy: str) -> str:
    if not records:
        return '<div class="history-empty">暂无历史交易记录</div>'

    rendered: list[str] = []
    for item in records:
        rendered.append(
            '<article class="batch-card">'
            '<div class="batch-head">'
            f'<span class="history-date">{html.escape(str(item["date"]))}</span>'
            f'<strong>{html.escape(str(item["title"]))}</strong>'
            '</div>'
            '<div class="batch-files">'
            f'{file_row("交易数据", item.get("csv"), strategy, "data")}'
            f'{file_row("分析报告", item.get("report"), strategy, "reports")}'
            '</div>'
            '</article>'
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
        source = replace_block(
            source,
            f"{strategy.upper()}_BATCH_RECORDS",
            batch_rows(load_batches(strategy), strategy),
        )
    PAGE.write_text(source, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
