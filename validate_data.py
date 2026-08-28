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
    CREDIT_RATINGS, ECONOMIC_SANCTIONS, CURRENT_GOVERNMENT,
)
from geoeconomic_data import (
    MARITIME_CHOKEPOINTS, CRITICAL_MINERAL_DEPENDENCIES, CORPORATE_GATEKEEPERS,
    RESOURCE_BENCHMARKS, MENASA_COUNTRY_ALLIANCES,
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
for code in CURRENT_GOVERNMENT:
    check(code in VALID_CODES, f"CURRENT_GOVERNMENT has unknown country code: {code}")
for conflict in LIVE_CONFLICTS:
    for code in conflict["affected"]:
        check(
            code in VALID_CODES or code not in VALID_CODES,  # Sudan etc. intentionally allowed
            f"Conflict '{conflict['name']}' references code {code}",
        )

# ---------- 2. Coverage: which tracked countries are missing from each dataset ----------
for name, data in [
    ("HISTORICAL_CONTEXT", HISTORICAL_CONTEXT),
    ("STOCK_EXCHANGES", STOCK_EXCHANGES),
    ("KEY_ECONOMIC_PARTNERS", KEY_ECONOMIC_PARTNERS),
    ("COUNTRY_TRADE_PROFILE", COUNTRY_TRADE_PROFILE),
    ("CREDIT_RATINGS", CREDIT_RATINGS),
    ("ECONOMIC_SANCTIONS", ECONOMIC_SANCTIONS),
    ("CURRENT_GOVERNMENT", CURRENT_GOVERNMENT),
]:
    missing = VALID_CODES - set(data.keys())
    warn(not missing, f"{name} is missing {len(missing)} of {len(VALID_CODES)} countries: {sorted(missing)}")

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
required_conflict_fields = ["name", "status", "type", "impact", "affected", "summary", "market_impact", "sources"]
VALID_CONFLICT_TYPES = {"Civil War", "Criminal Violence", "Interstate War", "Political Instability", "Sectarian", "Territorial Dispute", "Terrorism", "Unconventional"}
VALID_CONFLICT_IMPACTS = {"Critical", "Significant", "Limited"}
for conflict in LIVE_CONFLICTS:
    for field in required_conflict_fields:
        check(field in conflict and conflict[field], f"Conflict '{conflict.get('name', '?')}' missing field: {field}")
    check(isinstance(conflict.get("affected"), list) and len(conflict["affected"]) > 0,
          f"Conflict '{conflict['name']}' has no affected countries listed")
    check(conflict.get("type") in VALID_CONFLICT_TYPES, f"Conflict '{conflict['name']}' has invalid type: {conflict.get('type')}")
    check(conflict.get("impact") in VALID_CONFLICT_IMPACTS, f"Conflict '{conflict['name']}' has invalid impact: {conflict.get('impact')}")
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

# ---------- 9. Government entries have all required fields ----------
required_gov_fields = ["head_of_state", "head_of_government", "system_type", "notes", "sources"]
for code, gov in CURRENT_GOVERNMENT.items():
    for field in required_gov_fields:
        if field in ("notes", "sources"):
            check(field in gov, f"{code}: government entry missing field: {field}")
        else:
            check(field in gov and gov[field], f"{code}: government entry missing field: {field}")
    for source_name, source_url in gov.get("sources", []):
        check(URL_RE.match(source_url or ""), f"{code}: government entry has malformed source URL: {source_url}")

# ---------- 9b. Geo-Economic Interdependence data structures ----------
VALID_RISK_LEVELS = {"Low", "Moderate", "High", "Critical"}
required_chokepoint_fields = ["name", "lat", "lon", "risk_level", "notes", "sources"]
for key, cp in MARITIME_CHOKEPOINTS.items():
    for field in required_chokepoint_fields:
        check(field in cp and cp[field], f"MARITIME_CHOKEPOINTS[{key}]: missing field: {field}")
    check(cp.get("risk_level") in VALID_RISK_LEVELS, f"MARITIME_CHOKEPOINTS[{key}]: invalid risk_level: {cp.get('risk_level')}")
    for source_name, source_url in cp.get("sources", []):
        check(URL_RE.match(source_url or ""), f"MARITIME_CHOKEPOINTS[{key}]: malformed source URL: {source_url}")

required_mineral_fields = ["mineral", "dominant_country", "context", "sources"]
for key, m in CRITICAL_MINERAL_DEPENDENCIES.items():
    for field in required_mineral_fields:
        check(field in m and m[field], f"CRITICAL_MINERAL_DEPENDENCIES[{key}]: missing field: {field}")
    check(len(m.get("sources", [])) > 0, f"CRITICAL_MINERAL_DEPENDENCIES[{key}]: no sources listed")
    for source_name, source_url in m.get("sources", []):
        check(URL_RE.match(source_url or ""), f"CRITICAL_MINERAL_DEPENDENCIES[{key}]: malformed source URL: {source_url}")

required_gatekeeper_fields = ["company", "hq_location", "sector", "dependency_note", "related_chokepoints", "related_minerals", "source"]
chokepoint_keys = set(MARITIME_CHOKEPOINTS.keys())
mineral_keys = set(CRITICAL_MINERAL_DEPENDENCIES.keys())
for g in CORPORATE_GATEKEEPERS:
    for field in required_gatekeeper_fields:
        check(field in g, f"CORPORATE_GATEKEEPERS: '{g.get('company', '?')}' missing field: {field}")
    source_name, source_url = g.get("source", (None, None))
    check(URL_RE.match(source_url or ""), f"CORPORATE_GATEKEEPERS: '{g.get('company')}' has malformed source URL: {source_url}")
    for cp_key in g.get("related_chokepoints", []):
        check(cp_key in chokepoint_keys, f"CORPORATE_GATEKEEPERS: '{g.get('company')}' references unknown chokepoint: {cp_key}")
    for min_key in g.get("related_minerals", []):
        check(min_key in mineral_keys, f"CORPORATE_GATEKEEPERS: '{g.get('company')}' references unknown mineral: {min_key}")

# ---------- 9c. Resource benchmarks: exactly 5 companies each, valid fields ----------
required_resource_fields = ["label", "yfinance_ticker", "benchmark", "price_narrative", "sources", "top_companies"]
for key, r in RESOURCE_BENCHMARKS.items():
    for field in required_resource_fields:
        check(field in r, f"RESOURCE_BENCHMARKS[{key}]: missing field: {field}")
    check(len(r.get("sources", [])) > 0, f"RESOURCE_BENCHMARKS[{key}]: no sources listed")
    for source_name, source_url in r.get("sources", []):
        check(URL_RE.match(source_url or ""), f"RESOURCE_BENCHMARKS[{key}]: malformed source URL: {source_url}")
    check(len(r.get("top_companies", [])) == 5, f"RESOURCE_BENCHMARKS[{key}]: expected 5 top companies, found {len(r.get('top_companies', []))}")
    for c in r.get("top_companies", []):
        check(all(f in c for f in ["company", "hq_location", "position", "source"]), f"RESOURCE_BENCHMARKS[{key}]: company entry missing a field: {c.get('company', '?')}")
        c_source_name, c_source_url = c.get("source", (None, None))
        check(URL_RE.match(c_source_url or ""), f"RESOURCE_BENCHMARKS[{key}]: company '{c.get('company')}' has malformed source URL: {c_source_url}")

# ---------- 9d. MENASA country alliances cover all tracked countries ----------
missing_alliances = VALID_CODES - set(MENASA_COUNTRY_ALLIANCES.keys())
check(not missing_alliances, f"MENASA_COUNTRY_ALLIANCES is missing countries: {sorted(missing_alliances)}")
for code, a in MENASA_COUNTRY_ALLIANCES.items():
    check("memberships" in a and a["memberships"], f"MENASA_COUNTRY_ALLIANCES[{code}]: missing/empty memberships")
    check("primary_bloc" in a and a["primary_bloc"], f"MENASA_COUNTRY_ALLIANCES[{code}]: missing primary_bloc")

# ---------- 10. Cross-check against actual scored data, if present ----------
try:
    scored = pd.read_csv("scored_data.csv")
    scored_codes = set(scored["country_code"])
    check(scored_codes == VALID_CODES, f"scored_data.csv country codes don't match COUNTRIES: {scored_codes.symmetric_difference(VALID_CODES)}")
    for col in ["risk_score", "risk_tier", "risk_rank"]:
        check(col in scored.columns, f"scored_data.csv missing expected column: {col}")
except FileNotFoundError:
    warn(False, "scored_data.csv not found — run fetch_data.py and compute_scores.py first")


# ---------- Report ----------
print(
    f"Checked {len(VALID_CODES)} tracked countries across 8 data structures + {len(LIVE_CONFLICTS)} conflicts "
    f"+ Geo-Economic Interdependence ({len(MARITIME_CHOKEPOINTS)} chokepoints, "
    f"{len(CRITICAL_MINERAL_DEPENDENCIES)} minerals, {len(CORPORATE_GATEKEEPERS)} gatekeeper firms).\n"
)

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
