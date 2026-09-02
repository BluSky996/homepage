# AI Data Lab 网站建设与恢复手册

## 一、项目基本信息

- 本地仓库路径：`D:\AI-Data-Lab\homepage`
- GitHub 仓库：`BluSky996/homepage`
- 公网域名：<https://ai-data-lab.com/>
- 部署方式：GitHub Pages
- 常规上线流程：本地修改 → `git commit` → `git push origin main` → GitHub Pages 自动部署
- 重要原则：上线前必须本地预览，每个被修改页面都要截图确认。

当前 HEAD：`2ea710dbf0e38164e17a214e9faf65558b209a46`（`Restore derivatives page layout`）。该提交是当前衍生品页面的稳定恢复点。执行任何恢复命令前，仍需用 `git show` 检查目标提交中的文件内容。

## 二、当前网站主要页面清单

### 1. 首页

- 文件：`index.html`
- 用途：AI Data Lab 首页。
- 主要模块：数据资源、AI 应用项目、数据清洗整理等。

### 2. AI 商品调研智能体

- 文件：`product-intelligence.html`
- 报告页：`product-intelligence-report.html`
- 用途：商品搜索、市场评价、证据整理与报告展示。
- 维护要求：不要修改 API 地址，不要随意调整后端链路；修改前先核对现有配置和调用逻辑。

### 3. AI 儿童陪伴桌面机器人

- 文件：`ai-companion-toy.html`
- 用途：产品介绍与互动展示。
- 素材目录：`assets/images/ai-companion-toy/`

### 4. 金融数据应用首页

- 文件：`datasets/finance/index.html`
- 用途：金融数据应用入口。
- 当前结构：风险的释放、转移与管理；交易市场结构；大陆金融交易；跨境金融交易。

### 5. 衍生品页面

- 文件：`datasets/finance/derivatives.html`
- 用途：大陆金融交易中的商品期货与股指期权页面。
- 当前稳定提交：`2ea710dbf0e38164e17a214e9faf65558b209a46`
- 当前结构：
  - 商品期货
  - 策略项目与历史数据
  - 尿素期货 一号策略
  - 尿素期货 二号策略
  - 股指期权专题建设中
- 重要说明：这是修复恢复后的稳定版页面。页面曾因编码和标签损坏出现中文乱码、CSS 外露及 HTML 解析异常。恢复时应优先检查并使用上述稳定提交，不要重新设计。

### 6. A股股票与债券基金分红记录入口

- 文件：`datasets/finance/a-share-dividends.html`
- 用途：贵州茅台、海天味业股票分红记录以及债券基金净值与分红记录的入口。

### 7. 贵州茅台分红页面

- 文件：`datasets/finance/moutai-dividends.html`
- 用途：贵州茅台历史分红记录与 10 万元示范测算。

### 8. 海天味业分红页面

- 文件：`datasets/finance/haitian-dividends.html`
- 用途：海天味业历史分红记录与 10 万元示范测算。

### 9. 易方达债券基金页面

- 文件：`datasets/finance/bond-fund-yifangda.html`
- 用途：债券基金净值、现金分红与持有收益测算。
- 公开规则：页面不显示具体基金代码和完整基金名称。
- 数据规则：页面使用匿名后的 full 净值和分红数据；不得改用 sample 或 latest-sample 文件。

## 三、金融数据文件夹规则

### 1. 商品期货策略数据

- 一号策略数据：`datasets/finance/data/strategy_01/`
- 一号策略报告：`datasets/finance/reports/strategy_01/`
- 二号策略数据：`datasets/finance/data/strategy_02/`
- 二号策略报告：`datasets/finance/reports/strategy_02/`

`datasets/finance/derivatives.html` 当前直接在 HTML 中写入以下静态链接，没有自动扫描文件夹的脚本：

1. `data/strategy_01/尿素套利_202312-202608_交易明细.csv`
2. `reports/strategy_01/尿素套利_近两年交易记录_分析汇总.pdf`
3. `data/strategy_01/尿素套利_202311-202401_交易明细.csv`
4. `reports/strategy_01/尿素套利_交易记录_3个月_分析汇总.pdf`
5. `data/strategy_02/期货账户_202510-202608_平仓记录_交易明细.csv`
6. `reports/strategy_02/期货账户_平仓记录_分析汇总.pdf`

当前为静态链接展示。添加或重命名 CSV/PDF 后，必须同步修改页面中的文件名、`href` 和显示文字，并逐个点击验证。

### 2. 股票分红数据

目录：`datasets/finance/data/dividends/`

- `600519-kweichow-moutai-dividends.csv`
- `600519-dividend-visualization.json`
- `603288-haitian-flavouring-dividends.csv`
- `603288-dividend-visualization.json`
- `a-share-dividend-records_600519_603288.csv`

这些文件用于贵州茅台、海天味业的历史分红记录和 10 万元示范测算。更新数据时应保留既有字段、日期和记录顺序，并同步核验页面内嵌数据或读取逻辑。

### 3. 债券基金数据

目录：`datasets/finance/data/dividends/`

- `yifangda-bond-fund-nav-full.csv`
- `yifangda-bond-fund-nav-full.json`
- `yifangda-bond-fund-dividends.json`
- `yifangda-bond-fund-annual-dividends.json`
- `yifangda-bond-fund-nav-validation.json`

当前校验信息：

- full 净值记录数：5,111 条
- 最早净值日期：2005-09-19
- 最新净值日期：2026-09-01
- 分红明细：42 条
- 页面不得读取 sample 或 latest-sample 文件。
- 公开页面不得显示具体基金代码和完整基金名称。
- `bond-fund-yifangda.html` 当前包含用于静态 `file://` 预览的内嵌数据，并记录匿名 full 文件来源。更新 full 文件时，必须同步刷新并核对页面实际参与计算的数据数组，不能只替换外部文件。

## 四、每个页面的恢复方法

### 1. 恢复 `derivatives.html`

稳定恢复点：`2ea710dbf0e38164e17a214e9faf65558b209a46`。

先检查历史和目标内容：

```bash
git log --oneline -- datasets/finance/derivatives.html
git show 2ea710dbf0e38164e17a214e9faf65558b209a46:datasets/finance/derivatives.html
git diff 2ea710dbf0e38164e17a214e9faf65558b209a46 -- datasets/finance/derivatives.html
```

确认提交正确且当前工作区没有需要保留的同文件修改后，才可执行：

```bash
git checkout 2ea710dbf0e38164e17a214e9faf65558b209a46 -- datasets/finance/derivatives.html
```

注意事项：

- 执行 checkout 前必须确认 commit 和文件内容正确。
- 不要用 PowerShell `Set-Content` 大段重写中文 HTML。
- 不要从乱码页面复制正文或标签。
- 恢复后本地打开 `D:\AI-Data-Lab\homepage\datasets\finance\derivatives.html`。
- 检查深色样式、中文、两个尿素策略、股指期权模块、原始文件名和 6 个 CSV/PDF 链接。
- 检查页面正文没有 CSS 源码或 HTML 标签文本。

`datasets/finance/derivatives-recovered-preview.html` 是本地恢复参考文件，不应提交到公网；长期恢复应以经过确认的 Git commit 或 tag 为准。

### 2. 恢复债券基金页面

- `bond-fund-yifangda.html` 的测算数据必须来自 `yifangda-bond-fund-nav-full.json` 对应的完整记录。
- 不得读取或复制 sample、latest-sample 数据参与正式测算。
- 年份选项必须从完整 full 净值数据自动生成。
- 结束年份不得选择尚未完整结束的 2026 年；当前默认完整结束年份为 2025。
- 净值变化收益使用单位净值；现金分红收益使用完整分红明细，不能用累计净值再重复叠加分红。
- 本地检查以下关键词，公开页中均不应出现：

```text
sample
latest-sample
110008
易方达稳健收益债券B
```

- 同时核对页面实际计算数组为 5,111 条，范围为 2005-09-19 至 2026-09-01；分红明细为 42 条。

### 3. 恢复 A股分红页面

- `moutai-dividends.html` 使用贵州茅台分红数据。
- `haitian-dividends.html` 使用海天味业分红数据。
- 两页的 10 万元示范测算仅用于数据观察，不构成投资建议。
- 恢复后检查默认参考买入价、估算持股数、年度柱状图、最近年度估算分红及分红率的联动。
- 不要把不同年份的历史累计分红误写成当前买入可获得的收益。

## 五、上线前检查清单

每次 push 前必须检查：

- [ ] 本地打开所有本次修改过的页面
- [ ] 为每个被修改页面保存截图并人工确认
- [ ] 页面没有白底源码
- [ ] 页面没有 CSS 外露
- [ ] 中文没有乱码
- [ ] 链接能正常点击
- [ ] 数据文件路径正确
- [ ] 不应公开的信息没有出现
- [ ] `git status --short` 检查只提交目标文件
- [ ] `git diff --cached --check` 无输出
- [ ] 不提交临时 preview 文件
- [ ] 不提交 `.bak`
- [ ] 不提交 `__pycache__`
- [ ] 不提交临时截图
- [ ] commit 后再 push
- [ ] push 后等待 GitHub Actions / Pages 绿色对勾
- [ ] 公网页面使用 Ctrl+F5 强制刷新确认

当前工作区检查时还应特别留意 `derivatives-recovered-preview.html`、`product-intelligence.html.bak.fc`、`tests/__pycache__/` 和临时截图文件，除非有明确发布需求，否则不要纳入提交。

## 六、禁止事项

- 不要用 PowerShell `Set-Content` 大段重写中文 HTML。
- 不要没有本地预览就 push。
- 不要一次混合提交多个无关页面。
- 不要把 sample 数据当 full 数据使用。
- 不要把临时 preview 文件提交到公网。
- 不要把产品页、金融页和 API 页面混在一起修改。
- 不要修改 `product-intelligence` 的 API 地址或后端链路。
- 不要删除历史数据链接。
- 不要写投资建议、推荐买入、稳赚、保本或“带你赚钱”。

## 七、推荐的 Git 备份策略

1. 每个稳定页面单独 commit，commit 前只暂存目标文件。
2. 每次重要上线后可以创建带日期的稳定 tag。
3. 金融页面稳定版建议 tag：`finance-pages-stable-2026-09-02`。
4. 衍生品页面稳定版建议 tag：`derivatives-layout-stable-2026-09-02`。
5. 页面损坏时，先检查 tag 中的文件，再恢复单个文件。

示例命令如下，仅供以后确认稳定版本后执行，本次不要执行：

```bash
git tag derivatives-layout-stable-2026-09-02
git push origin derivatives-layout-stable-2026-09-02
```

从 tag 检查或恢复单个页面的示例：

```bash
git show derivatives-layout-stable-2026-09-02:datasets/finance/derivatives.html
git checkout derivatives-layout-stable-2026-09-02 -- datasets/finance/derivatives.html
```

## 八、短视频和广告页面对应关系

- 尿素期货广告 → `datasets/finance/derivatives.html`
- 股票分红广告 → `datasets/finance/a-share-dividends.html`
- 债券基金广告 → `datasets/finance/bond-fund-yifangda.html`
- AI 玩具广告 → `ai-companion-toy.html`

每条广告只讲一个页面，不要把多个产品或数据方向混在同一条内容中。
