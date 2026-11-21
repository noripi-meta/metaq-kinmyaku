  const JIKKAN = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"];
  const JUNISHI = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"];
  const YINYANG = {"甲":1,"乙":-1,"丙":1,"丁":-1,"戊":1,"己":-1,"庚":1,"辛":-1,"壬":1,"癸":-1};
  const JUNIUN_NAMES = ["長生","沐浴","冠帯","建禄","帝旺","衰","病","死","墓","絶","胎","養"];
  const CHANGSHENG_BRANCH = {
    "甲":"亥","乙":"午","丙":"寅","丁":"酉","戊":"寅",
    "己":"酉","庚":"巳","辛":"子","壬":"申","癸":"卯"
  };

  const MONTH_BRANCH_ORDER = ["寅","卯","辰","巳","午","未","申","酉","戌","亥","子","丑"];
  const WUHU_DUN  = {0:2,5:2, 1:4,6:4, 2:6,7:6, 3:8,8:8, 4:0,9:0};   // 月干用(五虎遁)
  function toJulianDay(y, m, d, h) {
    let yy = y, mm = m;
    if (mm <= 2) { yy -= 1; mm += 12; }
    const A = Math.floor(yy / 100);
    // グレゴリオ暦への切替(1582/10/15)より前の日付は、歴史資料上ユリウス暦で
    // 記録されているのが通例のため、ユリウス暦として扱う(Meeusの標準的な方法)。
    // これを分けないと、切替前の日付(織田信長など)の日柱が約10日ズレる。
    const isGregorian = (y > 1582) || (y === 1582 && (m > 10 || (m === 10 && d >= 15)));
    const B = isGregorian ? (2 - A + Math.floor(A / 4)) : 0;
    const jd = Math.floor(365.25 * (yy + 4716)) + Math.floor(30.6001 * (mm + 1)) + d + B - 1524.5;
    return jd + (h / 24.0);
  }

  // ---------- 太陽黄経（簡易高精度式、誤差最大約20秒角） ----------
  function sunLongitude(jd) {
    const T = (jd - 2451545.0) / 36525.0;
    const L0 = 280.46646 + 36000.76983 * T + 0.0003032 * T * T;
    const M = 357.52911 + 35999.05029 * T - 0.0001537 * T * T;
    const Mrad = M * Math.PI / 180;
    const C = (1.914602 - 0.004817 * T - 0.000014 * T * T) * Math.sin(Mrad)
            + (0.019993 - 0.000101 * T) * Math.sin(2 * Mrad)
            + 0.000289 * Math.sin(3 * Mrad);
    const trueLong = L0 + C;
    const omega = 125.04 - 1934.136 * T;
    let lam = trueLong - 0.00569 - 0.00478 * Math.sin(omega * Math.PI / 180);
    lam = lam % 360;
    if (lam < 0) lam += 360;
    return lam;
  }

  // ---------- 日柱 ----------
  const REF_JD = toJulianDay(1900, 1, 31, 0); // 1900-01-31 = 甲辰
  const REF_INDEX = 40;

  function dayIndex(y, m, d) {
    const jd = toJulianDay(y, m, d, 0);
    const delta = Math.round(jd - REF_JD);
    let idx = (REF_INDEX + delta) % 60;
    if (idx < 0) idx += 60;
    return idx;
  }

  // ---------- 月柱 ----------
  function monthBranchIndex(longitude) {
    let shifted = (longitude - 315) % 360;
    if (shifted < 0) shifted += 360;
    const block = Math.floor(shifted / 30);
    return JUNISHI.indexOf(MONTH_BRANCH_ORDER[block]);
  }

  function monthStemIndex(yearStemIdx, monthBranchIdx) {
    const startStem = WUHU_DUN[yearStemIdx];
    const posInCycle = MONTH_BRANCH_ORDER.indexOf(JUNISHI[monthBranchIdx]);
    return (startStem + posInCycle) % 10;
  }

  // ---------- 年柱（立春基準） ----------
  function findLichunDate(y) {
    // 月柱の節入り判定(正午基準)と同じ基準で立春日を探す。
    // 深夜0時基準だと立春が午前に来る年に年の切替が1日遅れ、月柱とズレる。
    for (let i = 0; i < 6; i++) {
      const dt = new Date(y, 1, 2 + i); // 2/2始まりで探索
      const jd = toJulianDay(dt.getFullYear(), dt.getMonth() + 1, dt.getDate(), 12);
      const lon = sunLongitude(jd);
      if (lon >= 315) return dt;
    }
    return new Date(y, 1, 4);
  }

  function yearGanzhiIndex(y, m, d) {
    const lichun = findLichunDate(y);
    const target = new Date(y, m - 1, d);
    const effYear = (target >= lichun) ? y : y - 1;
    let idx = (effYear - 4) % 60;
    if (idx < 0) idx += 60;
    return { idx, effYear };
  }

  // ---------- 時柱 ----------
  function hourBranchIndex(hour, minute) {
    const totalMin = hour * 60 + minute;
    let shifted = (totalMin - 23 * 60 + 24 * 60) % (24 * 60); // 23:00を子の開始とする
    return Math.floor(shifted / 120) % 12;
  }

  function hourStemIndex(dayStemIdx, hourBranchIdx) {
    const ziStem = WUSHU_DUN[dayStemIdx];
    return (ziStem + hourBranchIdx) % 10;
  }

  // ---------- 十二運 ----------
  function juniunFor(dayStem, branchIdx) {
    const startBranch = JUNISHI.indexOf(CHANGSHENG_BRANCH[dayStem]);
    const isYang = YINYANG[dayStem] === 1;
    let pos;
    if (isYang) pos = (branchIdx - startBranch + 12) % 12;
    else pos = (startBranch - branchIdx + 12) % 12;
    return JUNIUN_NAMES[pos];
  }

  // ---------- 月律分野蔵干表（レール計算用） ----------
  // のりぴさんから提供された65件の実例から逆算して確定(64/65件一致、99%)。
  // 各支について [蔵干, 節入りからの累積経過日数(1始まり)の上限] のペア。
  // 子はサンプルが無く一般的配分で仮置き(将来サンプルが増えれば調整可能)。