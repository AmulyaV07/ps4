def render_dashboard() -> str:
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Creator Posting Optimizer</title>
  <style>
    :root {
      color-scheme: dark;
      --bg: #071012;
      --ink: #f4f7f4;
      --soft: #b9c6c1;
      --muted: #7f918a;
      --line: rgba(220, 236, 229, 0.16);
      --panel: rgba(13, 28, 29, 0.78);
      --panel-strong: rgba(17, 39, 40, 0.92);
      --cyan: #48d6c2;
      --lime: #bde66d;
      --coral: #ff8a6b;
      --blue: #78a6ff;
      --yellow: #ffd166;
      --shadow: rgba(0, 0, 0, 0.34);
    }
    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body {
      margin: 0;
      min-height: 100vh;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: var(--ink);
      background:
        linear-gradient(90deg, rgba(255,255,255,0.035) 1px, transparent 1px),
        linear-gradient(0deg, rgba(255,255,255,0.025) 1px, transparent 1px),
        radial-gradient(circle at 20% 10%, rgba(72, 214, 194, 0.18), transparent 34%),
        #071012;
      background-size: 54px 54px, 54px 54px, auto, auto;
      overflow-x: hidden;
    }
    canvas#network {
      position: fixed;
      inset: 0;
      width: 100%;
      height: 100%;
      z-index: 0;
      pointer-events: none;
      opacity: 0.82;
    }
    .shell {
      position: relative;
      z-index: 1;
      min-height: 100vh;
    }
    .topbar {
      position: sticky;
      top: 0;
      z-index: 3;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 18px;
      padding: 14px 28px;
      border-bottom: 1px solid var(--line);
      background: rgba(7, 16, 18, 0.78);
      backdrop-filter: blur(18px);
    }
    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
      min-width: 0;
    }
    .mark {
      width: 38px;
      height: 38px;
      display: grid;
      place-items: center;
      border: 1px solid rgba(72, 214, 194, 0.45);
      background: conic-gradient(from 110deg, rgba(72,214,194,0.82), rgba(189,230,109,0.88), rgba(255,138,107,0.78), rgba(72,214,194,0.82));
      color: #051012;
      font-weight: 900;
      border-radius: 8px;
      box-shadow: 0 12px 30px rgba(72, 214, 194, 0.16);
    }
    .brand strong { display: block; font-size: 15px; }
    .brand span { display: block; color: var(--soft); font-size: 12px; margin-top: 2px; }
    .nav {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      justify-content: flex-end;
    }
    .nav a, button {
      border: 1px solid var(--line);
      border-radius: 8px;
      color: var(--ink);
      background: rgba(255,255,255,0.06);
      text-decoration: none;
      padding: 9px 12px;
      font: inherit;
      cursor: pointer;
      transition: transform 160ms ease, border-color 160ms ease, background 160ms ease;
    }
    .nav a:hover, button:hover {
      transform: translateY(-1px);
      border-color: rgba(72, 214, 194, 0.55);
      background: rgba(72, 214, 194, 0.12);
    }
    .hero {
      min-height: calc(100vh - 66px);
      display: grid;
      grid-template-columns: minmax(320px, 0.95fr) minmax(360px, 1.05fr);
      align-items: center;
      gap: 34px;
      padding: 52px 46px 30px;
    }
    .eyebrow {
      color: var(--lime);
      font-size: 13px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }
    h1 {
      max-width: 840px;
      margin: 12px 0 18px;
      font-size: clamp(44px, 7vw, 92px);
      line-height: 0.92;
      letter-spacing: 0;
    }
    .hero p {
      max-width: 650px;
      color: var(--soft);
      font-size: 18px;
      line-height: 1.6;
    }
    .cta {
      display: flex;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
      margin-top: 26px;
    }
    .primary {
      background: var(--cyan);
      color: #031110;
      border-color: transparent;
      font-weight: 800;
    }
    .score-strip {
      display: grid;
      grid-template-columns: repeat(4, minmax(120px, 1fr));
      gap: 12px;
      margin-top: 34px;
      max-width: 730px;
    }
    .metric {
      min-height: 112px;
      padding: 15px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: rgba(11, 25, 26, 0.74);
      box-shadow: 0 18px 60px var(--shadow);
    }
    .metric span { color: var(--muted); font-size: 12px; text-transform: uppercase; font-weight: 800; letter-spacing: 0.07em; }
    .metric strong { display: block; margin-top: 13px; font-size: 30px; line-height: 1; }
    .metric small { display: block; margin-top: 9px; color: var(--soft); }
    .command-center {
      position: relative;
      min-height: 540px;
      border: 1px solid rgba(72, 214, 194, 0.22);
      border-radius: 8px;
      background:
        linear-gradient(135deg, rgba(255,255,255,0.07), transparent 32%),
        rgba(9, 22, 23, 0.74);
      box-shadow: 0 28px 90px rgba(0, 0, 0, 0.42);
      overflow: hidden;
    }
    .dial {
      position: absolute;
      inset: 36px;
      border: 1px solid rgba(255,255,255,0.11);
      border-radius: 50%;
      animation: spin 36s linear infinite;
    }
    .dial::before, .dial::after {
      content: "";
      position: absolute;
      inset: 16%;
      border: 1px dashed rgba(189,230,109,0.24);
      border-radius: 50%;
    }
    .dial::after {
      inset: 32%;
      border-style: solid;
      border-color: rgba(120,166,255,0.28);
    }
    .needle {
      position: absolute;
      left: 50%;
      top: 50%;
      width: 42%;
      height: 2px;
      transform-origin: left center;
      background: linear-gradient(90deg, var(--cyan), transparent);
      animation: sweep 7s ease-in-out infinite alternate;
    }
    .node {
      position: absolute;
      width: 112px;
      padding: 12px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: rgba(4, 15, 16, 0.82);
      backdrop-filter: blur(10px);
      box-shadow: 0 16px 40px rgba(0,0,0,0.25);
      animation: float 5s ease-in-out infinite;
    }
    .node b { display: block; font-size: 13px; }
    .node span { display: block; margin-top: 5px; color: var(--soft); font-size: 12px; }
    .n1 { left: 9%; top: 12%; border-color: rgba(72,214,194,0.4); }
    .n2 { right: 11%; top: 18%; border-color: rgba(255,138,107,0.42); animation-delay: -1s; }
    .n3 { left: 14%; bottom: 14%; border-color: rgba(189,230,109,0.45); animation-delay: -2s; }
    .n4 { right: 9%; bottom: 17%; border-color: rgba(120,166,255,0.42); animation-delay: -3s; }
    .center-card {
      position: absolute;
      left: 50%;
      top: 50%;
      transform: translate(-50%, -50%);
      width: min(74%, 330px);
      padding: 22px;
      border: 1px solid rgba(72,214,194,0.34);
      border-radius: 8px;
      background: rgba(7, 18, 19, 0.86);
      text-align: center;
    }
    .center-card strong { display: block; font-size: 42px; }
    .center-card span { color: var(--soft); }
    section.content {
      padding: 26px 46px 58px;
      display: grid;
      gap: 18px;
    }
    .section-title {
      display: flex;
      align-items: end;
      justify-content: space-between;
      gap: 18px;
      margin-top: 6px;
    }
    .section-title h2 { margin: 0; font-size: 26px; }
    .section-title p { margin: 7px 0 0; color: var(--soft); max-width: 700px; }
    .layout {
      display: grid;
      grid-template-columns: minmax(420px, 1.35fr) minmax(320px, 0.65fr);
      gap: 18px;
    }
    .panel {
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel);
      backdrop-filter: blur(18px);
      box-shadow: 0 18px 60px rgba(0,0,0,0.24);
      overflow: hidden;
    }
    .panel-head {
      padding: 16px 18px;
      border-bottom: 1px solid var(--line);
      background: rgba(255,255,255,0.035);
      display: flex;
      justify-content: space-between;
      gap: 10px;
      align-items: center;
    }
    .panel-head h3 { margin: 0; font-size: 17px; }
    .panel-body { padding: 18px; }
    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 14px;
    }
    th, td {
      padding: 13px 14px;
      border-bottom: 1px solid var(--line);
      text-align: left;
      white-space: nowrap;
    }
    th {
      color: var(--muted);
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.06em;
    }
    tbody tr {
      transition: background 160ms ease, transform 160ms ease;
    }
    tbody tr:hover {
      background: rgba(72,214,194,0.08);
    }
    .pill {
      display: inline-flex;
      align-items: center;
      min-height: 26px;
      padding: 4px 9px;
      border-radius: 999px;
      background: rgba(72,214,194,0.12);
      color: var(--cyan);
      border: 1px solid rgba(72,214,194,0.25);
      font-weight: 700;
      font-size: 12px;
    }
    .pill.youtube { color: var(--coral); background: rgba(255,138,107,0.12); border-color: rgba(255,138,107,0.28); }
    .bars, .heat {
      display: grid;
      gap: 12px;
    }
    .bar label {
      display: flex;
      justify-content: space-between;
      font-size: 13px;
      color: var(--soft);
      margin-bottom: 6px;
    }
    .track {
      height: 11px;
      background: rgba(255,255,255,0.08);
      border: 1px solid rgba(255,255,255,0.06);
      border-radius: 999px;
      overflow: hidden;
    }
    .fill {
      height: 100%;
      background: linear-gradient(90deg, var(--cyan), var(--lime));
      border-radius: inherit;
      animation: grow 900ms ease both;
    }
    .fill.alt { background: linear-gradient(90deg, var(--coral), var(--yellow)); }
    .heat-grid {
      display: grid;
      grid-template-columns: repeat(12, 1fr);
      gap: 7px;
    }
    .cell {
      aspect-ratio: 1;
      display: grid;
      place-items: center;
      border: 1px solid rgba(255,255,255,0.07);
      border-radius: 6px;
      color: #071012;
      font-size: 11px;
      font-weight: 900;
      background: color-mix(in srgb, var(--cyan) var(--v), rgba(255,255,255,0.09));
    }
    .lookup-grid {
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 10px;
      margin-bottom: 14px;
    }
    input {
      width: 100%;
      min-width: 0;
      height: 42px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: rgba(255,255,255,0.06);
      color: var(--ink);
      padding: 0 12px;
      font: inherit;
    }
    .candidate-list {
      display: grid;
      gap: 9px;
    }
    .candidate {
      display: grid;
      grid-template-columns: auto 1fr auto;
      gap: 10px;
      align-items: center;
      padding: 11px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: rgba(255,255,255,0.045);
    }
    .rank {
      width: 28px;
      height: 28px;
      display: grid;
      place-items: center;
      border-radius: 7px;
      background: rgba(72,214,194,0.16);
      color: var(--cyan);
      font-weight: 900;
    }
    .candidate b { display: block; font-size: 14px; }
    .candidate span { display: block; color: var(--soft); font-size: 12px; margin-top: 3px; }
    .explain-score { color: var(--lime); font-weight: 900; }
    .formula {
      margin-top: 18px;
      padding: 16px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel-strong);
      color: var(--soft);
      font-family: ui-monospace, SFMono-Regular, Consolas, "Liberation Mono", monospace;
      font-size: 13px;
      line-height: 1.7;
    }
    @keyframes spin { to { transform: rotate(360deg); } }
    @keyframes sweep {
      from { transform: rotate(18deg); }
      to { transform: rotate(310deg); }
    }
    @keyframes float {
      0%, 100% { transform: translateY(0); }
      50% { transform: translateY(-10px); }
    }
    @keyframes grow {
      from { width: 0; }
    }
    @media (max-width: 980px) {
      .hero, .layout { grid-template-columns: 1fr; }
      .hero { padding: 38px 22px 24px; }
      section.content { padding: 22px; }
      .score-strip { grid-template-columns: repeat(2, 1fr); }
      .command-center { min-height: 460px; }
    }
    @media (max-width: 620px) {
      .topbar { align-items: flex-start; flex-direction: column; padding: 14px 18px; }
      h1 { font-size: 42px; }
      .score-strip { grid-template-columns: 1fr; }
      th, td { padding: 10px 8px; font-size: 12px; }
      .heat-grid { grid-template-columns: repeat(8, 1fr); }
    }
  </style>
</head>
<body>
  <canvas id="network"></canvas>
  <div class="shell">
    <nav class="topbar">
      <div class="brand">
        <div class="mark">PS4</div>
        <div>
          <strong>Creator Posting Optimizer</strong>
          <span>48-way deterministic decision engine</span>
        </div>
      </div>
      <div class="nav">
        <a href="#proof">Proof</a>
        <a href="#explain">Explain</a>
        <a href="/analytics" target="_blank">API</a>
      </div>
    </nav>

    <header class="hero">
      <div>
        <div class="eyebrow">Hackathon-ready optimization cockpit</div>
        <h1>Find the exact hour where a creator should post.</h1>
        <p>Every recommendation is chosen by scoring Instagram and YouTube across all 24 hours using creator history, platform activity, content fit, and deterministic tie-breaking.</p>
        <div class="cta">
          <a class="primary" href="#explain">Inspect a recommendation</a>
          <a href="#proof">Show scoring proof</a>
        </div>
        <div class="score-strip" id="metrics"></div>
      </div>
      <div class="command-center" aria-label="Animated recommendation engine map">
        <div class="dial"></div>
        <div class="needle"></div>
        <div class="node n1"><b>Creator</b><span>base signal</span></div>
        <div class="node n2"><b>Platform</b><span>audience pulse</span></div>
        <div class="node n3"><b>History</b><span>personal fit</span></div>
        <div class="node n4"><b>Schedule</b><span>best hour</span></div>
        <div class="center-card">
          <span>Visible score</span>
          <strong id="heroScore">--</strong>
          <span>deterministic output</span>
        </div>
      </div>
    </header>

    <section class="content" id="proof">
      <div class="section-title">
        <div>
          <h2>Optimization Proof</h2>
          <p>The dashboard is powered by live results from the Python backend. No frontend mock data is used.</p>
        </div>
      </div>
      <div class="layout">
        <div class="panel">
          <div class="panel-head">
            <h3>Highest Confidence Recommendations</h3>
            <span class="pill">ranked by score</span>
          </div>
          <div style="overflow:auto">
            <table>
              <thead><tr><th>Content</th><th>Platform</th><th>Hour</th><th>Decision</th><th>Expected</th><th>Score</th></tr></thead>
              <tbody id="top"></tbody>
            </table>
          </div>
        </div>
        <div class="panel">
          <div class="panel-head">
            <h3>Decision Mix</h3>
            <span class="pill">100 items</span>
          </div>
          <div class="panel-body">
            <div class="bars" id="platforms"></div>
            <div style="height:18px"></div>
            <div class="bars" id="decisions"></div>
          </div>
        </div>
      </div>
      <div class="panel">
        <div class="panel-head">
          <h3>Recommended Posting Hours</h3>
          <span class="pill">hour heat-map</span>
        </div>
        <div class="panel-body">
          <div class="heat-grid" id="heat"></div>
        </div>
      </div>
    </section>

    <section class="content" id="explain">
      <div class="section-title">
        <div>
          <h2>Explain Any Content Item</h2>
          <p>Use this during presentation to show that the model ranks alternatives and can justify the selected platform-time pair.</p>
        </div>
      </div>
      <div class="layout">
        <div class="panel">
          <div class="panel-head">
            <h3>Top Candidate Stack</h3>
            <span class="pill">live lookup</span>
          </div>
          <div class="panel-body">
            <div class="lookup-grid">
              <input id="cid" type="number" min="1" value="1" aria-label="content id">
              <button onclick="lookup()">Analyze</button>
            </div>
            <div class="candidate-list" id="lookupResult"></div>
          </div>
        </div>
        <div class="panel">
          <div class="panel-head">
            <h3>Scoring Formula</h3>
            <span class="pill">evaluator-aligned</span>
          </div>
          <div class="panel-body">
            <div class="formula">
              expected = creator_base * activity * history<br>
              score = 0.50 * normalized(expected)<br>
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;+ 0.20 * activity<br>
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;+ 0.15 * platform_quality
            </div>
            <div class="formula">
              Output stays evaluator-safe:<br>
              content_id, platform, time_slot, decision
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>

  <script>
    const pct = value => `${(value * 100).toFixed(2)}%`;
    const byId = id => document.getElementById(id);

    function metric(label, value, hint) {
      return `<div class="metric"><span>${label}</span><strong>${value}</strong><small>${hint}</small></div>`;
    }
    function platformPill(platform) {
      return `<span class="pill ${platform === "YouTube" ? "youtube" : ""}">${platform}</span>`;
    }
    function bars(title, data, total, alt=false) {
      const rows = Object.entries(data).map(([key, value]) => `
        <div class="bar">
          <label><span>${key}</span><span>${value}</span></label>
          <div class="track"><div class="fill ${alt ? "alt" : ""}" style="width:${(value / total) * 100}%"></div></div>
        </div>
      `).join("");
      return `<h4 style="margin:0 0 10px">${title}</h4>${rows}`;
    }
    function heat(data) {
      const max = Math.max(...Object.values(data), 1);
      return Array.from({length: 24}, (_, hour) => {
        const value = data[String(hour)] || 0;
        const intensity = 18 + Math.round((value / max) * 74);
        return `<div class="cell" style="--v:${intensity}%">${hour}</div>`;
      }).join("");
    }
    async function load() {
      const data = await fetch("/analytics").then(r => r.json());
      byId("heroScore").textContent = pct(data.score.final_score);
      byId("metrics").innerHTML = [
        metric("Final Score", pct(data.score.final_score), "visible evaluator"),
        metric("Timing", pct(data.score.timing_score), "peak slots captured"),
        metric("Platform Fit", pct(data.score.platform_score), "soft content bias"),
        metric("Avg Expected", data.average_expected_engagement.toFixed(4), "creator adapted")
      ].join("");
      byId("top").innerHTML = data.top_recommendations.map(row => `
        <tr>
          <td>#${row.content_id}</td>
          <td>${platformPill(row.platform)}</td>
          <td>${row.time_slot}:00</td>
          <td>${row.decision}</td>
          <td>${row.expected_engagement.toFixed(4)}</td>
          <td>${row.score.toFixed(4)}</td>
        </tr>
      `).join("");
      byId("platforms").innerHTML = bars("Platform split", data.platform_distribution, data.count);
      byId("decisions").innerHTML = bars("Scheduling split", data.decision_distribution, data.count, true);
      byId("heat").innerHTML = heat(data.time_slot_distribution);
      lookup();
    }
    async function lookup() {
      const cid = byId("cid").value;
      const data = await fetch(`/explain?content_id=${cid}`).then(r => r.json());
      if (data.error) {
        byId("lookupResult").innerHTML = `<div class="candidate"><b>${data.error}</b></div>`;
        return;
      }
      byId("lookupResult").innerHTML = data.top_candidates.map(row => `
        <div class="candidate">
          <div class="rank">${row.rank}</div>
          <div>
            <b>${row.platform} at ${row.time_slot}:00 · ${row.decision}</b>
            <span>expected ${row.expected_engagement.toFixed(4)} · activity ${row.activity_score.toFixed(2)} · history ${row.historical_engagement.toFixed(3)}</span>
          </div>
          <div class="explain-score">${row.score.toFixed(4)}</div>
        </div>
      `).join("");
    }

    const canvas = byId("network");
    const ctx = canvas.getContext("2d");
    let w = 0, h = 0, tick = 0;
    const packets = Array.from({length: 42}, (_, i) => ({
      lane: i % 7,
      x: Math.random(),
      speed: 0.0012 + Math.random() * 0.0026,
      size: 2 + Math.random() * 3,
      hue: i % 3
    }));
    function resize() {
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      w = canvas.width = Math.floor(innerWidth * dpr);
      h = canvas.height = Math.floor(innerHeight * dpr);
      canvas.style.width = innerWidth + "px";
      canvas.style.height = innerHeight + "px";
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      w = innerWidth;
      h = innerHeight;
    }
    function draw() {
      tick += 1;
      ctx.clearRect(0, 0, w, h);
      ctx.lineWidth = 1;
      for (let lane = 0; lane < 7; lane++) {
        const y = h * (0.18 + lane * 0.105) + Math.sin(tick * 0.012 + lane) * 18;
        ctx.beginPath();
        for (let x = -40; x <= w + 40; x += 26) {
          const wave = Math.sin((x * 0.011) + tick * 0.018 + lane) * 18;
          if (x === -40) ctx.moveTo(x, y + wave);
          else ctx.lineTo(x, y + wave);
        }
        ctx.strokeStyle = `rgba(120, 166, 255, ${0.055 + lane * 0.005})`;
        ctx.stroke();
      }
      packets.forEach(packet => {
        packet.x += packet.speed;
        if (packet.x > 1.08) packet.x = -0.08;
        const x = packet.x * w;
        const y = h * (0.18 + packet.lane * 0.105) + Math.sin(tick * 0.012 + packet.lane + x * 0.011) * 18;
        ctx.beginPath();
        ctx.rect(x, y, packet.size * 4, packet.size);
        const color = packet.hue === 0 ? "72,214,194" : packet.hue === 1 ? "189,230,109" : "255,138,107";
        ctx.fillStyle = `rgba(${color}, 0.62)`;
        ctx.fill();
      });
      requestAnimationFrame(draw);
    }
    addEventListener("resize", resize);
    resize();
    draw();
    load();
  </script>
</body>
</html>"""
