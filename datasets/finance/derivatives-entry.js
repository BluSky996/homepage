(() => {
  const dialog = document.getElementById('entry-dialog');
  const title = document.getElementById('entry-dialog-title');
  const content = document.getElementById('entry-dialog-content');
  // Existing delivery-standard entries in secondary-market.html.
  const deliveries = {
    review: ['策略复盘交付', '交易假设记录、执行过程整理、结果复盘、风险暴露与改进建议。', 'https://mp.weixin.qq.com/s/cb6V9e8wtjN-ihl_u6Exgw'],
    research: ['策略研究交付', '市场数据整理、交易品种分类、指标口径说明、策略逻辑梳理。', 'https://mp.weixin.qq.com/s/SZyELC7CsAEb3FK8uaNJow']
  };
  function link(label, href, external = false) {
    const a = document.createElement('a'); a.textContent = label; a.href = href;
    if (external) { a.target = '_blank'; a.rel = 'noopener noreferrer'; }
    content.append(a);
  }
  // 查询业绩：两个尿素策略的资料索引。文件与链接全部沿用页面已有内容，未新增任何文件。
  const strategyLookup = [
    {
      title: '尿素期货 一号策略',
      product: '云财富期货有限公司',
      batches: [
        {
          date: '2026-08-12', name: '尿素套利近两年交易记录',
          csv: 'data/strategy_01/尿素套利_202312-202608_交易明细.csv',
          pdf: 'reports/strategy_01/尿素套利_近两年交易记录_分析汇总.pdf'
        },
        {
          date: '2026-08-11', name: '尿素套利三个月交易记录',
          csv: 'data/strategy_01/尿素套利_202311-202401_交易明细.csv',
          pdf: 'reports/strategy_01/尿素套利_交易记录_3个月_分析汇总.pdf'
        }
      ]
    },
    {
      title: '尿素期货 二号策略',
      product: '新世纪期货有限公司',
      batches: [
        {
          date: '2026-08-12', name: '期货账户平仓记录',
          csv: 'data/strategy_02/期货账户_202510-202608_平仓记录_交易明细.csv',
          pdf: 'reports/strategy_02/期货账户_平仓记录_分析汇总.pdf'
        }
      ]
    }
  ];
  const escapeHtml = value => String(value).replace(/[&<>"]/g, ch => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[ch]));
  function renderStrategyLookup() {
    const cards = strategyLookup.map(strategy => {
      const rows = strategy.batches.map(batch => {
        const csvName = escapeHtml(batch.csv.split('/').pop());
        const pdfName = escapeHtml(batch.pdf.split('/').pop());
        return '<div class="lookup-row">'
          + '<div class="lookup-row-head"><span class="history-date">' + escapeHtml(batch.date) + '</span><strong>' + escapeHtml(batch.name) + '</strong></div>'
          + '<div class="lookup-files">'
          + '<div class="lookup-file"><span class="lookup-file-label">交易数据</span><span class="lookup-file-name" title="' + csvName + '">' + csvName + '</span><a href="' + escapeHtml(batch.csv) + '" download>下载 CSV</a></div>'
          + '<div class="lookup-file"><span class="lookup-file-label">分析报告</span><span class="lookup-file-name" title="' + pdfName + '">' + pdfName + '</span><a href="' + escapeHtml(batch.pdf) + '" target="_blank" rel="noreferrer">查看 / 下载</a></div>'
          + '</div></div>';
      }).join('');
      return '<section class="lookup-card">'
        + '<h3>' + escapeHtml(strategy.title) + '</h3>'
        + '<dl class="lookup-meta"><dt>运行产品</dt><dd>' + escapeHtml(strategy.product) + '</dd>'
        + '<dt>交易品种</dt><dd>尿素期货</dd>'
        + '<dt>数据内容</dt><dd>开仓记录 / 平仓记录 / 盈亏数据 / 持仓变化 / 策略执行记录</dd></dl>'
        + rows + '</section>';
    }).join('');
    content.innerHTML = '<p class="lookup-lead">展示最近策略记录与可下载资料，页面仅作为研究资料索引。</p>' + cards;
  }
  document.querySelectorAll('[data-entry]').forEach(button => button.addEventListener('click', () => {
    content.replaceChildren();
    const kind = button.dataset.entry;
    if (deliveries[kind]) {
      const [label, description, url] = deliveries[kind]; title.textContent = label;
      const p = document.createElement('p'); p.textContent = description; content.append(p);
    } else if (kind === 'trade') {
      title.textContent = '尿素期货策略业绩查询';
      renderStrategyLookup();
    } else { title.textContent = '正在建设中'; }
    dialog.showModal();
  }));
  dialog.querySelector('.dialog-close').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => { if (event.target === dialog) { const r = dialog.getBoundingClientRect(); if (event.clientX < r.left || event.clientX > r.right || event.clientY < r.top || event.clientY > r.bottom) dialog.close(); } });
  function route() {
    const key = location.hash.slice(1);
    const strategy = ['strategy_01', 'strategy_02'].includes(key) ? document.querySelector(`[data-strategy="${key}"]`) : null;
    const legacy = ['commodity-title', 'option-title', 'urea-strategies', 'option-strategies'].includes(key);
    document.body.classList.toggle('strategy-detail', Boolean(strategy || legacy));
    document.querySelector('.strategy-return').hidden = !(strategy || legacy);
    if (dialog.open) dialog.close();
    if (strategy) {
      const panel = strategy.closest('.strategy-content');
      panel.classList.add('open'); panel.setAttribute('aria-hidden', 'false');
      const toggle = document.querySelector(`[data-target="${panel.id}"]`);
      toggle.setAttribute('aria-expanded', 'true'); toggle.setAttribute('aria-label', '收起套利策略项目'); toggle.querySelector('span').textContent = '−';
      requestAnimationFrame(() => strategy.closest('.strategy-card').scrollIntoView({block:'start'}));
    }
  }
  window.addEventListener('hashchange', route); route();
})();
