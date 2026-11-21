# -*- coding: utf-8 -*-
import io, json, os, data
BASE = os.path.dirname(os.path.abspath(__file__))
ENGINE = io.open(os.path.join(BASE, "_engine.js"), encoding="utf-8").read()
LOG_ENDPOINT = "https://script.google.com/macros/s/AKfycbyy5ZLj9EREvMBEAwc3ljXZM5k1lVL-EELxUWYZXAjsCUkEZmOvzzx8p_To4hfvhB6Y/exec"   # 記録用GAS（スプレッドシートへ追記）

D = {"gyakuStems":data.GYAKU_STEMS, "gyakuUns":data.GYAKU_UNS, "types":data.TYPES,
     "buki":data.BUKI, "kanban":data.KANBAN, "kachi":data.KACHI, "uketori":data.UKETORI,
     "seasons":data.SEASONS, "extra":data.EXTRA, "sdetail":data.SEASON_DETAIL}

HTML = r"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="robots" content="noindex">
<title>引き寄せ四柱推命 金脈編｜MetaQ</title>
<meta name="theme-color" content="#FDF2F6">
<style>
*{box-sizing:border-box}
:root{
  --bg:#FDF2F6; --card:#FFFCFD; --ink:#5B4450; --sub:#A48B99; --line:#F6E2EA;
  --gold:#E8BE86; --pink:#F08FB4; --pink-d:#D7638F; --lav:#AC8FDB;
}
html,body{margin:0;padding:0}
body{background:var(--bg);color:var(--ink);font-size:16px;line-height:1.9;
  font-family:"Hiragino Mincho ProN","Yu Mincho","MS PMincho",serif;
  background:linear-gradient(180deg,#FDEFF5 0%,#FFF8FA 48%,#FCF1F6 100%);
  background-attachment:fixed;}
.wrap{max-width:660px;margin:0 auto;padding:0 14px 60px}
header{text-align:center;padding:36px 14px 24px}
header .badge{display:inline-block;padding:5px 16px;border:1px solid var(--pink);border-radius:999px;
  background:#fff;color:var(--pink-d);font-size:11px;font-weight:900;letter-spacing:.18em;margin-bottom:14px;
  box-shadow:0 3px 10px rgba(240,143,180,.22)}
header h1{margin:0 0 9px;font-size:clamp(26px,6.4vw,34px);line-height:1.45;letter-spacing:.05em;font-weight:900;
  background:linear-gradient(90deg,#D7638F,#AC8FDB);-webkit-background-clip:text;background-clip:text;color:transparent}
header p{margin:0;font-size:13.5px;color:var(--sub)}
header h1 .hsub{display:block;margin:7px 0 0;font-size:.5em;letter-spacing:.34em;font-weight:900}
.card{background:var(--card);border:1px solid var(--line);border-radius:20px;padding:24px 19px;margin:0 0 16px;
  box-shadow:0 10px 26px rgba(199,120,152,.11)}
label.fl{display:block;font-size:13px;font-weight:700;color:var(--pink-d);margin:0 0 7px;letter-spacing:.05em}
input[type=date],select{width:100%;padding:14px 13px;font-size:16px;font-family:inherit;color:var(--ink);
  background:#fff;border:1px solid var(--line);border-radius:13px;appearance:none;-webkit-appearance:none}
input[type=date]:focus,select:focus{outline:none;border-color:var(--pink);box-shadow:0 0 0 3px rgba(240,143,180,.22)}
.row{margin-bottom:16px}
.hint{font-size:11.5px;color:var(--sub);margin-top:6px;line-height:1.7}
.go{width:100%;margin-top:4px;padding:17px;border:none;border-radius:16px;cursor:pointer;
  background:linear-gradient(180deg,#F7A3C2,#E0749D);color:#fff;font-size:17px;font-weight:bold;
  font-family:inherit;letter-spacing:.08em;box-shadow:0 6px 0 #C25680,0 12px 22px rgba(194,86,128,.28)}
.go:active{transform:translateY(3px);box-shadow:0 3px 0 #C25680}
.err{color:var(--pink-d);font-size:13px;margin-top:10px;font-weight:700}
/* 割合 */
.ratio{display:flex;justify-content:space-between;align-items:baseline;margin:2px 0 10px}
.ratio .n{font-size:14.5px;font-weight:900}
.ratio .n i{font-style:normal;font-size:27px;margin:0 2px}
.ratio .l{color:var(--lav)} .ratio .r{color:var(--pink-d)}
.bar{display:flex;height:16px;border-radius:999px;overflow:hidden;background:#fff;
  border:1px solid var(--line);box-shadow:inset 0 1px 3px rgba(199,120,152,.1)}
.bar i{display:block;height:100%}
.bar .b1{background:linear-gradient(90deg,#C3AAE8,#AC8FDB)}
.bar .b2{background:linear-gradient(90deg,#F7AFCA,#EE85AC)}
.mt{display:inline-block;font-size:12px;font-weight:900;letter-spacing:.1em;color:#fff;
  background:var(--lav);border-radius:999px;padding:4px 15px;margin:16px 0 9px}
.mt.is-r{background:var(--pink)}
.lead{font-size:15.5px;font-weight:700;margin:0 0 4px;line-height:1.75}
/* 季節パターン */
.season-ttl{font-size:12px;font-weight:900;letter-spacing:.2em;color:var(--pink);margin:0 0 2px}
.season-name{font-size:clamp(27px,7vw,34px);font-weight:900;line-height:1.3;margin:2px 0 7px;letter-spacing:.02em;
  background:linear-gradient(90deg,#D7638F,#AC8FDB);-webkit-background-clip:text;background-clip:text;color:transparent}
.season-lead{font-size:15px;line-height:1.8;color:var(--ink);font-weight:700}
.season-sub{font-size:15px;font-weight:700;color:var(--pink-d);margin:-3px 0 11px}
.stages{display:grid;grid-template-columns:repeat(3,1fr);gap:7px;margin-top:15px}
.st{text-align:center;padding:11px 4px;border-radius:13px;font-size:11.5px;font-weight:700;
  color:var(--sub);background:#fff;border:1px solid var(--line);line-height:1.45}
.st.on{color:#fff;background:linear-gradient(135deg,#F7A3C2,#E0749D);border-color:transparent;
  box-shadow:0 5px 14px rgba(224,116,157,.3)}
.st-now{margin-top:11px;font-size:14px;line-height:1.8;background:linear-gradient(135deg,#FFF6FA,#FDF1E9);
  border:1px solid #F6E2EA;border-radius:14px;padding:12px 15px}
.st-now b{color:var(--pink-d)}
/* 気をつけること・今日からの一歩 */
.extra{margin-top:14px;display:grid;gap:9px}
.ex{display:flex;gap:10px;align-items:flex-start;font-size:14px;line-height:1.8;
  background:#fff;border:1px solid var(--line);border-radius:14px;padding:11px 14px}
.ex b{flex:0 0 auto;font-size:11px;font-weight:900;color:#fff;border-radius:999px;padding:3px 11px;
  white-space:nowrap;letter-spacing:.04em;margin-top:3px}
.ex.warn b{background:#E8A66B}
.ex.step b{background:var(--lav)}
/* セクション */
h2{font-size:23px;font-weight:900;line-height:1.4;margin:0 0 14px;letter-spacing:.03em;
  padding-bottom:11px;border-bottom:1px solid var(--line)}
h2 span{display:block;font-size:10.5px;font-weight:900;letter-spacing:.2em;color:var(--pink);margin-bottom:5px}
ul{list-style:none;margin:0 0 15px;padding:0}
ul li{position:relative;padding:8px 0 8px 25px;font-size:15px;border-bottom:1px dashed #F6E6ED;line-height:1.75}
ul li:last-child{border-bottom:none}
ul li::before{content:"";position:absolute;left:5px;top:17px;width:8px;height:8px;border-radius:50%;
  background:linear-gradient(135deg,#F7AFCA,#E8BE86)}
.note{background:linear-gradient(135deg,#FFF6FA,#FDF1E9);border:1px solid #F6E2EA;border-radius:14px;
  padding:13px 15px;font-size:14.5px;line-height:1.85}
.kotsu{background:#fff;border:1px dashed var(--pink);border-radius:14px;padding:12px 15px;font-size:14.5px;margin-top:13px}
.kotsu b{color:var(--pink-d)}
.sep{text-align:center;font-size:15px;letter-spacing:.35em;padding:14px 0 10px;color:var(--pink);opacity:.6}
.again{width:100%;padding:15px;border:1px solid var(--line);border-radius:15px;background:#fff;
  color:var(--sub);font-size:15px;font-family:inherit;cursor:pointer;margin-top:6px}
footer{text-align:center;font-size:11px;color:var(--sub);padding:26px 14px 10px;line-height:1.9}
[hidden]{display:none!important}
</style>
</head>
<body>
<div class="wrap">

<header>
  <p class="badge">MetaQ</p>
  <h1>引き寄せ四柱推命<span class="hsub">金脈編</span></h1>
  <p>生まれた日から、あなたのマネーコードを解読します</p>
</header>

<section class="card" id="form">
  <div class="row">
    <label class="fl" for="bd">生年月日</label>
    <input type="date" id="bd" min="1900-01-01" max="2030-12-31">
  </div>
  <div class="row">
    <label class="fl" for="hh">生まれた時間</label>
    <select id="hh"></select>
    <p class="hint">わからなくて大丈夫です。23時台生まれの方だけ、結果が変わります</p>
  </div>
  <button class="go" id="go">診断する</button>
  <p class="err" id="err" hidden></p>
</section>

<section id="result" hidden></section>

<footer>
  ※ この診断は統計をもとにした傾向をお伝えするものです<br>
  結果はこの画面にだけ表示され、端末には保存されません
</footer>
</div>

<script>
(function(){
"use strict";
var LOG_ENDPOINT = "__ENDPOINT__";
var D = __DATA__;

// ====== 四柱推命エンジン（MetaQ占いアプリから移植・ISD実機検証済み） ======
__ENGINE__

function nextCalendarDay(y, m, d) {
  var leap = (y % 4 === 0 && y % 100 !== 0) || y % 400 === 0;
  var dim = [31, leap ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
  d++;
  if (d > dim[m - 1]) { d = 1; m++; }
  if (m > 12) { m = 1; y++; }
  return { y: y, m: m, d: d };
}
function calcMoney(y, m, d, h) {
  if (h === 23) { var nd = nextCalendarDay(y, m, d); y = nd.y; m = nd.m; d = nd.d; }
  var di = dayIndex(y, m, d);
  var dayStem = JIKKAN[di % 10];
  var noonH = (h === null) ? 12 : h;
  var mbIdx = monthBranchIndex(sunLongitude(toJulianDay(y, m, d, noonH)));
  var yg = yearGanzhiIndex(y, m, d);
  return { stem: dayStem, year: juniunFor(dayStem, yg.idx % 12),
           month: juniunFor(dayStem, mbIdx), day: juniunFor(dayStem, di % 12) };
}
function calcRatio(r) {
  var p = 0;
  if (D.gyakuStems.indexOf(r.stem) >= 0) p += 5;
  if (D.gyakuUns.indexOf(r.year)  >= 0) p += 15;
  if (D.gyakuUns.indexOf(r.month) >= 0) p += 30;
  if (D.gyakuUns.indexOf(r.day)   >= 0) p += 50;
  return p;
}
function esc(s){ return String(s).replace(/[&<>"]/g, function(c){
  return {"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;"}[c]; }); }
function listHtml(a){ return "<ul>" + a.map(function(x){ return "<li>"+esc(x)+"</li>"; }).join("") + "</ul>"; }
function secHtml(tag, title, pack, extra){
  return '<div class="card"><h2><span>'+esc(tag)+'</span>'+esc(title)+'</h2>' +
    listHtml(pack[0]) + '<div class="note">'+esc(pack[1])+'</div>' + (extra || '') + '</div>';
}
function seasonOf(un){
  for (var i = 0; i < D.seasons.length; i++) if (D.seasons[i].uns.indexOf(un) >= 0) return i;
  return -1;
}
function seasonHtml(un){
  var i = seasonOf(un); if (i < 0) return "";
  var s = D.seasons[i], d = D.sdetail[s.label];
  var k = s.uns.indexOf(un);
  var strip = d.stages.map(function(x, j){
    return '<div class="st'+(j === k ? " on" : "")+'">'+esc(x.split("｜")[0])+'</div>'; }).join("");
  var now = d.stages[k].split("｜");
  return '<div class="card">' +
    '<h2><span>STYLE</span>あなたの稼ぎ方のタイプ</h2>' +
    '<div class="season-name">'+esc(s.label)+'</div>' +
    '<div class="season-sub">'+esc(d.sub)+'</div>' +
    '<div class="note">'+esc(d.flow)+'</div>' +
    '<div class="stages">'+strip+'</div>' +
    '<div class="st-now">あなたは<b>「'+esc(now[0])+'」</b>── '+esc(now[1])+'</div>' +
    '</div>';
}
function extraHtml(un){
  var e = D.extra[un]; if (!e) return "";
  return '<div class="extra">' +
    '<div class="ex warn"><b>気をつけること</b><span>'+esc(e[0])+'</span></div>' +
    '<div class="ex step"><b>今日からの一歩</b><span>'+esc(e[1])+'</span></div></div>';
}

function render(r){
  var p = calcRatio(r), q = 100 - p;
  var gFirst = (p > q) ? true : (p < q) ? false : (D.gyakuUns.indexOf(r.day) >= 0);
  var t1 = gFirst ? D.types.gyaku : D.types.rinki;
  var t2 = gFirst ? D.types.rinki : D.types.gyaku;
  var n1 = gFirst ? p : q, n2 = gFirst ? q : p;

  var h = '<div class="card">' +
    '<h2><span>TYPE</span>あなたの引き寄せタイプ</h2>' +
    '<div class="ratio">' +
      '<span class="n '+(gFirst?"l":"r")+'">'+esc(t1.name)+' <i>'+n1+'</i>%</span>' +
      '<span class="n '+(gFirst?"r":"l")+'">'+esc(t2.name)+' <i>'+n2+'</i>%</span>' +
    '</div>' +
    '<div class="bar"><i class="'+(gFirst?"b1":"b2")+'" style="width:'+n1+'%"></i>' +
      '<i class="'+(gFirst?"b2":"b1")+'" style="width:'+n2+'%"></i></div>' +
    '<span class="mt'+(gFirst?"":" is-r")+'">'+esc(t1.name)+'</span>' +
    '<p class="lead">'+esc(t1.lead)+'</p>' +
    listHtml(t1.items) +
    '<div class="kotsu"><b>稼ぐコツ</b>　'+esc(t1.kotsu)+'</div></div>';

  h += '<div class="sep">♡ ✿ ♡</div>' + secHtml("WEAPON",  "あなたの武器",        D.buki[r.stem]);
  h += '<div class="sep">♡ ✿ ♡</div>' + secHtml("SIGN",    "あなたの看板",        D.kanban[r.year]);
  h += '<div class="sep">♡ ✿ ♡</div>' + secHtml("WIN",     "稼ぐ時の勝ちパターン", D.kachi[r.month], extraHtml(r.month));
  h += '<div class="sep">♡ ✿ ♡</div>' + secHtml("RECEIVE", "お金の受け取り方",    D.uketori[r.day]);
  h += '<div class="sep">♡ ✿ ♡</div>' + seasonHtml(r.month);
  h += '<button class="again" id="again">もう一度診断する</button>';
  return h;
}

// 記録（データ収集用。利用者の画面・端末には何も残さない）
function log(y, m, d, h, r, p){   // のりぴのデータ収集用。利用者の画面・端末には何も残らない
  if (!LOG_ENDPOINT) return;
  try {
    var body = JSON.stringify({ date: y+"/"+("0"+m).slice(-2)+"/"+("0"+d).slice(-2),
      hour: (h === "23" ? "23時台" : h === "day" ? "0〜22時" : "不明"),
      stem: r.stem, year: r.year, month: r.month, day: r.day,
      gyaku: p, rinki: 100 - p,
      style: (function(){ var i = seasonOf(r.month); return i < 0 ? "" : D.seasons[i].label; })() });
    if (navigator.sendBeacon) navigator.sendBeacon(LOG_ENDPOINT, body);
    else fetch(LOG_ENDPOINT, { method:"POST", mode:"no-cors", body: body });
  } catch (e) { /* 記録に失敗しても診断は止めない */ }
}

var hh = document.getElementById("hh");
// 時柱は出さないので、結果が変わるのは「23時台かどうか」だけ
hh.innerHTML = '<option value="">わからない</option>' +
  '<option value="day">0:00 〜 22:59</option>' +
  '<option value="23">23:00 〜 23:59</option>';

function run(){
  var err = document.getElementById("err");
  var mm = /^(\d{4})-(\d{2})-(\d{2})$/.exec(document.getElementById("bd").value || "");
  if (!mm) { err.textContent = "生年月日を選んでください"; err.hidden = false; return; }
  var y = +mm[1], m = +mm[2], d = +mm[3];
  if (y < 1900 || y > 2030) { err.textContent = "1900年〜2030年で入れてください"; err.hidden = false; return; }
  err.hidden = true;
  // 節入りの判定は正午でそろえる（23時台だけ翌日として扱う）
  var hv = hh.value, h = (hv === "23") ? 23 : null;
  var r = calcMoney(y, m, d, h), p = calcRatio(r);
  var out = document.getElementById("result");
  out.innerHTML = render(r); out.hidden = false;
  document.getElementById("form").hidden = true;
  window.scrollTo(0, 0);
  log(y, m, d, hv, r, p);
  document.getElementById("again").addEventListener("click", function(){
    out.hidden = true; out.innerHTML = "";
    document.getElementById("form").hidden = false; window.scrollTo(0, 0);
  });
}
document.getElementById("go").addEventListener("click", run);
window.__money = { calcMoney: calcMoney, calcRatio: calcRatio, render: render };
})();
</script>
</body>
</html>
"""
html = HTML.replace("__DATA__", json.dumps(D, ensure_ascii=False)) \
           .replace("__ENGINE__", ENGINE).replace("__ENDPOINT__", LOG_ENDPOINT)
io.open(os.path.join(BASE, "index.html"), "w", encoding="utf-8").write(html)
print("生成: index.html", len(html), "文字")
