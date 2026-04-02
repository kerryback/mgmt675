"""
Mean-Variance Optimization App (3 risky assets, no short sales)

Usage:
    uvicorn demos.m9.mean_variance_app:app --port 8000

    Open http://localhost:8000 in your browser.
"""

import numpy as np
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from scipy.optimize import minimize

app = FastAPI()


class MVInput(BaseModel):
    mu: list[float]        # expected returns (3)
    sigma: list[float]     # std devs (3)
    corr12: float
    corr13: float
    corr23: float
    rf: float              # risk-free rate


def solve(data: MVInput):
    mu = np.array(data.mu)
    sd = np.array(data.sigma)
    C = np.array([
        [1, data.corr12, data.corr13],
        [data.corr12, 1, data.corr23],
        [data.corr13, data.corr23, 1],
    ])
    cov = np.outer(sd, sd) * C

    n = len(mu)
    w0 = np.ones(n) / n
    bounds = [(0, 1)] * n
    cons_sum = {"type": "eq", "fun": lambda w: w.sum() - 1}

    # Tangency portfolio (max Sharpe, no short sales)
    def neg_sharpe(w):
        port_sd = np.sqrt(w @ cov @ w)
        return -(w @ mu - data.rf) / port_sd

    res_tan = minimize(neg_sharpe, w0, bounds=bounds, constraints=cons_sum)
    w_tan = res_tan.x
    mu_tan = float(w_tan @ mu)
    sd_tan = float(np.sqrt(w_tan @ cov @ w_tan))
    sharpe = (mu_tan - data.rf) / sd_tan

    # Minimum-variance portfolio (no short sales)
    def port_var(w):
        return float(w @ cov @ w)

    res_mv = minimize(port_var, w0, bounds=bounds, constraints=cons_sum)
    mv_mu = float(res_mv.x @ mu)

    # Efficient frontier (no short sales)
    targets = np.linspace(mv_mu, mu.max(), 100)
    mu_grid, sd_frontier, w_frontier = [], [], []
    for t in targets:
        cons_t = [
            cons_sum,
            {"type": "eq", "fun": lambda w, _t=t: w @ mu - _t},
        ]
        res_t = minimize(port_var, w0, bounds=bounds, constraints=cons_t)
        if res_t.success:
            mu_grid.append(t)
            sd_frontier.append(float(np.sqrt(res_t.x @ cov @ res_t.x)))
            w_frontier.append(res_t.x.tolist())

    # Capital market line
    sd_cal = np.linspace(0, max(sd_frontier) * 1.15, 100)
    mu_cal = data.rf + sharpe * sd_cal

    return {
        "w_tan": w_tan.tolist(),
        "mu_tan": mu_tan,
        "sd_tan": sd_tan,
        "sharpe": float(sharpe),
        "mu_grid": mu_grid,
        "sd_frontier": sd_frontier,
        "w_frontier": w_frontier,
        "sd_cal": sd_cal.tolist(),
        "mu_cal": mu_cal.tolist(),
    }


@app.post("/solve")
def api_solve(data: MVInput):
    return solve(data)


@app.get("/", response_class=HTMLResponse)
def index():
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Mean-Variance Optimizer</title>
<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: system-ui, sans-serif; background: #f0f2f5; padding: 1.5rem; }
  .container { max-width: 1200px; margin: 0 auto; }
  h1 { text-align: center; color: #1e293b; margin-bottom: 0.3rem; font-size: 1.8rem; }
  .subtitle { text-align: center; color: #64748b; margin-bottom: 1.5rem; font-size: 0.95rem; }
  .layout { display: grid; grid-template-columns: 340px 1fr; gap: 1.5rem; }
  .panel { background: #fff; border-radius: 12px; padding: 1.5rem;
           box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
  h2 { font-size: 1rem; color: #1e293b; margin-bottom: 0.8rem; }
  .section { margin-bottom: 1.2rem; }
  .section-title { font-size: 0.8rem; font-weight: 600; color: #64748b;
                   text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem; }
  .row { display: flex; gap: 0.5rem; margin-bottom: 0.4rem; align-items: center; }
  .row label { width: 70px; font-size: 0.85rem; color: #475569; }
  .row input { flex: 1; padding: 0.4rem 0.6rem; border: 1px solid #cbd5e1;
               border-radius: 6px; font-size: 0.85rem; }
  .row input:focus { border-color: #2563eb; outline: none; }
  button { width: 100%; padding: 0.7rem; border: none; border-radius: 8px;
           background: #2563eb; color: #fff; font-size: 0.95rem;
           font-weight: 600; cursor: pointer; margin-top: 0.5rem; }
  button:hover { background: #1d4ed8; }
  button:disabled { opacity: 0.5; cursor: default; }
  #result { margin-top: 1rem; font-size: 0.85rem; color: #1e293b;
            background: #f8fafc; border-radius: 8px; padding: 0.8rem; display: none; }
  #result h3 { font-size: 0.9rem; margin-bottom: 0.4rem; color: #2563eb; }
  #plot { width: 100%; height: 600px; }
  .error { color: #dc2626; font-size: 0.85rem; margin-top: 0.5rem; }
</style>
</head>
<body>
<div class="container">
  <h1>Mean-Variance Optimizer</h1>
  <p class="subtitle">Three Risky Assets + Risk-Free &bull; No Short Sales</p>
  <div class="layout">
    <div class="panel">
      <div class="section">
        <div class="section-title">Expected Returns (%)</div>
        <div class="row"><label>Asset 1</label><input id="mu1" type="number" step="0.1" value="10"></div>
        <div class="row"><label>Asset 2</label><input id="mu2" type="number" step="0.1" value="14"></div>
        <div class="row"><label>Asset 3</label><input id="mu3" type="number" step="0.1" value="8"></div>
      </div>
      <div class="section">
        <div class="section-title">Standard Deviations (%)</div>
        <div class="row"><label>Asset 1</label><input id="sd1" type="number" step="0.1" value="18"></div>
        <div class="row"><label>Asset 2</label><input id="sd2" type="number" step="0.1" value="25"></div>
        <div class="row"><label>Asset 3</label><input id="sd3" type="number" step="0.1" value="15"></div>
      </div>
      <div class="section">
        <div class="section-title">Correlations</div>
        <div class="row"><label>1 &amp; 2</label><input id="c12" type="number" step="0.05" value="0.3" min="-1" max="1"></div>
        <div class="row"><label>1 &amp; 3</label><input id="c13" type="number" step="0.05" value="0.1" min="-1" max="1"></div>
        <div class="row"><label>2 &amp; 3</label><input id="c23" type="number" step="0.05" value="0.2" min="-1" max="1"></div>
      </div>
      <div class="section">
        <div class="section-title">Risk-Free Rate (%)</div>
        <div class="row"><label>Rate</label><input id="rf" type="number" step="0.1" value="4"></div>
      </div>
      <button id="btn" onclick="run()">Optimize</button>
      <div id="error" class="error"></div>
      <div id="result">
        <h3>Tangency Portfolio</h3>
        <div id="weights"></div>
      </div>
    </div>
    <div class="panel">
      <div id="plot"></div>
    </div>
  </div>
</div>
<script>
const v = id => parseFloat(document.getElementById(id).value);

async function run() {
  const btn = document.getElementById("btn");
  const err = document.getElementById("error");
  err.textContent = "";
  btn.disabled = true;
  try {
    const body = {
      mu: [v("mu1")/100, v("mu2")/100, v("mu3")/100],
      sigma: [v("sd1")/100, v("sd2")/100, v("sd3")/100],
      corr12: v("c12"), corr13: v("c13"), corr23: v("c23"),
      rf: v("rf")/100
    };
    const res = await fetch("/solve", {
      method: "POST", headers: {"Content-Type": "application/json"},
      body: JSON.stringify(body)
    });
    if (!res.ok) throw new Error(await res.text());
    const d = await res.json();
    showResult(d, body);
  } catch(e) { err.textContent = "Error: " + e.message; }
  btn.disabled = false;
}

function showResult(d, inp) {
  const pct = x => (x*100).toFixed(2) + "%";
  const r = document.getElementById("result");
  r.style.display = "block";
  const w = d.w_tan;
  document.getElementById("weights").innerHTML =
    `<b>Asset 1:</b> ${pct(w[0])} &nbsp; <b>Asset 2:</b> ${pct(w[1])} &nbsp; <b>Asset 3:</b> ${pct(w[2])}<br>` +
    `<b>Expected Return:</b> ${pct(d.mu_tan)} &nbsp; <b>Std Dev:</b> ${pct(d.sd_tan)} &nbsp; <b>Sharpe:</b> ${d.sharpe.toFixed(3)}`;

  // Frontier hover text with weights
  const frontierHover = d.mu_grid.map((m, i) => {
    const wf = d.w_frontier[i];
    return `Return: ${(m*100).toFixed(2)}%<br>Std Dev: ${(d.sd_frontier[i]*100).toFixed(2)}%<br>` +
           `w1: ${(wf[0]*100).toFixed(1)}% w2: ${(wf[1]*100).toFixed(1)}% w3: ${(wf[2]*100).toFixed(1)}%`;
  });

  const frontier = {
    x: d.sd_frontier.map(s => s*100), y: d.mu_grid.map(m => m*100),
    mode: "lines", name: "Efficient Frontier",
    line: { color: "#3b82f6", width: 3 },
    text: frontierHover, hoverinfo: "text"
  };
  const cal = {
    x: d.sd_cal.map(s => s*100), y: d.mu_cal.map(m => m*100),
    mode: "lines", name: "Capital Market Line",
    line: { color: "#f59e0b", width: 2, dash: "dash" },
    hoverinfo: "x+y"
  };
  const tan = {
    x: [d.sd_tan*100], y: [d.mu_tan*100],
    mode: "markers", name: "Tangency Portfolio",
    marker: { color: "#dc2626", size: 14, symbol: "star" },
    text: [`<b>Tangency Portfolio</b><br>Return: ${pct(d.mu_tan)}<br>Std Dev: ${pct(d.sd_tan)}<br>` +
           `w1: ${(w[0]*100).toFixed(1)}% w2: ${(w[1]*100).toFixed(1)}% w3: ${(w[2]*100).toFixed(1)}%<br>` +
           `Sharpe: ${d.sharpe.toFixed(3)}`],
    hoverinfo: "text"
  };
  const rf = {
    x: [0], y: [inp.rf*100],
    mode: "markers", name: "Risk-Free",
    marker: { color: "#22c55e", size: 10 },
    hoverinfo: "y"
  };
  const assets = {
    x: inp.sigma.map(s => s*100), y: inp.mu.map(m => m*100),
    mode: "markers+text", name: "Individual Assets",
    marker: { color: "#8b5cf6", size: 11, symbol: "diamond" },
    text: ["Asset 1", "Asset 2", "Asset 3"],
    textposition: "top center",
    textfont: { size: 12, color: "#8b5cf6" },
    hovertext: inp.mu.map((m, i) =>
      `<b>Asset ${i+1}</b><br>Return: ${(m*100).toFixed(2)}%<br>Std Dev: ${(inp.sigma[i]*100).toFixed(2)}%`),
    hoverinfo: "text"
  };

  const layout = {
    xaxis: { title: "Standard Deviation (%)", rangemode: "tozero",
             gridcolor: "#e2e8f0", zerolinecolor: "#cbd5e1" },
    yaxis: { title: "Expected Return (%)",
             gridcolor: "#e2e8f0", zerolinecolor: "#cbd5e1" },
    plot_bgcolor: "#fafbfc",
    paper_bgcolor: "#fff",
    font: { family: "system-ui, sans-serif", size: 13 },
    legend: { x: 0.02, y: 0.98, bgcolor: "rgba(255,255,255,0.8)" },
    margin: { t: 30, r: 30, b: 60, l: 60 },
    hovermode: "closest"
  };
  Plotly.newPlot("plot", [frontier, cal, tan, rf, assets], layout, {responsive: true});
}

// Run on load
run();
</script>
</body>
</html>"""
