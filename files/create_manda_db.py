"""
Generate a synthetic but realistic M&A transactions database for MBA students.
"""

import sqlite3
import random
import math
from datetime import date, timedelta

random.seed(42)

DB_PATH = "C:/Users/kerry/repos/mgmt675/files/manda.db"

# ── Reference data ──────────────────────────────────────────────────────

SECTORS = [
    "Technology", "Healthcare", "Financial Services", "Energy",
    "Industrials", "Consumer", "Real Estate", "Telecom",
]

COUNTRIES = [
    "United States", "United Kingdom", "Canada", "Germany", "France",
    "Japan", "Australia", "Netherlands", "Switzerland", "India",
    "Brazil", "Singapore", "South Korea", "Israel", "Sweden",
]

ADVISOR_BANKS = [
    "Goldman Sachs", "Morgan Stanley", "JPMorgan", "BofA Securities",
    "Citi", "Lazard", "Evercore", "Centerview Partners", "Barclays",
    "Credit Suisse", "UBS", "Deutsche Bank", "Jefferies",
    "Guggenheim Securities", "Moelis & Company", "PJT Partners",
    "Qatalyst Partners",
]

LENDERS = [
    "JPMorgan", "BofA", "Wells Fargo", "Citi",
    "Barclays", "Deutsche Bank", "Credit Suisse", "Goldman Sachs",
]

FINANCING_SOURCES = [
    "Revolving Credit", "Term Loan", "Senior Notes",
    "Equity Contribution", "Mezzanine", "Bridge Loan",
]

PAYMENT_METHODS = ["Cash", "Stock", "Cash and Stock"]
DEAL_TYPES = ["Acquisition", "Merger", "Leveraged Buyout", "Management Buyout", "Divestiture"]
DEAL_STATUSES = ["Completed", "Pending", "Withdrawn"]

# ── Real mega-deals (based on actual transactions 2019-2025) ────────────

REAL_DEALS = [
    # (acquirer, target, acquirer_sector, target_sector, target_country, year, deal_value_mm, deal_type, payment)
    ("Microsoft", "Activision Blizzard", "Technology", "Technology", "United States", 2022, 68700, "Acquisition", "Cash"),
    ("Broadcom", "VMware", "Technology", "Technology", "United States", 2022, 61000, "Acquisition", "Cash and Stock"),
    ("Pfizer", "Seagen", "Healthcare", "Healthcare", "United States", 2023, 43000, "Acquisition", "Cash"),
    ("Amgen", "Horizon Therapeutics", "Healthcare", "Healthcare", "United States", 2022, 28300, "Acquisition", "Cash"),
    ("Adobe", "Figma", "Technology", "Technology", "United States", 2022, 20000, "Acquisition", "Cash and Stock"),
    ("Broadcom", "Symantec Enterprise", "Technology", "Technology", "United States", 2019, 10700, "Acquisition", "Cash"),
    ("Salesforce", "Slack Technologies", "Technology", "Technology", "United States", 2020, 27700, "Acquisition", "Cash and Stock"),
    ("AMD", "Xilinx", "Technology", "Technology", "United States", 2020, 35000, "Merger", "Stock"),
    ("Oracle", "Cerner", "Technology", "Healthcare", "United States", 2021, 28300, "Acquisition", "Cash"),
    ("Exxon Mobil", "Pioneer Natural Resources", "Energy", "Energy", "United States", 2023, 59500, "Acquisition", "Stock"),
    ("Chevron", "Hess Corporation", "Energy", "Energy", "United States", 2023, 53000, "Merger", "Stock"),
    ("ConocoPhillips", "Marathon Oil", "Energy", "Energy", "United States", 2024, 22500, "Acquisition", "Stock"),
    ("Capital One", "Discover Financial", "Financial Services", "Financial Services", "United States", 2024, 35300, "Merger", "Stock"),
    ("Nippon Steel", "U.S. Steel", "Industrials", "Industrials", "United States", 2023, 14900, "Acquisition", "Cash"),
    ("Cisco Systems", "Splunk", "Technology", "Technology", "United States", 2023, 28000, "Acquisition", "Cash"),
    ("Johnson & Johnson", "Abiomed", "Healthcare", "Healthcare", "United States", 2022, 16600, "Acquisition", "Cash"),
    ("Merck", "Prometheus Biosciences", "Healthcare", "Healthcare", "United States", 2023, 10800, "Acquisition", "Cash"),
    ("ExxonMobil", "Denbury", "Energy", "Energy", "United States", 2023, 4900, "Acquisition", "Stock"),
    ("Palo Alto Networks", "Talon Cyber Security", "Technology", "Technology", "Israel", 2023, 625, "Acquisition", "Cash"),
    ("Thoma Bravo", "Coupa Software", "Technology", "Technology", "United States", 2022, 8000, "Leveraged Buyout", "Cash"),
    ("Vista Equity", "Citrix Systems", "Technology", "Technology", "United States", 2022, 16500, "Leveraged Buyout", "Cash"),
    ("Kroger", "Albertsons", "Consumer", "Consumer", "United States", 2022, 24600, "Merger", "Cash and Stock"),
    ("LVMH", "Tiffany & Co.", "Consumer", "Consumer", "United States", 2019, 15800, "Acquisition", "Cash"),
    ("Hewlett Packard Enterprise", "Juniper Networks", "Technology", "Technology", "United States", 2024, 14000, "Acquisition", "Cash"),
    ("Synopsys", "Ansys", "Technology", "Technology", "United States", 2024, 35000, "Acquisition", "Cash and Stock"),
    ("Mars", "Kellanova", "Consumer", "Consumer", "United States", 2024, 35900, "Acquisition", "Cash"),
    ("Diamondback Energy", "Endeavor Energy", "Energy", "Energy", "United States", 2024, 26000, "Merger", "Cash and Stock"),
    ("BlackRock", "Global Infrastructure Partners", "Financial Services", "Financial Services", "United States", 2024, 12500, "Acquisition", "Cash and Stock"),
    ("Danaher", "Abcam", "Healthcare", "Healthcare", "United Kingdom", 2023, 5700, "Acquisition", "Cash"),
    ("Emerson Electric", "National Instruments", "Industrials", "Technology", "United States", 2023, 8200, "Acquisition", "Cash"),
]

# ── Fictional company name generators ───────────────────────────────────

TECH_COMPANIES = [
    "Nextera Software", "CloudVault Inc.", "DataPrime Analytics", "Synthetix AI",
    "CyberEdge Security", "QuantumPath Systems", "PivotPoint Technologies",
    "Aethon Cloud", "Meridian Data Solutions", "Helix Software Group",
    "Stratos Computing", "VectorShift Labs", "TerraCode Inc.", "NovaBridge Tech",
    "Apex Digital Solutions", "Cirrus Logic Systems", "Onyx Cybersecurity",
    "Prism Analytics Corp.", "Luminary Software", "ZetaWave Technologies",
    "Skyline SaaS", "Ironclad Systems", "BlueArc Technologies", "Vertex AI Labs",
    "Catalyst Data Corp.", "Paladin Software", "Evergreen Tech Solutions",
]

HEALTHCARE_COMPANIES = [
    "MedVista Therapeutics", "Pinnacle Health Sciences", "Aurogen Biosciences",
    "ClearPath Medical", "Nexus Pharma", "BioVantage Inc.", "Meridian Life Sciences",
    "Helios Biotech", "Coronis Health Solutions", "Aspire Medical Devices",
    "Zenith Diagnostics", "Vanguard Pharmaceuticals", "Luminos Genomics",
    "Radiant Health Corp.", "Solara Biomedical", "Everwell Health Systems",
    "Keystone Medical Group", "Precision Therapeutics Inc.", "NovaCure Sciences",
]

FINANCIAL_COMPANIES = [
    "Vanguard Capital Partners", "Meridian Financial Group", "Apex Wealth Management",
    "Silverstone Insurance", "Pinnacle Asset Management", "Keystone Financial Corp.",
    "Trident Capital Advisors", "Horizon Bancshares", "Pacific Coast Financial",
    "Atlas Reinsurance", "Summit Credit Corp.", "Ironwood Capital Group",
    "Bridgewater Insurance Holdings", "Centurion Financial Services",
]

ENERGY_COMPANIES = [
    "Frontier Energy Corp.", "Redstone Petroleum", "Blue Ridge Resources",
    "Summit Exploration", "Cascade Energy Partners", "Ironwood Natural Gas",
    "Pinnacle Power Solutions", "Vanguard Renewables", "TerraVolt Energy",
    "Meridian Upstream Corp.", "Atlas Pipeline Services", "Sentinel Energy Holdings",
    "Greenfield Solar Corp.", "Pacific Rim LNG", "Continental Shale Resources",
]

INDUSTRIAL_COMPANIES = [
    "Sterling Manufacturing", "Apex Industrial Solutions", "Keystone Engineering",
    "Frontier Aerospace", "Meridian Logistics Corp.", "Vanguard Defense Systems",
    "Pacific Industrial Group", "Atlas Precision Components", "Summit Materials Corp.",
    "Ironbridge Construction", "Pinnacle Automation", "Continental Manufacturing",
    "Northwind Aerospace", "Sentinel Defense Group", "Trident Marine Systems",
]

CONSUMER_COMPANIES = [
    "Evergreen Brands Inc.", "Pinnacle Consumer Group", "Atlas Retail Holdings",
    "Meridian Foods Corp.", "Summit Hospitality Group", "Keystone Apparel",
    "Vanguard Consumer Products", "Pacific Lifestyle Brands", "Redwood Restaurant Group",
    "Ironwood Spirits Co.", "Frontier Home Goods", "Sterling Consumer Holdings",
    "Brightleaf Organics", "Cascade Beverages", "Trident Leisure Corp.",
]

REALESTATE_COMPANIES = [
    "Pinnacle REIT", "Atlas Property Group", "Meridian Real Estate Partners",
    "Summit Development Corp.", "Keystone Properties", "Vanguard Realty Trust",
    "Pacific Coast Properties", "Ironbridge Real Estate", "Continental Realty Holdings",
    "Northwind Property Fund", "Frontier Land Partners", "Sentinel REIT",
]

TELECOM_COMPANIES = [
    "Meridian Telecom", "Apex Communications", "Skybridge Networks",
    "Pinnacle Wireless", "Atlas Fiber Corp.", "Frontier Broadband",
    "Continental Telecom Group", "Vanguard Wireless Holdings", "Summit Connectivity",
    "Ironwood Communications", "Pacific Digital Networks", "Sentinel Telecom",
]

SECTOR_COMPANIES = {
    "Technology": TECH_COMPANIES,
    "Healthcare": HEALTHCARE_COMPANIES,
    "Financial Services": FINANCIAL_COMPANIES,
    "Energy": ENERGY_COMPANIES,
    "Industrials": INDUSTRIAL_COMPANIES,
    "Consumer": CONSUMER_COMPANIES,
    "Real Estate": REALESTATE_COMPANIES,
    "Telecom": TELECOM_COMPANIES,
}

# Large acquirers by sector (for synthetic deals)
LARGE_ACQUIRERS = {
    "Technology": ["Alphabet", "Amazon", "Apple", "Meta Platforms", "Intel", "IBM", "SAP", "Accenture", "Infosys"],
    "Healthcare": ["UnitedHealth Group", "Abbott Laboratories", "Thermo Fisher Scientific", "Becton Dickinson", "Stryker"],
    "Financial Services": ["JPMorgan Chase", "Goldman Sachs Group", "Morgan Stanley", "Blackstone", "KKR"],
    "Energy": ["Shell", "BP", "TotalEnergies", "Enbridge", "NextEra Energy"],
    "Industrials": ["Honeywell", "3M", "General Electric", "Caterpillar", "Lockheed Martin"],
    "Consumer": ["Procter & Gamble", "Nestle", "Unilever", "PepsiCo", "Nike"],
    "Real Estate": ["Prologis", "American Tower", "Simon Property Group", "Brookfield Asset Management"],
    "Telecom": ["AT&T", "Verizon", "T-Mobile US", "Comcast", "Charter Communications"],
}

# EV/EBITDA multiple ranges by sector (low, high)
SECTOR_MULTIPLES = {
    "Technology": (12, 25),
    "Healthcare": (10, 22),
    "Financial Services": (8, 16),
    "Energy": (5, 12),
    "Industrials": (6, 13),
    "Consumer": (8, 16),
    "Real Estate": (10, 20),
    "Telecom": (6, 11),
}


def random_date(start_year, end_year):
    start = date(start_year, 1, 1)
    end = date(end_year, 12, 31)
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, delta))


def generate_deal_value():
    """Log-normal distribution skewed toward smaller deals."""
    # Mean ~$1.5B, but mostly smaller with a few mega-deals
    log_val = random.gauss(6.5, 1.5)  # ln(millions)
    val = math.exp(log_val)
    val = max(50, min(80000, val))
    # Round nicely
    if val > 10000:
        val = round(val / 500) * 500
    elif val > 1000:
        val = round(val / 100) * 100
    elif val > 100:
        val = round(val / 10) * 10
    else:
        val = round(val)
    return float(val)


def generate_transactions():
    transactions = []
    used_company_names = set()

    # First, add real deals
    for i, deal in enumerate(REAL_DEALS):
        acquirer, target, acq_sector, tgt_sector, tgt_country, year, value, dtype, payment = deal
        ann_date = random_date(year, year)
        is_cross_border = 1 if tgt_country != "United States" else 0

        # Closing date
        if dtype == "Leveraged Buyout":
            close_delta = random.randint(90, 180)
        else:
            close_delta = random.randint(60, 365)

        # Some real deals were withdrawn
        if target == "Figma":  # Adobe/Figma was withdrawn
            status = "Withdrawn"
            closing_date = None
        elif target == "Albertsons":  # Kroger/Albertsons was blocked
            status = "Withdrawn"
            closing_date = None
        elif target == "U.S. Steel":  # Nippon Steel blocked
            status = "Withdrawn"
            closing_date = None
        else:
            status = "Completed"
            closing_date = (ann_date + timedelta(days=close_delta)).isoformat()

        # Multiples
        mult_range = SECTOR_MULTIPLES.get(tgt_sector, (8, 16))
        ev_ebitda = round(random.uniform(mult_range[0], mult_range[1]), 1) if random.random() > 0.15 else None
        ev_revenue = round(random.uniform(2, 10), 1) if random.random() > 0.3 else None

        premium = round(random.uniform(20, 55), 1) if random.random() > 0.2 else None
        is_hostile = 1 if target == "U.S. Steel" else 0

        transactions.append({
            "announcement_date": ann_date.isoformat(),
            "closing_date": closing_date,
            "acquirer": acquirer,
            "acquirer_sector": acq_sector,
            "target": target,
            "target_sector": tgt_sector,
            "target_country": tgt_country,
            "deal_value_mm": value,
            "payment_method": payment,
            "ev_ebitda_multiple": ev_ebitda,
            "ev_revenue_multiple": ev_revenue,
            "premium_pct": premium,
            "deal_status": status,
            "deal_type": dtype,
            "is_hostile": is_hostile,
            "is_cross_border": is_cross_border,
        })
        used_company_names.add(acquirer)
        used_company_names.add(target)

    # Generate remaining synthetic deals
    remaining = 200 - len(REAL_DEALS)

    for _ in range(remaining):
        tgt_sector = random.choice(SECTORS)
        acq_sector = tgt_sector if random.random() < 0.65 else random.choice(SECTORS)

        # Pick target
        available = [c for c in SECTOR_COMPANIES[tgt_sector] if c not in used_company_names]
        if not available:
            available = SECTOR_COMPANIES[tgt_sector]
        target = random.choice(available)
        used_company_names.add(target)

        # Deal value
        deal_value = generate_deal_value()

        # Acquirer — larger deals more likely to have real acquirers
        if deal_value > 5000 and random.random() < 0.6:
            acquirer = random.choice(LARGE_ACQUIRERS.get(acq_sector, ["Unknown Corp."]))
        else:
            acq_candidates = [c for c in SECTOR_COMPANIES.get(acq_sector, TECH_COMPANIES) if c not in used_company_names and c != target]
            if not acq_candidates:
                acq_candidates = LARGE_ACQUIRERS.get(acq_sector, ["Unknown Corp."])
            acquirer = random.choice(acq_candidates)

        # Cross-border (larger deals more likely)
        is_cross_border = 1 if random.random() < (0.25 if deal_value > 5000 else 0.12) else 0
        tgt_country = random.choice([c for c in COUNTRIES if c != "United States"]) if is_cross_border else "United States"

        # Date
        ann_date = random_date(2019, 2025)

        # Status
        r = random.random()
        if r < 0.75:
            status = "Completed"
        elif r < 0.90:
            status = "Pending"
        else:
            status = "Withdrawn"

        # Closing date
        if status == "Completed":
            close_delta = random.randint(30, 300)
            closing_date = (ann_date + timedelta(days=close_delta)).isoformat()
        elif status == "Pending":
            closing_date = None
        else:
            closing_date = None

        # Deal type
        r = random.random()
        if r < 0.55:
            dtype = "Acquisition"
        elif r < 0.72:
            dtype = "Merger"
        elif r < 0.85:
            dtype = "Leveraged Buyout"
        elif r < 0.92:
            dtype = "Divestiture"
        else:
            dtype = "Management Buyout"

        # Payment
        if dtype in ("Leveraged Buyout", "Management Buyout"):
            payment = "Cash"
        else:
            payment = random.choice(PAYMENT_METHODS)

        # Hostile
        is_hostile = 1 if random.random() < 0.05 else 0

        # Multiples — sector-dependent
        mult_range = SECTOR_MULTIPLES[tgt_sector]
        ev_ebitda = round(random.uniform(mult_range[0], mult_range[1]), 1) if random.random() > 0.2 else None
        ev_revenue = round(random.uniform(1.5, 8), 1) if random.random() > 0.35 else None

        # Premium — NULL for ~30% (private targets etc.)
        premium = round(random.uniform(15, 60), 1) if random.random() > 0.3 else None

        transactions.append({
            "announcement_date": ann_date.isoformat(),
            "closing_date": closing_date,
            "acquirer": acquirer,
            "acquirer_sector": acq_sector,
            "target": target,
            "target_sector": tgt_sector,
            "target_country": tgt_country,
            "deal_value_mm": deal_value,
            "payment_method": payment,
            "ev_ebitda_multiple": ev_ebitda,
            "ev_revenue_multiple": ev_revenue,
            "premium_pct": premium,
            "deal_status": status,
            "deal_type": dtype,
            "is_hostile": is_hostile,
            "is_cross_border": is_cross_border,
        })

    return transactions


def generate_advisors(transactions):
    advisors = []
    for txn_id, txn in enumerate(transactions, start=1):
        deal_value = txn["deal_value_mm"]

        # Number of acquirer advisors (larger deals = more advisors)
        if deal_value > 20000:
            n_acq = random.choice([2, 3])
            n_tgt = random.choice([2, 3])
        elif deal_value > 5000:
            n_acq = random.choice([1, 2])
            n_tgt = random.choice([1, 2])
        elif deal_value > 1000:
            n_acq = random.choice([1, 1, 2])
            n_tgt = random.choice([0, 1, 1])
        else:
            n_acq = random.choice([0, 0, 1])
            n_tgt = random.choice([0, 1])

        # Withdrawn/small deals sometimes have no advisors
        if txn["deal_status"] == "Withdrawn" and random.random() < 0.3:
            n_acq = max(0, n_acq - 1)

        # Pick unique banks
        banks_pool = list(ADVISOR_BANKS)
        random.shuffle(banks_pool)

        # Bulge bracket more likely for large deals
        if deal_value > 10000:
            elite = ["Goldman Sachs", "Morgan Stanley", "JPMorgan", "BofA Securities", "Citi"]
            boutique = ["Lazard", "Evercore", "Centerview Partners", "Qatalyst Partners", "PJT Partners", "Moelis & Company"]
            banks_pool = random.sample(elite, min(3, len(elite))) + random.sample(boutique, min(3, len(boutique))) + banks_pool

        used_banks = set()
        for i in range(n_acq):
            bank = next((b for b in banks_pool if b not in used_banks), None)
            if bank is None:
                break
            used_banks.add(bank)
            # Fee: ~0.5-2% for smaller, lower % for larger
            if random.random() < 0.4:
                fee = None
            else:
                fee_pct = random.uniform(0.002, 0.015) if deal_value > 5000 else random.uniform(0.005, 0.025)
                fee = round(deal_value * fee_pct, 1)
            advisors.append({
                "transaction_id": txn_id,
                "bank": bank,
                "role": "Acquirer Advisor",
                "advisory_fee_mm": fee,
            })

        for i in range(n_tgt):
            bank = next((b for b in banks_pool if b not in used_banks), None)
            if bank is None:
                break
            used_banks.add(bank)
            if random.random() < 0.4:
                fee = None
            else:
                fee_pct = random.uniform(0.003, 0.02) if deal_value > 5000 else random.uniform(0.008, 0.03)
                fee = round(deal_value * fee_pct, 1)
            advisors.append({
                "transaction_id": txn_id,
                "bank": bank,
                "role": "Target Advisor",
                "advisory_fee_mm": fee,
            })

    return advisors


def generate_financing(transactions):
    financing = []
    for txn_id, txn in enumerate(transactions, start=1):
        if txn["deal_status"] == "Withdrawn":
            continue
        deal_value = txn["deal_value_mm"]
        dtype = txn["deal_type"]
        payment = txn["payment_method"]

        # Only cash/cash-and-stock deals need financing details
        if payment == "Stock" and dtype not in ("Leveraged Buyout", "Management Buyout"):
            if random.random() < 0.8:
                continue

        # LBOs have much more debt
        if dtype in ("Leveraged Buyout", "Management Buyout"):
            debt_pct = random.uniform(0.55, 0.75)
            equity_pct = 1.0 - debt_pct
            n_sources = random.choice([3, 4, 5])
        elif deal_value > 10000:
            debt_pct = random.uniform(0.2, 0.5) if payment != "Stock" else random.uniform(0, 0.15)
            equity_pct = 1.0 - debt_pct
            n_sources = random.choice([2, 3, 4])
        elif deal_value > 1000:
            if random.random() < 0.3:
                continue  # Some don't disclose
            debt_pct = random.uniform(0.15, 0.45)
            equity_pct = 1.0 - debt_pct
            n_sources = random.choice([1, 2, 3])
        else:
            if random.random() < 0.5:
                continue
            debt_pct = random.uniform(0.1, 0.4)
            equity_pct = 1.0 - debt_pct
            n_sources = random.choice([1, 2])

        total_debt = deal_value * debt_pct
        total_equity = deal_value * equity_pct

        # Allocate financing sources
        lenders_pool = list(LENDERS)
        random.shuffle(lenders_pool)

        # Always add equity contribution
        financing.append({
            "transaction_id": txn_id,
            "source": "Equity Contribution",
            "amount_mm": round(total_equity, 1),
            "lender": txn["acquirer"],
        })

        # Add debt tranches
        debt_remaining = total_debt
        debt_sources = []
        if dtype in ("Leveraged Buyout", "Management Buyout"):
            debt_sources = random.sample(
                ["Term Loan", "Senior Notes", "Revolving Credit", "Mezzanine", "Bridge Loan"],
                min(n_sources - 1, 4)
            )
        else:
            debt_sources = random.sample(
                ["Term Loan", "Senior Notes", "Revolving Credit", "Bridge Loan"],
                min(n_sources - 1, 3)
            )

        for j, source in enumerate(debt_sources):
            if j == len(debt_sources) - 1:
                amt = debt_remaining
            else:
                amt = debt_remaining * random.uniform(0.25, 0.6)
                debt_remaining -= amt

            lender = lenders_pool[j % len(lenders_pool)]
            financing.append({
                "transaction_id": txn_id,
                "source": source,
                "amount_mm": round(amt, 1),
                "lender": lender,
            })

    return financing


def create_database():
    transactions = generate_transactions()
    advisors = generate_advisors(transactions)
    financing = generate_financing(transactions)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Create tables
    c.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY,
            announcement_date TEXT,
            closing_date TEXT,
            acquirer TEXT,
            acquirer_sector TEXT,
            target TEXT,
            target_sector TEXT,
            target_country TEXT,
            deal_value_mm REAL,
            payment_method TEXT,
            ev_ebitda_multiple REAL,
            ev_revenue_multiple REAL,
            premium_pct REAL,
            deal_status TEXT,
            deal_type TEXT,
            is_hostile INTEGER,
            is_cross_border INTEGER
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS advisors (
            id INTEGER PRIMARY KEY,
            transaction_id INTEGER,
            bank TEXT,
            role TEXT,
            advisory_fee_mm REAL,
            FOREIGN KEY (transaction_id) REFERENCES transactions(id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS financing (
            id INTEGER PRIMARY KEY,
            transaction_id INTEGER,
            source TEXT,
            amount_mm REAL,
            lender TEXT,
            FOREIGN KEY (transaction_id) REFERENCES transactions(id)
        )
    """)

    # Insert data
    for i, txn in enumerate(transactions, start=1):
        c.execute("""
            INSERT INTO transactions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            i, txn["announcement_date"], txn["closing_date"], txn["acquirer"],
            txn["acquirer_sector"], txn["target"], txn["target_sector"],
            txn["target_country"], txn["deal_value_mm"], txn["payment_method"],
            txn["ev_ebitda_multiple"], txn["ev_revenue_multiple"], txn["premium_pct"],
            txn["deal_status"], txn["deal_type"], txn["is_hostile"], txn["is_cross_border"],
        ))

    for i, adv in enumerate(advisors, start=1):
        c.execute("""
            INSERT INTO advisors VALUES (?, ?, ?, ?, ?)
        """, (i, adv["transaction_id"], adv["bank"], adv["role"], adv["advisory_fee_mm"]))

    for i, fin in enumerate(financing, start=1):
        c.execute("""
            INSERT INTO financing VALUES (?, ?, ?, ?, ?)
        """, (i, fin["transaction_id"], fin["source"], fin["amount_mm"], fin["lender"]))

    conn.commit()
    conn.close()
    print(f"Database created at {DB_PATH}")
    print(f"  Transactions: {len(transactions)}")
    print(f"  Advisors: {len(advisors)}")
    print(f"  Financing: {len(financing)}")


if __name__ == "__main__":
    create_database()
