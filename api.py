import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from optimizer.analytics import build_analytics
from optimizer.data import Dataset
from optimizer.dashboard import render_dashboard
from optimizer.engine import RecommendationEngine
from optimizer.models import ContentItem


DATASET = Dataset("data/raw")
ENGINE = RecommendationEngine(DATASET)
CONTENT_BY_ID = {item.content_id: item for item in DATASET.content}
SUBMITTED_CONTENT: dict[int, ContentItem] = {}


def _find_content(content_id: int) -> ContentItem | None:
    return SUBMITTED_CONTENT.get(content_id) or CONTENT_BY_ID.get(content_id)


def _content_item(payload: dict) -> ContentItem:
    return ContentItem(
        content_id=int(payload.get("content_id", 0)),
        creator_id=int(payload["creator_id"]),
        content_type=str(payload["content_type"]).upper(),
        created_timestamp=int(payload["created_timestamp"]),
        time_sensitivity=str(payload.get("time_sensitivity", "Medium")),
    )


def _recommendation_detail(rec) -> dict:
    return {
        "rank": rec.rank,
        "platform": rec.platform,
        "time_slot": rec.time_slot,
        "decision": rec.decision,
        "expected_engagement": round(rec.expected_engagement, 6),
        "activity_score": rec.activity_score,
        "historical_engagement": rec.historical_engagement,
        "platform_quality": rec.platform_quality,
        "score": round(rec.score, 6),
    }


def _submit_content_page() -> str:
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Submit Content</title>
  <style>
    body {
      margin: 0;
      min-height: 100vh;
      display: grid;
      place-items: center;
      font-family: Inter, system-ui, sans-serif;
      color: #f4f7f4;
      background:
        linear-gradient(90deg, rgba(255,255,255,0.04) 1px, transparent 1px),
        linear-gradient(0deg, rgba(255,255,255,0.03) 1px, transparent 1px),
        radial-gradient(circle at 20% 10%, rgba(72,214,194,0.18), transparent 34%),
        #071012;
      background-size: 52px 52px, 52px 52px, auto, auto;
      padding: 24px;
    }
    main {
      width: min(760px, 100%);
      border: 1px solid rgba(220,236,229,0.16);
      border-radius: 8px;
      background: rgba(13,28,29,0.86);
      box-shadow: 0 28px 90px rgba(0,0,0,0.42);
      overflow: hidden;
    }
    header { padding: 22px 24px; border-bottom: 1px solid rgba(220,236,229,0.16); }
    h1 { margin: 0 0 7px; font-size: 28px; }
    p { margin: 0; color: #b9c6c1; line-height: 1.5; }
    form { padding: 24px; display: grid; gap: 14px; }
    .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
    label { display: grid; gap: 6px; color: #b9c6c1; font-size: 13px; }
    input, select, button {
      height: 42px;
      border-radius: 8px;
      border: 1px solid rgba(220,236,229,0.18);
      background: rgba(255,255,255,0.06);
      color: #f4f7f4;
      padding: 0 12px;
      font: inherit;
    }
    button {
      background: #48d6c2;
      color: #031110;
      border-color: transparent;
      font-weight: 800;
      cursor: pointer;
    }
    pre {
      margin: 0 24px 24px;
      min-height: 110px;
      white-space: pre-wrap;
      border-radius: 8px;
      background: #050b0c;
      color: #bde66d;
      padding: 16px;
      overflow: auto;
    }
    a { color: #48d6c2; }
    @media (max-width: 640px) { .grid { grid-template-columns: 1fr; } }
  </style>
</head>
<body>
  <main>
    <header>
      <h1>POST /submit_content</h1>
      <p>This page is a browser demo. The required API endpoint is still POST /submit_content and returns recommendation JSON.</p>
    </header>
    <form id="form">
      <div class="grid">
        <label>Content ID <input name="content_id" type="number" value="1001"></label>
        <label>Creator ID <input name="creator_id" type="number" value="24"></label>
        <label>Content Type
          <select name="content_type">
            <option>SHORT</option>
            <option>LONG</option>
          </select>
        </label>
        <label>Created Timestamp <input name="created_timestamp" type="number" min="0" max="23" value="18"></label>
        <label>Time Sensitivity
          <select name="time_sensitivity">
            <option>High</option>
            <option>Medium</option>
            <option>Low</option>
          </select>
        </label>
      </div>
      <button type="submit">Submit Content</button>
      <p>For existing content, use <a href="/get_recommendation?content_id=1">/get_recommendation?content_id=1</a>.</p>
    </form>
    <pre id="result">Submit the form to call POST /submit_content.</pre>
  </main>
  <script>
    document.getElementById("form").addEventListener("submit", async event => {
      event.preventDefault();
      const body = Object.fromEntries(new FormData(event.target).entries());
      body.content_id = Number(body.content_id);
      body.creator_id = Number(body.creator_id);
      body.created_timestamp = Number(body.created_timestamp);
      const response = await fetch("/submit_content", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(body)
      });
      const data = await response.json();
      document.getElementById("result").textContent = JSON.stringify(data, null, 2);
    });
  </script>
</body>
</html>"""


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/":
            self._html(render_dashboard())
            return
        if parsed.path == "/submit_content":
            self._html(_submit_content_page())
            return
        if parsed.path == "/get_recommendation":
            query = parse_qs(parsed.query)
            content_id = int(query.get("content_id", ["0"])[0])
            item = _find_content(content_id)
            if item is None:
                self._json({"error": "content_id not found"}, 404)
                return
            self._json(ENGINE.recommend(item).submission_row())
            return
        if parsed.path == "/explain":
            query = parse_qs(parsed.query)
            content_id = int(query.get("content_id", ["0"])[0])
            item = _find_content(content_id)
            if item is None:
                self._json({"error": "content_id not found"}, 404)
                return
            self._json(
                {
                    "content_id": content_id,
                    "top_candidates": [
                        _recommendation_detail(rec)
                        for rec in ENGINE.rank_candidates(item, limit=5)
                    ],
                }
            )
            return
        if parsed.path == "/analytics":
            self._json(build_analytics(DATASET, ENGINE))
            return
        if parsed.path == "/health":
            self._json({"status": "ok"})
            return
        self._json({"error": "not found"}, 404)

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        if path not in {"/submit_content", "/batch_recommendations"}:
            self._json({"error": "not found"}, 404)
            return
        length = int(self.headers.get("Content-Length", "0"))
        payload = json.loads(self.rfile.read(length) or b"{}")
        if path == "/batch_recommendations":
            items = [_content_item(row) for row in payload.get("items", [])]
            for item in items:
                SUBMITTED_CONTENT[item.content_id] = item
            self._json({"recommendations": [ENGINE.recommend(item).submission_row() for item in items]})
            return
        item = _content_item(payload)
        SUBMITTED_CONTENT[item.content_id] = item
        self._json(ENGINE.recommend(item).submission_row())

    def _json(self, payload: dict, status: int = 200) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _html(self, html: str, status: int = 200) -> None:
        body = html.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args) -> None:
        return


def main() -> None:
    server = ThreadingHTTPServer(("127.0.0.1", 8000), Handler)
    print("Dashboard running at http://127.0.0.1:8000")
    print("GET /get_recommendation?content_id=1")
    print("GET /explain?content_id=1")
    print("GET /analytics")
    print("POST /submit_content")
    print("POST /batch_recommendations")
    server.serve_forever()


if __name__ == "__main__":
    main()
