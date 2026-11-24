# -*- coding: utf-8 -*-
import io, json, os, data
BASE = os.path.dirname(os.path.abspath(__file__))
ENGINE = io.open(os.path.join(BASE, "_engine.js"), encoding="utf-8").read()
APP_URL = "https://noripi-meta.github.io/metaq-kinmyaku/"   # シェア用に案内するリンク
LOG_ENDPOINT = "https://script.google.com/macros/s/AKfycbyy5ZLj9EREvMBEAwc3ljXZM5k1lVL-EELxUWYZXAjsCUkEZmOvzzx8p_To4hfvhB6Y/exec"   # 記録用GAS（スプレッドシートへ追記）
AUTH_ENDPOINT = "https://script.google.com/macros/s/AKfycbyEk0tnupchygK6NtYLF0bVjpHn-oE2lmlseGqmFWjI0E82lyi3rneojssRi1g6BlUaAg/exec"   # 読者確認GAS
MAG_URL = "https://www.reservestock.jp/subscribe/194781"   # メルマガ登録

D = {"gyakuStems":data.GYAKU_STEMS, "gyakuUns":data.GYAKU_UNS, "types":data.TYPES,
     "buki":data.BUKI, "kanban":data.KANBAN, "kachi":data.KACHI, "uketori":data.UKETORI,
     "seasons":data.SEASONS, "extra":data.EXTRA, "sdetail":data.SEASON_DETAIL,
     "shime":data.SHIME,
          "nedan":data.NEDAN, "first":data.FIRST,
     "tlong":data.TYPE_LONG, "slong":data.STAGE_LONG}

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
.ex{font-size:14px;line-height:1.8;
  background:#fff;border:1px solid var(--line);border-radius:14px;padding:11px 14px}
.ex b{display:inline-block;font-size:11px;font-weight:900;color:#fff;border-radius:999px;padding:3px 11px;
  white-space:nowrap;letter-spacing:.04em;margin-bottom:5px}
.ex span{display:block}
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
.sep{width:150px;height:1px;margin:17px auto 21px;border:none;
  background:linear-gradient(90deg,rgba(232,190,134,0),#E8BE86 50%,rgba(232,190,134,0))}
/* 登録版だけに出る行 */
.deep{margin-top:15px;background:linear-gradient(135deg,#FBF7FF,#FFF4F9);
  border:1px solid #EBDFF6;border-radius:17px;padding:15px 16px 13px}
.deep-t{margin:0 0 8px;font-size:12.5px;font-weight:900;letter-spacing:.09em;color:var(--lav)}
.deep p{margin:0 0 7px;font-size:14.5px;line-height:1.95;color:var(--ink)}
.deep p:last-child{margin-bottom:0}
.pri{display:grid;gap:9px;margin-top:14px}
.pri div{background:linear-gradient(135deg,#FFFBF3,#FFF6EC);border:1px solid #F0DCBC;border-radius:14px;
  padding:11px 14px;font-size:14px;line-height:1.9}
.pri b{display:block;font-size:12px;letter-spacing:.1em;color:#B5813A;margin-bottom:3px}
/* 鍵のかかったカード */
.lock{position:relative;margin:26px 0 12px;padding:30px 20px 24px;text-align:center;border-radius:28px;
  background:linear-gradient(155deg,#FFF3DC 0%,#FFE8F0 52%,#FFF1E2 100%);
  border:2.5px solid #E8BE86;box-shadow:0 14px 40px rgba(200,150,90,.28),0 0 0 6px rgba(255,243,224,.55)}
.lock-k{display:inline-block;margin:0 0 13px;padding:8px 22px;border-radius:999px;color:#fff;
  font-size:14px;font-weight:900;letter-spacing:.08em;
  background:linear-gradient(135deg,#E0A64C,#DB7FA4);box-shadow:0 5px 16px rgba(210,150,90,.42)}
.lock-t{margin:0 0 7px;font-size:23px;font-weight:900;line-height:1.55;color:var(--pink-d)}
.lock-s{margin:0 0 17px;font-size:14px;color:#7D6670;line-height:1.85}
.lock-l{display:grid;gap:8px;margin:0 0 19px;text-align:left}
.lock-l span{background:rgba(255,255,255,.82);border-radius:13px;
  padding:12px 15px;font-size:15px;font-weight:800;color:#8C7483}
.lock-l span::before{content:"🔒 ";font-weight:400}
.lock-l span.bonus{background:rgba(255,255,255,.52);font-size:14px;font-weight:700;color:#9A8392}
.lock-l span.bonus::before{content:"✨ "}
/* 「まだの方」「登録済みの方」の仕切り */
.lg-sec{display:flex;align-items:center;gap:11px;margin:24px 0 13px;
  font-size:12.5px;font-weight:900;letter-spacing:.08em;color:#A98A62}
.lg-sec::before,.lg-sec::after{content:"";flex:1 1 0;height:1px;background:#EAD6B8}
.lock-cta{display:block;width:100%;box-sizing:border-box;padding:17px 14px;border-radius:999px;
  color:#fff;font-size:17px;font-weight:900;text-decoration:none;line-height:1.4;
  background:linear-gradient(135deg,#F2A0BC,#DB7FA4);box-shadow:0 7px 20px rgba(219,127,164,.42)}
.lock-note{margin:11px 0 0;font-size:12.5px;line-height:1.9;color:var(--sub)}
.lg{display:grid;gap:9px}
.lg input{width:100%;padding:13px 14px;font-size:16px;border:1.5px solid var(--line);
  border-radius:13px;background:#fff;color:var(--ink);font-family:inherit}
.lg input:focus{outline:none;border-color:var(--gold)}
.lg-btn{width:100%;padding:14px;border:none;border-radius:999px;color:#fff;font-size:16px;
  font-weight:900;font-family:inherit;cursor:pointer;
  background:linear-gradient(135deg,#E8BE86,#D79F5C);box-shadow:0 6px 18px rgba(200,150,90,.35)}
.lg-btn:disabled{opacity:.55}
.lg-msg{margin:2px 0 0;font-size:13.5px;line-height:1.8;color:var(--pink-d)}
.lg-help{margin:12px 0 0;font-size:12.5px;line-height:1.85;color:var(--sub)}
.lg-help a{color:var(--pink-d)}
/* セミナー案内は紫系。金色の「鍵のカード」と一目で別物に見えるようにしている */
.sem{position:relative;margin:30px 0 12px;padding:34px 22px 26px;text-align:center;border-radius:28px;
  background:linear-gradient(155deg,#F4EFFF 0%,#EBE4FD 50%,#F6F1FF 100%);
  border:2.5px solid #B9A2E6;box-shadow:0 14px 40px rgba(126,90,196,.24),0 0 0 6px rgba(238,231,255,.6)}
.sem-free{display:inline-block;margin:0 0 15px;padding:9px 24px;border-radius:999px;color:#fff;
  font-size:16px;font-weight:900;letter-spacing:.1em;
  background:linear-gradient(135deg,#9A7BE0,#6F5AC8);box-shadow:0 5px 16px rgba(118,86,186,.42)}
.sem-date{margin:0 0 14px;font-size:14px;font-weight:800;letter-spacing:.06em;color:#6E57B4}
.sem-t{margin:0 0 12px;font-size:21px;font-weight:900;line-height:1.65;color:#5B43A4}
.sem-b{margin:0 0 17px;font-size:14.5px;line-height:1.95;color:#574A70}
.sem-pts{display:grid;gap:7px;margin:0 0 15px}
.sem-pt{background:rgba(255,255,255,.82);border-radius:13px;padding:9px 12px;font-size:13.5px;
  line-height:1.7;color:#5E5272}
.sem-hot{display:grid;gap:6px;margin:0 0 20px}
/* 急ぎの2行だけ、紫の中でピンクにして目立たせる */
.sem-hot span{background:#FFF1F6;border:1px dashed #EE9BB8;border-radius:13px;padding:9px 12px;
  font-size:13px;font-weight:700;line-height:1.7;color:#C8426F}
.sem-btn{display:block;width:100%;box-sizing:border-box;padding:20px 20px;border-radius:24px;
  background:linear-gradient(180deg,#A185E8,#6B4CC4);color:#fff;text-decoration:none;font-weight:bold;
  font-size:18px;letter-spacing:.08em;box-shadow:0 6px 0 #533A9C,0 16px 30px rgba(83,58,156,.32)}
.sem-btn:active{transform:translateY(4px);box-shadow:0 2px 0 #533A9C}
.sem-note{margin:18px 0 0;font-size:11.5px;line-height:1.9;color:#8B7FA3;text-align:left}
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
var AUTH_ENDPOINT = "__AUTH__";
var MAG_URL = "__MAGURL__";
/* ── 登録版の鍵。確認できた人のメアドだけを、その端末に覚えておく ── */
var MKEY = "mk_member";
function memberMail(){ try { return localStorage.getItem(MKEY) || ""; } catch (e) { return ""; } }
function setMember(m){ try { localStorage.setItem(MKEY, m); } catch (e) { /* 保存できなくても今回は見られる */ } }
var UNLOCKED = !!memberMail();
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
function lockHtml(){
  return '<div class="lock">' +
    '<p class="lock-k">ここから先は メルマガ読者さま限定 🔑</p>' +
    '<p class="lock-t">もっと詳しく見たい方へ</p>' +
    '<p class="lock-s">鍵のかかっている3つが、そのまま開きます ✨</p>' +
    '<div class="lock-l"><span>あなたの武器</span><span>稼ぐ時の勝ちパターン</span>' +
      '<span>お金の受け取り方</span>' +
      '<span class="bonus">シェア画像が「金脈鑑定書」に変わります</span></div>' +
    '<p class="lg-sec">メルマガがまだの方</p>' +
    '<a class="lock-cta" href="'+MAG_URL+'" target="_blank" rel="noopener">無料で登録して、続きを見る 💌</a>' +
    '<p class="lock-note">のりぴのメルマガ「宇宙×IQ 引き寄せロジック」に登録すると、<br>' +
    'そのあとすぐ、この先が開きます。登録は無料です。</p>' +
    '<p class="lg-sec">すでに登録している方</p>' +
    '<div class="lg">' +
      '<input id="lgMail" type="email" inputmode="email" autocomplete="email" placeholder="メールアドレス">' +
      '<button class="lg-btn" id="lgGo">詳しい版を見る ✨</button>' +
      '<p class="lg-msg" id="lgMsg"></p>' +
    '</div>' +
    '<p class="lock-note">メルマガを受け取っているアドレスを入れてください。<br>' +
    '一度入れれば、次からはそのまま開きます 😊</p>' +
    '</div>';
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
    '<div class="note">' + (UNLOCKED
        ? D.tlong[s.label].map(function(x){ return esc(x); }).join("<br>")
        : esc(d.flow)) + '</div>' +
    '<div class="stages">'+strip+'</div>' +
    '<div class="st-now">あなたは<b>「'+esc(now[0])+'」</b>── '+esc(now[1])+'</div>' +
    (UNLOCKED ? '<div class="deep"><p class="deep-t">「'+esc(now[0])+'」とは</p>' +
      D.slong[un].map(function(x){ return '<p>'+esc(x)+'</p>'; }).join("") + '</div>' : '') +
    (UNLOCKED ? '<div class="pri">' +
      '<div><b>値段の決め方</b>'+esc(D.nedan[s.label])+'</div>' +
      '<div><b>最初の1件</b>'+esc(D.first[s.label])+'</div></div>' : '') +
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
  '<p class="sem-t">目標設定が苦手な人のための<br>願望実現セミナー ✨</p>' +
  '<p class="sem-b">臨機応変型が50%以上の方に向けた<br>90分のオンラインセミナーです 💝</p>' +
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
var SEP = '<div class="sep"></div>';
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
    ctrSp("のりぴの", 216, "bold 22px " + GOT, GOLD, 6);
    ctr("引き寄せ四柱推命", 254, "44px " + MIN, NAVY);
    var bt = "金脈編", bfs = 28, bh2 = 50, byy = 322;
    c.font = bfs + "px " + MIN;
    var bw = Math.round(c.measureText(bt).width) + 72, bx = CX - bw / 2;
    var bg2 = c.createLinearGradient(0, byy, 0, byy + bh2);
    bg2.addColorStop(0, "#e4be70"); bg2.addColorStop(1, "#a2742a");
    c.fillStyle = bg2; rr(bx, byy, bw, bh2, bh2 / 2); c.fill();
    c.strokeStyle = GOLD2; c.lineWidth = 2; rr(bx, byy, bw, bh2, bh2 / 2); c.stroke();
    c.fillStyle = "#ffffff"; c.fillText(bt, CX - c.measureText(bt).width / 2, byy + (bh2 - bfs * 1.42) / 2);
    /* タイプ名 */
    var se = D.seasons[seasonOf(r.month)], sd = D.sdetail[se.label], gi = se.uns.indexOf(r.month);
    ctrSp("あなたの金脈タイプ", 398, "bold 26px " + GOT, GOLD, 2);
    ctr(se.label, 430, "118px " + MIN, PINK);
    ctrSp(sd.sub, 578, "bold 35px " + GOT, GOLD, 3);
    /* 割合 */
    var q = 100 - p;
    c.font = "bold 22px " + GOT; c.fillStyle = PINK;
    c.fillText("臨機応変型", 162, 640);
    var lw = c.measureText("臨機応変型").width;
    c.font = "34px " + MIN; c.fillText(q + "%", 162 + lw + 12, 632);
    var rt = p + "%"; c.font = "34px " + MIN; c.fillStyle = PURPLE;
    var rw = c.measureText(rt).width; c.fillText(rt, 862 - rw, 632);
    c.font = "bold 22px " + GOT;
    c.fillText("逆算設計型", 862 - rw - 12 - c.measureText("逆算設計型").width, 640);
    var x0 = 160, x1 = 864, by = 692, bh = 26;
    c.fillStyle = PURPLE; rr(x0, by, x1 - x0, bh, bh / 2); c.fill();
    var cut = x0 + Math.round((x1 - x0) * q / 100);
    if (cut > x0 + bh){ c.fillStyle = PINK; rr(x0, by, cut - x0, bh, bh / 2); c.fill(); }
    /* 3語 */
    var pw = 206, gap = 18, ph = 58, px0 = CX - (pw * 3 + gap * 2) / 2, py = 776;
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
    c.font = "20px " + GOT; c.fillStyle = "#7c7060"; c.fillText("のりぴの 引き寄せ四柱推命 金脈編", 442, 1332);
    line(442, 1372, 772, 1372, GOLD2, 1);
    c.font = "18px " + GOT; c.fillStyle = GOLD; c.fillText("無料・生年月日だけで診断できます", 442, 1382);
    done(cv.toDataURL("image/png"));
  }).catch(fail);
}
/* ── 金脈鑑定書（登録版のシェア画像。1024x1536の紺地） ── */
// 「、。」の区切りで折り返す。割れなくなったら諦めてそのまま出す（無限ループよけ）
function wrapKu(c, txt, mw){
  var ch = [], cur = "", i;
  for (i = 0; i < txt.length; i++){
    cur += txt[i];
    if (txt[i] === "、" || txt[i] === "。"){ ch.push(cur); cur = ""; }
  }
  if (cur) ch.push(cur);
  function byChar(t){
    var o = [], s = "", j;
    for (j = 0; j < t.length; j++){
      if (s && c.measureText(s + t[j]).width > mw){ o.push(s); s = t[j]; } else s += t[j];
    }
    if (s) o.push(s);
    return o;
  }
  var out = []; cur = "";
  for (i = 0; i < ch.length; i++){
    if (cur && c.measureText(cur + ch[i]).width > mw){ out.push(cur); cur = ch[i]; }
    else cur += ch[i];
    while (c.measureText(cur).width > mw){
      var w = byChar(cur);
      if (w.length < 2) break;
      out = out.concat(w.slice(0, -1)); cur = w[w.length - 1];
    }
  }
  if (cur) out.push(cur);
  return out;
}
function drawKantei(r, p, done, fail){
  Promise.all([loadImg("kantei_bg.jpg"), loadImg("share_qr.png")]).then(function(im){
    var W = 1024, H = 1536, CX = 512;
    var cv = document.createElement("canvas"); cv.width = W; cv.height = H;
    var c = cv.getContext("2d");
    c.drawImage(im[0], 0, 0, W, H);
    c.textBaseline = "top";
    var NAVY = "#1a2b4a", GOLD = "#d6b26a", GOLD2 = "#b08a46", CREAM = "#faf5e8",
        PINK = "#ec78a0", PURPLE = "#967aec", INK = "#342e26", LAV = "#7656ba";
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
    var se = D.seasons[seasonOf(r.month)], sd = D.sdetail[se.label], gi = se.uns.indexOf(r.month);
    var now0 = sd.stages[gi].split("｜")[0];

    /* 鑑定書の見出し */
    ctrSp("のりぴの 引き寄せ四柱推命", 96, "22px " + GOT, GOLD, 6);
    line(362, 138, 662, 138, GOLD2, 1);
    ctr("金 脈 鑑 定 書", 160, "56px " + MIN, GOLD);
    line(362, 238, 662, 238, GOLD2, 1);

    /* タイプ */
    ctrSp("あなたの金脈タイプ", 262, "bold 21px " + GOT, GOLD2, 4);
    ctr(se.label, 296, "92px " + MIN, CREAM);
    ctrSp(sd.sub, 414, "bold 28px " + GOT, GOLD, 3);

    /* 4タイプの解説 */
    c.font = "24px " + GOT;
    var yy = 470, tl = D.tlong[se.label];
    tl.forEach(function(t){
      wrapKu(c, t, 800).forEach(function(ln){ ctr(ln, yy, "24px " + GOT, CREAM); yy += 36; });
    });

    /* 割合バー */
    var BY = yy + 20, q = 100 - p;
    c.font = "bold 22px " + GOT; c.fillStyle = PURPLE;
    c.fillText("逆算設計型 " + p + "%", 136, BY);
    c.fillStyle = PINK;
    var rt = "臨機応変型 " + q + "%";
    c.fillText(rt, 888 - c.measureText(rt).width, BY);
    c.fillStyle = PINK; rr(136, BY + 44, 752, 20, 10); c.fill();
    var cut = Math.round(752 * p / 100);
    if (cut > 20){ c.fillStyle = PURPLE; rr(136, BY + 44, cut, 20, 10); c.fill(); }

    /* 3語 */
    var pw = 216, gap = 20, ph = 50, py = BY + 90, px0 = CX - (pw * 3 + gap * 2) / 2;
    sd.stages.forEach(function(st, i){
      var t = st.split("｜")[0], x = px0 + i * (pw + gap);
      if (i === gi){
        c.fillStyle = GOLD; rr(x, py, pw, ph, ph / 2); c.fill();
        c.font = "bold 25px " + GOT; c.fillStyle = NAVY;
      } else {
        c.strokeStyle = GOLD2; c.lineWidth = 2; rr(x, py, pw, ph, ph / 2); c.stroke();
        c.font = "25px " + GOT; c.fillStyle = GOLD;
      }
      c.fillText(t, x + (pw - c.measureText(t).width) / 2, py + (ph - 33) / 2);
    });

    /* 「○○」とは（アイボリーの紙） */
    var TOP = py + ph + 26, PW = 824, PX = CX - PW / 2, IW = PW - 80;
    var sl = D.slong[r.month], packed = [];
    c.font = "24px " + GOT;
    sl.forEach(function(t){ packed.push(wrapKu(c, t, IW)); });
    var nL = 0; packed.forEach(function(a){ nL += a.length; });
    var PH = 52 + nL * 38 + 6 * (packed.length - 1) + 18;
    c.fillStyle = CREAM; rr(PX, TOP, PW, PH, 20); c.fill();
    c.strokeStyle = GOLD2; c.lineWidth = 2; rr(PX, TOP, PW, PH, 20); c.stroke();
    ctrSp("「" + now0 + "」とは", TOP + 18, "bold 24px " + GOT, LAV, 3);
    yy = TOP + 58;
    packed.forEach(function(a){
      a.forEach(function(ln){ ctr(ln, yy, "24px " + GOT, INK); yy += 38; });
      yy += 6;
    });

    /* お金の流れ（紺の額に二重罫） */
    var txt = shimeText(r, p);
    c.font = "34px " + MIN;
    var ls = wrapKu(c, txt, 680), lh = 50;
    var FY = TOP + PH + 40, FH = 44 + ls.length * lh + 24;
    c.fillStyle = "#0e1b34"; rr(PX, FY, PW, FH, 18); c.fill();
    c.strokeStyle = GOLD; c.lineWidth = 3; rr(PX, FY, PW, FH, 18); c.stroke();
    c.strokeStyle = GOLD2; c.lineWidth = 1; rr(PX + 10, FY + 10, PW - 20, FH - 20, 12); c.stroke();
    var lab = "あなたのお金の流れ", lsp = 5;
    c.font = "bold 19px " + GOT;
    var lw = 0, k; for (k = 0; k < lab.length; k++) lw += c.measureText(lab[k]).width + lsp;
    lw = lw - lsp + 52;
    c.fillStyle = GOLD; rr(CX - lw / 2, FY - 19, lw, 38, 19); c.fill();
    ctrSp(lab, FY - 8, "bold 19px " + GOT, "#162440", lsp);
    yy = FY + 44;
    ls.forEach(function(t){ ctr(t, yy, "34px " + MIN, CREAM); yy += lh; });

    /* QR */
    var QY = FY + FH + 36;
    c.drawImage(im[1], 212, QY, 132, 132);
    c.strokeStyle = GOLD2; c.lineWidth = 2; rr(206, QY - 6, 144, 144, 8); c.stroke();
    c.font = "bold 25px " + GOT; c.fillStyle = CREAM;
    c.fillText("あなたも診断してみる", 382, QY + 14);
    c.font = "17px " + GOT; c.fillStyle = GOLD2;
    c.fillText("のりぴの 引き寄せ四柱推命 金脈編", 382, QY + 54);
    line(382, QY + 88, 716, QY + 88, GOLD2, 1);
    c.fillText("無料・生年月日だけで診断できます", 382, QY + 98);

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

  if (UNLOCKED) h += SEP + secHtml("WEAPON", "あなたの武器", D.buki[r.stem]);
  h += SEP + secHtml("SIGN", "あなたの看板", D.kanban[r.year]);
  h += SEP + seasonHtml(r.month);
  if (UNLOCKED) {
    h += SEP + secHtml("WIN",     "稼ぐ時の勝ちパターン", D.kachi[r.month], extraHtml(r.month));
    h += SEP + secHtml("RECEIVE", "お金の受け取り方",    D.uketori[r.day]);
  }
  h += '<div class="share"><div class="share-wrap" id="shareWrap">' +
       '<p class="share-load">シェア用の画像を作っています…</p></div></div>';
  if (!UNLOCKED) h += lockHtml();
  h += SEMINAR;
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
  LAST = { r: r, p: p };
  document.getElementById("form").hidden = true;
  window.scrollTo(0, 0);
  log(y, m, d, hv, r, p);
  show(r, p);
}
/* 結果を描く。ログインで鍵が開いた時も、ここをもう一度通る */
var LAST = null;
function show(r, p){
  var out = document.getElementById("result");
  out.innerHTML = render(r); out.hidden = false;
  var sw = document.getElementById("shareWrap");
  (UNLOCKED ? drawKantei : drawShare)(r, p, function(url){
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
  var lg = document.getElementById("lgGo");
  if (lg) lg.addEventListener("click", doLogin);
  document.getElementById("again").addEventListener("click", function(){
    out.hidden = true; out.innerHTML = "";
    document.getElementById("form").hidden = false; window.scrollTo(0, 0);
  });
}
/* メアドを送って、メルマガ読者かどうかGASに確かめてもらう */
function doLogin(){
  var em  = (document.getElementById("lgMail").value || "").trim();
  var msg = document.getElementById("lgMsg");
  var btn = document.getElementById("lgGo");
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(em)) { msg.textContent = "メールアドレスを確かめてください"; return; }
  if (!AUTH_ENDPOINT) { msg.textContent = "ただいま準備中です。少しお待ちください"; return; }
  btn.disabled = true; msg.textContent = "確認しています…";
  fetch(AUTH_ENDPOINT, { method:"POST", headers:{"Content-Type":"text/plain;charset=utf-8"},
                         body: JSON.stringify({ email: em }) })
    .then(function(res){ return res.json(); })
    .then(function(j){
      if (j && j.ok) { setMember(em); UNLOCKED = true; show(LAST.r, LAST.p); window.scrollTo(0, 0); }
      else { btn.disabled = false; msg.textContent = (j && j.msg) || "確認できませんでした"; }
    })
    .catch(function(){ btn.disabled = false;
      msg.textContent = "つながりませんでした。少し待ってから、もう一度お試しください"; });
}
document.getElementById("go").addEventListener("click", run);
window.__money = { calcMoney: calcMoney, calcRatio: calcRatio, render: render };
})();
</script>
</body>
</html>
"""
html = HTML.replace("__DATA__", json.dumps(D, ensure_ascii=False)) \
           .replace("__ENGINE__", ENGINE).replace("__ENDPOINT__", LOG_ENDPOINT).replace("__APPURL__", APP_URL) \
           .replace("__AUTH__", AUTH_ENDPOINT).replace("__MAGURL__", MAG_URL)
io.open(os.path.join(BASE, "index.html"), "w", encoding="utf-8").write(html)
print("生成: index.html", len(html), "文字")
