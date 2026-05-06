import json

with open('data_charts.json', encoding='utf-8') as f:
    D = json.load(f)

DATA_JS = json.dumps(D, ensure_ascii=False)

HTML = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Estudo de Raio — Dashboard Animado</title>
<script src="https://cdn.plot.ly/plotly-2.32.0.min.js"></script>
<style>
:root{--bg:#0f0f1a;--surface:#1a1a2e;--surface2:#16213e;--border:rgba(255,255,255,.07);--text:#e2e8f0;--muted:#94a3b8;--accent:#6366f1}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--text);font-family:'Segoe UI',system-ui,sans-serif;min-height:100vh;overflow-x:hidden}

#particles{position:fixed;inset:0;pointer-events:none;z-index:0;overflow:hidden}
.particle{position:absolute;border-radius:50%;background:radial-gradient(circle,rgba(99,102,241,.3),transparent 70%);animation:float linear infinite}
@keyframes float{0%{transform:translateY(110vh) scale(0);opacity:0}10%{opacity:.5}90%{opacity:.2}100%{transform:translateY(-10vh) scale(1);opacity:0}}

header{position:relative;z-index:10;background:linear-gradient(135deg,#1e1b4b 0%,#312e81 50%,#1e3a5f 100%);padding:44px 60px 56px;text-align:center;overflow:hidden}
header::after{content:'';position:absolute;bottom:-2px;left:0;right:0;height:3px;background:linear-gradient(90deg,#6366f1,#ec4899,#10b981,#f59e0b,#6366f1);background-size:200%;animation:rainbow 4s linear infinite}
@keyframes rainbow{0%{background-position:0%}100%{background-position:200%}}
header h1{font-size:clamp(20px,4vw,34px);font-weight:800;background:linear-gradient(135deg,#a5b4fc,#f9a8d4,#6ee7b7);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;animation:fadeDown .8s ease forwards;opacity:0;transform:translateY(-20px)}
header p{color:#a5b4fc;font-size:14px;margin-top:10px;animation:fadeDown .8s .2s ease forwards;opacity:0;transform:translateY(-10px)}
@keyframes fadeDown{to{opacity:1;transform:translateY(0)}}

nav{position:sticky;top:0;z-index:100;background:rgba(15,15,26,.92);backdrop-filter:blur(16px);border-bottom:1px solid var(--border);display:flex;gap:4px;padding:10px 40px;overflow-x:auto}
nav a{color:var(--muted);text-decoration:none;font-size:12px;font-weight:600;letter-spacing:.5px;padding:6px 14px;border-radius:20px;transition:all .25s;white-space:nowrap}
nav a:hover,nav a.active{color:#fff;background:var(--accent);box-shadow:0 0 16px rgba(99,102,241,.5)}

main{position:relative;z-index:5;max-width:1300px;margin:auto;padding:40px 24px 80px}
section{margin-bottom:60px}
.section-title{font-size:18px;font-weight:700;margin-bottom:24px;display:flex;align-items:center;gap:10px;opacity:0;transform:translateX(-30px);transition:all .6s ease}
.section-title.visible{opacity:1;transform:translateX(0)}
.section-title .line{flex:1;height:1px;background:linear-gradient(90deg,var(--accent),transparent)}

.kpi-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(185px,1fr));gap:16px}
.kpi-card{background:var(--surface);border:1px solid var(--border);border-radius:16px;padding:22px 20px;position:relative;overflow:hidden;cursor:default;opacity:0;transform:translateY(30px);transition:transform .35s ease,box-shadow .35s ease,opacity .5s ease}
.kpi-card.visible{opacity:1;transform:translateY(0)}
.kpi-card:hover{transform:translateY(-6px) scale(1.02);box-shadow:0 20px 40px rgba(0,0,0,.4)}
.kpi-card::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;background:var(--c);border-radius:16px 16px 0 0}
.kpi-card::after{content:'';position:absolute;top:-40px;right:-40px;width:120px;height:120px;border-radius:50%;background:radial-gradient(circle,var(--c),transparent 70%);opacity:.12;transition:opacity .3s}
.kpi-card:hover::after{opacity:.28}
.kpi-icon{font-size:26px;margin-bottom:10px}
.kpi-label{font-size:10px;color:var(--muted);text-transform:uppercase;letter-spacing:.8px;font-weight:600}
.kpi-value{font-size:18px;font-weight:800;margin:6px 0 4px;color:#fff}
.kpi-sub{font-size:11px;color:var(--muted)}

.chart-grid-2{display:grid;grid-template-columns:1fr 1fr;gap:20px}
@media(max-width:900px){.chart-grid-2{grid-template-columns:1fr}}
.chart-card{background:var(--surface);border:1px solid var(--border);border-radius:16px;padding:24px;opacity:0;transform:translateY(40px) scale(.97);transition:all .55s ease;overflow:hidden}
.chart-card.visible{opacity:1;transform:translateY(0) scale(1)}
.chart-card:hover{box-shadow:0 8px 32px rgba(99,102,241,.18);border-color:rgba(99,102,241,.3)}
.chart-card h3{font-size:12px;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.6px;margin-bottom:16px}
.chart-card.full{grid-column:1/-1}

#loader{position:fixed;inset:0;background:var(--bg);z-index:9999;display:flex;flex-direction:column;align-items:center;justify-content:center;transition:opacity .5s}
#loader.hide{opacity:0;pointer-events:none}
.loader-ring{width:60px;height:60px;border-radius:50%;border:3px solid transparent;border-top-color:#6366f1;border-right-color:#ec4899;animation:spin 1s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
#loader p{color:var(--muted);font-size:13px;margin-top:16px;letter-spacing:1px}

::-webkit-scrollbar{width:6px}
::-webkit-scrollbar-track{background:var(--bg)}
::-webkit-scrollbar-thumb{background:var(--accent);border-radius:3px}

.glow-line{height:1px;background:linear-gradient(90deg,transparent,rgba(99,102,241,.6),transparent);margin:0 0 40px}
</style>
</head>
<body>

<div id="loader"><div class="loader-ring"></div><p>Carregando dashboard...</p></div>
<div id="particles"></div>

<header>
  <h1>Estudo de Raio &mdash; Dashboard Anal&iacute;tico</h1>
  <p>Raio: 6 km &nbsp;&middot;&nbsp; 9 CNPJs &nbsp;&middot;&nbsp; Produtos: TAE &middot; TF &middot; TRE</p>
</header>

<nav id="mainnav">
  <a href="#kpis">KPIs</a>
  <a href="#volume">Volume</a>
  <a href="#ranking">Ranking</a>
  <a href="#ticket">Ticket M&eacute;dio</a>
  <a href="#recorrencia">Recorr&ecirc;ncia</a>
  <a href="#saldos">Saldos</a>
  <a href="#estab">Estabelecimentos</a>
</nav>

<main>
  <section id="kpis">
    <div class="section-title" id="st-kpis"><span>Indicadores-Chave (KPIs)</span><span class="line"></span></div>
    <div class="kpi-grid" id="kpi-grid"></div>
  </section>

  <div class="glow-line"></div>

  <section id="volume">
    <div class="section-title" id="st-vol"><span>Volume por CNPJ e Produto</span><span class="line"></span></div>
    <div class="chart-card full" id="cc-vol">
      <h3>Volume Total (R$) &mdash; barras agrupadas por produto</h3>
      <div id="chart-vol" style="height:420px"></div>
    </div>
  </section>

  <section id="ranking">
    <div class="section-title" id="st-rank"><span>Ranking &amp; Comparativo de Produtos</span><span class="line"></span></div>
    <div class="chart-grid-2">
      <div class="chart-card" id="cc-rank">
        <h3>Ranking de CNPJs por Volume Total</h3>
        <div id="chart-rank" style="height:380px"></div>
      </div>
      <div class="chart-card" id="cc-radar">
        <h3>Radar Comparativo de Produtos (normalizado)</h3>
        <div id="chart-radar" style="height:380px"></div>
      </div>
    </div>
  </section>

  <section id="ticket">
    <div class="section-title" id="st-ticket"><span>Ticket M&eacute;dio</span><span class="line"></span></div>
    <div class="chart-card full" id="cc-ticket">
      <h3>Ticket M&eacute;dio (R$) por CNPJ e Produto</h3>
      <div id="chart-ticket" style="height:400px"></div>
    </div>
  </section>

  <section id="recorrencia">
    <div class="section-title" id="st-rec"><span>Recorr&ecirc;ncia &amp; Dispers&atilde;o</span><span class="line"></span></div>
    <div class="chart-grid-2">
      <div class="chart-card" id="cc-rec">
        <h3>Recorr&ecirc;ncia por Produto (boxplot)</h3>
        <div id="chart-rec" style="height:370px"></div>
      </div>
      <div class="chart-card" id="cc-scatter">
        <h3>Ticket M&eacute;dio vs Recorr&ecirc;ncia (tamanho = volume)</h3>
        <div id="chart-scatter" style="height:370px"></div>
      </div>
    </div>
  </section>

  <section id="saldos">
    <div class="section-title" id="st-saldos"><span>Saldos M&eacute;dios</span><span class="line"></span></div>
    <div class="chart-card full" id="cc-saldos">
      <h3>Saldos M&eacute;dios TAE / TRE / TFE por Produto</h3>
      <div id="chart-saldos" style="height:380px"></div>
    </div>
  </section>

  <section id="estab">
    <div class="section-title" id="st-estab"><span>Estabelecimentos Credenciados</span><span class="line"></span></div>
    <div class="chart-card full" id="cc-estab">
      <h3>Qtd. Estabelecimentos Credenciados por CNPJ e Produto</h3>
      <div id="chart-estab" style="height:400px"></div>
    </div>
  </section>
</main>

<script>
const RAW = DATA_PLACEHOLDER;

const PROD_COLOR = {TAE:'#6366f1',TF:'#f59e0b',TRE:'#10b981'};
const CNPJ_COLORS = ['#6366f1','#f59e0b','#10b981','#ec4899','#3b82f6','#ef4444','#8b5cf6','#14b8a6','#f97316'];
const PRODUCTS = RAW.produtos;

const LAYOUT_BASE = {
  paper_bgcolor:'transparent', plot_bgcolor:'transparent',
  font:{family:'Segoe UI, system-ui, sans-serif', color:'#94a3b8', size:11},
  margin:{t:20,r:20,b:60,l:70},
  xaxis:{gridcolor:'rgba(255,255,255,.05)',zerolinecolor:'rgba(255,255,255,.1)',tickfont:{color:'#94a3b8'},titlefont:{color:'#94a3b8'}},
  yaxis:{gridcolor:'rgba(255,255,255,.05)',zerolinecolor:'rgba(255,255,255,.1)',tickfont:{color:'#94a3b8'},titlefont:{color:'#94a3b8'}},
  legend:{bgcolor:'transparent',bordercolor:'transparent',font:{color:'#cbd5e1'}},
  hoverlabel:{bgcolor:'#1e293b',bordercolor:'#6366f1',font:{color:'#e2e8f0',size:12}},
};
const CFG = {responsive:true, displayModeBar:false};

function L(extra={}) { return Object.assign({},LAYOUT_BASE,extra); }
function fmtK(v){ return v>=1e6?'R$'+(v/1e6).toFixed(2)+'M':v>=1e3?'R$'+(v/1e3).toFixed(0)+'k':'R$'+v.toFixed(0); }

// Partículas
const pel=document.getElementById('particles');
for(let i=0;i<16;i++){
  const d=document.createElement('div');d.className='particle';
  const sz=80+Math.random()*200;
  d.style.cssText=`width:${sz}px;height:${sz}px;left:${Math.random()*100}%;animation-duration:${14+Math.random()*18}s;animation-delay:${-Math.random()*20}s`;
  pel.appendChild(d);
}

// KPI cards
const grid=document.getElementById('kpi-grid');
RAW.kpis.forEach((k,i)=>{
  const el=document.createElement('div');el.className='kpi-card';
  el.style.setProperty('--c',k.color);el.style.transitionDelay=(i*.1)+'s';
  el.innerHTML=`<div class="kpi-icon">${k.icon}</div><div class="kpi-label">${k.label}</div><div class="kpi-value">${k.value}</div><div class="kpi-sub">${k.sub}</div>`;
  grid.appendChild(el);
});

function buildCharts(){
  // 1 - Volume por CNPJ e Produto
  {
    const traces=PRODUCTS.map(p=>{
      const rows=RAW.vol_cnpj.filter(r=>r.Produto===p);
      return {type:'bar',name:p,x:rows.map(r=>r.CNPJ_LABEL),y:rows.map(r=>r.volume_total_rs),
        marker:{color:PROD_COLOR[p],opacity:.88},
        text:rows.map(r=>fmtK(r.volume_total_rs)),textposition:'outside',
        hovertemplate:'<b>%{x}</b><br>'+p+': %{text}<extra></extra>'};
    });
    Plotly.newPlot('chart-vol',traces,L({barmode:'group',
      xaxis:{...LAYOUT_BASE.xaxis,tickangle:-30},
      yaxis:{...LAYOUT_BASE.yaxis,title:'Volume (R$)'},
      margin:{t:20,r:20,b:90,l:80}}),CFG);
  }

  // 2 - Ranking horizontal
  {
    const sorted=[...RAW.rank].sort((a,b)=>a.volume_total_rs-b.volume_total_rs);
    Plotly.newPlot('chart-rank',[{
      type:'bar',orientation:'h',
      y:sorted.map(r=>r.CNPJ_LABEL), x:sorted.map(r=>r.volume_total_rs),
      marker:{color:sorted.map((_,i)=>CNPJ_COLORS[i%CNPJ_COLORS.length]),opacity:.9},
      text:sorted.map(r=>fmtK(r.volume_total_rs)),textposition:'outside',
      hovertemplate:'<b>%{y}</b><br>%{text}<extra></extra>',
    }],L({margin:{t:20,r:110,b:40,l:210},
      xaxis:{...LAYOUT_BASE.xaxis,title:'Volume (R$)'},
    }),CFG);
  }

  // 3 - Radar
  {
    const volByP={}, tickByP={}, recByP={}, estabByP={};
    PRODUCTS.forEach(p=>{
      volByP[p]  =RAW.vol_cnpj.filter(r=>r.Produto===p).reduce((s,r)=>s+r.volume_total_rs,0);
      const tr   =RAW.ticket.filter(r=>r.Produto===p);
      tickByP[p] =tr.reduce((s,r)=>s+r.ticket_medio_rs,0)/tr.length;
      const sc   =RAW.scatter.filter(r=>r.Produto===p);
      recByP[p]  =sc.reduce((s,r)=>s+r.recorrencia_usuario_media,0)/sc.length;
      estabByP[p]=RAW.estab.filter(r=>r.Produto===p).reduce((s,r)=>s+r.qtd_estabelecimentos_credenciados,0);
    });
    const mxV=Math.max(...Object.values(volByP)),mxT=Math.max(...Object.values(tickByP));
    const mxR=Math.max(...Object.values(recByP)),mxE=Math.max(...Object.values(estabByP));
    const LABS=['Volume','Ticket Médio','Recorrência','Estabelecimentos'];
    const traces=PRODUCTS.map(p=>{
      const v=[volByP[p]/mxV,tickByP[p]/mxT,recByP[p]/mxR,estabByP[p]/mxE];
      v.push(v[0]);
      return {type:'scatterpolar',name:p,fill:'toself',r:v,theta:[...LABS,LABS[0]],
        line:{color:PROD_COLOR[p],width:2},fillcolor:PROD_COLOR[p]+'33',
        hovertemplate:'<b>'+p+'</b><br>%{theta}: %{r:.2f}<extra></extra>'};
    });
    Plotly.newPlot('chart-radar',traces,L({
      polar:{bgcolor:'transparent',
        radialaxis:{visible:true,range:[0,1],color:'#475569',gridcolor:'rgba(255,255,255,.08)'},
        angularaxis:{color:'#64748b',gridcolor:'rgba(255,255,255,.08)'}},
      margin:{t:20,r:40,b:40,l:40},showlegend:true}),CFG);
  }

  // 4 - Ticket médio
  {
    const traces=PRODUCTS.map(p=>{
      const rows=RAW.ticket.filter(r=>r.Produto===p);
      return {type:'bar',name:p,x:rows.map(r=>r.CNPJ_LABEL),y:rows.map(r=>r.ticket_medio_rs),
        marker:{color:PROD_COLOR[p],opacity:.88},
        text:rows.map(r=>fmtK(r.ticket_medio_rs)),textposition:'outside',
        hovertemplate:'<b>%{x}</b><br>Ticket '+p+': %{text}<extra></extra>'};
    });
    Plotly.newPlot('chart-ticket',traces,L({barmode:'group',
      xaxis:{...LAYOUT_BASE.xaxis,tickangle:-30},
      yaxis:{...LAYOUT_BASE.yaxis,title:'Ticket Médio (R$)'},
      margin:{t:20,r:20,b:90,l:80}}),CFG);
  }

  // 5 - Boxplot recorrência
  {
    const traces=PRODUCTS.map(p=>{
      const rows=RAW.scatter.filter(r=>r.Produto===p);
      return {type:'box',name:p,y:rows.map(r=>r.recorrencia_usuario_media),
        marker:{color:PROD_COLOR[p]},line:{color:PROD_COLOR[p]},fillcolor:PROD_COLOR[p]+'40',
        boxpoints:'all',jitter:.4,pointpos:0,
        hovertemplate:'<b>'+p+'</b><br>Recorrência: %{y:.2f}x<extra></extra>'};
    });
    Plotly.newPlot('chart-rec',traces,L({
      yaxis:{...LAYOUT_BASE.yaxis,title:'Recorrência Média'},
      margin:{t:20,r:20,b:40,l:70},showlegend:false}),CFG);
  }

  // 6 - Scatter
  {
    const traces=PRODUCTS.map(p=>{
      const rows=RAW.scatter.filter(r=>r.Produto===p);
      return {type:'scatter',mode:'markers',name:p,
        x:rows.map(r=>r.ticket_medio_rs),y:rows.map(r=>r.recorrencia_usuario_media),
        marker:{color:PROD_COLOR[p],size:rows.map(r=>7+r.volume_total_rs/3e6),opacity:.82,line:{color:'white',width:1}},
        text:rows.map(r=>r.CNPJ_LABEL),
        hovertemplate:'<b>%{text}</b><br>Ticket: R$%{x:,.0f}<br>Recorrência: %{y:.2f}x<extra></extra>'};
    });
    Plotly.newPlot('chart-scatter',traces,L({
      xaxis:{...LAYOUT_BASE.xaxis,title:'Ticket Médio (R$)'},
      yaxis:{...LAYOUT_BASE.yaxis,title:'Recorrência Média'},
      margin:{t:20,r:20,b:60,l:70}}),CFG);
  }

  // 7 - Saldos médios
  {
    const SK=['saldo_medio_tae','saldo_medio_tre','saldo_medio_tfe'];
    const SN=['TAE','TRE','TFE'];
    const SC=['#6366f1','#f59e0b','#10b981'];
    const traces=SK.map((k,i)=>({type:'bar',name:SN[i],
      x:RAW.saldos.map(r=>r.Produto),y:RAW.saldos.map(r=>r[k]),
      marker:{color:SC[i],opacity:.88},
      text:RAW.saldos.map(r=>fmtK(r[k])),textposition:'outside',
      hovertemplate:'<b>%{x}</b><br>Saldo '+SN[i]+': %{text}<extra></extra>'}));
    Plotly.newPlot('chart-saldos',traces,L({barmode:'group',
      yaxis:{...LAYOUT_BASE.yaxis,title:'Saldo Médio (R$)'},
      margin:{t:20,r:20,b:40,l:80}}),CFG);
  }

  // 8 - Estabelecimentos
  {
    const traces=PRODUCTS.map(p=>{
      const rows=RAW.estab.filter(r=>r.Produto===p);
      return {type:'bar',name:p,x:rows.map(r=>r.CNPJ_LABEL),y:rows.map(r=>r.qtd_estabelecimentos_credenciados),
        marker:{color:PROD_COLOR[p],opacity:.88},
        text:rows.map(r=>r.qtd_estabelecimentos_credenciados),textposition:'outside',
        hovertemplate:'<b>%{x}</b><br>'+p+': %{y}<extra></extra>'};
    });
    Plotly.newPlot('chart-estab',traces,L({barmode:'group',
      xaxis:{...LAYOUT_BASE.xaxis,tickangle:-30},
      yaxis:{...LAYOUT_BASE.yaxis,title:'Qtd. Estabelecimentos'},
      margin:{t:20,r:20,b:90,l:70}}),CFG);
  }
}

// IntersectionObserver — fade-in ao rolar
const io=new IntersectionObserver(entries=>{
  entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add('visible');io.unobserve(e.target);}});
},{threshold:.08});
document.querySelectorAll('.chart-card,.kpi-card,.section-title').forEach(el=>io.observe(el));

// Nav ativa
const navLinks=document.querySelectorAll('nav a');
const ioNav=new IntersectionObserver(entries=>{
  entries.forEach(e=>{
    if(e.isIntersecting){
      navLinks.forEach(a=>a.classList.remove('active'));
      const a=document.querySelector(`nav a[href="#${e.target.id}"]`);
      if(a)a.classList.add('active');
    }
  });
},{threshold:.25});
document.querySelectorAll('main section[id]').forEach(s=>ioNav.observe(s));

window.addEventListener('load',()=>{
  buildCharts();
  setTimeout(()=>{
    document.getElementById('loader').classList.add('hide');
    document.querySelectorAll('.kpi-card').forEach((el,i)=>setTimeout(()=>el.classList.add('visible'),i*100));
  },700);
});
</script>
</body>
</html>"""

HTML = HTML.replace('DATA_PLACEHOLDER', DATA_JS)

with open('dashboard_animado.html', 'w', encoding='utf-8') as f:
    f.write(HTML)

print('ok')
