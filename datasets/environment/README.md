# 气候环境实验文件

把真实实验文件放到以下目录，并严格使用规定文件名：

- CSV：`data/esp32_environment_YYYYMMDD.csv`
- PNG：`reports/environment_report_YYYYMMDD.png`

例如：

- `data/esp32_environment_20260815.csv`
- `reports/environment_report_20260815.png`

页面分别按日期从新到旧显示最近 5 个 CSV 和最近 5 个 PNG。较早文件仍保留在目录中，只是不显示在最近记录列表。

本地更新页面：

```powershell
python scripts/update_environment_records.py
```

文件推送到 GitHub 后，工作流也会自动运行并更新页面。
