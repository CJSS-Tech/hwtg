<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Telegram中文资源导航</title>
  <meta name="description" content="Telegram 中文资源导航：频道、群组、机器人、行业交流、海外商机、求职招聘、频道主专区等聚合入口。" />
  <meta name="keywords" content="Telegram, 中文, 频道, 群组, 机器人, 招聘, 行业交流群, 海外商机, SEO 导航" />
  <meta name="robots" content="index,follow" />
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 256 256'><circle cx='128' cy='128' r='120' fill='%230ea5e9'/><path d='M64 128l64 32 64-96' stroke='white' stroke-width='20' fill='none' stroke-linecap='round' stroke-linejoin='round'/></svg>">
  <!-- Tailwind via CDN （GitHub Pages 直接可用） -->
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    /* 简单的卡片 hover 与粘性目录 */
    .card { transition: transform .15s ease, box-shadow .15s ease; }
    .card:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(0,0,0,.08); }
    .sticky-nav { position: sticky; top: 0; z-index: 40; backdrop-filter: blur(8px); }
    .chip { border: 1px solid rgba(0,0,0,.08); border-radius: 9999px; padding: 4px 10px; }
  </style>
</head>
<body class="bg-slate-50 text-slate-800">
  <!-- 顶部导航 -->
  <header class="sticky-nav bg-white/80 border-b border-slate-200">
    <div class="max-w-7xl mx-auto px-4 py-3 flex items-center gap-4">
      <a href="#home" class="flex items-center gap-2 font-semibold">
        <span class="inline-block w-8 h-8 rounded-xl bg-sky-500"></span>
        Telegram中文资源导航
      </a>
      <nav class="ml-auto hidden md:flex gap-6 text-sm">
        <a href="#home" class="hover:text-sky-600">首页</a>
        <a href="#cn" class="hover:text-sky-600">中文频道</a>
        <a href="#jobs" class="hover:text-sky-600">求职招聘</a>
        <a href="#overseas" class="hover:text-sky-600">海外商机</a>
        <a href="#industry" class="hover:text-sky-600">行业交流群</a>
        <a href="#tools" class="hover:text-sky-600">工具&机器人</a>
        <a href="#owner" class="hover:text-sky-600">频道主专区</a>
      </nav>
    </div>
  </header>

  <!-- Hero & 搜索 -->
  <section id="home" class="max-w-7xl mx-auto px-4 pt-10 pb-6">
    <div class="grid md:grid-cols-2 gap-6">
      <div>
        <h1 class="text-2xl md:text-3xl font-bold leading-tight">发现与订阅优质 Telegram 中文资源</h1>
        <p class="mt-2 text-slate-600">频道 / 群组 / 机器人，一站式收录。支持搜索、分类筛选、排行榜、投稿与品牌合作入口。</p>
        <div class="mt-4 flex items-center gap-2">
          <input id="q" type="search" placeholder="搜索：频道名 / 简介 / @username / 标签"
                 class="w-full md:w-4/5 px-4 py-3 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-sky-500"/>
          <button id="goSearch" class="px-4 py-3 rounded-xl bg-sky-600 text-white">搜索</button>
        </div>
        <div id="hotKeywords" class="mt-3 flex flex-wrap gap-2 text-sm"></div>
        <div class="mt-4 flex gap-3 text-sm">
          <a href="#ads" class="chip hover:bg-slate-100">广告投放入口</a>
          <a href="#brand" class="chip hover:bg-slate-100">品牌&赞助入口</a>
        </div>
      </div>
      <div class="rounded-2xl bg-white border card p-5">
        <div class="h-40 md:h-48 rounded-xl bg-gradient-to-br from-sky-100 to-indigo-50 flex items-center justify-center text-slate-500">Banner（可替换为频道轮播）</div>
        <div class="mt-4">
          <h3 class="font-semibold">频道排行榜</h3>
          <ol id="topList" class="mt-2 list-decimal list-inside text-sm space-y-1 text-slate-700"></ol>
        </div>
      </div>
    </div>
  </section>

  <!-- 中文频道 -->
  <section id="cn" class="max-w-7xl mx-auto px-4 py-8">
    <div class="flex items-end justify-between">
      <h2 class="text-xl font-bold">中文频道</h2>
      <div class="text-sm text-slate-500">> 通过频道的昵称/简介/群组，增加入群提示与订阅按钮</div>
    </div>
    <div id="cnTabs" class="mt-4 flex flex-wrap gap-2 text-sm"></div>
    <div id="cnGrid" class="mt-4 grid sm:grid-cols-2 lg:grid-cols-3 gap-4"></div>
  </section>

  <!-- 求职招聘 -->
  <section id="jobs" class="max-w-7xl mx-auto px-4 py-8">
    <h2 class="text-xl font-bold">求职招聘</h2>
    <p class="text-slate-600 mt-1 text-sm">求职群 / 招聘群 / 猎头 / 区域招聘等</p>
    <div id="jobsGrid" class="mt-4 grid sm:grid-cols-2 lg:grid-cols-3 gap-4"></div>
  </section>

  <!-- 海外商机 -->
  <section id="overseas" class="max-w-7xl mx-auto px-4 py-8">
    <h2 class="text-xl font-bold">海外商机</h2>
    <div id="overseasGrid" class="mt-4 grid sm:grid-cols-2 lg:grid-cols-3 gap-4"></div>
  </section>

  <!-- 行业交流群 -->
  <section id="industry" class="max-w-7xl mx-auto px-4 py-8">
    <h2 class="text-xl font-bold">行业交流群</h2>
    <div id="industryGrid" class="mt-4 grid sm:grid-cols-2 lg:grid-cols-3 gap-4"></div>
  </section>

  <!-- 工具 & 机器人 -->
  <section id="tools" class="max-w-7xl mx-auto px-4 py-8">
    <h2 class="text-xl font-bold">工具 & 机器人</h2>
    <div id="toolsGrid" class="mt-4 grid sm:grid-cols-2 lg:grid-cols-3 gap-4"></div>
  </section>

  <!-- 频道主专区 -->
  <section id="owner" class="max-w-7xl mx-auto px-4 py-8">
    <h2 class="text-xl font-bold">频道主专区</h2>
    <div class="grid md:grid-cols-3 gap-4 mt-4">
      <a id="submit" class="card bg-white border rounded-2xl p-5" href="#" onclick="alert('请在 data.channels 中添加投稿机器人链接或表单地址'); return false;">
        <h3 class="font-semibold">投稿上榜</h3>
        <p class="text-sm text-slate-600 mt-1">提交优质频道/群/机器人，优先展示。</p>
      </a>
      <a id="toolkit" class="card bg-white border rounded-2xl p-5" href="#" onclick="alert('可替换为工具箱页面链接：封面制作、统计分析、互推工具等'); return false;">
        <h3 class="font-semibold">频道主工具箱</h3>
        <p class="text-sm text-slate-600 mt-1">封面模板、SEO清单、增长攻略、互推合作。</p>
      </a>
      <a id="seoGuide" class="card bg-white border rounded-2xl p-5" href="#" onclick="alert('可替换为 SEO 引流教程的单独页面链接'); return false;">
        <h3 class="font-semibold">SEO 引流教程</h3>
        <p class="text-sm text-slate-600 mt-1">如何被搜索收录、关键词矩阵、内容优化。</p>
      </a>
    </div>
  </section>

  <!-- 广告/品牌位占位 -->
  <section id="ads" class="max-w-7xl mx-auto px-4 py-8">
    <div class="grid md:grid-cols-2 gap-4">
      <div class="card bg-white border rounded-2xl p-5">
        <h3 class="font-semibold">广告投放入口</h3>
        <p class="text-sm text-slate-600 mt-1">支持 Banner、置顶推荐、榜单赞助、关键词联想等位。</p>
      </div>
      <div id="brand" class="card bg-white border rounded-2xl p-5">
        <h3 class="font-semibold">品牌&赞助入口</h3>
        <p class="text-sm text-slate-600 mt-1">长期合作、主题活动、榜单联合、渠道推广。</p>
      </div>
    </div>
  </section>

  <footer class="border-t border-slate-200 mt-8">
    <div class="max-w-7xl mx-auto px-4 py-8 text-sm text-slate-500">
      <div>© <span id="y"></span> Telegram中文资源导航 · 纯静态开源站点（GitHub Pages）</div>
      <div class="mt-1">数据以用户投稿与人工整理为主，若有侵权/违规请联系下架。</div>
    </div>
  </footer>

  <!-- 站点数据（示例，可自行增删改） -->
  <script>
    const channels = [
      // ==== 中文频道（示例）====
      {cat:'中文频道', sub:'吃瓜爆料', name:'东南亚大事件', user:'@asean_hot', desc:'东南亚热点/吃瓜/爆料/政策观察', score:96, tags:['时事','东南亚']},
      {cat:'中文频道', sub:'电影', name:'影迷观影室', user:'@cn_movie_room', desc:'新片预告、片单推荐与观影讨论', score:91, tags:['电影']},
      {cat:'中文频道', sub:'健身', name:'徒手健身营', user:'@calisthenics_cn', desc:'训练计划/打卡群/饮食建议', score:87, tags:['健身']},
      {cat:'中文频道', sub:'人物故事', name:'个人成长志', user:'@growth_daily_cn', desc:'见闻、复盘与人物专访', score:84, tags:['成长']},
      // ==== 求职招聘（示例）====
      {cat:'求职招聘', sub:'求职群', name:'找工作-互联网', user:'@job_seek_cn', desc:'简历互评/内推/面经', score:82, tags:['求职','互联网']},
      {cat:'求职招聘', sub:'招聘群', name:'招聘-跨境电商', user:'@hire_xborder', desc:'岗位发布/猎头合作', score:80, tags:['招聘','跨境']},
      {cat:'求职招聘', sub:'区域招聘群', name:'柬埔寨招聘', user:'@kh_jobs', desc:'金边/西港/暹粒岗位', score:79, region:'东南亚'},
      // ==== 海外商机（示例）====
      {cat:'海外商机', sub:'出海情报', name:'东南亚出海情报局', user:'@asean_go', desc:'市场信息/获客渠道/合规提醒', score:90, tags:['出海','东南亚']},
      // ==== 行业交流群（示例）====
      {cat:'行业交流群', sub:'跨境独立站', name:'跨境独立站卖家群', user:'@indie_seller_cn', desc:'建站/广告/支付/风控', score:85, tags:['跨境','独立站']},
      {cat:'行业交流群', sub:'AI/生产力', name:'AI 工具&工作流', user:'@dosai_lab', desc:'AI 工具链/自动化/工作流', score:88, tags:['AI','生产力']},
      // ==== 工具&机器人（示例）====
      {cat:'工具&机器人', sub:'搜索', name:'Seek 搜索机器人', user:'@seek_search_bot', desc:'搜索群/频道/帖子/机器人', score:93, tags:['机器人','搜索']},
      {cat:'工具&机器人', sub:'投稿', name:'投稿机器人', user:'@submit_nav_bot', desc:'提交频道/群/机器人以收录', score:89, tags:['投稿']},
    ];

    const hotKeywords = ['东南亚','AI 工具','跨境','招聘','电影','吃瓜'];

    // 顶部热词
    const hotEl = document.getElementById('hotKeywords');
    hotKeywords.forEach(k => {
      const a = document.createElement('a');
      a.className = 'chip hover:bg-slate-100';
      a.href = '#'; a.textContent = k;
      a.onclick = (e)=>{e.preventDefault(); document.getElementById('q').value=k; doSearch();};
      hotEl.appendChild(a);
    });

    // 排行榜（示例：score 排序 Top 8）
    const top = [...channels].sort((a,b)=>b.score-a.score).slice(0,8);
    const topList = document.getElementById('topList');
    top.forEach(x=>{
      const li=document.createElement('li');
      li.innerHTML = `<span class='font-medium'>${x.name}</span> <span class='text-slate-500'>${x.user}</span>`;
      topList.appendChild(li);
    });

    // 中文频道 Tab
    const cnSubs = [...new Set(channels.filter(c=>c.cat==='中文频道').map(c=>c.sub))];
    const cnTabs = document.getElementById('cnTabs');
    const cnGrid = document.getElementById('cnGrid');
    let currentCn = cnSubs[0] || '';

    function renderCnTabs(){
      cnTabs.innerHTML='';
      cnSubs.forEach(s=>{
        const b=document.createElement('button');
        b.className='chip hover:bg-slate-100 '+(s===currentCn?'bg-sky-50 border-sky-300 text-sky-700':'');
        b.textContent=s; b.onclick=()=>{currentCn=s; renderCnGrid(); renderCnTabs();};
        cnTabs.appendChild(b);
      });
    }

    function card(x){
      return `<div class='card bg-white border rounded-2xl p-4'>
        <div class='flex items-start justify-between'>
          <div>
            <h3 class='font-semibold'>${x.name}</h3>
            <div class='text-xs text-slate-500 mt-0.5'>${x.user || ''}</div>
          </div>
          <a class='text-sm text-white bg-sky-600 px-3 py-1 rounded-lg' target='_blank' rel='noopener' href='https://t.me/${(x.user||'').replace('@','')}'>点击订阅</a>
        </div>
        <p class='text-sm text-slate-600 mt-2'>${x.desc || ''}</p>
        <div class='mt-2 flex flex-wrap gap-2 text-xs'>${(x.tags||[]).map(t=>`<span class='chip'>#${t}</span>`).join('')}</div>
      </div>`
    }

    function renderCnGrid(){
      const list = channels.filter(c=>c.cat==='中文频道' && (currentCn?c.sub===currentCn:true));
      cnGrid.innerHTML = list.map(card).join('');
    }

    // 其他分类渲染
    function renderGrid(containerId, cat){
      const box = document.getElementById(containerId);
      box.innerHTML = channels.filter(c=>c.cat===cat).map(card).join('');
    }

    renderCnTabs();
    renderCnGrid();
    renderGrid('jobsGrid','求职招聘');
    renderGrid('overseasGrid','海外商机');
    renderGrid('industryGrid','行业交流群');
    renderGrid('toolsGrid','工具&机器人');

    // 搜索
    function doSearch(){
      const q = document.getElementById('q').value.trim().toLowerCase();
      if(!q){ renderCnGrid(); renderGrid('jobsGrid','求职招聘');renderGrid('overseasGrid','海外商机');renderGrid('industryGrid','行业交流群');renderGrid('toolsGrid','工具&机器人'); return; }
      const hit = channels.filter(x=>`${x.name} ${x.user||''} ${x.desc||''} ${(x.tags||[]).join(' ')}`.toLowerCase().includes(q));
      // 命中分桶展示：中文频道优先
      const cnHit = hit.filter(x=>x.cat==='中文频道');
      const other = hit.filter(x=>x.cat!=='中文频道');
      cnGrid.innerHTML = cnHit.map(card).join('') || `<div class='text-slate-500'>中文频道暂无匹配</div>`;
      const fill = (id,cat)=>{
        const arr = other.filter(x=>x.cat===cat);
        document.getElementById(id).innerHTML = arr.map(card).join('') || `<div class='text-slate-500'>暂无匹配</div>`;
      }
      fill('jobsGrid','求职招聘');
      fill('overseasGrid','海外商机');
      fill('industryGrid','行业交流群');
      fill('toolsGrid','工具&机器人');
    }

    document.getElementById('goSearch').onclick = doSearch;
    document.getElementById('q').addEventListener('keydown', (e)=>{ if(e.key==='Enter') doSearch(); });

    // 年份
    document.getElementById('y').textContent = new Date().getFullYear();
  </script>
</body>
</html>
