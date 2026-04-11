"""
Portfolio Review Agent — MGMT 675 Demo
Uses the Claude Agent SDK with tools for portfolio analysis,
tax-loss harvesting, and replacement selection.
"""

import anthropic
import duckdb
import io
import json
import os
import sys
from dotenv import load_dotenv

# ─────────────────────────────────────────────────────────────
# 1. MOCK DATA: Portfolio holdings, targets, and recommendations
# ─────────────────────────────────────────────────────────────

# Target sector allocations for the portfolio
TARGET_ALLOCATION = {
    "Technology": 0.25,
    "Healthcare": 0.15,
    "Financial Services": 0.15,
    "Consumer Cyclical": 0.10,
    "Industrials": 0.10,
    "Energy": 0.08,
    "Communication Services": 0.07,
    "Consumer Defensive": 0.05,
    "Utilities": 0.03,
    "Real Estate": 0.02,
}

# Portfolio holdings with tax lots
# Each holding: ticker, sector, lots: [{date_acquired, shares, cost_basis_per_share}]
HOLDINGS = [
    # ── Technology (target 25%) ──
    {"ticker": "AAPL", "sector": "Technology", "lots": [
        {"date_acquired": "2021-03-15", "shares": 80, "cost_basis": 122.50},
        {"date_acquired": "2022-01-10", "shares": 50, "cost_basis": 172.30},
        {"date_acquired": "2023-06-20", "shares": 40, "cost_basis": 185.00},
        {"date_acquired": "2024-07-01", "shares": 30, "cost_basis": 220.00},
    ]},
    {"ticker": "MSFT", "sector": "Technology", "lots": [
        {"date_acquired": "2020-11-01", "shares": 60, "cost_basis": 215.00},
        {"date_acquired": "2022-05-15", "shares": 35, "cost_basis": 270.00},
        {"date_acquired": "2023-09-10", "shares": 25, "cost_basis": 330.00},
    ]},
    {"ticker": "NVDA", "sector": "Technology", "lots": [
        {"date_acquired": "2022-10-01", "shares": 100, "cost_basis": 125.00},
        {"date_acquired": "2023-05-15", "shares": 60, "cost_basis": 305.00},
        {"date_acquired": "2024-03-01", "shares": 40, "cost_basis": 790.00},
        {"date_acquired": "2024-09-15", "shares": 25, "cost_basis": 118.00},
    ]},
    {"ticker": "AVGO", "sector": "Technology", "lots": [
        {"date_acquired": "2022-06-01", "shares": 30, "cost_basis": 520.00},
        {"date_acquired": "2023-11-01", "shares": 20, "cost_basis": 875.00},
    ]},
    {"ticker": "CRM", "sector": "Technology", "lots": [
        {"date_acquired": "2022-12-01", "shares": 45, "cost_basis": 132.00},
        {"date_acquired": "2023-08-15", "shares": 30, "cost_basis": 215.00},
        {"date_acquired": "2024-06-01", "shares": 20, "cost_basis": 248.00},
    ]},
    {"ticker": "ADBE", "sector": "Technology", "lots": [
        {"date_acquired": "2021-11-15", "shares": 25, "cost_basis": 650.00},
        {"date_acquired": "2023-01-10", "shares": 20, "cost_basis": 345.00},
        {"date_acquired": "2024-02-01", "shares": 15, "cost_basis": 560.00},
    ]},
    {"ticker": "AMD", "sector": "Technology", "lots": [
        {"date_acquired": "2022-07-01", "shares": 70, "cost_basis": 85.00},
        {"date_acquired": "2023-10-15", "shares": 40, "cost_basis": 105.00},
        {"date_acquired": "2024-08-01", "shares": 30, "cost_basis": 145.00},
    ]},
    {"ticker": "INTC", "sector": "Technology", "lots": [
        {"date_acquired": "2021-04-01", "shares": 100, "cost_basis": 64.00},
        {"date_acquired": "2022-09-01", "shares": 80, "cost_basis": 29.00},
        {"date_acquired": "2023-12-15", "shares": 60, "cost_basis": 47.00},
        {"date_acquired": "2024-10-01", "shares": 50, "cost_basis": 23.00},
    ]},
    {"ticker": "NOW", "sector": "Technology", "lots": [
        {"date_acquired": "2022-03-01", "shares": 15, "cost_basis": 540.00},
        {"date_acquired": "2023-07-01", "shares": 10, "cost_basis": 560.00},
    ]},
    {"ticker": "ORCL", "sector": "Technology", "lots": [
        {"date_acquired": "2023-01-15", "shares": 50, "cost_basis": 82.00},
        {"date_acquired": "2024-04-01", "shares": 35, "cost_basis": 125.00},
    ]},
    # ── Healthcare (target 15%) ──
    {"ticker": "UNH", "sector": "Healthcare", "lots": [
        {"date_acquired": "2021-06-01", "shares": 20, "cost_basis": 400.00},
        {"date_acquired": "2022-10-15", "shares": 15, "cost_basis": 525.00},
        {"date_acquired": "2024-01-10", "shares": 10, "cost_basis": 540.00},
    ]},
    {"ticker": "JNJ", "sector": "Healthcare", "lots": [
        {"date_acquired": "2020-08-01", "shares": 40, "cost_basis": 148.00},
        {"date_acquired": "2022-04-15", "shares": 30, "cost_basis": 178.00},
        {"date_acquired": "2023-10-01", "shares": 25, "cost_basis": 155.00},
    ]},
    {"ticker": "LLY", "sector": "Healthcare", "lots": [
        {"date_acquired": "2021-09-01", "shares": 25, "cost_basis": 260.00},
        {"date_acquired": "2023-03-15", "shares": 15, "cost_basis": 340.00},
        {"date_acquired": "2024-05-01", "shares": 10, "cost_basis": 780.00},
    ]},
    {"ticker": "PFE", "sector": "Healthcare", "lots": [
        {"date_acquired": "2021-08-01", "shares": 100, "cost_basis": 48.00},
        {"date_acquired": "2022-02-15", "shares": 80, "cost_basis": 52.00},
        {"date_acquired": "2023-05-01", "shares": 60, "cost_basis": 38.00},
        {"date_acquired": "2024-03-01", "shares": 50, "cost_basis": 27.00},
    ]},
    {"ticker": "ABBV", "sector": "Healthcare", "lots": [
        {"date_acquired": "2022-01-01", "shares": 35, "cost_basis": 135.00},
        {"date_acquired": "2023-06-15", "shares": 25, "cost_basis": 148.00},
    ]},
    {"ticker": "MRK", "sector": "Healthcare", "lots": [
        {"date_acquired": "2021-12-01", "shares": 45, "cost_basis": 76.00},
        {"date_acquired": "2023-02-15", "shares": 30, "cost_basis": 110.00},
        {"date_acquired": "2024-06-01", "shares": 25, "cost_basis": 128.00},
    ]},
    {"ticker": "TMO", "sector": "Healthcare", "lots": [
        {"date_acquired": "2022-08-01", "shares": 12, "cost_basis": 570.00},
        {"date_acquired": "2023-11-15", "shares": 8, "cost_basis": 480.00},
    ]},
    {"ticker": "BMY", "sector": "Healthcare", "lots": [
        {"date_acquired": "2021-05-01", "shares": 60, "cost_basis": 65.00},
        {"date_acquired": "2022-12-01", "shares": 45, "cost_basis": 72.00},
        {"date_acquired": "2024-02-15", "shares": 40, "cost_basis": 50.00},
    ]},
    {"ticker": "AMGN", "sector": "Healthcare", "lots": [
        {"date_acquired": "2022-04-01", "shares": 20, "cost_basis": 245.00},
        {"date_acquired": "2023-09-01", "shares": 15, "cost_basis": 270.00},
    ]},
    {"ticker": "GILD", "sector": "Healthcare", "lots": [
        {"date_acquired": "2022-06-15", "shares": 50, "cost_basis": 62.00},
        {"date_acquired": "2023-12-01", "shares": 35, "cost_basis": 80.00},
    ]},
    # ── Financial Services (target 15%) ──
    {"ticker": "JPM", "sector": "Financial Services", "lots": [
        {"date_acquired": "2021-02-01", "shares": 40, "cost_basis": 135.00},
        {"date_acquired": "2022-07-15", "shares": 30, "cost_basis": 115.00},
        {"date_acquired": "2023-10-01", "shares": 25, "cost_basis": 148.00},
    ]},
    {"ticker": "V", "sector": "Financial Services", "lots": [
        {"date_acquired": "2021-05-15", "shares": 35, "cost_basis": 230.00},
        {"date_acquired": "2023-01-01", "shares": 20, "cost_basis": 215.00},
        {"date_acquired": "2024-04-15", "shares": 15, "cost_basis": 280.00},
    ]},
    {"ticker": "MA", "sector": "Financial Services", "lots": [
        {"date_acquired": "2022-03-01", "shares": 20, "cost_basis": 355.00},
        {"date_acquired": "2023-08-15", "shares": 15, "cost_basis": 400.00},
    ]},
    {"ticker": "BAC", "sector": "Financial Services", "lots": [
        {"date_acquired": "2021-09-01", "shares": 100, "cost_basis": 38.00},
        {"date_acquired": "2022-10-01", "shares": 80, "cost_basis": 32.00},
        {"date_acquired": "2023-11-15", "shares": 60, "cost_basis": 29.00},
        {"date_acquired": "2024-08-01", "shares": 50, "cost_basis": 40.00},
    ]},
    {"ticker": "GS", "sector": "Financial Services", "lots": [
        {"date_acquired": "2022-01-15", "shares": 15, "cost_basis": 380.00},
        {"date_acquired": "2023-05-01", "shares": 10, "cost_basis": 330.00},
    ]},
    {"ticker": "MS", "sector": "Financial Services", "lots": [
        {"date_acquired": "2021-11-01", "shares": 40, "cost_basis": 98.00},
        {"date_acquired": "2023-03-15", "shares": 30, "cost_basis": 88.00},
    ]},
    {"ticker": "BLK", "sector": "Financial Services", "lots": [
        {"date_acquired": "2022-05-01", "shares": 10, "cost_basis": 640.00},
        {"date_acquired": "2024-01-15", "shares": 8, "cost_basis": 810.00},
    ]},
    {"ticker": "SCHW", "sector": "Financial Services", "lots": [
        {"date_acquired": "2022-02-01", "shares": 50, "cost_basis": 88.00},
        {"date_acquired": "2023-04-01", "shares": 40, "cost_basis": 52.00},
        {"date_acquired": "2024-05-15", "shares": 30, "cost_basis": 74.00},
    ]},
    {"ticker": "AXP", "sector": "Financial Services", "lots": [
        {"date_acquired": "2021-07-01", "shares": 25, "cost_basis": 170.00},
        {"date_acquired": "2023-06-01", "shares": 20, "cost_basis": 175.00},
    ]},
    {"ticker": "C", "sector": "Financial Services", "lots": [
        {"date_acquired": "2022-09-01", "shares": 60, "cost_basis": 46.00},
        {"date_acquired": "2023-10-15", "shares": 45, "cost_basis": 41.00},
        {"date_acquired": "2024-07-01", "shares": 35, "cost_basis": 63.00},
    ]},
    # ── Consumer Cyclical (target 10%) ──
    {"ticker": "AMZN", "sector": "Consumer Cyclical", "lots": [
        {"date_acquired": "2022-01-01", "shares": 50, "cost_basis": 165.00},
        {"date_acquired": "2022-11-15", "shares": 80, "cost_basis": 92.00},
        {"date_acquired": "2023-09-01", "shares": 40, "cost_basis": 135.00},
    ]},
    {"ticker": "TSLA", "sector": "Consumer Cyclical", "lots": [
        {"date_acquired": "2021-11-01", "shares": 30, "cost_basis": 390.00},
        {"date_acquired": "2022-06-15", "shares": 40, "cost_basis": 220.00},
        {"date_acquired": "2023-01-01", "shares": 50, "cost_basis": 125.00},
        {"date_acquired": "2024-04-15", "shares": 25, "cost_basis": 165.00},
    ]},
    {"ticker": "HD", "sector": "Consumer Cyclical", "lots": [
        {"date_acquired": "2021-08-01", "shares": 20, "cost_basis": 330.00},
        {"date_acquired": "2023-04-15", "shares": 15, "cost_basis": 295.00},
    ]},
    {"ticker": "MCD", "sector": "Consumer Cyclical", "lots": [
        {"date_acquired": "2022-03-15", "shares": 25, "cost_basis": 240.00},
        {"date_acquired": "2023-07-01", "shares": 18, "cost_basis": 295.00},
        {"date_acquired": "2024-09-01", "shares": 12, "cost_basis": 280.00},
    ]},
    {"ticker": "NKE", "sector": "Consumer Cyclical", "lots": [
        {"date_acquired": "2021-12-01", "shares": 40, "cost_basis": 165.00},
        {"date_acquired": "2022-09-15", "shares": 35, "cost_basis": 105.00},
        {"date_acquired": "2023-12-01", "shares": 25, "cost_basis": 108.00},
        {"date_acquired": "2024-06-15", "shares": 30, "cost_basis": 95.00},
    ]},
    {"ticker": "LOW", "sector": "Consumer Cyclical", "lots": [
        {"date_acquired": "2022-05-01", "shares": 18, "cost_basis": 195.00},
        {"date_acquired": "2023-10-15", "shares": 12, "cost_basis": 210.00},
    ]},
    {"ticker": "SBUX", "sector": "Consumer Cyclical", "lots": [
        {"date_acquired": "2021-07-15", "shares": 45, "cost_basis": 120.00},
        {"date_acquired": "2022-10-01", "shares": 35, "cost_basis": 88.00},
        {"date_acquired": "2024-01-15", "shares": 25, "cost_basis": 95.00},
    ]},
    {"ticker": "TJX", "sector": "Consumer Cyclical", "lots": [
        {"date_acquired": "2023-02-01", "shares": 30, "cost_basis": 80.00},
        {"date_acquired": "2024-03-15", "shares": 25, "cost_basis": 97.00},
    ]},
    {"ticker": "BKNG", "sector": "Consumer Cyclical", "lots": [
        {"date_acquired": "2022-06-01", "shares": 3, "cost_basis": 1950.00},
        {"date_acquired": "2023-11-01", "shares": 2, "cost_basis": 3200.00},
    ]},
    {"ticker": "F", "sector": "Consumer Cyclical", "lots": [
        {"date_acquired": "2021-06-01", "shares": 200, "cost_basis": 15.00},
        {"date_acquired": "2022-03-01", "shares": 150, "cost_basis": 17.00},
        {"date_acquired": "2023-07-15", "shares": 100, "cost_basis": 14.50},
        {"date_acquired": "2024-05-01", "shares": 100, "cost_basis": 12.00},
    ]},
    {"ticker": "GM", "sector": "Consumer Cyclical", "lots": [
        {"date_acquired": "2022-01-15", "shares": 60, "cost_basis": 58.00},
        {"date_acquired": "2023-04-01", "shares": 45, "cost_basis": 36.00},
        {"date_acquired": "2024-02-15", "shares": 35, "cost_basis": 40.00},
    ]},
    {"ticker": "ROST", "sector": "Consumer Cyclical", "lots": [
        {"date_acquired": "2022-08-01", "shares": 30, "cost_basis": 88.00},
        {"date_acquired": "2023-10-15", "shares": 22, "cost_basis": 115.00},
    ]},
    # ── Industrials (target 10%) ──
    {"ticker": "CAT", "sector": "Industrials", "lots": [
        {"date_acquired": "2021-10-01", "shares": 20, "cost_basis": 200.00},
        {"date_acquired": "2023-02-15", "shares": 15, "cost_basis": 250.00},
        {"date_acquired": "2024-06-01", "shares": 10, "cost_basis": 340.00},
    ]},
    {"ticker": "UNP", "sector": "Industrials", "lots": [
        {"date_acquired": "2022-01-15", "shares": 25, "cost_basis": 250.00},
        {"date_acquired": "2023-05-01", "shares": 18, "cost_basis": 205.00},
    ]},
    {"ticker": "HON", "sector": "Industrials", "lots": [
        {"date_acquired": "2021-04-01", "shares": 22, "cost_basis": 225.00},
        {"date_acquired": "2022-10-15", "shares": 18, "cost_basis": 190.00},
        {"date_acquired": "2024-02-01", "shares": 12, "cost_basis": 200.00},
    ]},
    {"ticker": "UPS", "sector": "Industrials", "lots": [
        {"date_acquired": "2021-11-01", "shares": 20, "cost_basis": 210.00},
        {"date_acquired": "2022-08-15", "shares": 25, "cost_basis": 190.00},
        {"date_acquired": "2023-10-01", "shares": 15, "cost_basis": 155.00},
    ]},
    {"ticker": "BA", "sector": "Industrials", "lots": [
        {"date_acquired": "2022-06-01", "shares": 20, "cost_basis": 135.00},
        {"date_acquired": "2023-03-15", "shares": 15, "cost_basis": 205.00},
        {"date_acquired": "2024-01-01", "shares": 12, "cost_basis": 250.00},
        {"date_acquired": "2024-08-15", "shares": 10, "cost_basis": 175.00},
    ]},
    {"ticker": "RTX", "sector": "Industrials", "lots": [
        {"date_acquired": "2022-09-01", "shares": 30, "cost_basis": 88.00},
        {"date_acquired": "2023-07-15", "shares": 25, "cost_basis": 98.00},
    ]},
    {"ticker": "DE", "sector": "Industrials", "lots": [
        {"date_acquired": "2021-05-15", "shares": 12, "cost_basis": 365.00},
        {"date_acquired": "2023-08-01", "shares": 10, "cost_basis": 420.00},
    ]},
    {"ticker": "GE", "sector": "Industrials", "lots": [
        {"date_acquired": "2023-01-01", "shares": 40, "cost_basis": 75.00},
        {"date_acquired": "2024-04-01", "shares": 25, "cost_basis": 160.00},
    ]},
    {"ticker": "LMT", "sector": "Industrials", "lots": [
        {"date_acquired": "2022-02-15", "shares": 12, "cost_basis": 385.00},
        {"date_acquired": "2023-09-01", "shares": 8, "cost_basis": 440.00},
    ]},
    {"ticker": "MMM", "sector": "Industrials", "lots": [
        {"date_acquired": "2021-01-15", "shares": 30, "cost_basis": 175.00},
        {"date_acquired": "2022-04-01", "shares": 25, "cost_basis": 150.00},
        {"date_acquired": "2023-06-15", "shares": 20, "cost_basis": 100.00},
        {"date_acquired": "2024-07-01", "shares": 20, "cost_basis": 105.00},
    ]},
    {"ticker": "WM", "sector": "Industrials", "lots": [
        {"date_acquired": "2022-03-01", "shares": 18, "cost_basis": 155.00},
        {"date_acquired": "2023-07-15", "shares": 12, "cost_basis": 170.00},
    ]},
    {"ticker": "ETN", "sector": "Industrials", "lots": [
        {"date_acquired": "2023-01-01", "shares": 20, "cost_basis": 165.00},
        {"date_acquired": "2024-05-01", "shares": 15, "cost_basis": 310.00},
    ]},
    # ── Energy (target 8%) ──
    {"ticker": "XOM", "sector": "Energy", "lots": [
        {"date_acquired": "2021-03-01", "shares": 50, "cost_basis": 58.00},
        {"date_acquired": "2022-06-15", "shares": 35, "cost_basis": 95.00},
        {"date_acquired": "2023-09-01", "shares": 25, "cost_basis": 112.00},
    ]},
    {"ticker": "CVX", "sector": "Energy", "lots": [
        {"date_acquired": "2021-07-01", "shares": 30, "cost_basis": 105.00},
        {"date_acquired": "2022-11-15", "shares": 20, "cost_basis": 180.00},
        {"date_acquired": "2024-01-01", "shares": 15, "cost_basis": 148.00},
    ]},
    {"ticker": "COP", "sector": "Energy", "lots": [
        {"date_acquired": "2022-01-01", "shares": 30, "cost_basis": 75.00},
        {"date_acquired": "2023-04-15", "shares": 20, "cost_basis": 105.00},
    ]},
    {"ticker": "SLB", "sector": "Energy", "lots": [
        {"date_acquired": "2022-07-01", "shares": 50, "cost_basis": 40.00},
        {"date_acquired": "2023-09-15", "shares": 35, "cost_basis": 58.00},
        {"date_acquired": "2024-06-01", "shares": 30, "cost_basis": 48.00},
    ]},
    {"ticker": "EOG", "sector": "Energy", "lots": [
        {"date_acquired": "2022-03-15", "shares": 25, "cost_basis": 118.00},
        {"date_acquired": "2023-06-01", "shares": 20, "cost_basis": 120.00},
    ]},
    {"ticker": "OXY", "sector": "Energy", "lots": [
        {"date_acquired": "2022-05-01", "shares": 45, "cost_basis": 62.00},
        {"date_acquired": "2023-01-15", "shares": 35, "cost_basis": 65.00},
        {"date_acquired": "2024-03-01", "shares": 30, "cost_basis": 58.00},
    ]},
    {"ticker": "PSX", "sector": "Energy", "lots": [
        {"date_acquired": "2022-08-01", "shares": 20, "cost_basis": 90.00},
        {"date_acquired": "2023-11-01", "shares": 15, "cost_basis": 118.00},
    ]},
    {"ticker": "VLO", "sector": "Energy", "lots": [
        {"date_acquired": "2022-04-01", "shares": 25, "cost_basis": 108.00},
        {"date_acquired": "2023-08-15", "shares": 18, "cost_basis": 135.00},
    ]},
    {"ticker": "HAL", "sector": "Energy", "lots": [
        {"date_acquired": "2022-06-15", "shares": 40, "cost_basis": 32.00},
        {"date_acquired": "2023-10-01", "shares": 30, "cost_basis": 42.00},
        {"date_acquired": "2024-05-15", "shares": 25, "cost_basis": 36.00},
    ]},
    {"ticker": "DVN", "sector": "Energy", "lots": [
        {"date_acquired": "2022-03-01", "shares": 35, "cost_basis": 58.00},
        {"date_acquired": "2023-05-15", "shares": 25, "cost_basis": 50.00},
        {"date_acquired": "2024-04-01", "shares": 20, "cost_basis": 45.00},
    ]},
    # ── Communication Services (target 7%) ──
    {"ticker": "GOOG", "sector": "Communication Services", "lots": [
        {"date_acquired": "2022-01-01", "shares": 40, "cost_basis": 140.00},
        {"date_acquired": "2022-11-01", "shares": 50, "cost_basis": 96.00},
        {"date_acquired": "2023-07-15", "shares": 30, "cost_basis": 120.00},
    ]},
    {"ticker": "META", "sector": "Communication Services", "lots": [
        {"date_acquired": "2022-10-15", "shares": 35, "cost_basis": 130.00},
        {"date_acquired": "2023-02-01", "shares": 25, "cost_basis": 185.00},
        {"date_acquired": "2024-01-15", "shares": 15, "cost_basis": 380.00},
    ]},
    {"ticker": "NFLX", "sector": "Communication Services", "lots": [
        {"date_acquired": "2022-05-15", "shares": 20, "cost_basis": 190.00},
        {"date_acquired": "2023-01-01", "shares": 15, "cost_basis": 295.00},
        {"date_acquired": "2024-02-01", "shares": 10, "cost_basis": 570.00},
    ]},
    {"ticker": "DIS", "sector": "Communication Services", "lots": [
        {"date_acquired": "2021-03-01", "shares": 40, "cost_basis": 195.00},
        {"date_acquired": "2022-05-01", "shares": 35, "cost_basis": 115.00},
        {"date_acquired": "2023-08-15", "shares": 30, "cost_basis": 88.00},
        {"date_acquired": "2024-04-01", "shares": 25, "cost_basis": 115.00},
    ]},
    {"ticker": "CMCSA", "sector": "Communication Services", "lots": [
        {"date_acquired": "2022-02-01", "shares": 55, "cost_basis": 48.00},
        {"date_acquired": "2023-05-15", "shares": 40, "cost_basis": 40.00},
    ]},
    {"ticker": "T", "sector": "Communication Services", "lots": [
        {"date_acquired": "2021-06-01", "shares": 100, "cost_basis": 29.00},
        {"date_acquired": "2022-07-15", "shares": 80, "cost_basis": 19.00},
        {"date_acquired": "2023-10-01", "shares": 60, "cost_basis": 15.50},
    ]},
    {"ticker": "VZ", "sector": "Communication Services", "lots": [
        {"date_acquired": "2021-09-01", "shares": 70, "cost_basis": 54.00},
        {"date_acquired": "2022-10-15", "shares": 55, "cost_basis": 38.00},
        {"date_acquired": "2023-12-01", "shares": 40, "cost_basis": 37.00},
    ]},
    {"ticker": "TMUS", "sector": "Communication Services", "lots": [
        {"date_acquired": "2022-04-01", "shares": 25, "cost_basis": 128.00},
        {"date_acquired": "2023-08-15", "shares": 18, "cost_basis": 140.00},
        {"date_acquired": "2024-06-01", "shares": 12, "cost_basis": 178.00},
    ]},
    {"ticker": "CHTR", "sector": "Communication Services", "lots": [
        {"date_acquired": "2022-01-15", "shares": 8, "cost_basis": 590.00},
        {"date_acquired": "2023-05-01", "shares": 6, "cost_basis": 360.00},
        {"date_acquired": "2024-03-15", "shares": 5, "cost_basis": 290.00},
    ]},
    {"ticker": "WBD", "sector": "Communication Services", "lots": [
        {"date_acquired": "2022-04-15", "shares": 80, "cost_basis": 24.00},
        {"date_acquired": "2023-01-01", "shares": 60, "cost_basis": 12.00},
        {"date_acquired": "2024-02-01", "shares": 50, "cost_basis": 10.00},
    ]},
    # ── Consumer Defensive (target 5%) ──
    {"ticker": "PG", "sector": "Consumer Defensive", "lots": [
        {"date_acquired": "2021-04-01", "shares": 30, "cost_basis": 135.00},
        {"date_acquired": "2023-01-15", "shares": 20, "cost_basis": 150.00},
    ]},
    {"ticker": "KO", "sector": "Consumer Defensive", "lots": [
        {"date_acquired": "2021-08-15", "shares": 60, "cost_basis": 56.00},
        {"date_acquired": "2022-12-01", "shares": 40, "cost_basis": 63.00},
        {"date_acquired": "2024-02-15", "shares": 30, "cost_basis": 59.00},
    ]},
    {"ticker": "PEP", "sector": "Consumer Defensive", "lots": [
        {"date_acquired": "2022-01-01", "shares": 25, "cost_basis": 172.00},
        {"date_acquired": "2023-05-15", "shares": 18, "cost_basis": 188.00},
    ]},
    {"ticker": "COST", "sector": "Consumer Defensive", "lots": [
        {"date_acquired": "2022-06-01", "shares": 12, "cost_basis": 480.00},
        {"date_acquired": "2023-09-15", "shares": 8, "cost_basis": 570.00},
    ]},
    {"ticker": "WMT", "sector": "Consumer Defensive", "lots": [
        {"date_acquired": "2021-11-01", "shares": 35, "cost_basis": 145.00},
        {"date_acquired": "2023-03-01", "shares": 25, "cost_basis": 148.00},
    ]},
    {"ticker": "CL", "sector": "Consumer Defensive", "lots": [
        {"date_acquired": "2022-04-15", "shares": 30, "cost_basis": 78.00},
        {"date_acquired": "2024-01-01", "shares": 22, "cost_basis": 80.00},
    ]},
    {"ticker": "MDLZ", "sector": "Consumer Defensive", "lots": [
        {"date_acquired": "2022-07-01", "shares": 40, "cost_basis": 64.00},
        {"date_acquired": "2023-11-15", "shares": 30, "cost_basis": 72.00},
    ]},
    {"ticker": "GIS", "sector": "Consumer Defensive", "lots": [
        {"date_acquired": "2022-02-01", "shares": 35, "cost_basis": 68.00},
        {"date_acquired": "2023-06-15", "shares": 25, "cost_basis": 82.00},
    ]},
    {"ticker": "KHC", "sector": "Consumer Defensive", "lots": [
        {"date_acquired": "2021-10-01", "shares": 50, "cost_basis": 37.00},
        {"date_acquired": "2022-08-15", "shares": 40, "cost_basis": 40.00},
        {"date_acquired": "2023-12-01", "shares": 30, "cost_basis": 35.00},
    ]},
    {"ticker": "SYY", "sector": "Consumer Defensive", "lots": [
        {"date_acquired": "2022-05-01", "shares": 28, "cost_basis": 85.00},
        {"date_acquired": "2023-09-15", "shares": 20, "cost_basis": 72.00},
    ]},
    # ── Utilities (target 3%) ──
    {"ticker": "NEE", "sector": "Utilities", "lots": [
        {"date_acquired": "2021-12-01", "shares": 40, "cost_basis": 88.00},
        {"date_acquired": "2022-09-15", "shares": 35, "cost_basis": 85.00},
        {"date_acquired": "2023-10-01", "shares": 30, "cost_basis": 60.00},
    ]},
    {"ticker": "DUK", "sector": "Utilities", "lots": [
        {"date_acquired": "2022-03-01", "shares": 25, "cost_basis": 105.00},
        {"date_acquired": "2023-06-15", "shares": 20, "cost_basis": 92.00},
    ]},
    {"ticker": "SO", "sector": "Utilities", "lots": [
        {"date_acquired": "2022-05-15", "shares": 35, "cost_basis": 72.00},
        {"date_acquired": "2023-08-01", "shares": 25, "cost_basis": 70.00},
    ]},
    {"ticker": "D", "sector": "Utilities", "lots": [
        {"date_acquired": "2021-10-01", "shares": 30, "cost_basis": 78.00},
        {"date_acquired": "2023-01-15", "shares": 25, "cost_basis": 62.00},
        {"date_acquired": "2024-03-01", "shares": 20, "cost_basis": 48.00},
    ]},
    {"ticker": "AEP", "sector": "Utilities", "lots": [
        {"date_acquired": "2022-08-01", "shares": 25, "cost_basis": 98.00},
        {"date_acquired": "2024-01-15", "shares": 20, "cost_basis": 82.00},
    ]},
    {"ticker": "SRE", "sector": "Utilities", "lots": [
        {"date_acquired": "2022-01-15", "shares": 20, "cost_basis": 135.00},
        {"date_acquired": "2023-05-01", "shares": 15, "cost_basis": 155.00},
    ]},
    {"ticker": "EXC", "sector": "Utilities", "lots": [
        {"date_acquired": "2021-11-01", "shares": 40, "cost_basis": 56.00},
        {"date_acquired": "2022-09-15", "shares": 30, "cost_basis": 43.00},
        {"date_acquired": "2024-01-01", "shares": 25, "cost_basis": 38.00},
    ]},
    {"ticker": "PCG", "sector": "Utilities", "lots": [
        {"date_acquired": "2023-03-01", "shares": 80, "cost_basis": 16.00},
        {"date_acquired": "2024-06-01", "shares": 60, "cost_basis": 18.00},
    ]},
    # ── Real Estate (target 2%) ──
    {"ticker": "PLD", "sector": "Real Estate", "lots": [
        {"date_acquired": "2021-09-01", "shares": 25, "cost_basis": 135.00},
        {"date_acquired": "2022-12-15", "shares": 20, "cost_basis": 115.00},
        {"date_acquired": "2024-02-01", "shares": 15, "cost_basis": 130.00},
    ]},
    {"ticker": "AMT", "sector": "Real Estate", "lots": [
        {"date_acquired": "2021-11-15", "shares": 15, "cost_basis": 275.00},
        {"date_acquired": "2022-10-01", "shares": 12, "cost_basis": 225.00},
        {"date_acquired": "2023-10-15", "shares": 10, "cost_basis": 180.00},
    ]},
    {"ticker": "EQIX", "sector": "Real Estate", "lots": [
        {"date_acquired": "2022-04-01", "shares": 6, "cost_basis": 720.00},
        {"date_acquired": "2023-07-01", "shares": 5, "cost_basis": 780.00},
    ]},
    {"ticker": "SPG", "sector": "Real Estate", "lots": [
        {"date_acquired": "2022-06-15", "shares": 18, "cost_basis": 108.00},
        {"date_acquired": "2023-04-01", "shares": 14, "cost_basis": 118.00},
        {"date_acquired": "2024-05-01", "shares": 10, "cost_basis": 152.00},
    ]},
    {"ticker": "O", "sector": "Real Estate", "lots": [
        {"date_acquired": "2021-08-01", "shares": 40, "cost_basis": 70.00},
        {"date_acquired": "2022-11-01", "shares": 30, "cost_basis": 62.00},
        {"date_acquired": "2023-09-15", "shares": 25, "cost_basis": 52.00},
    ]},
    {"ticker": "VICI", "sector": "Real Estate", "lots": [
        {"date_acquired": "2022-07-01", "shares": 50, "cost_basis": 32.00},
        {"date_acquired": "2023-03-15", "shares": 35, "cost_basis": 33.00},
        {"date_acquired": "2024-04-01", "shares": 30, "cost_basis": 30.00},
    ]},
    {"ticker": "AVB", "sector": "Real Estate", "lots": [
        {"date_acquired": "2022-01-01", "shares": 12, "cost_basis": 250.00},
        {"date_acquired": "2023-06-15", "shares": 10, "cost_basis": 185.00},
    ]},
    {"ticker": "MAA", "sector": "Real Estate", "lots": [
        {"date_acquired": "2022-04-01", "shares": 15, "cost_basis": 210.00},
        {"date_acquired": "2023-08-01", "shares": 12, "cost_basis": 145.00},
        {"date_acquired": "2024-02-15", "shares": 10, "cost_basis": 130.00},
    ]},
]

# Analyst "Strong Buy" recommendations by sector
STRONG_BUY = {
    "Technology": ["PANW", "SNOW", "PLTR", "CRWD", "MRVL", "ANET", "CDNS", "SNPS"],
    "Healthcare": ["VRTX", "ISRG", "DXCM", "IDXX", "REGN", "ZTS", "EW", "ALNY"],
    "Financial Services": ["ICE", "MKTX", "FIS", "COIN", "HOOD", "AFRM", "SQ", "PYPL"],
    "Consumer Cyclical": ["LULU", "DECK", "POOL", "RCL", "ABNB", "UBER", "DASH", "EXPE"],
    "Industrials": ["AXON", "CARR", "PWR", "FAST", "EMR", "ITW", "ROK", "VRSK"],
    "Energy": ["FANG", "MPC", "TRGP", "WMB", "KMI", "OKE", "CTRA", "EQT"],
    "Communication Services": ["SPOT", "RBLX", "TTWO", "EA", "ZM", "ROKU", "PINS", "SNAP"],
    "Consumer Defensive": ["MNST", "HSY", "SJM", "K", "TSN", "ADM", "CAG", "CLX"],
    "Utilities": ["VST", "CEG", "XEL", "WEC", "ES", "AWK", "EVRG", "CMS"],
    "Real Estate": ["WELL", "IRM", "DLR", "PSA", "EXR", "INVH", "ARE", "CBRE"],
}


# ─────────────────────────────────────────────────────────────
# 2. DATABASE CONNECTION
# ─────────────────────────────────────────────────────────────

load_dotenv("C:/Users/kerry/repos/data_app/.env")


def run_sql_query(sql: str) -> str:
    """Execute a SQL query against MotherDuck and return results as JSON."""
    token = os.getenv("MOTHERDUCK_TOKEN")
    conn = duckdb.connect(f"md:ndl?motherduck_token={token}")
    try:
        df = conn.execute(sql).fetchdf()
        # Limit output size for the agent
        if len(df) > 500:
            df = df.head(500)
        return df.to_json(orient="records", date_format="iso")
    except Exception as e:
        return json.dumps({"error": str(e)})
    finally:
        conn.close()


# Shared namespace for run_python — persists across calls so the agent
# can build on previous results (e.g., store a DataFrame, then correlate)
_python_namespace: dict = {}


def run_python_code(code: str) -> str:
    """Execute Python code and return its printed output."""
    import numpy as np
    import pandas as pd

    # Seed the namespace with useful libraries on first use
    if "pd" not in _python_namespace:
        _python_namespace["pd"] = pd
        _python_namespace["np"] = np
        _python_namespace["json"] = json

    old_stdout = sys.stdout
    sys.stdout = buf = io.StringIO()
    try:
        exec(code, _python_namespace)
        output = buf.getvalue()
        return output if output else "(no output)"
    except Exception as e:
        return f"Error: {e}"
    finally:
        sys.stdout = old_stdout


# ─────────────────────────────────────────────────────────────
# 3. TOOL DEFINITIONS (JSON Schema for the Claude API)
# ─────────────────────────────────────────────────────────────

tools = [
    {
        "name": "get_holdings",
        "description": (
            "Retrieve all portfolio holdings with tax lot detail. "
            "Returns each position's ticker, sector, and individual lots "
            "(date acquired, shares, cost basis per share). "
            "Use this to understand what the portfolio owns."
        ),
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    {
        "name": "get_target_allocation",
        "description": (
            "Retrieve the target sector allocation for this portfolio. "
            "Returns a dictionary mapping each sector to its target weight (0-1). "
            "Compare against current weights to identify drift."
        ),
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    {
        "name": "get_analyst_recommendations",
        "description": (
            "Get a list of stocks rated 'Strong Buy' by analysts for a given sector. "
            "Use this to find replacement candidates when tax-loss harvesting "
            "creates a need to replenish sector exposure."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "sector": {
                    "type": "string",
                    "description": "The sector to get recommendations for (e.g., 'Technology', 'Healthcare')",
                }
            },
            "required": ["sector"],
        },
    },
    {
        "name": "run_sql",
        "description": (
            "Execute a SQL query against the MotherDuck database. "
            "Available tables:\n"
            "  - sep: daily stock prices (ticker, date VARCHAR, open, high, low, close, closeadj, volume)\n"
            "  - tickers: stock metadata (ticker, name, sector, industry, exchange, scalemarketcap, isdelisted)\n\n"
            "IMPORTANT SQL rules:\n"
            "  - 'close' is a reserved word: always use a table alias (e.g., s.close)\n"
            "  - date is VARCHAR: cast with s.date::DATE for comparisons\n"
            "  - Use closeadj for return calculations (adjusted for splits/dividends)\n\n"
            "Use this tool to get current prices, compute returns, correlations, "
            "drawdowns, or any other price-based analysis."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "sql": {
                    "type": "string",
                    "description": "The SQL query to execute",
                }
            },
            "required": ["sql"],
        },
    },
    {
        "name": "run_python",
        "description": (
            "Execute Python code and return the printed output. "
            "pandas (as pd), numpy (as np), and json are available. "
            "The namespace persists across calls, so you can store variables "
            "(e.g., a DataFrame) in one call and use them in the next.\n\n"
            "Use this to compute returns, correlations, statistics, or any "
            "analysis on data retrieved via run_sql. Parse JSON strings from "
            "run_sql with pd.read_json(data) or json.loads(data)."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "Python code to execute. Use print() to return results.",
                }
            },
            "required": ["code"],
        },
    },
]


# ─────────────────────────────────────────────────────────────
# 4. TOOL EXECUTION
# ─────────────────────────────────────────────────────────────


def execute_tool(name: str, inputs: dict) -> str:
    """Route a tool call to the appropriate handler."""
    if name == "get_holdings":
        return json.dumps(HOLDINGS)
    elif name == "get_target_allocation":
        return json.dumps(TARGET_ALLOCATION)
    elif name == "get_analyst_recommendations":
        sector = inputs.get("sector", "")
        recs = STRONG_BUY.get(sector, [])
        return json.dumps({"sector": sector, "strong_buy": recs})
    elif name == "run_sql":
        return run_sql_query(inputs["sql"])
    elif name == "run_python":
        return run_python_code(inputs["code"])
    else:
        return json.dumps({"error": f"Unknown tool: {name}"})


# ─────────────────────────────────────────────────────────────
# 5. AGENT LOOP
# ─────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """\
You are a portfolio analyst assistant. You help review a client portfolio,
identify tax-loss harvesting opportunities, and recommend replacement securities.

When analyzing the portfolio:
1. Use get_holdings to see positions and tax lots
2. Use run_sql to fetch price data from the SEP table
3. Use run_python to compute returns, correlations, and other analytics from
   the price data returned by run_sql
4. Use get_target_allocation to compare current vs. target sector weights
5. When harvesting losses, sell the lots with the largest unrealized loss first
   (highest cost basis relative to current price) for maximum tax benefit
6. Use get_analyst_recommendations to find Strong Buy replacements in sectors
   where harvesting creates underweight positions
7. When recommending a replacement, compute return correlations between the
   stock being sold and each Strong Buy candidate, then recommend the most
   highly correlated candidate (to maintain similar factor exposure)

When writing SQL:
- The SEP table has columns: ticker, date (VARCHAR), open, high, low, close, closeadj, volume
- The tickers table has: ticker, name, sector, industry, exchange, scalemarketcap, isdelisted
- Always alias tables and use the alias for column references (e.g., SELECT s.close FROM sep s)
- Cast date for comparisons: s.date::DATE >= '2024-01-01'
- Use closeadj for return calculations

When writing Python:
- pandas (pd), numpy (np), and json are pre-imported
- The namespace persists across calls — store DataFrames as variables for later use
- Use print() to return results to the conversation

Be concise and quantitative. Show dollar amounts and percentages.
"""


def main():
    client = anthropic.Anthropic()
    messages = []

    print("=" * 60)
    print("  Portfolio Review Agent")
    print("  Type 'quit' to exit")
    print("=" * 60)
    print()

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit"):
            break

        messages.append({"role": "user", "content": user_input})

        # Agentic loop: keep going until the agent stops calling tools
        while True:
            response = client.messages.create(
                model="claude-sonnet-4-6",
                system=SYSTEM_PROMPT,
                tools=tools,
                messages=messages,
                max_tokens=4096,
            )

            if response.stop_reason == "tool_use":
                # Add assistant's response (contains tool_use blocks)
                messages.append({"role": "assistant", "content": response.content})

                # Execute each tool call and collect results
                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        print(f"  [calling {block.name}...]")
                        result = execute_tool(block.name, block.input)
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result,
                        })

                # Send results back to the agent
                messages.append({"role": "user", "content": tool_results})
            else:
                # Agent is done — print its response
                for block in response.content:
                    if hasattr(block, "text"):
                        print(f"\nAgent: {block.text}\n")
                messages.append({"role": "assistant", "content": response.content})
                break


if __name__ == "__main__":
    main()
