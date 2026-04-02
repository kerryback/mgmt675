"""
Mean-Variance Portfolio Optimization

Prompts for asset parameters, computes the tangency portfolio (no short sales),
and produces two plots: Plotly (HTML) and Matplotlib (PNG).
"""

import subprocess
import sys

def ensure_installed(package):
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

ensure_installed("numpy")
ensure_installed("scipy")
ensure_installed("plotly")
ensure_installed("matplotlib")

import numpy as np
from scipy.optimize import minimize
import plotly.graph_objects as go
import matplotlib.pyplot as plt


def get_inputs():
    n = int(input("Number of risky assets: "))
    print(f"\nEnter expected returns (%) for {n} assets:")
    mu = np.array([float(input(f"  Asset {i+1}: ")) for i in range(n)]) / 100

    print(f"\nEnter standard deviations (%) for {n} assets:")
    sigma = np.array([float(input(f"  Asset {i+1}: ")) for i in range(n)]) / 100

    print(f"\nEnter correlations (upper triangle):")
    corr = np.eye(n)
    for i in range(n):
        for j in range(i + 1, n):
            val = float(input(f"  Corr({i+1},{j+1}): "))
            corr[i, j] = val
            corr[j, i] = val

    rf = float(input("\nRisk-free rate (%): ")) / 100

    cov = np.outer(sigma, sigma) * corr
    return n, mu, sigma, cov, rf


def tangency_portfolio(mu, cov, rf, n):
    def neg_sharpe(w):
        port_ret = w @ mu
        port_sd = np.sqrt(w @ cov @ w)
        return -(port_ret - rf) / port_sd

    w0 = np.ones(n) / n
    bounds = [(0, 1)] * n
    constraints = [{"type": "eq", "fun": lambda w: np.sum(w) - 1}]
    result = minimize(neg_sharpe, w0, method="SLSQP", bounds=bounds, constraints=constraints)
    wt = result.x
    mu_t = wt @ mu
    sd_t = np.sqrt(wt @ cov @ wt)
    sharpe = (mu_t - rf) / sd_t
    return wt, mu_t, sd_t, sharpe


def efficient_frontier(mu, cov, rf, n, n_points=300):
    def port_var(w):
        return w @ cov @ w

    bounds = [(0, 1)] * n
    eq_constraint = {"type": "eq", "fun": lambda w: np.sum(w) - 1}

    # Min-variance portfolio
    w0 = np.ones(n) / n
    result = minimize(port_var, w0, method="SLSQP", bounds=bounds, constraints=[eq_constraint])
    mu_min = float(result.x @ mu)

    mu_max = float(np.max(mu))
    mu_grid = np.linspace(mu_min, mu_max, n_points)

    sd_list = []
    w_list = []
    for target in mu_grid:
        constraints = [
            eq_constraint,
            {"type": "ineq", "fun": lambda w, t=target: w @ mu - t},
        ]
        result = minimize(port_var, w0, method="SLSQP", bounds=bounds, constraints=constraints)
        if result.success:
            wv = result.x
            sd_list.append(np.sqrt(wv @ cov @ wv))
            w_list.append(wv)
        else:
            sd_list.append(np.nan)
            w_list.append(np.full(n, np.nan))

    return mu_grid, np.array(sd_list), np.array(w_list)


def plot_plotly(n, mu, sigma, rf, mu_t, sd_t, wt, sharpe, mu_grid, sd_frontier, w_frontier):
    pct = lambda x: f"{x*100:.2f}%"

    # Frontier
    hover_frontier = []
    for i in range(len(mu_grid)):
        wf = w_frontier[i]
        lines = [f"Return: {pct(mu_grid[i])}", f"Std Dev: {pct(sd_frontier[i])}"]
        for j in range(n):
            lines.append(f"w{j+1}: {pct(wf[j])}")
        hover_frontier.append("<br>".join(lines))

    frontier_trace = go.Scatter(
        x=sd_frontier * 100, y=mu_grid * 100,
        mode="lines", name="Efficient Frontier",
        line=dict(color="#3b82f6", width=3),
        text=hover_frontier, hoverinfo="text",
    )

    # Capital allocation line
    sd_cal = np.linspace(0, np.nanmax(sd_frontier) * 1.15, 200)
    mu_cal = rf + sharpe * sd_cal
    cal_trace = go.Scatter(
        x=sd_cal * 100, y=mu_cal * 100,
        mode="lines", name="Capital Allocation Line",
        line=dict(color="#f59e0b", width=2, dash="dash"),
        hoverinfo="x+y",
    )

    # Tangency portfolio
    tan_hover = [f"<b>Tangency Portfolio</b><br>Return: {pct(mu_t)}<br>Std Dev: {pct(sd_t)}"]
    for j in range(n):
        tan_hover[0] += f"<br>w{j+1}: {pct(wt[j])}"
    tan_hover[0] += f"<br>Sharpe: {sharpe:.3f}"

    tan_trace = go.Scatter(
        x=[sd_t * 100], y=[mu_t * 100],
        mode="markers", name="Tangency Portfolio",
        marker=dict(color="#dc2626", size=14, symbol="star"),
        text=tan_hover, hoverinfo="text",
    )

    # Risk-free
    rf_trace = go.Scatter(
        x=[0], y=[rf * 100],
        mode="markers", name="Risk-Free",
        marker=dict(color="#22c55e", size=10),
        hoverinfo="y",
    )

    # Individual assets
    asset_hover = [
        f"<b>Asset {j+1}</b><br>Return: {pct(mu[j])}<br>Std Dev: {pct(sigma[j])}"
        for j in range(n)
    ]
    asset_trace = go.Scatter(
        x=sigma * 100, y=mu * 100,
        mode="markers+text", name="Individual Assets",
        marker=dict(color="#8b5cf6", size=11, symbol="diamond"),
        text=[f"Asset {j+1}" for j in range(n)],
        textposition="top center",
        textfont=dict(size=12, color="#8b5cf6"),
        hovertext=asset_hover, hoverinfo="text",
    )

    fig = go.Figure(data=[frontier_trace, cal_trace, tan_trace, rf_trace, asset_trace])
    fig.update_layout(
        xaxis_title="Standard Deviation (%)",
        yaxis_title="Expected Return (%)",
        xaxis=dict(rangemode="tozero", gridcolor="#e2e8f0"),
        yaxis=dict(gridcolor="#e2e8f0"),
        plot_bgcolor="#fafbfc",
        font=dict(family="system-ui, sans-serif", size=13),
        legend=dict(x=0.02, y=0.98, bgcolor="rgba(255,255,255,0.8)"),
        margin=dict(t=40, r=30, b=60, l=60),
        hovermode="closest",
    )
    fig.write_html("efficient_frontier.html", auto_open=True)
    print("Saved: efficient_frontier.html")


def plot_matplotlib(n, mu, sigma, rf, mu_t, sd_t, wt, sharpe, mu_grid, sd_frontier):
    fig, ax = plt.subplots(figsize=(10, 7))

    # Efficient frontier
    ax.plot(sd_frontier * 100, mu_grid * 100, color="#3b82f6", linewidth=2.5, label="Efficient Frontier")

    # Capital allocation line
    sd_cal = np.linspace(0, np.nanmax(sd_frontier) * 1.15, 200)
    mu_cal = rf + sharpe * sd_cal
    ax.plot(sd_cal * 100, mu_cal * 100, color="#f59e0b", linewidth=1.5, linestyle="--", label="Capital Allocation Line")

    # Tangency portfolio
    ax.scatter([sd_t * 100], [mu_t * 100], color="#dc2626", s=150, marker="*", zorder=5, label="Tangency Portfolio")

    # Risk-free
    ax.scatter([0], [rf * 100], color="#22c55e", s=80, zorder=5, label="Risk-Free")

    # Individual assets
    ax.scatter(sigma * 100, mu * 100, color="#8b5cf6", s=70, marker="D", zorder=5, label="Individual Assets")
    for j in range(n):
        ax.annotate(f"Asset {j+1}", (sigma[j] * 100, mu[j] * 100),
                     textcoords="offset points", xytext=(5, 8),
                     fontsize=9, color="#8b5cf6")

    ax.set_xlabel("Standard Deviation (%)", fontsize=12)
    ax.set_ylabel("Expected Return (%)", fontsize=12)
    ax.set_xlim(left=0)
    ax.legend(loc="upper left", fontsize=10)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig("efficient_frontier.png", dpi=150)
    print("Saved: efficient_frontier.png")
    plt.close(fig)

    import webbrowser, os
    webbrowser.open(os.path.abspath("efficient_frontier.png"))


def main():
    n, mu, sigma, cov, rf = get_inputs()

    wt, mu_t, sd_t, sharpe = tangency_portfolio(mu, cov, rf, n)

    print("\n" + "=" * 50)
    print("TANGENCY PORTFOLIO")
    print("=" * 50)
    for j in range(n):
        print(f"  Asset {j+1}: {wt[j]*100:.2f}%")
    print(f"  Expected Return: {mu_t*100:.2f}%")
    print(f"  Standard Deviation: {sd_t*100:.2f}%")
    print(f"  Sharpe Ratio: {sharpe:.4f}")
    print("=" * 50)

    mu_grid, sd_frontier, w_frontier = efficient_frontier(mu, cov, rf, n)

    # Remove NaN points
    valid = ~np.isnan(sd_frontier)
    mu_grid = mu_grid[valid]
    sd_frontier = sd_frontier[valid]
    w_frontier = w_frontier[valid]

    plot_plotly(n, mu, sigma, rf, mu_t, sd_t, wt, sharpe, mu_grid, sd_frontier, w_frontier)
    plot_matplotlib(n, mu, sigma, rf, mu_t, sd_t, wt, sharpe, mu_grid, sd_frontier)


if __name__ == "__main__":
    main()
