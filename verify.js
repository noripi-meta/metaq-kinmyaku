const fs=require("fs");
// --- 新アプリの中身を取り出す ---
const html=fs.readFileSync("index.html","utf8");
const code=html.slice(html.indexOf("<script>")+8, html.lastIndexOf("</script>"));
const els={};
function el(id){ return els[id] || (els[id]={innerHTML:"",textContent:"",value:"",hidden:false,addEventListener(){}}); }
global.window={__money:null,scrollTo(){},addEventListener(){}};
global.document={getElementById:el,addEventListener(){}};
global.navigator={userAgent:"node",sendBeacon(){return true;}};
eval(code);
const NEW=global.window.__money;

// --- 本家エンジン ---
let a=fs.readFileSync("/Users/noripi/MetaQ-uranai/app.js","utf8");
const i=a.lastIndexOf("})();");
a=a.slice(0,i)+"; globalThis.__t={calcFourPillars};\n"+a.slice(i);
const W={addEventListener(){},localStorage:{getItem:()=>null,setItem(){}},location:{href:""}};
const Dm={addEventListener(){},getElementById:()=>null,querySelector:()=>null,querySelectorAll:()=>[],
 createElement:()=>({style:{},classList:{add(){},remove(){}},appendChild(){},setAttribute(){}}),
 body:{appendChild(){},classList:{add(){},remove(){}}},head:{appendChild(){}}};
(function(){ const window=W, document=Dm, localStorage=W.localStorage,
   navigator={userAgent:""}, fetch=()=>Promise.resolve({ok:false}); eval(a); })();
const OLD=globalThis.__t.calcFourPillars;

// --- ① 仕様書テストケース ---
const T=[[1990,6,24,null,"庚","沐浴","沐浴","建禄",5],[1990,6,24,23,"辛","病","病","建禄",45],
 [1987,11,13,null,"丙","沐浴","絶","長生",55],[1977,1,29,null,"丙","冠帯","養","墓",70],
 [1960,6,29,null,"戊","胎","帝旺","胎",100]];
let ok=0;
console.log("① 仕様書のテストケース");
T.forEach(t=>{
  const r=NEW.calcMoney(t[0],t[1],t[2],t[3]), p=NEW.calcRatio(r);
  const hit=r.stem===t[4]&&r.year===t[5]&&r.month===t[6]&&r.day===t[7]&&p===t[8];
  if(hit)ok++;
  console.log(`  ${t[0]}/${t[1]}/${t[2]} ${t[3]===null?"時間不明":t[3]+"時"} → ${r.stem}/${r.year}/${r.month}/${r.day} 逆算${p}% ${hit?"✅":"❌ 期待:"+t.slice(4).join("/")}`);
});
console.log(`  ${ok}/5\n`);

// --- ② 1900〜2030 全日付 × 時間不明/0時/23時 で本家と照合 ---
console.log("② 本家エンジンとの全日照合（1900〜2030）");
let n=0,ng=0,first=null;
for(let y=1900;y<=2030;y++)for(let m=1;m<=12;m++){
  const dim=new Date(y,m,0).getDate();
  for(let d=1;d<=dim;d++){
    for(const h of [null,0,23]){
      const a1=NEW.calcMoney(y,m,d,h);
      const b1=OLD(y,m,d,h===null?null:h,0);
      n++;
      if(a1.stem!==b1.dayStem||a1.year!==b1.ishi.juniun||a1.month!==b1.hyomen.juniun||a1.day!==b1.honshitsu.juniun){
        ng++; if(!first)first=`${y}/${m}/${d} h=${h} 新:${a1.stem}/${a1.year}/${a1.month}/${a1.day} 旧:${b1.dayStem}/${b1.ishi.juniun}/${b1.hyomen.juniun}/${b1.honshitsu.juniun}`;
      }
    }
  }
}
console.log(`  照合 ${n.toLocaleString()} 件 / 不一致 ${ng} 件 ${ng?"❌ 例: "+first:"🎉 全一致"}\n`);

// --- ③ 割合の分布と、取りうる値の網羅 ---
console.log("③ 逆算設計型の割合の分布（1900〜2030 時間不明）");
const dist={};
for(let y=1900;y<=2030;y++)for(let m=1;m<=12;m++){
  const dim=new Date(y,m,0).getDate();
  for(let d=1;d<=dim;d++){ const p=NEW.calcRatio(NEW.calcMoney(y,m,d,null)); dist[p]=(dist[p]||0)+1; }
}
const tot=Object.values(dist).reduce((a,b)=>a+b,0);
Object.keys(dist).map(Number).sort((a,b)=>a-b).forEach(k=>
  console.log(`  逆算${String(k).padStart(3)}% / 臨機${String(100-k).padStart(3)}%  ${(dist[k]/tot*100).toFixed(1)}%  ${"█".repeat(Math.round(dist[k]/tot*120))}`));
console.log(`  取りうる値 ${Object.keys(dist).length} 通り（理論値 2^4=16通り）`);
