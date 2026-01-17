import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Vocalytics AI",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800&display=swap');

.stApp{
  background: radial-gradient(circle at top left, #151824, #06070a);
  color:#eef1f6;
  font-family:'Plus Jakarta Sans',sans-serif;
}
.block-container{ padding: 2.6rem 4.2rem; }

.main-title{
  font-size: 2.4rem;
  font-weight: 800;
  letter-spacing: -1px;
  margin: 0 0 6px 0;
  background: linear-gradient(90deg,#ffffff 0%, #b6f4ff 45%, #00f2fe 100%);
  -webkit-background-clip:text;
  -webkit-text-fill-color:transparent;
}
.sub-title{
  color: rgba(255,255,255,.55);
  font-size:.78rem;
  text-transform:uppercase;
  letter-spacing:2.6px;
  margin: 0 0 28px 0;
}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">The Vocal Viz</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Neural Spectrometry & Feature Extraction</div>',
    unsafe_allow_html=True,
)

vocalytics_2026_html = r"""
<div class="vx-shell">
  <div class="vx-topbar">
    <div class="vx-brand">
      <div class="vx-mark"></div>
      <div class="vx-brandtext">
        <div class="vx-name">Vocalytics</div>
        <div class="vx-desc">Realtime audio compare + feature readout</div>
      </div>
    </div>

    <div class="vx-actions">
      <div class="vx-inline">
        <span class="vx-inline-label">Compare</span>
        <label class="vx-switch" title="Overlay A vs B sparklines">
          <input type="checkbox" id="compareToggle"/>
          <span class="vx-slider"></span>
        </label>
      </div>

      <div class="vx-inline" title="Mic noise gate threshold (dB). Higher = more gating.">
        <span class="vx-inline-label">Gate</span>
        <input id="gateSlider" class="vx-range" type="range" min="-60" max="0" step="1" value="-50"/>
        <span id="gateVal" class="vx-inline-val">-50 dB</span>
      </div>

      <button class="vx-btn vx-btn-ghost" id="swapBtn" title="Swap A/B">Swap</button>
      <button class="vx-btn vx-btn-ghost" id="resetBtn" title="Reset analysis">Reset</button>
      <button class="vx-btn vx-btn-ghost" id="snapBtn" title="Download canvas snapshot">Snapshot</button>
      <button class="vx-btn vx-btn-primary" id="fsBtn" title="Fullscreen active canvas">Fullscreen</button>
    </div>
  </div>

  <div class="vx-grid">
    <!-- Panel A -->
    <section class="vx-panel" data-panel="0">
      <header class="vx-panel-h">
        <div class="vx-left">
          <span class="vx-pill vx-pill-dot vx-red"><i></i>Reference A</span>
          <span class="vx-status" id="stA">Ready</span>
        </div>

        <div class="vx-right">
          <label class="vx-filebtn">
            Upload
            <input type="file" id="f1" accept="audio/*" />
          </label>
          <button class="vx-btn vx-btn-ghost vx-sm" id="playA" disabled>Play</button>
          <button class="vx-btn vx-btn-ghost vx-sm" id="pauseA" disabled>Pause</button>
        </div>
      </header>

      <div class="vx-canvas-wrap">
        <canvas id="c1"></canvas>
        <div class="vx-canvas-overlay">
          <div class="vx-overlay-title">Spectrogram</div>
          <div class="vx-overlay-sub">Source: Reference A</div>
        </div>
      </div>

      <div class="vx-player" id="p1"></div>
    </section>

    <!-- Panel B -->
    <section class="vx-panel" data-panel="1">
      <header class="vx-panel-h">
        <div class="vx-left">
          <span class="vx-pill vx-pill-dot vx-cyan"><i></i>Input B</span>
          <span class="vx-status" id="stB">Ready</span>
        </div>

        <div class="vx-right">
          <button class="vx-btn vx-btn-ghost vx-sm" id="mBtn">Mic</button>
          <label class="vx-filebtn">
            Upload
            <input type="file" id="f2" accept="audio/*" />
          </label>
          <button class="vx-btn vx-btn-ghost vx-sm" id="playB" disabled>Play</button>
          <button class="vx-btn vx-btn-ghost vx-sm" id="pauseB" disabled>Pause</button>
        </div>
      </header>

      <div class="vx-canvas-wrap">
        <canvas id="c2"></canvas>
        <div class="vx-canvas-overlay">
          <div class="vx-overlay-title">Spectrogram</div>
          <div class="vx-overlay-sub">Source: Live / Upload</div>
        </div>
      </div>

      <div class="vx-player" id="p2"></div>
    </section>
  </div>

  <div class="vx-metrics">
    <div class="vx-card">
      <div class="vx-card-top">
        <div class="vx-k">Spectral centroid</div>
        <div class="vx-badge">Timbre</div>
      </div>

      <div class="vx-row">
        <div id="sc_val" class="vx-v">0 Hz</div>
        <div id="sc_cmp" class="vx-cmp" style="display:none;">A: 0 Hz</div>
      </div>

      <div class="vx-spark-wrap" id="sc_spark_wrap" style="display:none;">
        <canvas id="sp_sc" class="vx-spark" height="28"></canvas>
        <div class="vx-spark-legend">
          <span class="vx-leg vx-leg-a">A</span>
          <span class="vx-leg vx-leg-b">B</span>
        </div>
      </div>

      <div class="vx-hint">Higher = brighter sound</div>
    </div>

    <div class="vx-card">
      <div class="vx-card-top">
        <div class="vx-k">RMS power</div>
        <div class="vx-badge">Energy</div>
      </div>

      <div class="vx-row">
        <div id="rms_val" class="vx-v">0 dB</div>
        <div id="rms_cmp" class="vx-cmp" style="display:none;">A: 0 dB</div>
      </div>

      <div class="vx-spark-wrap" id="rms_spark_wrap" style="display:none;">
        <canvas id="sp_rms" class="vx-spark" height="28"></canvas>
        <div class="vx-spark-legend">
          <span class="vx-leg vx-leg-a">A</span>
          <span class="vx-leg vx-leg-b">B</span>
        </div>
      </div>

      <div class="vx-hint">Tracks loudness stability</div>
    </div>

    <div class="vx-card">
      <div class="vx-card-top">
        <div class="vx-k">Clarity ratio</div>
        <div class="vx-badge">Signal</div>
      </div>

      <div class="vx-row">
        <div id="sr_val" class="vx-v">0 %</div>
        <div id="sr_cmp" class="vx-cmp" style="display:none;">A: 0 %</div>
      </div>

      <div class="vx-spark-wrap" id="sr_spark_wrap" style="display:none;">
        <canvas id="sp_sr" class="vx-spark" height="28"></canvas>
        <div class="vx-spark-legend">
          <span class="vx-leg vx-leg-a">A</span>
          <span class="vx-leg vx-leg-b">B</span>
        </div>
      </div>

      <div class="vx-hint">Proxy for harmonic definition</div>
    </div>
  </div>
</div>

<style>
  :root{
    --vx-bg: rgba(255,255,255,.03);
    --vx-bd: rgba(255,255,255,.09);
    --vx-bd2: rgba(255,255,255,.06);
    --vx-tx: rgba(255,255,255,.92);
    --vx-sub: rgba(255,255,255,.55);
    --vx-sub2: rgba(255,255,255,.42);
    --vx-shadow: 0 18px 55px rgba(0,0,0,.45);
    --vx-r: 22px;
  }

  .vx-shell{ width: 100%; }

  .vx-topbar{
    display:flex;
    justify-content:space-between;
    align-items:center;
    gap:16px;
    padding: 14px 14px;
    margin: 0 0 18px 0;
    border: 1px solid var(--vx-bd2);
    background: linear-gradient(180deg, rgba(255,255,255,.05), rgba(255,255,255,.025));
    border-radius: 18px;
    backdrop-filter: blur(10px);
  }

  .vx-brand{ display:flex; align-items:center; gap:12px; min-width: 260px; }
  .vx-mark{
    width: 34px; height: 34px; border-radius: 12px;
    background: radial-gradient(circle at 35% 30%, rgba(0,242,254,.85), rgba(255,255,255,.08));
    border: 1px solid rgba(255,255,255,.12);
    box-shadow: 0 12px 25px rgba(0,242,254,.08);
  }
  .vx-name{ font-weight: 800; letter-spacing: -.3px; color: var(--vx-tx); font-size: 14px; line-height: 1; }
  .vx-desc{ color: var(--vx-sub2); font-size: 11px; margin-top: 2px; }

  .vx-actions{ display:flex; gap:12px; flex-wrap:wrap; justify-content:flex-end; align-items:center; }

  .vx-inline{
    display:flex;
    align-items:center;
    gap:10px;
    padding: 7px 10px;
    border-radius: 999px;
    border: 1px solid rgba(255,255,255,.08);
    background: rgba(255,255,255,.03);
  }
  .vx-inline-label{
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.6px;
    text-transform: uppercase;
    color: rgba(255,255,255,.62);
  }
  .vx-inline-val{
    font-size: 12px;
    font-weight: 700;
    color: rgba(255,255,255,.78);
    min-width: 60px;
    text-align: right;
    font-variant-numeric: tabular-nums;
  }

  /* Toggle switch */
  .vx-switch{ position:relative; display:inline-block; width: 44px; height: 24px; }
  .vx-switch input{ opacity:0; width:0; height:0; }
  .vx-slider{
    position:absolute; cursor:pointer; inset:0;
    background: rgba(255,255,255,.10);
    border: 1px solid rgba(255,255,255,.10);
    transition: .18s ease;
    border-radius: 999px;
  }
  .vx-slider:before{
    position:absolute; content:"";
    height: 18px; width: 18px;
    left: 3px; top: 2px;
    background: rgba(255,255,255,.85);
    transition: .18s ease;
    border-radius: 50%;
  }
  .vx-switch input:checked + .vx-slider{
    background: rgba(0,242,254,.25);
    border-color: rgba(0,242,254,.35);
  }
  .vx-switch input:checked + .vx-slider:before{
    transform: translateX(20px);
    background: rgba(0,0,0,.85);
  }

  /* Range slider */
  .vx-range{
    width: 130px;
    accent-color: #00f2fe;
  }

  .vx-grid{
    display:grid;
    grid-template-columns: 1fr 1fr;
    gap: 18px;
    margin-bottom: 18px;
  }

  .vx-panel{
    background: var(--vx-bg);
    border: 1px solid var(--vx-bd2);
    border-radius: var(--vx-r);
    padding: 14px;
    box-shadow: var(--vx-shadow);
    backdrop-filter: blur(10px);
    position: relative;
    overflow: hidden;
  }

  .vx-panel:before{
    content:"";
    position:absolute; inset:-120px -80px auto auto;
    width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(0,242,254,.14), transparent 60%);
    transform: rotate(18deg);
    pointer-events:none;
  }

  .vx-panel-h{ display:flex; justify-content:space-between; align-items:center; gap: 10px; margin-bottom: 12px; }
  .vx-left{ display:flex; align-items:center; gap: 10px; }
  .vx-right{ display:flex; align-items:center; gap: 10px; flex-wrap:wrap; justify-content:flex-end; }

  .vx-pill{
    display:inline-flex; align-items:center; gap:8px;
    padding: 7px 10px;
    border-radius: 999px;
    border: 1px solid var(--vx-bd2);
    background: rgba(255,255,255,.03);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: .6px;
    text-transform: uppercase;
    color: rgba(255,255,255,.78);
  }
  .vx-pill-dot i{ width: 7px; height: 7px; border-radius: 50%; display:inline-block; }
  .vx-red i{ background:#ff4b2b; box-shadow: 0 0 0 3px rgba(255,75,43,.14); }
  .vx-cyan i{ background:#00f2fe; box-shadow: 0 0 0 3px rgba(0,242,254,.12); }

  .vx-status{
    font-size: 12px;
    color: var(--vx-sub);
    padding: 6px 10px;
    border-radius: 999px;
    border: 1px solid var(--vx-bd2);
    background: rgba(0,0,0,.18);
  }

  .vx-btn{
    border: 1px solid var(--vx-bd);
    background: rgba(255,255,255,.05);
    color: rgba(255,255,255,.86);
    padding: 9px 12px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 700;
    cursor: pointer;
    transition: transform .15s ease, background .15s ease, border-color .15s ease, opacity .15s ease;
    user-select:none;
  }
  .vx-btn:hover{
    background: rgba(255,255,255,.08);
    transform: translateY(-1px);
    border-color: rgba(255,255,255,.22);
  }
  .vx-btn:active{ transform: translateY(0px); opacity:.92; }
  .vx-btn:disabled{ opacity:.45; cursor:not-allowed; transform:none; }
  .vx-btn-ghost{ background: rgba(255,255,255,.03); border-color: rgba(255,255,255,.10); }
  .vx-btn-primary{
    background: linear-gradient(90deg, rgba(0,242,254,.95), rgba(182,244,255,.95));
    border: 1px solid rgba(255,255,255,.18);
    color: rgba(0,0,0,.88);
  }
  .vx-btn-primary:hover{ background: linear-gradient(90deg, rgba(0,242,254,1), rgba(182,244,255,1)); }
  .vx-sm{ padding: 8px 11px; font-size: 12px; }

  .vx-filebtn{
    position: relative;
    display:inline-flex;
    align-items:center;
    justify-content:center;
    padding: 8px 12px;
    border-radius: 999px;
    border: 1px solid rgba(255,255,255,.10);
    background: rgba(255,255,255,.03);
    color: rgba(255,255,255,.86);
    font-size: 12px;
    font-weight: 700;
    cursor: pointer;
    transition: background .15s ease, transform .15s ease, border-color .15s ease;
    overflow:hidden;
  }
  .vx-filebtn:hover{ background: rgba(255,255,255,.07); transform: translateY(-1px); border-color: rgba(255,255,255,.20); }
  .vx-filebtn input{ position:absolute; inset:0; opacity:0; cursor:pointer; width:100%; }

  .vx-canvas-wrap{
    border-radius: 18px;
    overflow:hidden;
    border: 1px solid rgba(255,255,255,.08);
    background: #000;
    position: relative;
  }
  canvas{
    display:block;
    width:100%;
    height: 390px;
    background:#000;
  }
  .vx-canvas-overlay{
    position:absolute;
    left: 14px;
    bottom: 12px;
    padding: 10px 12px;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,.10);
    background: rgba(0,0,0,.42);
    backdrop-filter: blur(8px);
  }
  .vx-overlay-title{ font-size: 12px; font-weight: 800; color: rgba(255,255,255,.88); letter-spacing: .2px; }
  .vx-overlay-sub{ font-size: 11px; color: rgba(255,255,255,.55); margin-top: 2px; }

  .vx-player{ margin-top: 10px; min-height: 34px; }
  audio{ width: 100%; height: 34px; opacity: .62; filter: invert(1); }

  .vx-metrics{ display:grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
  .vx-card{
    background: rgba(255,255,255,.025);
    border: 1px solid rgba(255,255,255,.06);
    border-radius: 18px;
    padding: 16px 16px;
    backdrop-filter: blur(10px);
  }
  .vx-card-top{ display:flex; align-items:center; justify-content:space-between; gap: 10px; margin-bottom: 10px; }
  .vx-k{
    font-size: 12px;
    font-weight: 800;
    color: rgba(255,255,255,.75);
    text-transform: uppercase;
    letter-spacing: 1.8px;
  }
  .vx-badge{
    font-size: 11px;
    padding: 6px 10px;
    border-radius: 999px;
    border: 1px solid rgba(255,255,255,.10);
    background: rgba(255,255,255,.03);
    color: rgba(255,255,255,.62);
    font-weight: 700;
  }
  .vx-row{ display:flex; align-items:baseline; justify-content:space-between; gap: 10px; }
  .vx-v{
    font-size: 32px;
    font-weight: 300;
    color: rgba(255,255,255,.92);
    font-variant-numeric: tabular-nums;
    letter-spacing: -.4px;
  }
  .vx-cmp{
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1.4px;
    text-transform: uppercase;
    color: rgba(255,255,255,.55);
    white-space: nowrap;
  }

  .vx-spark-wrap{
    margin-top: 10px;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,.06);
    background: rgba(0,0,0,.20);
    padding: 8px 10px;
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap: 10px;
  }
  .vx-spark{
    width: 100%;
    height: 28px;
  }
  .vx-spark-legend{ display:flex; gap: 10px; align-items:center; }
  .vx-leg{
    font-size: 11px;
    font-weight: 900;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    padding: 6px 9px;
    border-radius: 999px;
    border: 1px solid rgba(255,255,255,.10);
    background: rgba(255,255,255,.03);
    color: rgba(255,255,255,.70);
  }
  .vx-leg-a{ }
  .vx-leg-b{ }

  .vx-hint{ margin-top: 10px; font-size: 12px; color: rgba(255,255,255,.48); }

  @media (max-width: 980px){
    .vx-grid{ grid-template-columns: 1fr; }
    .vx-metrics{ grid-template-columns: 1fr; }
    canvas{ height: 330px; }
    .vx-range{ width: 110px; }
  }
</style>

<script>
  const canvasEls = [document.getElementById('c1'), document.getElementById('c2')];
  const ctxs = canvasEls.map(c => c.getContext('2d'));

  const sp_sc = document.getElementById('sp_sc');
  const sp_rms = document.getElementById('sp_rms');
  const sp_sr = document.getElementById('sp_sr');

  const compareToggle = document.getElementById('compareToggle');
  const gateSlider = document.getElementById('gateSlider');
  const gateVal = document.getElementById('gateVal');

  const sc_cmp = document.getElementById('sc_cmp');
  const rms_cmp = document.getElementById('rms_cmp');
  const sr_cmp = document.getElementById('sr_cmp');

  const sc_spark_wrap = document.getElementById('sc_spark_wrap');
  const rms_spark_wrap = document.getElementById('rms_spark_wrap');
  const sr_spark_wrap = document.getElementById('sr_spark_wrap');

  function setCompareUI(on){
    const disp = on ? "" : "none";
    sc_cmp.style.display = disp;
    rms_cmp.style.display = disp;
    sr_cmp.style.display = disp;

    sc_spark_wrap.style.display = disp;
    rms_spark_wrap.style.display = disp;
    sr_spark_wrap.style.display = disp;
    drawAllSparks();
  }

  function fitCanvas(c){
    const dpr = window.devicePixelRatio || 1;
    const rect = c.getBoundingClientRect();
    c.width  = Math.floor(rect.width * dpr);
    c.height = Math.floor(rect.height * dpr);
    return dpr;
  }

  // HiDPI scaling for main canvases
  canvasEls.forEach(fitCanvas);
  window.addEventListener('resize', () => {
    canvasEls.forEach(fitCanvas);
    // sparks too
    fitSpark(sp_sc); fitSpark(sp_rms); fitSpark(sp_sr);
    drawAllSparks();
  });

  function fitSpark(c){
    if(!c) return;
    const dpr = window.devicePixelRatio || 1;
    const rect = c.getBoundingClientRect();
    c.width = Math.floor(rect.width * dpr);
    c.height = Math.floor(rect.height * dpr);
  }
  fitSpark(sp_sc); fitSpark(sp_rms); fitSpark(sp_sr);

  let aCtx;
  let activeCanvasIndex = 1;

  const stA = document.getElementById('stA');
  const stB = document.getElementById('stB');

  const playA = document.getElementById('playA');
  const pauseA = document.getElementById('pauseA');
  const playB = document.getElementById('playB');
  const pauseB = document.getElementById('pauseB');

  const p1 = document.getElementById('p1');
  const p2 = document.getElementById('p2');

  let audioA = null;
  let audioB = null;
  let micStream = null;

  // Feature state (latest)
  let latestA = { sc: 0, rmsDb: 0, sr: 0 };
  let latestB = { sc: 0, rmsDb: 0, sr: 0 };

  // Compare histories (sparklines)
  const MAX_H = 120;
  const hist = {
    A: { sc: [], rms: [], sr: [] },
    B: { sc: [], rms: [], sr: [] }
  };

  function pushHist(which, key, v){
    const arr = hist[which][key];
    arr.push(v);
    if(arr.length > MAX_H) arr.shift();
  }

  function setStatus(which, text){
    if(which === 'A') stA.textContent = text;
    else stB.textContent = text;
  }

  function clearCanvas(i){
    const c = canvasEls[i];
    const ctx = ctxs[i];
    ctx.clearRect(0,0,c.width,c.height);
    ctx.fillStyle = '#000';
    ctx.fillRect(0,0,c.width,c.height);
  }
  clearCanvas(0); clearCanvas(1);

  async function ensureAudioContext(){
    if(!aCtx) aCtx = new (window.AudioContext || window.webkitAudioContext)();
    if(aCtx.state === "suspended") await aCtx.resume();
  }

  function connectAndRun(sourceNode, idx, which, sampleRate, isMic=false){
    const analyser = aCtx.createAnalyser();
    analyser.fftSize = 2048;
    sourceNode.connect(analyser);

    const c = canvasEls[idx];
    const ctx = ctxs[idx];
    const dpr = window.devicePixelRatio || 1;

    const buffer = new Uint8Array(analyser.frequencyBinCount);

    function draw(){
      analyser.getByteFrequencyData(buffer);

      const shift = Math.max(2, Math.floor(3 * dpr));
      const frame = ctx.getImageData(shift, 0, c.width - shift, c.height);
      ctx.putImageData(frame, 0, 0);

      const x = c.width - shift;
      const sliceH = c.height / buffer.length;

      for(let i=0;i<buffer.length;i++){
        const v = buffer[i];
        const r = Math.min(255, v + 20);
        const g = Math.floor(v * 0.45);
        const b = Math.max(0, 240 - Math.floor(v * 0.25));
        const a = Math.max(0.05, v/255);

        ctx.fillStyle = `rgba(${r},${g},${b},${a})`;
        ctx.fillRect(x, c.height - (i*sliceH), shift, sliceH);
      }

      extractData(buffer, sampleRate || aCtx.sampleRate, which, isMic);

      requestAnimationFrame(draw);
    }
    draw();
  }

  function toDb(rmsLinear){
    // rmsLinear expected 0..1
    return 20 * Math.log10(Math.max(1e-6, rmsLinear));
  }

  function extractData(data, rate, which, isMic){
    let sFreq=0, sMag=0, rmsS=0;
    const binHz = rate/2048;

    for(let i=0;i<data.length;i++){
      const m = data[i];
      sFreq += (i * binHz) * m;
      sMag  += m;
      rmsS  += m*m;
    }

    const cent = sMag > 0 ? (sFreq/sMag) : 0;
    const rms = Math.sqrt(rmsS/data.length); // 0..255 approx
    const rmsLinear01 = rms/255;
    const rmsDb = toDb(rmsLinear01);

    // Your ratio idea, clamped nicely
    const ratio = Math.max(0, Math.min(100, (cent/150)));

    // Noise gate ONLY for mic on B
    const gateDb = parseInt(gateSlider.value, 10);
    if(isMic && which === 'B' && rmsDb < gateDb){
      setStatus('B', "Mic gated");
      // still keep last values, but don't update / push history
      return;
    }

    if(which === 'A'){
      latestA = { sc: cent, rmsDb: rmsDb, sr: ratio };
      pushHist('A','sc',cent);
      pushHist('A','rms',rmsDb);
      pushHist('A','sr',ratio);
    }else{
      latestB = { sc: cent, rmsDb: rmsDb, sr: ratio };
      pushHist('B','sc',cent);
      pushHist('B','rms',rmsDb);
      pushHist('B','sr',ratio);
    }

    // Primary display focuses on B (Input)
    document.getElementById('sc_val').innerText  = `${latestB.sc.toFixed(0)} Hz`;
    document.getElementById('rms_val').innerText = `${latestB.rmsDb.toFixed(1)} dB`;
    document.getElementById('sr_val').innerText  = `${latestB.sr.toFixed(1)} %`;

    // Compare display shows A secondary
    document.getElementById('sc_cmp').innerText  = `A: ${latestA.sc.toFixed(0)} Hz`;
    document.getElementById('rms_cmp').innerText = `A: ${latestA.rmsDb.toFixed(1)} dB`;
    document.getElementById('sr_cmp').innerText  = `A: ${latestA.sr.toFixed(1)} %`;

    if(compareToggle.checked) drawAllSparks();
  }

  function mountAudio(el, mount, which){
    mount.innerHTML = '';
    mount.appendChild(el);

    el.onplay  = () => setStatus(which, "Playing");
    el.onpause = () => setStatus(which, "Paused");
    el.onended = () => setStatus(which, "Ready");
  }

  async function runMediaElement(audioEl, idx, which){
    await ensureAudioContext();
    const src = aCtx.createMediaElementSource(audioEl);
    src.connect(aCtx.destination);

    activeCanvasIndex = idx;
    setStatus(which, "Analyzing");

    connectAndRun(src, idx, which, aCtx.sampleRate, false);
  }

  async function runMic(idx){
    await ensureAudioContext();
    micStream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const src = aCtx.createMediaStreamSource(micStream);

    activeCanvasIndex = idx;
    setStatus('B', "Mic live");

    connectAndRun(src, idx, 'B', aCtx.sampleRate, true);
  }

  // Spark drawing
  function drawSpark(canvas, seriesA, seriesB, domain){
    if(!canvas) return;
    const ctx = canvas.getContext('2d');
    const w = canvas.width;
    const h = canvas.height;

    // background
    ctx.clearRect(0,0,w,h);
    ctx.fillStyle = 'rgba(0,0,0,.0)';
    ctx.fillRect(0,0,w,h);

    // grid line
    ctx.strokeStyle = 'rgba(255,255,255,.06)';
    ctx.lineWidth = Math.max(1, (window.devicePixelRatio||1));
    ctx.beginPath();
    ctx.moveTo(0, h-1);
    ctx.lineTo(w, h-1);
    ctx.stroke();

    function plot(series, stroke){
      if(series.length < 2) return;
      const minV = domain.min;
      const maxV = domain.max;
      const span = Math.max(1e-6, maxV - minV);

      ctx.beginPath();
      for(let i=0;i<series.length;i++){
        const x = (i/(MAX_H-1)) * w;
        const v = Math.max(minV, Math.min(maxV, series[i]));
        const y = h - ((v - minV)/span) * (h-2) - 1;
        if(i===0) ctx.moveTo(x,y);
        else ctx.lineTo(x,y);
      }
      ctx.strokeStyle = stroke;
      ctx.lineWidth = Math.max(1.2, 1.6*(window.devicePixelRatio||1));
      ctx.lineJoin = 'round';
      ctx.lineCap = 'round';
      ctx.stroke();
    }

    // A is slightly dimmer, B is brighter
    plot(seriesA, 'rgba(255,255,255,.35)');
    plot(seriesB, 'rgba(0,242,254,.70)');
  }

  function drawAllSparks(){
    if(!compareToggle.checked) return;

    // Use dynamic-ish domains (stable but responsive)
    const scMax = Math.max(500, latestA.sc, latestB.sc, ...hist.A.sc, ...hist.B.sc);
    const scMin = 0;

    const rmsMax = Math.max(-3, latestA.rmsDb, latestB.rmsDb, ...hist.A.rms, ...hist.B.rms);
    const rmsMin = Math.min(-60, latestA.rmsDb, latestB.rmsDb, ...hist.A.rms, ...hist.B.rms);

    const srMin = 0;
    const srMax = 100;

    drawSpark(sp_sc,  hist.A.sc,  hist.B.sc,  {min: scMin, max: scMax});
    drawSpark(sp_rms, hist.A.rms, hist.B.rms, {min: rmsMin, max: rmsMax});
    drawSpark(sp_sr,  hist.A.sr,  hist.B.sr,  {min: srMin, max: srMax});
  }

  // Upload handlers
  document.getElementById('f1').onchange = function(){
    if(!this.files?.[0]) return;
    const url = URL.createObjectURL(this.files[0]);
    audioA = new Audio(url);
    audioA.crossOrigin = "anonymous";
    mountAudio(audioA, p1, 'A');

    playA.disabled = false;
    pauseA.disabled = false;
    setStatus('A', "Loaded");

    audioA.onplay = () => runMediaElement(audioA, 0, 'A');
  };

  document.getElementById('f2').onchange = function(){
    if(!this.files?.[0]) return;
    const url = URL.createObjectURL(this.files[0]);
    audioB = new Audio(url);
    audioB.crossOrigin = "anonymous";
    mountAudio(audioB, p2, 'B');

    playB.disabled = false;
    pauseB.disabled = false;
    setStatus('B', "Loaded");

    audioB.onplay = () => runMediaElement(audioB, 1, 'B');
  };

  // Controls
  playA.onclick = () => audioA && audioA.play();
  pauseA.onclick = () => audioA && audioA.pause();

  playB.onclick = () => audioB && audioB.play();
  pauseB.onclick = () => audioB && audioB.pause();

  document.getElementById('mBtn').onclick = async () => {
    try{
      await runMic(1);
    }catch(e){
      setStatus('B', "Mic blocked");
      console.error(e);
    }
  };

  document.getElementById('resetBtn').onclick = () => {
    if(micStream){
      micStream.getTracks().forEach(t => t.stop());
      micStream = null;
    }
    if(audioA){ audioA.pause(); audioA.currentTime = 0; }
    if(audioB){ audioB.pause(); audioB.currentTime = 0; }

    setStatus('A', "Ready");
    setStatus('B', "Ready");

    clearCanvas(0); clearCanvas(1);

    latestA = { sc: 0, rmsDb: 0, sr: 0 };
    latestB = { sc: 0, rmsDb: 0, sr: 0 };
    hist.A.sc = []; hist.A.rms = []; hist.A.sr = [];
    hist.B.sc = []; hist.B.rms = []; hist.B.sr = [];

    document.getElementById('sc_val').innerText = "0 Hz";
    document.getElementById('rms_val').innerText = "0 dB";
    document.getElementById('sr_val').innerText = "0 %";

    document.getElementById('sc_cmp').innerText = "A: 0 Hz";
    document.getElementById('rms_cmp').innerText = "A: 0 dB";
    document.getElementById('sr_cmp').innerText = "A: 0 %";

    if(compareToggle.checked) drawAllSparks();
  };

  document.getElementById('swapBtn').onclick = () => {
    const tmpA = audioA; audioA = audioB; audioB = tmpA;
    const tmpHTML = p1.innerHTML; p1.innerHTML = p2.innerHTML; p2.innerHTML = tmpHTML;

    const a = stA.textContent; stA.textContent = stB.textContent; stB.textContent = a;

    const aEn = playA.disabled; playA.disabled = playB.disabled; playB.disabled = aEn;
    const aPa = pauseA.disabled; pauseA.disabled = pauseB.disabled; pauseB.disabled = aPa;

    // swap latest & histories to keep semantics consistent
    const tmpLatest = latestA; latestA = latestB; latestB = tmpLatest;

    const tmpHist = hist.A; hist.A = hist.B; hist.B = tmpHist;

    document.getElementById('sc_val').innerText  = `${latestB.sc.toFixed(0)} Hz`;
    document.getElementById('rms_val').innerText = `${latestB.rmsDb.toFixed(1)} dB`;
    document.getElementById('sr_val').innerText  = `${latestB.sr.toFixed(1)} %`;

    document.getElementById('sc_cmp').innerText  = `A: ${latestA.sc.toFixed(0)} Hz`;
    document.getElementById('rms_cmp').innerText = `A: ${latestA.rmsDb.toFixed(1)} dB`;
    document.getElementById('sr_cmp').innerText  = `A: ${latestA.sr.toFixed(1)} %`;

    if(compareToggle.checked) drawAllSparks();
  };

  document.getElementById('snapBtn').onclick = () => {
    const c = canvasEls[activeCanvasIndex] || canvasEls[1];
    const link = document.createElement('a');
    link.download = 'vocalytics_snapshot.png';
    link.href = c.toDataURL('image/png');
    link.click();
  };

  document.getElementById('fsBtn').onclick = async () => {
    const c = canvasEls[activeCanvasIndex] || canvasEls[1];
    try{
      if(c.requestFullscreen) await c.requestFullscreen();
    }catch(e){
      console.error(e);
    }
  };

  // Compare toggle
  compareToggle.addEventListener('change', (e) => {
    setCompareUI(e.target.checked);
  });

  // Noise gate slider
  function updateGateLabel(){
    gateVal.textContent = `${gateSlider.value} dB`;
  }
  gateSlider.addEventListener('input', () => {
    updateGateLabel();
  });
  updateGateLabel();

  // Initial UI state
  setCompareUI(false);
</script>
"""

components.html(vocalytics_2026_html, height=940)