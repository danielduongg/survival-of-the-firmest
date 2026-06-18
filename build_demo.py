import json
M=json.load(open("web_model.json"))
HTML=r'''<!DOCTYPE html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>survival-of-the-firmest — will the business make it?</title>
<style>
 :root{--bg:#070b11;--panel:#0f1622;--panel2:#0b101a;--line:#1e2a3e;--ink:#eaf1ff;--mut:#8aa0bf;
   --blue:#5b8cff;--green:#27d08a;--red:#ff5d6c;--warn:#ffb454;}
 *{box-sizing:border-box}
 body{margin:0;background:radial-gradient(1100px 650px at 75% -10%,#11233f 0%,var(--bg) 55%);color:var(--ink);
   font:16px/1.55 ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,Inter,sans-serif;-webkit-font-smoothing:antialiased}
 .wrap{max-width:920px;margin:0 auto;padding:36px 20px 80px}
 .eyebrow{letter-spacing:.16em;text-transform:uppercase;font-size:12px;color:var(--blue);font-weight:700}
 h1{font-size:29px;margin:.25em 0 .15em;line-height:1.15}
 .sub{color:var(--mut);max-width:66ch}
 .grid{display:grid;grid-template-columns:1.3fr .8fr;gap:18px;margin-top:22px}
 @media(max-width:780px){.grid{grid-template-columns:1fr}}
 .card{background:linear-gradient(180deg,var(--panel),var(--panel2));border:1px solid var(--line);border-radius:16px;padding:18px 20px;box-shadow:0 20px 50px -30px #000}
 select,input[type=range]{width:100%}
 select{background:#0a1018;color:var(--ink);border:1px solid var(--line);border-radius:9px;padding:9px 11px;font-size:14px}
 input[type=range]{accent-color:var(--blue);height:5px}
 .frow{margin:11px 0}.frow .lab{display:flex;justify-content:space-between;font-size:13px;color:var(--mut);margin-bottom:4px}
 .frow .lab b{color:var(--ink);font-variant-numeric:tabular-nums;font-size:14px}
 .toggle{display:flex;gap:6px}.pill{font-size:12.5px;border:1px solid var(--line);background:#0c1422;color:var(--mut);padding:6px 12px;border-radius:999px;cursor:pointer}
 .pill.on{border-color:var(--blue);color:#fff;background:#13203d}
 svg{width:100%;height:auto;display:block}
 .surv{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:12px}
 .sv{background:#0a1018;border:1px solid var(--line);border-radius:10px;padding:9px;text-align:center}
 .sv .k{font-size:11px;color:var(--mut)}.sv .v{font-size:20px;font-weight:800;font-variant-numeric:tabular-nums}
 .big{font-size:46px;font-weight:800;text-align:center;font-variant-numeric:tabular-nums;line-height:1.1}
 h2{font-size:14px;margin:16px 0 8px;color:var(--mut);font-weight:600;letter-spacing:.02em;text-transform:uppercase}
 .stat{display:flex;justify-content:space-between;font-size:14px;padding:6px 0;border-bottom:1px solid var(--line)}
 .stat b{font-variant-numeric:tabular-nums}
 .note{margin-top:14px;border-left:3px solid var(--warn);background:#1a160c;padding:12px 15px;border-radius:0 10px 10px 0;color:#ecd9b0;font-size:14px}
 .foot{margin-top:22px;color:var(--mut);font-size:13px;text-align:center}
 a{color:var(--blue);text-decoration:none}a:hover{text-decoration:underline}
</style></head><body><div class="wrap">
 <div class="eyebrow">survival-of-the-firmest · live demo</div>
 <h1>Will the business make it?</h1>
 <p class="sub">Kaplan–Meier-style survival curves for new businesses by industry, grounded in U.S. Bureau of Labor Statistics establishment-survival data — plus an honest test of whether firm and founder traits can predict an <i>individual</i> company's fate.</p>
 <div class="grid">
  <div class="card">
   <div class="frow"><label style="font-size:13px;color:var(--mut)">Industry</label><select id="sector"></select></div>
   <svg id="curve" viewBox="0 0 560 250"></svg>
   <div class="surv" id="surv"></div>
   <h2 style="margin-top:16px">Founder / firm traits</h2>
   <div class="frow"><div class="lab"><span>Initial employees</span><b id="vsize"></b></div><input type="range" id="size" min="1" max="50" value="8"></div>
   <div class="frow"><div class="lab"><span>Founder experience</span><b id="vexp"></b></div><input type="range" id="exp" min="0" max="30" value="8"></div>
   <div class="frow"><div class="lab"><span>VC-funded</span><b></b></div><div class="toggle"><span class="pill" id="f0">No</span><span class="pill" id="f1">Yes</span></div></div>
   <div class="frow"><div class="lab"><span>Urban location</span><b></b></div><div class="toggle"><span class="pill" id="u0">No</span><span class="pill" id="u1">Yes</span></div></div>
  </div>
  <div class="card">
   <div style="font-size:12px;color:var(--mut);text-align:center;letter-spacing:.04em">PREDICTED 5-YEAR SURVIVAL</div>
   <div class="big" id="p5">—</div>
   <div style="text-align:center;font-size:13px;color:var(--mut)" id="vsbase"></div>
   <h2>Can a model pick the survivors?</h2>
   <div class="stat"><span>AUC — sector base rate only</span><b id="ab"></b></div>
   <div class="stat"><span>AUC — founder/firm traits only</span><b id="aa"></b></div>
   <div class="stat"><span>AUC — base rate + traits</span><b id="af"></b></div>
   <div class="note" id="note"></div>
  </div>
 </div>
 <div class="foot">Weibull survival fit to BLS Business Employment Dynamics anchors · logistic 5-yr predictor · <a href="https://github.com/danielduongg/survival-of-the-firmest" target="_blank">source &amp; data →</a></div>
</div>
<script>
const M=__MODEL__;const C=M.curves;const names=Object.keys(C);
const st={sector:names[0],size:8,exp:8,funded:0,urban:0};
const sectorSel=document.getElementById('sector');
names.forEach(n=>{const o=document.createElement('option');o.textContent=n+'  ('+Math.round(C[n].s5*100)+'% @5yr)';o.value=n;sectorSel.appendChild(o);});
function logit(p){return Math.log(p/(1-p));}function sig(z){return 1/(1+Math.exp(-z));}
function p5(){
  const base=C[st.sector].s5;
  const attrs=[st.size,st.funded,st.exp,st.urban];
  let adj=0;for(let i=0;i<attrs.length;i++)adj+=M.attr_coef[i]*((attrs[i]-M.attr_mean[i])/M.attr_scale[i]);
  return sig(logit(base)+adj);
}
function drawCurve(){
  const W=560,H=250,pad=36;const cur=C[st.sector].survival;
  const xs=t=>pad+t/10*(W-pad-10);const ys=v=>H-26-v*(H-46);
  // overall average curve
  const avg=[];for(let t=0;t<=10;t++){let s=0;names.forEach(n=>s+=C[n].survival[t]);avg.push(s/names.length);}
  const line=(arr,col,w)=>`<polyline points="${arr.map((v,t)=>xs(t).toFixed(1)+','+ys(v).toFixed(1)).join(' ')}" fill="none" stroke="${col}" stroke-width="${w}"/>`;
  let grid='';for(let v=0;v<=1;v+=0.25){grid+=`<line x1="${pad}" y1="${ys(v)}" x2="${W-10}" y2="${ys(v)}" stroke="#16203200" style="stroke:#172033"/><text x="${pad-6}" y="${ys(v)+4}" fill="#5f7396" font-size="10" text-anchor="end">${Math.round(v*100)}%</text>`;}
  for(let t=0;t<=10;t+=2)grid+=`<text x="${xs(t)}" y="${H-8}" fill="#5f7396" font-size="10" text-anchor="middle">${t}y</text>`;
  document.getElementById('curve').innerHTML=grid+line(avg,'#42506e',1.5)+line(cur,'#27d08a',3)+
    `<text x="${W-12}" y="${ys(cur[10])-6}" fill="#27d08a" font-size="11" text-anchor="end">this industry</text>`+
    `<text x="${W-12}" y="${ys(avg[10])+14}" fill="#8aa0bf" font-size="10" text-anchor="end">all-industry avg</text>`;
}
function render(){
  document.getElementById('vsize').textContent=st.size;
  document.getElementById('vexp').textContent=st.exp+' yrs';
  document.getElementById('f0').className='pill'+(st.funded?'':' on');document.getElementById('f1').className='pill'+(st.funded?' on':'');
  document.getElementById('u0').className='pill'+(st.urban?'':' on');document.getElementById('u1').className='pill'+(st.urban?' on':'');
  const cur=C[st.sector].survival;
  document.getElementById('surv').innerHTML=[[1,'1-yr'],[3,'3-yr'],[5,'5-yr'],[10,'10-yr']].map(([t,l])=>
    `<div class="sv"><div class="k">${l}</div><div class="v">${Math.round(cur[t]*100)}%</div></div>`).join('');
  drawCurve();
  const p=p5(),base=C[st.sector].s5;
  document.getElementById('p5').textContent=Math.round(p*100)+'%';
  document.getElementById('p5').style.color=p>=0.5?'var(--green)':p>=0.42?'var(--warn)':'var(--red)';
  const d=Math.round((p-base)*100);
  document.getElementById('vsbase').textContent=`sector base ${Math.round(base*100)}% · traits ${d>=0?'+':''}${d} pts`;
}
document.getElementById('sector').addEventListener('change',e=>{st.sector=e.target.value;render();});
document.getElementById('size').addEventListener('input',e=>{st.size=+e.target.value;render();});
document.getElementById('exp').addEventListener('input',e=>{st.exp=+e.target.value;render();});
document.getElementById('f0').onclick=()=>{st.funded=0;render();};document.getElementById('f1').onclick=()=>{st.funded=1;render();};
document.getElementById('u0').onclick=()=>{st.urban=0;render();};document.getElementById('u1').onclick=()=>{st.urban=1;render();};
document.getElementById('ab').textContent=M.metrics.auc_base.toFixed(3);
document.getElementById('aa').textContent=M.metrics.auc_attr.toFixed(3);
document.getElementById('af').textContent=M.metrics.auc_full.toFixed(3);
document.getElementById('note').innerHTML=`<b>Barely.</b> Founder/firm traits lift AUC only from ${M.metrics.auc_base.toFixed(2)} (sector base rate alone) to ${M.metrics.auc_full.toFixed(2)} — a hair above a coin flip. Which <i>industry</i> you're in matters far more than the details, and the survivors you read about are a <b>survivorship-biased</b> sample. Predicting an individual company's fate is mostly base rate.`;
render();
</script></body></html>'''
open("index.html","w").write(HTML.replace("__MODEL__",json.dumps(M)))
print("wrote index.html",round(len(HTML)/1024,1),"KB")
