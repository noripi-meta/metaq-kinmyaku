# -*- coding: utf-8 -*-
import io, json, os, data
BASE = os.path.dirname(os.path.abspath(__file__))
ENGINE = io.open(os.path.join(BASE, "_engine.js"), encoding="utf-8").read()
APP_URL = "https://noripi-meta.github.io/metaq-kinmyaku/"   # シェア用に案内するリンク
LOG_ENDPOINT = "https://script.google.com/macros/s/AKfycbyy5ZLj9EREvMBEAwc3ljXZM5k1lVL-EELxUWYZXAjsCUkEZmOvzzx8p_To4hfvhB6Y/exec"   # 記録用GAS（スプレッドシートへ追記）

D = {"gyakuStems":data.GYAKU_STEMS, "gyakuUns":data.GYAKU_UNS, "types":data.TYPES,
     "buki":data.BUKI, "kanban":data.KANBAN, "kachi":data.KACHI, "uketori":data.UKETORI,
     "seasons":data.SEASONS, "extra":data.EXTRA, "sdetail":data.SEASON_DETAIL,
     "shime":data.SHIME}

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
  --bg:#FDF3F7; --card:#FFFDFE; --ink:#64505C; --sub:#AE97A3; --line:#F8E8EE;
  --gold:#E8BE86; --pink:#F08FB4; --pink-d:#D7638F; --lav:#AC8FDB;
}
html,body{margin:0;padding:0}
body{background:var(--bg);color:var(--ink);font-size:16px;line-height:2.0;letter-spacing:.02em;
  font-family:"Hiragino Maru Gothic ProN","ヒラギノ丸ゴ ProN W4","Hiragino Maru Gothic Pro",
    -apple-system,"BIZ UDPGothic","Yu Gothic Medium","Meiryo",sans-serif;
  background:linear-gradient(180deg,#FDEFF5 0%,#FFF8FA 48%,#FCF1F6 100%);
  background-attachment:fixed;}
.wrap{max-width:660px;margin:0 auto;padding:0 14px 60px}
header{text-align:center;padding:36px 14px 24px}
header .badge{display:inline-block;padding:5px 16px;border:1px solid var(--pink);border-radius:999px;
  background:#fff;color:var(--pink-d);font-size:11px;font-weight:900;letter-spacing:.18em;margin-bottom:14px;
  box-shadow:0 3px 10px rgba(240,143,180,.22)}
header h1{margin:0 0 11px;font-size:clamp(25px,6.2vw,33px);line-height:1.55;letter-spacing:.1em;font-weight:800;
  background:linear-gradient(90deg,#D7638F,#AC8FDB);-webkit-background-clip:text;background-clip:text;color:transparent}
header p{margin:0;font-size:13.5px;color:var(--sub)}
header h1 .hsub{display:block;margin:7px 0 0;font-size:.5em;letter-spacing:.34em;font-weight:900}
.card{background:var(--card);border:1px solid var(--line);border-radius:26px;padding:26px 21px;margin:0 0 20px;
  box-shadow:0 10px 30px rgba(199,120,152,.08)}
label.fl{display:block;font-size:13px;font-weight:700;color:var(--pink-d);margin:0 0 7px;letter-spacing:.05em}
input[type=text],select{width:100%;padding:15px 14px;font-size:16px;font-family:inherit;color:var(--ink);
  background:#fff;border:1px solid var(--line);border-radius:17px;appearance:none;-webkit-appearance:none}
select:invalid{color:#B9A3AE}
input[type=text]:focus,select:focus{outline:none;border-color:var(--pink);box-shadow:0 0 0 3px rgba(240,143,180,.22)}
.row{margin-bottom:16px}
.hint{font-size:11.5px;color:var(--sub);margin-top:6px;line-height:1.7}
.go{width:100%;margin-top:6px;padding:18px;border:none;border-radius:22px;cursor:pointer;
  background:linear-gradient(180deg,#F7A3C2,#E0749D);color:#fff;font-size:17px;font-weight:bold;
  font-family:inherit;letter-spacing:.12em;box-shadow:0 5px 0 #D98AAB,0 12px 24px rgba(194,86,128,.2)}
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
h2{font-size:22px;font-weight:800;line-height:1.55;margin:0 0 15px;letter-spacing:.05em;
  padding-bottom:12px;border-bottom:1px solid var(--line)}
h2 span{display:block;font-size:10.5px;font-weight:900;letter-spacing:.2em;color:var(--pink);margin-bottom:5px}
ul{list-style:none;margin:0 0 15px;padding:0}
ul li{position:relative;padding:9px 0 9px 26px;font-size:15px;border-bottom:1px dashed #F8EDF2;line-height:1.95}
ul li:last-child{border-bottom:none}
ul li::before{content:"";position:absolute;left:5px;top:17px;width:8px;height:8px;border-radius:50%;
  background:linear-gradient(135deg,#F7AFCA,#E8BE86)}
.note{background:linear-gradient(135deg,#FFF7FB,#FEF4EC);border:1px solid #F8E8EE;border-radius:18px;
  padding:15px 17px;font-size:14.5px;line-height:2.0}
.kotsu{background:#fff;border:1px dashed var(--pink);border-radius:14px;padding:12px 15px;font-size:14.5px;margin-top:13px}
.kotsu b{color:var(--pink-d)}
.sep{text-align:center;padding:9px 0 14px;line-height:0}
.sep .kao{display:inline-block;width:90px;height:auto}
.sem{position:relative;margin:30px 0 12px;padding:34px 22px 26px;text-align:center;border-radius:28px;
  background:linear-gradient(155deg,#FFF6DF 0%,#FFE7F1 48%,#FFEFE2 100%);
  border:2.5px solid #F2B86B;box-shadow:0 14px 40px rgba(214,138,80,.26),0 0 0 6px rgba(255,236,206,.5)}
.sem-free{display:inline-block;margin:0 0 15px;padding:9px 24px;border-radius:999px;color:#fff;
  font-size:16px;font-weight:900;letter-spacing:.1em;
  background:linear-gradient(135deg,#F2A03C,#E0749D);box-shadow:0 5px 16px rgba(226,140,80,.4)}
.sem-date{margin:0 0 14px;font-size:14px;font-weight:800;letter-spacing:.06em;color:#B5713A}
.sem-t{margin:0 0 12px;font-size:21px;font-weight:900;line-height:1.65;color:var(--pink-d)}
.sem-b{margin:0 0 17px;font-size:14.5px;line-height:1.95;color:var(--ink)}
.sem-pts{display:grid;gap:7px;margin:0 0 15px}
.sem-pt{background:rgba(255,255,255,.78);border-radius:13px;padding:9px 12px;font-size:13.5px;
  line-height:1.7;color:#6B5460}
.sem-hot{display:grid;gap:6px;margin:0 0 20px}
.sem-hot span{background:#FFF0F4;border:1px dashed #EE9BB8;border-radius:13px;padding:9px 12px;
  font-size:13px;font-weight:700;line-height:1.7;color:#C8426F}
.sem-btn{display:block;width:100%;box-sizing:border-box;padding:20px 20px;border-radius:24px;
  background:linear-gradient(180deg,#FF9BBF,#D43F75);color:#fff;text-decoration:none;font-weight:bold;
  font-size:18px;letter-spacing:.08em;box-shadow:0 6px 0 #AE3360,0 16px 30px rgba(174,51,96,.32)}
.sem-btn:active{transform:translateY(4px);box-shadow:0 2px 0 #AE3360}
.sem-note{margin:18px 0 0;font-size:11.5px;line-height:1.9;color:#9A8290;text-align:left}
.cta{margin:26px 0 8px;padding:28px 22px;text-align:center;border-radius:26px;
  background:linear-gradient(145deg,#FFF3F8,#FDEDE2);border:1px solid var(--line);
  box-shadow:0 10px 26px rgba(199,120,152,.13)}
.cta-t{margin:0 0 8px;font-size:12px;font-weight:900;letter-spacing:.2em;color:var(--pink)}
.cta-b{margin:0 0 17px;font-size:14.5px;line-height:1.9;color:var(--ink)}
.cta-b b{color:var(--pink-d);font-size:16px}
.cta-btn{display:inline-block;max-width:100%;box-sizing:border-box;padding:16px 30px;border-radius:20px;
  background:linear-gradient(180deg,#F7A3C2,#E0749D);color:#fff;text-decoration:none;font-weight:bold;
  font-size:16px;letter-spacing:.1em;box-shadow:0 4px 0 #D98AAB,0 11px 22px rgba(194,86,128,.2)}
.cta-btn:active{transform:translateY(2px);box-shadow:0 3px 0 #C25680}
.again{width:100%;padding:16px;border:1px solid var(--line);border-radius:20px;background:#fff;
  color:var(--sub);font-size:15px;font-family:inherit;cursor:pointer;margin-top:6px}
footer{text-align:center;font-size:11px;color:var(--sub);padding:26px 14px 10px;line-height:1.9}
[hidden]{display:none!important}
.share{margin:26px 0 8px}
.share-wrap{text-align:center}
.share-load{padding:30px 0;font-size:14px;color:#a8977f}
.share-wrap img{width:100%;max-width:420px;border-radius:12px;box-shadow:0 6px 22px rgba(0,0,0,.14)}
.share-tip{margin-top:10px;font-size:13px;color:#8a7c68;line-height:1.7}
.sl{margin:16px auto 0;max-width:420px;padding:16px;border:1px solid #ecdfc6;border-radius:16px;
  background:linear-gradient(180deg,#fffdf8,#fdf7ea)}
.sl-t{margin:0 0 10px;font-size:13px;font-weight:700;color:#a8863c}
.sl-url{display:block;padding:11px 12px;border:1px solid #efe4cf;border-radius:10px;background:#fff;
  font-size:12px;color:#6b6152;word-break:break-all;line-height:1.5;user-select:all;-webkit-user-select:all}
.sl-btn{width:100%;margin-top:10px;padding:13px;border:none;border-radius:14px;cursor:pointer;
  background:linear-gradient(135deg,#e8c77a,#c69a42);color:#fff;font-size:15px;font-weight:700;
  font-family:inherit;box-shadow:0 3px 10px rgba(198,154,66,.28)}
.sl-btn.done{background:linear-gradient(135deg,#9ccc9e,#6fae74);box-shadow:none}
.sl-note{margin:9px 0 0;font-size:12px;color:#9c8f7c;line-height:1.6}
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
    <input type="text" id="bd" inputmode="numeric" placeholder="1990/06/24" autocomplete="off">
  </div>
  <div class="row">
    <label class="fl" for="hh">生まれた時間</label>
    <select id="hh" required></select>
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
var APP_URL = "__APPURL__";
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
    '<h2><span>STYLE</span>あなたのビジネス設計タイプ</h2>' +
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

var SEMINAR = '<div class="sem">' +
  '<p class="sem-free">参加費 無料 🎁</p>' +
  '<p class="sem-date">12月4日（金）21:00〜22:30</p>' +
  '<p class="sem-t">目標設定が苦手な人のための<br>願望実現法 ✨</p>' +
  '<p class="sem-b">臨機応変型が50%以上のあなたに向けた<br>90分のオンラインセミナーです 💝</p>' +
  '<div class="sem-pts">' +
    '<span class="sem-pt">ゲストは田中克成さん 🎤</span>' +
    '<span class="sem-pt">ZOOMだから、スマホからでも参加できます 📱</span>' +
    '<span class="sem-pt">アバター参加もOKです 😊</span>' +
  '</div>' +
  '<div class="sem-hot">' +
    '<span>先着30名・埋まり次第しめきりです ⏳</span>' +
    '<span>アーカイブはなし、当日のライブだけです 📼</span>' +
  '</div>' +
  '<a class="sem-btn" href="https://www.reservestock.jp/events/1204008" target="_blank" rel="noopener">無料で申し込む 🎉</a>' +
  '<p class="sem-note">※ 逆算設計型が50%以上の方もご参加いただけます。ご家族や従業員の方のために学びたい方も歓迎です。内容は臨機応変型の方に向けたものになります 🙌</p>' +
  '</div>';
var CTA = '<div class="cta">' +
  '<p class="cta-b">あなたにぴったりな引き寄せのやり方を<br>' +
  'のりぴのメルマガでお届けしています 💌</p>' +
  '<a class="cta-btn" href="https://www.reservestock.jp/subscribe/194781" target="_blank" rel="noopener">メルマガを受け取る（無料）✨</a>' +
  '</div>';
var SEP = '<div class="sep"><img class="kao" src="data:image/png;base64,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" alt="" width="90" height="30"></div>';
/* ── シェア用シート（1024x1536のカードを描く） ── */
var MIN = '"Hiragino Mincho ProN","Yu Mincho",YuMincho,serif';
var GOT = '"Hiragino Sans","Hiragino Kaku Gothic ProN","Noto Sans JP","Yu Gothic",sans-serif';
function shimeText(r, p){
  var S = D.shime;
  return S.type[p >= 50 ? "gyaku" : "rinki"] + S.stem[r.stem] + "、" + S.year[r.year] + "ながら、" + S.month[r.month];
}
function loadImg(src){
  return new Promise(function(ok, ng){ var i = new Image(); i.onload = function(){ ok(i); }; i.onerror = ng; i.src = src; });
}
function copyLink(btn){
  var base = btn.textContent;
  function ok(){
    btn.textContent = "コピーしました ✨"; btn.classList.add("done");
    setTimeout(function(){ btn.textContent = base; btn.classList.remove("done"); }, 2200);
  }
  function fallback(){
    var ta = document.createElement("textarea");
    ta.value = APP_URL; ta.setAttribute("readonly", "");
    ta.style.position = "fixed"; ta.style.top = "0"; ta.style.opacity = "0";
    document.body.appendChild(ta); ta.select(); ta.setSelectionRange(0, 99999);
    var done = false;
    try { done = document.execCommand("copy"); } catch (e) {}
    document.body.removeChild(ta);
    if (done) ok(); else btn.textContent = "上のリンクを長押ししてコピーしてください";
  }
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(APP_URL).then(ok, fallback);
  } else fallback();
}
function drawShare(r, p, done, fail){
  Promise.all([loadImg("share_bg.jpg"), loadImg("share_qr.png")]).then(function(im){
    var W = 1024, H = 1536, CX = 512;
    var cv = document.createElement("canvas"); cv.width = W; cv.height = H;
    var c = cv.getContext("2d");
    c.drawImage(im[0], 0, 0, W, H);
    c.textBaseline = "top";
    var NAVY = "#1a2b4a", GOLD = "#aa7e2a", GOLD2 = "#c69e4e",
        PINK = "#e42870", PURPLE = "#7650e4", CREAM = "#fcf6e8";
    function ctr(t, y, font, col){ c.font = font; c.fillStyle = col; c.fillText(t, CX - c.measureText(t).width / 2, y); }
    function ctrSp(t, y, font, col, sp){
      c.font = font; c.fillStyle = col;
      var w = 0, i; for (i = 0; i < t.length; i++) w += c.measureText(t[i]).width + sp; w -= sp;
      var x = CX - w / 2;
      for (i = 0; i < t.length; i++){ c.fillText(t[i], x, y); x += c.measureText(t[i]).width + sp; }
    }
    function rr(x, y, w, h, rad){
      c.beginPath(); c.moveTo(x + rad, y);
      c.arcTo(x + w, y, x + w, y + h, rad); c.arcTo(x + w, y + h, x, y + h, rad);
      c.arcTo(x, y + h, x, y, rad); c.arcTo(x, y, x + w, y, rad); c.closePath();
    }
    function line(x1, y1, x2, y2, col, w){
      c.beginPath(); c.strokeStyle = col; c.lineWidth = w || 1; c.moveTo(x1, y1); c.lineTo(x2, y2); c.stroke();
    }
    /* 見出し */
    ctr("引き寄せ四柱推命", 236, "44px " + MIN, NAVY);
    var bt = "金脈編", bfs = 28, bh2 = 50, byy = 304;
    c.font = bfs + "px " + MIN;
    var bw = Math.round(c.measureText(bt).width) + 72, bx = CX - bw / 2;
    var bg2 = c.createLinearGradient(0, byy, 0, byy + bh2);
    bg2.addColorStop(0, "#e4be70"); bg2.addColorStop(1, "#a2742a");
    c.fillStyle = bg2; rr(bx, byy, bw, bh2, bh2 / 2); c.fill();
    c.strokeStyle = GOLD2; c.lineWidth = 2; rr(bx, byy, bw, bh2, bh2 / 2); c.stroke();
    c.fillStyle = "#ffffff"; c.fillText(bt, CX - c.measureText(bt).width / 2, byy + (bh2 - bfs * 1.42) / 2);
    /* タイプ名 */
    var se = D.seasons[seasonOf(r.month)], sd = D.sdetail[se.label], gi = se.uns.indexOf(r.month);
    ctrSp("あなたの金脈タイプ", 386, "bold 26px " + GOT, GOLD, 2);
    ctr(se.label, 424, "118px " + MIN, PINK);
    ctrSp(sd.sub, 572, "bold 35px " + GOT, GOLD, 3);
    /* 割合 */
    var q = 100 - p;
    c.font = "bold 22px " + GOT; c.fillStyle = PINK;
    c.fillText("臨機応変型", 162, 636);
    var lw = c.measureText("臨機応変型").width;
    c.font = "34px " + MIN; c.fillText(q + "%", 162 + lw + 12, 628);
    var rt = p + "%"; c.font = "34px " + MIN; c.fillStyle = PURPLE;
    var rw = c.measureText(rt).width; c.fillText(rt, 862 - rw, 628);
    c.font = "bold 22px " + GOT;
    c.fillText("逆算設計型", 862 - rw - 12 - c.measureText("逆算設計型").width, 636);
    var x0 = 160, x1 = 864, by = 688, bh = 26;
    c.fillStyle = PURPLE; rr(x0, by, x1 - x0, bh, bh / 2); c.fill();
    var cut = x0 + Math.round((x1 - x0) * q / 100);
    if (cut > x0 + bh){ c.fillStyle = PINK; rr(x0, by, cut - x0, bh, bh / 2); c.fill(); }
    /* 3語 */
    var pw = 206, gap = 18, ph = 58, px0 = CX - (pw * 3 + gap * 2) / 2, py = 772;
    sd.stages.forEach(function(st, i){
      var t = st.split("｜")[0], x = px0 + i * (pw + gap), col;
      if (i === gi){
        var g = c.createLinearGradient(0, py, 0, py + ph);
        g.addColorStop(0, "#e4be70"); g.addColorStop(1, "#a2742a");
        c.fillStyle = g; rr(x, py, pw, ph, ph / 2); c.fill();
        c.strokeStyle = GOLD2; c.lineWidth = 2; rr(x, py, pw, ph, ph / 2); c.stroke();
        col = "#ffffff";
      } else {
        c.fillStyle = "#fdfaf3"; rr(x, py, pw, ph, ph / 2); c.fill();
        c.strokeStyle = "#e0cea9"; c.lineWidth = 2; rr(x, py, pw, ph, ph / 2); c.stroke();
        col = "#766a5a";
      }
      c.font = "bold 25px " + GOT; c.fillStyle = col;
      c.fillText(t, x + (pw - c.measureText(t).width) / 2, py + (ph - 33) / 2);
    });
    /* 締めの1文 */
    c.fillStyle = NAVY; rr(78, 886, 868, 300, 16); c.fill();
    c.strokeStyle = GOLD2; c.lineWidth = 1; rr(86, 894, 852, 284, 10); c.stroke();
    ctr("あなたの金脈を活かすと", 922, "25px " + MIN, GOLD2);
    line(148, 936, 348, 936, GOLD2, 1); line(676, 936, 876, 936, GOLD2, 1);
    var txt = shimeText(r, p), ls, size, lh;
    for (size = 42; size >= 24; size--){
      c.font = size + "px " + MIN; lh = Math.round(size * 1.62);
      var ch = txt.split("、"), parts = [], i;
      for (i = 0; i < ch.length; i++) parts.push(i < ch.length - 1 ? ch[i] + "、" : ch[i]);
      ls = []; var cur = "", over = false;
      for (i = 0; i < parts.length; i++){
        if (c.measureText(parts[i]).width > 744){ over = true; break; }
        if (cur && c.measureText(cur + parts[i]).width > 744){ ls.push(cur); cur = parts[i]; }
        else cur += parts[i];
      }
      if (over){ ls = []; cur = "";
        for (i = 0; i < txt.length; i++){
          if (cur && c.measureText(cur + txt[i]).width > 744){ ls.push(cur); cur = txt[i]; }
          else cur += txt[i];
        }
      }
      if (cur) ls.push(cur);
      if (ls.length * lh <= 198) break;
    }
    var yy = 962 + (198 - ls.length * lh) / 2;
    ls.forEach(function(t){ ctr(t, yy, size + "px " + MIN, CREAM); yy += lh; });
    /* QRと誘導 */
    c.drawImage(im[1], 236, 1256, 168, 168);
    c.strokeStyle = GOLD2; c.lineWidth = 2; rr(230, 1250, 180, 180, 8); c.stroke();
    c.font = "bold 29px " + GOT; c.fillStyle = NAVY; c.fillText("あなたも診断してみる", 442, 1286);
    c.font = "20px " + GOT; c.fillStyle = "#7c7060"; c.fillText("引き寄せ四柱推命 金脈編", 442, 1332);
    line(442, 1372, 772, 1372, GOLD2, 1);
    c.font = "18px " + GOT; c.fillStyle = GOLD; c.fillText("無料・生年月日だけで診断できます", 442, 1382);
    done(cv.toDataURL("image/png"));
  }).catch(fail);
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

  h += SEP + secHtml("WEAPON",  "あなたの武器",        D.buki[r.stem]);
  h += SEP + secHtml("SIGN",    "あなたの看板",        D.kanban[r.year]);
  h += SEP + seasonHtml(r.month);
  h += SEP + secHtml("WIN",     "稼ぐ時の勝ちパターン", D.kachi[r.month], extraHtml(r.month));
  h += SEP + secHtml("RECEIVE", "お金の受け取り方",    D.uketori[r.day]);
  h += '<div class="share"><div class="share-wrap" id="shareWrap">' +
       '<p class="share-load">シェア用の画像を作っています…</p></div></div>';
  h += SEMINAR;
  h += CTA;
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

function daysIn(y, m) {
  if (!y || !m) return 31;
  var leap = (y % 4 === 0 && y % 100 !== 0) || y % 400 === 0;
  return [31, leap ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1];
}
var hh = document.getElementById("hh");
// 時柱は出さないので、結果が変わるのは「23時台かどうか」だけ
hh.innerHTML = '<option value="" disabled selected>選択する</option>' +
  '<option value="unknown">わからない</option>' +
  '<option value="day">0:00 〜 22:59</option>' +
  '<option value="23">23:00 〜 23:59</option>';

function run(){
  var err = document.getElementById("err");
  var mm = (document.getElementById("bd").value || "").match(/(\d{4})\D*(\d{1,2})\D*(\d{1,2})/);
  if (!mm) { err.textContent = "生年月日を 1990/06/24 のように入れてください"; err.hidden = false; return; }
  var y = +mm[1], m = +mm[2], d = +mm[3];
  if (y < 1900 || y > 2030) { err.textContent = "1900年〜2030年で入れてください"; err.hidden = false; return; }
  if (m < 1 || m > 12 || d < 1 || d > daysIn(y, m)) { err.textContent = "その日付は存在しません"; err.hidden = false; return; }
  var hv = hh.value;
  if (!hv) { err.textContent = "生まれた時間を選んでください（わからない でも大丈夫です）"; err.hidden = false; return; }
  // 節入りの判定は正午でそろえる（23時台だけ翌日として扱う）
  var h = (hv === "23") ? 23 : null;
  err.hidden = true;
  var r = calcMoney(y, m, d, h), p = calcRatio(r);
  var out = document.getElementById("result");
  out.innerHTML = render(r); out.hidden = false;
  document.getElementById("form").hidden = true;
  window.scrollTo(0, 0);
  log(y, m, d, hv, r, p);
  var sw = document.getElementById("shareWrap");
  drawShare(r, p, function(url){
    if (!sw.isConnected) return;
    sw.innerHTML = '<img src="' + url + '" alt="あなたの金脈タイプ">' +
      '<p class="share-tip">画像を長押しすると保存できます 📱<br>SNSやLINEでシェアしてください ✨</p>' +
      '<div class="sl"><p class="sl-t">診断のリンク 🔗</p>' +
      '<code class="sl-url">' + APP_URL + '</code>' +
      '<button class="sl-btn" id="slCopy">リンクをコピーする 📋</button>' +
      '<p class="sl-note">画像と一緒に貼ると、見た人がそのまま診断できます 😊</p></div>';
    var cp = document.getElementById("slCopy");
    if (cp) cp.addEventListener("click", function(){ copyLink(cp); });
  }, function(){ sw.innerHTML = ""; });
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
           .replace("__ENGINE__", ENGINE).replace("__ENDPOINT__", LOG_ENDPOINT).replace("__APPURL__", APP_URL)
io.open(os.path.join(BASE, "index.html"), "w", encoding="utf-8").write(html)
print("生成: index.html", len(html), "文字")
