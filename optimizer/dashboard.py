def render_dashboard() -> str:
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>PostPulse Optimizer</title>
  <style>
    :root {
      --bg: #081018;
      --panel: rgba(12, 21, 34, 0.78);
      --panel2: rgba(255, 255, 255, 0.07);
      --line: rgba(255, 255, 255, 0.14);
      --text: #f7fbff;
      --muted: #a9b7c8;
      --blue: #58a6ff;
      --green: #33d69f;
      --yellow: #ffd166;
      --pink: #ff6b9a;
      --purple: #a78bfa;
      --shadow: 0 22px 70px rgba(0, 0, 0, 0.30);
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      min-height: 100vh;
      color: var(--text);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
      background:
        radial-gradient(circle at 15% 0%, rgba(88, 166, 255, 0.28), transparent 30%),
        radial-gradient(circle at 88% 8%, rgba(51, 214, 159, 0.20), transparent 34%),
        radial-gradient(circle at 58% 88%, rgba(167, 139, 250, 0.12), transparent 30%),
        linear-gradient(135deg, #081018 0%, #0b1728 48%, #071019 100%);
      overflow-x: hidden;
    }
    body::before {
      content: "";
      position: fixed;
      inset: 0;
      pointer-events: none;
      background-image:
        linear-gradient(rgba(255,255,255,0.05) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.05) 1px, transparent 1px);
      background-size: 54px 54px;
      mask-image: linear-gradient(to bottom, black, transparent 85%);
    }
    .shell {
      position: relative;
      z-index: 1;
      max-width: 1500px;
      margin: 0 auto;
      padding: 22px;
    }
    .nav {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 14px;
      padding: 12px 0 24px;
    }
    .brand { display: flex; align-items: center; gap: 12px; }
    .logo {
      width: 42px;
      height: 42px;
      display: grid;
      place-items: center;
      border-radius: 8px;
      color: #071018;
      font-weight: 950;
      background: linear-gradient(135deg, var(--green), var(--blue));
      box-shadow: 0 12px 30px rgba(88, 166, 255, 0.28);
    }
    .brand strong { display: block; font-size: 16px; }
    .brand span { display: block; color: var(--muted); font-size: 12px; margin-top: 2px; }
    .links { display: flex; gap: 8px; flex-wrap: wrap; justify-content: flex-end; }
    .links a, button {
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 10px 13px;
      background: rgba(255,255,255,0.06);
      color: var(--text);
      text-decoration: none;
      font: inherit;
      font-weight: 800;
      cursor: pointer;
      transition: transform .16s ease, background .16s ease, border-color .16s ease;
    }
    .links a:hover, button:hover { transform: translateY(-1px); border-color: rgba(88,166,255,.55); }
    .primary {
      color: #061017 !important;
      background: linear-gradient(135deg, var(--green), var(--blue)) !important;
      border-color: transparent !important;
    }
    .hero {
      display: grid;
      grid-template-columns: 0.88fr 1.12fr;
      gap: 22px;
      align-items: stretch;
    }
    .card {
      border: 1px solid var(--line);
      border-radius: 16px;
      background: var(--panel);
      box-shadow: var(--shadow);
      backdrop-filter: blur(16px);
      overflow: hidden;
    }
    .pad { padding: 28px; }
    .eyebrow {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 7px 10px;
      border: 1px solid rgba(51,214,159,.35);
      border-radius: 999px;
      color: var(--green);
      background: rgba(51,214,159,.08);
      font-size: 12px;
      font-weight: 900;
      letter-spacing: .06em;
      text-transform: uppercase;
    }
    h1 {
      margin: 16px 0 14px;
      font-size: clamp(42px, 5vw, 78px);
      line-height: .92;
      letter-spacing: 0;
    }
    p { color: var(--muted); line-height: 1.65; margin: 0; }
    .kpis {
      display: grid;
      grid-template-columns: repeat(2, minmax(160px, 1fr));
      gap: 12px;
      margin-top: 22px;
    }
    .kpi {
      min-height: 112px;
      padding: 16px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel2);
    }
    .kpi label {
      display: block;
      color: var(--muted);
      font-size: 11px;
      font-weight: 900;
      letter-spacing: .08em;
      text-transform: uppercase;
    }
    .kpi strong { display: block; margin-top: 12px; font-size: 30px; }
    .kpi small { display: block; color: var(--muted); margin-top: 8px; font-size: 12px; }
    .chart-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 14px;
      height: 100%;
    }
    .chart-card {
      border: 1px solid var(--line);
      border-radius: 14px;
      background: var(--panel2);
      padding: 16px;
      min-height: 285px;
    }
    .chart-title {
      display: flex;
      justify-content: space-between;
      gap: 10px;
      align-items: center;
      margin-bottom: 10px;
      font-weight: 950;
    }
    canvas { width: 100%; height: 230px; display: block; }
    section { margin-top: 18px; scroll-margin-top: 16px; }
    .section-head {
      display: flex;
      justify-content: space-between;
      align-items: end;
      gap: 14px;
      margin: 0 0 12px;
    }
    .section-head h2 { margin: 0; font-size: 22px; }
    .section-head p { max-width: 760px; font-size: 14px; }
    .two { display: grid; grid-template-columns: 1.15fr .85fr; gap: 18px; align-items: start; }
    .three { display: grid; grid-template-columns: 1fr 1fr 0.85fr; gap: 14px; }
    .head {
      padding: 16px 18px;
      border-bottom: 1px solid var(--line);
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 10px;
    }
    .head h3 { margin: 0; font-size: 15px; }
    .pill {
      display: inline-flex;
      align-items: center;
      padding: 5px 9px;
      border-radius: 999px;
      color: var(--muted);
      border: 1px solid var(--line);
      background: rgba(255,255,255,.05);
      font-size: 12px;
      font-weight: 900;
    }
    table { width: 100%; border-collapse: collapse; font-size: 13px; }
    th, td { padding: 12px 14px; border-bottom: 1px solid var(--line); text-align: left; white-space: nowrap; }
    th { color: var(--muted); font-size: 11px; text-transform: uppercase; letter-spacing: .07em; }
    .table-wrap { overflow: auto; }
    .platform { color: var(--green); font-weight: 950; }
    .platform.yt { color: var(--pink); }
    form { display: grid; gap: 12px; }
    .form-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; }
    label { display: grid; gap: 7px; color: var(--muted); font-size: 12px; font-weight: 900; }
    input, select, textarea {
      width: 100%;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: rgba(255,255,255,.07);
      color: var(--text);
      padding: 11px 12px;
      font: inherit;
      outline: none;
    }
    input, select { height: 44px; }
    select option { color: #0f172a; }
    textarea { min-height: 150px; resize: vertical; line-height: 1.4; }
    .result {
      min-height: 195px;
      margin: 0;
      padding: 16px;
      border-radius: 8px;
      background: #03070b;
      border: 1px solid rgba(255,255,255,.1);
      color: #b7ffcf;
      white-space: pre-wrap;
      overflow: auto;
      font-size: 12px;
      line-height: 1.45;
    }
    .tabs { display: flex; gap: 8px; padding: 16px 18px 0; }
    .tab[aria-selected="true"] { background: rgba(88,166,255,.18); border-color: rgba(88,166,255,.45); }
    .tabpanels { padding: 16px 18px 18px; }
    .tabpanel[hidden] { display: none; }
    .candidate-list { display: grid; gap: 10px; }
    .candidate {
      display: grid;
      grid-template-columns: auto 1fr auto;
      align-items: center;
      gap: 12px;
      padding: 12px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel2);
    }
    .rank {
      width: 32px;
      height: 32px;
      display: grid;
      place-items: center;
      border-radius: 8px;
      background: rgba(88,166,255,.16);
      color: var(--blue);
      font-weight: 950;
    }
    .candidate b { display: block; font-size: 13px; }
    .candidate span { display: block; color: var(--muted); font-size: 12px; margin-top: 4px; }
    .score { color: var(--green); font-weight: 950; }
    .bar-row { display: grid; gap: 8px; margin-top: 12px; }
    .bar-label { display: flex; justify-content: space-between; color: var(--muted); font-size: 12px; font-weight: 900; }
    .track { height: 10px; border-radius: 999px; background: rgba(255,255,255,.08); overflow: hidden; }
    .fill { height: 100%; border-radius: inherit; background: linear-gradient(90deg, var(--green), var(--blue)); width: 0; transition: width .8s ease; }
    @media (max-width: 980px) {
      .hero, .two { grid-template-columns: 1fr; }
      .kpis, .chart-grid, .three { grid-template-columns: repeat(2, 1fr); }
    }
    @media (max-width: 680px) {
      .shell { padding: 16px; }
      .nav { align-items: flex-start; flex-direction: column; }
      .kpis, .chart-grid, .three, .form-grid { grid-template-columns: 1fr; }
      h1 { font-size: 40px; }
    }
  </style>
</head>
<body>
  <div class="shell">
    <nav class="nav">
      <div class="brand">
        <div class="logo">P</div>
        <div><strong>PostPulse Optimizer</strong><span>Creator-aware platform and timing intelligence</span></div>
      </div>
      <div class="links">
        <a href="#analytics">Analytics</a>
        <a href="#submit">Submit API</a>
        <a href="#explain">Explain</a>
        <a class="primary" href="/analytics" target="_blank">Raw JSON</a>
      </div>
    </nav>

    <header class="hero">
      <div class="card pad">
        <div class="eyebrow">Live evaluator-aligned backend</div>
        <h1>Predict the best moment to publish.</h1>
        <p>PostPulse scores Instagram and YouTube across every hour, then chooses the highest-value platform-time pair using creator history, platform activity, and content fit.</p>
        <div class="kpis" id="metrics"></div>
      </div>
      <div class="card pad">
        <div class="chart-grid">
          <div class="chart-card">
            <div class="chart-title"><span>Score Breakdown</span><span class="pill" id="finalScore">--</span></div>
            <canvas id="scoreChart" width="520" height="260"></canvas>
          </div>
          <div class="chart-card">
            <div class="chart-title"><span>Platform Mix</span><span class="pill">Live</span></div>
            <canvas id="platformChart" width="520" height="260"></canvas>
          </div>
        </div>
      </div>
    </header>

    <section id="analytics">
      <div class="section-head">
        <div><h2>Analytics Dashboard</h2><p>Charts are generated from `/analytics`, so the presentation visuals and backend output stay consistent.</p></div>
      </div>
      <div class="three">
        <div class="card pad">
          <h3>Decision Split</h3>
          <canvas id="decisionChart" width="430" height="250"></canvas>
        </div>
        <div class="card pad">
          <h3>Recommended Hours</h3>
          <canvas id="hourChart" width="520" height="250"></canvas>
        </div>
        <div class="card pad">
          <h3>Metric Bars</h3>
          <div id="metricBars"></div>
        </div>
      </div>
    </section>

    <section>
      <div class="section-head">
        <div><h2>Top Recommendations</h2><p>Highest-confidence recommendations ranked by optimizer score.</p></div>
      </div>
      <div class="card">
        <div class="table-wrap">
          <table>
            <thead><tr><th>Content</th><th>Platform</th><th>Hour</th><th>Decision</th><th>Expected</th><th>Score</th></tr></thead>
            <tbody id="topRows"></tbody>
          </table>
        </div>
      </div>
    </section>

    <section id="submit">
      <div class="section-head">
        <div><h2>Submit Content API</h2><p>Use the buttons here instead of manual testing. Submitted content is stored in backend memory, so `/get_recommendation` can retrieve it by id afterward.</p></div>
      </div>
      <div class="two">
        <div class="card">
          <div class="head"><h3>Request Builder</h3><span class="pill">POST APIs</span></div>
          <div class="tabs">
            <button class="tab" id="tab-single" aria-selected="true" onclick="selectTab('single')">Single Submit</button>
            <button class="tab" id="tab-batch" aria-selected="false" onclick="selectTab('batch')">Batch Submit</button>
          </div>
          <div class="tabpanels">
            <div class="tabpanel" id="panel-single">
              <form id="submitForm">
                <div class="form-grid">
                  <label>Content ID <input name="content_id" type="number" value="1040"></label>
                  <label>Creator ID <input name="creator_id" type="number" value="24"></label>
                  <label>Content Type <select name="content_type"><option>SHORT</option><option selected>LONG</option></select></label>
                  <label>Created Timestamp <input name="created_timestamp" min="0" max="23" type="number" value="22"></label>
                  <label>Time Sensitivity <select name="time_sensitivity"><option>High</option><option selected>Medium</option><option>Low</option></select></label>
                </div>
                <button class="primary" type="submit">Submit Content</button>
              </form>
            </div>
            <div class="tabpanel" id="panel-batch" hidden>
              <textarea id="batchPayload" spellcheck="false">{
  "items": [
    {"content_id": 2001, "creator_id": 24, "content_type": "SHORT", "created_timestamp": 18, "time_sensitivity": "High"},
    {"content_id": 2002, "creator_id": 43, "content_type": "LONG", "created_timestamp": 22, "time_sensitivity": "Medium"}
  ]
}</textarea>
              <div style="height:12px"></div>
              <button class="primary" onclick="submitBatch()">Submit Batch</button>
            </div>
          </div>
        </div>
        <div class="card">
          <div class="head"><h3>API Response</h3><span class="pill">Live JSON</span></div>
          <div class="pad"><pre class="result" id="submitResult">Click Submit Content to call POST /submit_content.</pre></div>
        </div>
      </div>
    </section>

    <section id="explain">
      <div class="section-head">
        <div><h2>Explain a Recommendation</h2><p>Shows the top five platform-time candidates and the activity/history values that drove the decision.</p></div>
      </div>
      <div class="two">
        <div class="card pad">
          <div class="form-grid" style="grid-template-columns:1fr auto">
            <label>Content ID <input id="cid" type="number" value="1"></label>
            <button class="primary" style="align-self:end" onclick="lookup()">Analyze</button>
          </div>
          <div style="height:14px"></div>
          <div class="candidate-list" id="lookupResult"></div>
        </div>
        <div class="card pad">
          <h3>Scoring Formula</h3>
          <pre class="result">expected = creator_base * activity_score * historical_engagement

score = 0.50 * normalized(expected)
      + 0.20 * activity_score
      + 0.15 * platform_quality</pre>
        </div>
      </div>
    </section>
  </div>

  <script>
    const byId = id => document.getElementById(id);
    const pct = value => `${(value * 100).toFixed(2)}%`;
    const colors = ["#33d69f", "#58a6ff", "#ffd166", "#ff6b9a", "#a78bfa"];

    async function safeJson(response) {
      try { return await response.json(); } catch { return {error: "Invalid response"}; }
    }

    function kpi(label, value, note) {
      return `<div class="kpi"><label>${label}</label><strong>${value}</strong><small>${note}</small></div>`;
    }

    function drawBars(canvas, labels, values, maxValue, colorList = colors) {
      const ctx = canvas.getContext("2d");
      const w = canvas.width, h = canvas.height;
      ctx.clearRect(0, 0, w, h);
      if (values.length <= 4) {
        const left = 94, right = 26, top = 28, rowH = 48;
        values.forEach((v, i) => {
          const y = top + i * rowH;
          const maxW = w - left - right;
          const bw = Math.max(4, (maxW * v) / maxValue);
          ctx.fillStyle = "#a9b7c8";
          ctx.font = "800 14px system-ui";
          ctx.textAlign = "left";
          ctx.fillText(labels[i], 14, y + 20);
          ctx.fillStyle = "rgba(255,255,255,.08)";
          roundRect(ctx, left, y, maxW, 20, 10); ctx.fill();
          const grad = ctx.createLinearGradient(left, y, left + bw, y);
          grad.addColorStop(0, colorList[i % colorList.length]);
          grad.addColorStop(1, "rgba(255,255,255,.36)");
          ctx.fillStyle = grad;
          roundRect(ctx, left, y, bw, 20, 10); ctx.fill();
          ctx.fillStyle = "#f7fbff";
          ctx.font = "900 13px system-ui";
          ctx.textAlign = "right";
          ctx.fillText(`${Math.round(v * 100)}%`, w - 10, y + 16);
        });
        return;
      }
      const left = 34, bottom = h - 34, top = 20;
      const gap = 4;
      const barW = (w - left - 18 - gap * (values.length - 1)) / values.length;
      ctx.strokeStyle = "rgba(255,255,255,.12)";
      ctx.beginPath(); ctx.moveTo(left, top); ctx.lineTo(left, bottom); ctx.lineTo(w - 8, bottom); ctx.stroke();
      values.forEach((v, i) => {
        const bh = ((bottom - top) * v) / maxValue;
        const x = left + i * (barW + gap);
        const y = bottom - bh;
        const grad = ctx.createLinearGradient(0, y, 0, bottom);
        grad.addColorStop(0, colorList[i % colorList.length]);
        grad.addColorStop(1, "rgba(255,255,255,.08)");
        ctx.fillStyle = grad;
        roundRect(ctx, x, y, barW, bh, 7); ctx.fill();
        if (i % 3 === 0) {
          ctx.fillStyle = "#a9b7c8"; ctx.font = "11px system-ui"; ctx.textAlign = "center";
          ctx.fillText(labels[i], x + barW / 2, h - 10);
        }
      });
    }

    function drawDonut(canvas, data) {
      const ctx = canvas.getContext("2d");
      const entries = Object.entries(data);
      const total = entries.reduce((sum, [,v]) => sum + v, 0) || 1;
      const cx = canvas.width / 2, cy = canvas.height / 2 - 10, radius = Math.min(86, canvas.height * 0.32);
      let start = -Math.PI / 2;
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      entries.forEach(([label, value], i) => {
        const angle = (value / total) * Math.PI * 2;
        ctx.beginPath();
        ctx.arc(cx, cy, radius, start, start + angle);
        ctx.lineWidth = 30;
        ctx.strokeStyle = colors[i % colors.length];
        ctx.stroke();
        start += angle;
      });
      ctx.fillStyle = "#f7fbff"; ctx.font = "950 30px system-ui"; ctx.textAlign = "center";
      ctx.fillText(String(total), cx, cy + 8);
      ctx.font = "12px system-ui"; ctx.fillStyle = "#a9b7c8";
      ctx.fillText("items", cx, cy + 28);
      entries.forEach(([label, value], i) => {
        const y = canvas.height - 52 + i * 22;
        ctx.fillStyle = colors[i % colors.length]; roundRect(ctx, 18, y - 10, 12, 12, 3); ctx.fill();
        ctx.fillStyle = "#a9b7c8"; ctx.textAlign = "left"; ctx.font = "12px system-ui";
        ctx.fillText(`${label}: ${value}`, 38, y);
      });
    }

    function roundRect(ctx, x, y, w, h, r) {
      const rr = Math.min(r, w / 2, h / 2);
      ctx.beginPath();
      ctx.moveTo(x + rr, y);
      ctx.arcTo(x + w, y, x + w, y + h, rr);
      ctx.arcTo(x + w, y + h, x, y + h, rr);
      ctx.arcTo(x, y + h, x, y, rr);
      ctx.arcTo(x, y, x + w, y, rr);
      ctx.closePath();
    }

    function metricBars(score) {
      const rows = [
        ["Engagement", score.engagement_score],
        ["Timing", score.timing_score],
        ["Platform", score.platform_score],
        ["Efficiency", score.efficiency_score]
      ];
      return rows.map(([label, value]) => `
        <div class="bar-row">
          <div class="bar-label"><span>${label}</span><span>${pct(value)}</span></div>
          <div class="track"><div class="fill" style="width:${value * 100}%"></div></div>
        </div>
      `).join("");
    }

    async function load() {
      const data = await fetch("/analytics").then(safeJson);
      if (data.error) return;
      byId("finalScore").textContent = pct(data.score.final_score);
      byId("metrics").innerHTML = [
        kpi("Final Score", pct(data.score.final_score), "weighted evaluator score"),
        kpi("Timing", pct(data.score.timing_score), "chosen slots hit peak activity"),
        kpi("Platform", pct(data.score.platform_score), "SHORT/LONG fit quality"),
        kpi("Avg Expected", data.average_expected_engagement.toFixed(4), "base x activity x history")
      ].join("");
      byId("metricBars").innerHTML = metricBars(data.score);
      byId("topRows").innerHTML = data.top_recommendations.map(row => `
        <tr><td>#${row.content_id}</td><td><span class="platform ${row.platform === "YouTube" ? "yt" : ""}">${row.platform}</span></td><td>${row.time_slot}:00</td><td>${row.decision}</td><td>${row.expected_engagement.toFixed(4)}</td><td>${row.score.toFixed(4)}</td></tr>
      `).join("");
      drawBars(byId("scoreChart"), ["Eng", "Time", "Plat", "Eff"], [data.score.engagement_score, data.score.timing_score, data.score.platform_score, data.score.efficiency_score], 1);
      drawDonut(byId("platformChart"), data.platform_distribution);
      drawDonut(byId("decisionChart"), data.decision_distribution);
      const hourLabels = Array.from({length: 24}, (_, i) => String(i));
      const hourValues = hourLabels.map(h => data.time_slot_distribution[h] || 0);
      drawBars(byId("hourChart"), hourLabels, hourValues, Math.max(...hourValues, 1), ["#58a6ff"]);
      lookup();
    }

    function selectTab(tab) {
      const single = tab === "single";
      byId("tab-single").setAttribute("aria-selected", String(single));
      byId("tab-batch").setAttribute("aria-selected", String(!single));
      byId("panel-single").hidden = !single;
      byId("panel-batch").hidden = single;
    }

    async function postJson(path, body) {
      const response = await fetch(path, {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(body)});
      return safeJson(response);
    }

    byId("submitForm").addEventListener("submit", async event => {
      event.preventDefault();
      const body = Object.fromEntries(new FormData(event.target).entries());
      body.content_id = Number(body.content_id);
      body.creator_id = Number(body.creator_id);
      body.created_timestamp = Number(body.created_timestamp);
      byId("submitResult").textContent = "Submitting...";
      const data = await postJson("/submit_content", body);
      byId("submitResult").textContent = JSON.stringify(data, null, 2);
      byId("cid").value = body.content_id;
      await lookup();
      await load();
    });

    async function submitBatch() {
      try {
        byId("submitResult").textContent = "Submitting batch...";
        const data = await postJson("/batch_recommendations", JSON.parse(byId("batchPayload").value));
        byId("submitResult").textContent = JSON.stringify(data, null, 2);
        await load();
      } catch {
        byId("submitResult").textContent = JSON.stringify({error: "Invalid batch JSON"}, null, 2);
      }
    }

    async function lookup() {
      const cid = byId("cid").value;
      const data = await fetch(`/explain?content_id=${cid}`).then(safeJson);
      if (data.error) {
        byId("lookupResult").innerHTML = `<div class="candidate"><div class="rank">!</div><div><b>${data.error}</b><span>Submit this content id first or choose an existing id.</span></div><div class="score">--</div></div>`;
        return;
      }
      byId("lookupResult").innerHTML = data.top_candidates.map(row => `
        <div class="candidate">
          <div class="rank">${row.rank}</div>
          <div><b>${row.platform} at ${row.time_slot}:00 - ${row.decision}</b><span>expected ${row.expected_engagement.toFixed(4)} | activity ${row.activity_score.toFixed(2)} | history ${row.historical_engagement.toFixed(3)}</span></div>
          <div class="score">${row.score.toFixed(4)}</div>
        </div>
      `).join("");
    }

    load();
  </script>
</body>
</html>"""
