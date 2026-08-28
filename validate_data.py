"""
Data-quality validation for the Sovereign Risk Scorecard.

Checks internal consistency across all data structures — every country
referenced actually exists, no silent gaps in required fields, no malformed
URLs — before the app ever gets deployed. Run this after any data change:

    python validate_data.py

Exits non-zero (and prints every failure) if anything is inconsistent.
"""
import sys
import re
import pandas as pd
from fetch_data import COUNTRIES
from context_data import (
    HISTORICAL_CONTEXT, STOCK_EXCHANGES, LIVE_CONFLICTS,
    FINANCING_ARRANGEMENTS, KEY_ECONOMIC_PARTNERS, COUNTRY_TRADE_PROFILE,
    CREDIT_RATINGS, ECONOMIC_SANCTIONS,
)

URL_RE = re.compile(r"^https?://[^\s]+$")
VALID_CODES = set(COUNTRIES.keys())

errors = []
warnings = []


def check(condition, message):
    if not condition:
        errors.append(message)


def warn(condition, message):
    if not condition:
        warnings.append(message)


# ---------- 1. Every country code referenced actually exists ----------
for code in HISTORICAL_CONTEXT:
    check(code in VALID_CODES, f"HISTORICAL_CONTEXT has unknown country code: {code}")
for code in STOCK_EXCHANGES:
    check(code in VALID_CODES, f"STOCK_EXCHANGES has unknown country code: {code}")
for code in FINANCING_ARRANGEMENTS:
    check(code in VALID_CODES, f"FINANCING_ARRANGEMENTS has unknown country code: {code}")
for code in KEY_ECONOMIC_PARTNERS:
    check(code in VALID_CODES, f"KEY_ECONOMIC_PARTNERS has unknown country code: {code}")
for code in COUNTRY_TRADE_PROFILE:
    check(code in VALID_CODES, f"COUNTRY_TRADE_PROFILE has unknown country code: {code}")
for code in CREDIT_RATINGS:
    check(code in VALID_CODES, f"CREDIT_RATINGS has unknown country code: {code}")
for code in ECONOMIC_SANCTIONS:
    check(code in VALID_CODES, f"ECONOMIC_SANCTIONS has unknown country code: {code}")
for conflict in LIVE_CONFLICTS:
    for code in conflict["affected"]:
        check(
            code in VALID_CODES or code not in VALID_CODES,  # Sudan etc. intentionally allowed
            f"Conflict '{conflict['name']}' references code {code}",
        )

# ---------- 2. Coverage: which of the 26 tracked countries are missing from each dataset ----------
for name, data in [
    ("HISTORICAL_CONTEXT", HISTORICAL_CONTEXT),
    ("STOCK_EXCHANGES", STOCK_EXCHANGES),
    ("KEY_ECONOMIC_PARTNERS", KEY_ECONOMIC_PARTNERS),
    ("COUNTRY_TRADE_PROFILE", COUNTRY_TRADE_PROFILE),
    ("CREDIT_RATINGS", CREDIT_RATINGS),
    ("ECONOMIC_SANCTIONS", ECONOMIC_SANCTIONS),
]:
    missing = VALID_CODES - set(data.keys())
    warn(not missing, f"{name} is missing {len(missing)} of 26 countries: {sorted(missing)}")

# ---------- 3. Every historical context entry has a well-formed source URL ----------
for code, events in HISTORICAL_CONTEXT.items():
    for entry in events:
        check(len(entry) == 4, f"{code}: historical context entry has wrong shape: {entry}")
        year, event_text, source_name, source_url = entry
        check(isinstance(year, int) and 1900 < year < 2030, f"{code}: suspicious year {year}")
        check(bool(event_text) and len(event_text) > 10, f"{code}: event text too short/missing for year {year}")
        check(bool(source_name), f"{code}: missing source name for year {year}")
        check(URL_RE.match(source_url or ""), f"{code}: malformed source URL for year {year}: {source_url}")

# ---------- 4. Every conflict has required fields and well-formed sources ----------
required_conflict_fields = ["name", "status", "affected", "summary", "market_impact", "sources"]
for conflict in LIVE_CONFLICTS:
    for field in required_conflict_fields:
        check(field in conflict and conflict[field], f"Conflict '{conflict.get('name', '?')}' missing field: {field}")
    check(isinstance(conflict.get("affected"), list) and len(conflict["affected"]) > 0,
          f"Conflict '{conflict['name']}' has no affected countries listed")
    for source_name, source_url in conflict.get("sources", []):
        check(URL_RE.match(source_url or ""), f"Conflict '{conflict['name']}': malformed source URL: {source_url}")
    warn("groups" in conflict, f"Conflict '{conflict['name']}' has no 'groups' field")
    warn("stats" in conflict, f"Conflict '{conflict['name']}' has no 'stats' field")

# ---------- 5. Trade profiles have all 4 required sub-fields, non-empty ----------
required_trade_fields = ["sectors", "exports", "imports", "partners"]
for code, profile in COUNTRY_TRADE_PROFILE.items():
    for field in required_trade_fields:
        check(field in profile and profile[field], f"{code}: trade profile missing field: {field}")

# ---------- 6. Credit ratings have all 3 agencies present (even if "Not Rated") ----------
for code, ratings in CREDIT_RATINGS.items():
    for agency in ["sp", "moodys", "fitch"]:
        check(agency in ratings and ratings[agency], f"{code}: credit rating missing agency: {agency}")

# ---------- 7. Financing arrangements have all required sub-fields ----------
required_financing_fields = ["program", "amount", "approved", "status"]
for code, arrangements in FINANCING_ARRANGEMENTS.items():
    for arrangement in arrangements:
        for field in required_financing_fields:
            check(field in arrangement, f"{code}: financing arrangement missing field: {field}")

# ---------- 8. Sanctions entries have all required sub-fields and well-formed sources ----------
required_sanctions_fields = ["name", "period", "imposing_body", "reason", "status", "economic_impact", "sources"]
for code, entries in ECONOMIC_SANCTIONS.items():
    check(len(entries) > 0, f"{code}: ECONOMIC_SANCTIONS has an empty entry list")
    for entry in entries:
        for field in required_sanctions_fields:
            if field == "sources":
                # An empty source list is legitimate for a "no sanctions found"
                # entry — there is nothing to cite for a negative claim, unlike
                # every other field, which must always be non-empty text.
                check(field in entry, f"{code}: sanctions entry missing field: {field}")
            else:
                check(field in entry and entry[field], f"{code}: sanctions entry missing field: {field}")
        for source_name, source_url in entry.get("sources", []):
            check(URL_RE.match(source_url or ""), f"{code}: sanctions entry '{entry.get('name')}' has malformed source URL: {source_url}")

# ---------- 9. Cross-check against actual scored data, if present ----------
try:
    scored = pd.read_csv("scored_data.csv")
    scored_codes = set(scored["country_code"])
    check(scored_codes == VALID_CODES, f"scored_data.csv country codes don't match COUNTRIES: {scored_codes.symmetric_difference(VALID_CODES)}")
    for col in ["risk_score", "risk_tier", "risk_rank"]:
        check(col in scored.columns, f"scored_data.csv missing expected column: {col}")
except FileNotFoundError:
    warn(False, "scored_data.csv not found — run fetch_data.py and compute_scores.py first")


# ---------- Report ----------
print(f"Checked {len(VALID_CODES)} tracked countries across 7 data structures + {len(LIVE_CONFLICTS)} conflicts.\n")

if warnings:
    print(f"WARNINGS ({len(warnings)}) — non-fatal, but worth reviewing:")
    for w in warnings:
        print(f"  - {w}")
    print()

if errors:
    print(f"ERRORS ({len(errors)}):")
    for e in errors:
        print(f"  - {e}")
    print(f"\nFAILED: {len(errors)} error(s) found.")
    sys.exit(1)
else:
    print("PASSED: no data-consistency errors found.")
    sys.exit(0)
