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
  document.querySelectorAll('[data-entry]').forEach(button => button.addEventListener('click', () => {
    content.replaceChildren();
    const kind = button.dataset.entry;
    if (deliveries[kind]) {
      const [label, description, url] = deliveries[kind]; title.textContent = label;
      const p = document.createElement('p'); p.textContent = description; content.append(p);
      link('查看原有交付内容 ↗', url, true);
    } else if (kind === 'trade') {
      title.textContent = '选择尿素策略';
      link('尿素期货一号策略', '#strategy_01');
      link('尿素期货二号策略', '#strategy_02');
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
