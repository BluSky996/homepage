# 金融市场实验数据目录

金融页面为每个策略展示最近 3 份交易 CSV 和最近 3 份分析报告。更早的文件继续保留在目录中，不会删除。

## 文件目录

- `data/strategy_01/`：尿素期货一号策略 CSV
- `data/strategy_02/`：尿素期货二号策略 CSV
- `reports/strategy_01/`：尿素期货一号策略 PNG/PDF 报告
- `reports/strategy_02/`：尿素期货二号策略 PNG/PDF 报告

文件名建议包含日期，例如：

- `urea_strategy_01_20260811.csv`
- `urea_strategy_02_2026-08-11.csv`
- `report_strategy_01_20260811.png`
- `report_strategy_02_20260811.pdf`

手动放入文件后，在项目根目录运行：

```powershell
python scripts/update_finance_records.py
```

脚本只更新网页列表，不删除任何历史文件，也不会自动上传 GitHub。
