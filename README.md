# 引き寄せ四柱推命 金脈編

生年月日（と23時台かどうか）から、お金の流れを6枚のカードで解説する診断アプリ。

- 公開URL: https://noripi-meta.github.io/metaq-kinmyaku/
- 1ファイル完結（index.html）。外部読み込みなし
- 計算エンジンは MetaQ-uranai から移植（1900〜2030の全日で照合済み・不一致ゼロ）

## 直し方

文言は `data.py`、画面は `build.py` にあります。

```bash
python3 build.py     # index.html を作り直す
node verify.js       # 仕様書のテストケース＋全日照合
```

`_engine.js` は MetaQ-uranai/app.js から抜き出した四柱推命の計算部分です（手で編集しないこと）。
