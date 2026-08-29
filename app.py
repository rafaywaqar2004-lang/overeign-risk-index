import re
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import yfinance as yf
from datetime import datetime, timezone
from context_data import HISTORICAL_CONTEXT, STOCK_EXCHANGES, LIVE_CONFLICTS, FINANCING_ARRANGEMENTS, KEY_ECONOMIC_PARTNERS, COUNTRY_TRADE_PROFILE, CREDIT_RATINGS, CREDIT_RATINGS_SOURCES, ECONOMIC_SANCTIONS, HDI_DATA, CURRENT_GOVERNMENT
from geoeconomic_data import MARITIME_CHOKEPOINTS, CRITICAL_MINERAL_DEPENDENCIES, CORPORATE_GATEKEEPERS, TRADE_ARTERIES, TRADE_ALLIANCES, MENASA_COUNTRY_ALLIANCES, COUNTRY_CAPITAL_COORDS, RESOURCE_BENCHMARKS, SEMICONDUCTOR_SUBDIVISIONS, ENERGY_FLOW_GRANULARITY, UNCTAD_RMT_2025
from pdf_export import generate_country_pdf
# Reuse the exact scoring methodology from compute_scores.py for the
# year-over-year factor drill-down below, so the "what drove this year's
# score" explanation is always consistent with how the composite is actually
# calculated, rather than a separate, potentially drifting reimplementation.
from compute_scores import WEIGHTS, HIGHER_IS_RISKIER, normalize_to_risk_0_100

st.set_page_config(page_title="MENASA Risk Monitor", page_icon="assets/favicon.png", layout="wide")

# ============================================================
# DESIGN SYSTEM — "Institute Brief": a near-black editorial theme
# modeled on the CFR site's own actual look (not its lighter conflict-
# tracker sub-tool) — true near-black ground, off-white body text, a
# serif display face for headlines/section titles (evoking a print
# "foreign affairs" journal), and a restrained institutional blue
# accent rather than CFR's own cardinal-red brand color, since red is
# already this app's own "Higher Risk / Critical" severity color —
# reusing it as the general UI accent would recreate the exact
# color-collision problem this project deliberately fixed earlier (a
# status color must never double as a plain navigation/link color).
# ============================================================
BG = "#0a0a0a"
SURFACE = "#161616"
SURFACE_ALT = "#1f1f1f"
BORDER = "rgba(255,255,255,0.10)"
ACCENT = "#0d9488"
ACCENT_DIM = "rgba(13,148,136,0.12)"
# A second, deliberately distinct accent — reserved specifically for
# curated/editorial content (sourced narrative, historical context,
# government cards) as opposed to ACCENT's live-quantitative-data meaning.
# Kept away from the bright risk-tier amber (#fbbf24) so it never reads as
# a severity signal.
ACCENT2 = "#c9a876"
ACCENT2_DIM = "rgba(201,168,118,0.12)"
TEXT = "#f5f5f4"
TEXT_MUTED = "#a3a3a3"
TIER_COLORS = {
    "Lower Risk": "#34d399",
    "Moderate Risk": "#fbbf24",
    "Higher Risk": "#f87171",
    "Insufficient data": "#94a3b8",
}

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&family=Newsreader:ital,wght@0,500;0,600;0,700;1,500&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', -apple-system, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }}

    h1, h2, h3 {{ font-family: 'Inter', sans-serif !important; }}

    /* editorial serif for headline-level moments, CFR-style */
    .masthead-title, .section-title {{ font-family: 'Newsreader', Georgia, serif !important; }}

    /* subtle depth instead of a flat background */
    [data-testid="stAppViewContainer"] > .main {{
        background: radial-gradient(ellipse 1400px 800px at 50% -10%, rgba(13,148,136,0.06), transparent),
                    linear-gradient(180deg, {BG} 0%, #050505 100%);
    }}

    /* ---- masthead ---- */
    .tag-label {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 500;
        letter-spacing: 0.08em;
        color: {ACCENT};
        margin-bottom: 0.7rem;
    }}
    .masthead-title {{
        font-family: 'Inter', sans-serif;
        font-size: 2.75rem;
        font-weight: 800;
        color: {TEXT};
        line-height: 1.08;
        margin: 0 0 0.7rem 0;
        letter-spacing: -0.02em;
    }}
    .masthead-title span {{ color: {ACCENT}; }}
    .masthead-sub {{
        font-size: 0.96rem;
        color: {TEXT_MUTED};
        max-width: 660px;
        line-height: 1.65;
        margin-bottom: 1.4rem;
    }}
    .section-tag {{
        font-family: 'Inter', sans-serif;
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: {ACCENT};
        opacity: 0.85;
        margin-bottom: 0.4rem;
    }}
    .section-title {{
        font-family: 'Inter', sans-serif;
        font-size: 1.35rem;
        font-weight: 700;
        color: {TEXT};
        margin-bottom: 1.3rem;
        letter-spacing: -0.01em;
    }}

    /* ---- stat cards ---- */
    .stat-card {{
        --card-accent: {ACCENT};
        background: linear-gradient(160deg, {SURFACE_ALT} 0%, {SURFACE} 100%);
        border: 1px solid {BORDER};
        border-top: 2px solid var(--card-accent);
        border-radius: 10px;
        padding: 1.2rem 1.4rem 1.15rem;
        height: 100%;
        box-shadow: 0 4px 16px rgba(0,0,0,0.28);
        transition: transform 0.18s ease, box-shadow 0.18s ease;
        position: relative;
        overflow: hidden;
    }}
    .stat-card::before {{
        content: "";
        position: absolute; top: -50%; right: -15%;
        width: 130px; height: 130px;
        background: radial-gradient(circle, color-mix(in srgb, var(--card-accent) 16%, transparent) 0%, transparent 70%);
        pointer-events: none;
    }}
    .stat-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.36);
    }}
    .stat-label {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.62rem;
        font-weight: 500;
        letter-spacing: 0.09em;
        text-transform: uppercase;
        color: {TEXT_MUTED};
        margin-bottom: 0.55rem;
        position: relative;
    }}
    .stat-value {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.85rem;
        font-weight: 700;
        color: {TEXT};
        line-height: 1.15;
        position: relative;
    }}
    .stat-sub {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.76rem;
        color: {ACCENT};
        margin-top: 0.45rem;
    }}

    /* ---- narrative callout ---- */
    .narrative-box {{
        background: linear-gradient(135deg, {ACCENT_DIM} 0%, rgba(13,148,136,0.03) 100%);
        border-left: 3px solid {ACCENT};
        padding: 1.15rem 1.4rem;
        font-size: 0.9rem;
        line-height: 1.7;
        color: {TEXT};
        border-radius: 4px 12px 12px 4px;
    }}
    .narrative-box b {{ color: {ACCENT}; font-weight: 600; }}

    /* ---- risk tier badge ---- */
    .tier-badge {{
        display: inline-block;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.66rem;
        font-weight: 600;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        padding: 0.3rem 0.75rem;
        border-radius: 20px;
        margin-top: 0.4rem;
    }}

    /* ---- custom html table ---- */
    .custom-table {{
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        font-size: 0.85rem;
        margin-bottom: 1rem;
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid {BORDER};
    }}
    .custom-table th {{
        text-align: left;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.64rem;
        font-weight: 500;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: {ACCENT};
        background: {SURFACE};
        border-bottom: 1px solid {BORDER};
        padding: 0.7rem 0.9rem;
    }}
    .custom-table td {{
        padding: 0.65rem 0.9rem;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        color: {TEXT};
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.82rem;
        transition: background 0.12s ease;
    }}
    .custom-table tr:last-child td {{ border-bottom: none; }}
    .custom-table tr:hover td {{ background: rgba(13,148,136,0.04); }}

    /* ---- pill link buttons ---- */
    .pill-link {{
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.03em;
        color: {BG} !important;
        background: {ACCENT};
        padding: 0.55rem 1.15rem;
        border-radius: 20px;
        text-decoration: none !important;
        margin-right: 0.75rem;
        margin-bottom: 0.5rem;
        box-shadow: 0 2px 8px rgba(13,148,136,0.22);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }}
    .pill-link:hover {{
        transform: translateY(-1px);
        box-shadow: 0 4px 14px rgba(13,148,136,0.32);
    }}

    /* ---- streamlit widget overrides ---- */
    [data-testid="stTabs"] button[role="tab"] {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.76rem;
        font-weight: 500;
        letter-spacing: 0.04em;
        transition: color 0.15s ease;
    }}
    [data-testid="stAlert"] {{
        background: {ACCENT_DIM} !important;
        border-left: 3px solid {ACCENT} !important;
        border-radius: 4px 12px 12px 4px !important;
    }}
    [data-testid="stVerticalBlockBorderWrapper"] {{
        border-color: {BORDER} !important;
        border-radius: 12px !important;
        transition: border-color 0.15s ease;
    }}
    [data-baseweb="select"] > div {{
        border-radius: 10px !important;
    }}
    [data-testid="stSlider"] {{ padding-top: 0.2rem; }}
    hr {{ border-color: {BORDER} !important; }}
    footer {{ visibility: hidden; }}

    .site-footer {{
        margin-top: 3rem;
        padding-top: 1.5rem;
        border-top: 1px solid {BORDER};
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: {TEXT_MUTED};
    }}
    .site-footer a {{ color: {ACCENT}; text-decoration: none; }}

    /* ---- tab bar: scroll affordance so extra tabs are never invisible ---- */
    [data-testid="stTabs"] [data-baseweb="tab-list"] {{
        overflow-x: auto;
        scrollbar-width: thin;
        scrollbar-color: {ACCENT} transparent;
        -webkit-overflow-scrolling: touch;
        mask-image: linear-gradient(to right, black calc(100% - 28px), transparent 100%);
        -webkit-mask-image: linear-gradient(to right, black calc(100% - 28px), transparent 100%);
    }}
    [data-testid="stTabs"] [data-baseweb="tab-list"]::-webkit-scrollbar {{
        height: 4px;
    }}
    [data-testid="stTabs"] [data-baseweb="tab-list"]::-webkit-scrollbar-thumb {{
        background: {ACCENT};
        border-radius: 4px;
    }}

    /* ---- restyle Streamlit's own rerun/status chrome to match the theme
       instead of its stock red/white look ---- */
    [data-testid="stStatusWidget"] {{
        background: {SURFACE_ALT} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 20px !important;
        color: {TEXT_MUTED} !important;
    }}
    [data-testid="stStatusWidget"] svg {{ fill: {ACCENT} !important; }}
    .stSpinner > div {{ border-top-color: {ACCENT} !important; }}
    .stSpinner p {{ color: {TEXT_MUTED} !important; }}

    /* ---- mobile ---- */
    @media (max-width: 640px) {{
        .masthead-title {{ font-size: 1.9rem; }}
        .masthead-sub {{ font-size: 0.88rem; }}
        .stat-card {{ padding: 0.9rem 1rem; }}
        .stat-value {{ font-size: 1.35rem; }}
        [data-testid="stTabs"] button[role="tab"] {{ font-size: 0.78rem; padding: 0.5rem 0.6rem; white-space: nowrap; }}
    }}
</style>
""", unsafe_allow_html=True)


def tier_badge_html(tier):
    colors = {
        "Lower Risk": ("rgba(52,211,153,0.14)", "#34d399"),
        "Moderate Risk": ("rgba(251,191,36,0.14)", "#fbbf24"),
        "Higher Risk": ("rgba(248,113,113,0.14)", "#f87171"),
        "Insufficient data": ("rgba(100,116,139,0.14)", "#94a3b8"),
    }
    bg, fg = colors.get(tier, colors["Insufficient data"])
    return f'<span class="tier-badge" style="background:{bg};color:{fg};">{tier}</span>'


def sparkline_svg(values, color=None):
    """Minimal inline trend line for a stat card — no axes, no library overhead.
    values must be chronological; needs at least 2 points to draw a line."""
    if not values or len(values) < 2:
        return ""
    color = color or ACCENT
    w, h, pad = 100, 26, 3
    lo, hi = min(values), max(values)
    span = (hi - lo) or 1
    n = len(values)
    pts = [
        (pad + i * (w - 2 * pad) / (n - 1), h - pad - (v - lo) / span * (h - 2 * pad))
        for i, v in enumerate(values)
    ]
    path = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    lx, ly = pts[-1]
    return (
        f'<svg width="100%" height="{h}" viewBox="0 0 {w} {h}" preserveAspectRatio="none" '
        f'style="display:block;margin-top:0.5rem;">'
        f'<polyline points="{path}" fill="none" stroke="{color}" stroke-width="1.6" '
        f'stroke-linecap="round" stroke-linejoin="round" vector-effect="non-scaling-stroke"/>'
        f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="2.2" fill="{color}"/>'
        f'</svg>'
    )


def stat_card(label, value, sub=None, spark=None, accent=None):
    accent = accent or ACCENT
    sub_html = f'<div class="stat-sub" style="color:{accent};">{sub}</div>' if sub else ""
    spark_html = sparkline_svg(spark, color=accent) if spark else ""
    st.markdown(
        f'<div class="stat-card" style="--card-accent:{accent};"><div class="stat-label">{label}</div>'
        f'<div class="stat-value">{value}</div>{spark_html}{sub_html}</div>',
        unsafe_allow_html=True,
    )


def custom_table(rows, headers):
    # Wrapped in its own horizontal-scroll container -- on a narrow viewport
    # a wide table (many columns, or long cell content like a 4-country
    # compare) has nowhere else to go, since the page itself doesn't scroll
    # sideways. Without this, columns past the viewport edge were simply
    # unreachable, not just visually cramped.
    html = '<div style="overflow-x:auto;"><table class="custom-table"><thead><tr>'
    html += "".join(f"<th>{h}</th>" for h in headers)
    html += "</tr></thead><tbody>"
    for row in rows:
        html += "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>"
    html += "</tbody></table></div>"
    st.markdown(html, unsafe_allow_html=True)


def style_chart(fig, height=420):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="JetBrains Mono, monospace", color=TEXT, size=12),
        height=height,
        margin=dict(t=30, b=30, l=10, r=10),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        hoverlabel=dict(bgcolor=SURFACE_ALT, font_color=TEXT, bordercolor=ACCENT),
        modebar=dict(bgcolor="rgba(0,0,0,0)", color=TEXT_MUTED, activecolor=ACCENT),
    )
    fig.update_xaxes(gridcolor="rgba(148,163,184,0.10)", zerolinecolor="rgba(148,163,184,0.16)")
    fig.update_yaxes(gridcolor="rgba(148,163,184,0.10)", zerolinecolor="rgba(148,163,184,0.16)")
    return fig


def sourced_table(rows, headers):
    """Like custom_table, but the last column of each row is rendered as a link."""
    html = '<div style="overflow-x:auto;"><table class="custom-table"><thead><tr>'
    html += "".join(f"<th>{h}</th>" for h in headers)
    html += "</tr></thead><tbody>"
    for row in rows:
        cells = row[:-1]
        source_name, source_url = row[-1]
        html += "<tr>" + "".join(f"<td>{c}</td>" for c in cells)
        html += f'<td><a href="{source_url}" target="_blank" rel="noopener noreferrer" style="color:{ACCENT};">{source_name} ↗</a></td></tr>'
    html += "</tbody></table></div>"
    st.markdown(html, unsafe_allow_html=True)


def _fmt_usd(value):
    """Formats a raw US-dollar figure (e.g. GDP in current US$, which can run
    into the hundreds of billions) as a human-readable abbreviated amount —
    $45.2B rather than $45,200,000,000 — since a 12-digit number is not
    actually easier to read than a rounded, labeled one for a general audience."""
    abs_v = abs(value)
    sign = "-" if value < 0 else ""
    if abs_v >= 1e12:
        return f"{sign}${abs_v / 1e12:.2f}T"
    if abs_v >= 1e9:
        return f"{sign}${abs_v / 1e9:.2f}B"
    if abs_v >= 1e6:
        return f"{sign}${abs_v / 1e6:.2f}M"
    if abs_v >= 1e3:
        return f"{sign}${abs_v / 1e3:.1f}K"
    return f"{sign}${abs_v:,.0f}"


def _fmt_value_unit(value, unit):
    """Formats a raw indicator value with its unit for inline/table display.
    Percent units suffix directly (e.g. '1.87%'); longer descriptive units
    (e.g. 'WGI estimate, -2.5 to +2.5') are parenthesized and shortened so
    they read as an annotation rather than running straight into the number;
    USD-denominated indicators are abbreviated via _fmt_usd."""
    if unit == "%":
        return f"{value:.2f}%"
    if "WGI estimate" in unit:
        return f"{value:.2f} (WGI scale)"
    if unit == "USD":
        return _fmt_usd(value)
    return f"{value:.2f} {unit}"


def _event_headline(event_text, max_len=160):
    """Historical Context events are now full 2-4 sentence analytical entries,
    not one-line headlines — so when a snippet of one is quoted inline inside
    the Country Brief, only the first sentence (or a hard truncation as a
    fallback for a very long first sentence) is used, never the whole entry."""
    first_period = event_text.find(". ")
    if 20 < first_period < max_len:
        return event_text[:first_period]
    if first_period == -1 and len(event_text) <= max_len:
        return event_text.rstrip(".")
    return event_text[:max_len].rsplit(" ", 1)[0] + "…"


def build_country_brief(country_name, country_code, row, driver_row, events, conflicts):
    """Synthesizes score + trajectory + top historical events + conflict exposure
    into a flowing analyst-style paragraph that explains *why* the score is what
    it is and *where it's headed*, rather than stating disconnected facts."""
    parts = []

    score = row.get("risk_score")
    tier = row.get("risk_tier", "").lower()
    rank = row.get("risk_rank")
    n_countries = TOTAL_COUNTRIES
    if pd.notna(score):
        parts.append(
            f"{country_name} scores <b>{score:.1f}/100</b> on the composite index, placing it in the "
            f"<b>{tier}</b> tier and ranked <b>{int(rank)} of {n_countries}</b> tracked MENASA economies."
        )

    yoy = row.get("yoy_change")
    yoy_latest_year = row.get("yoy_latest_year")
    yoy_prior_year = row.get("yoy_prior_year")
    if pd.notna(yoy):
        if yoy > 1.5:
            traj = f"risk has <b>worsened by {yoy:.1f} points</b>"
        elif yoy < -1.5:
            traj = f"risk has <b>eased by {abs(yoy):.1f} points</b>"
        else:
            traj = f"risk has been <b>broadly stable ({yoy:+.1f} points)</b>"
        if pd.notna(yoy_latest_year) and pd.notna(yoy_prior_year):
            parts.append(
                f"Since {int(yoy_prior_year)}, {traj} — the trajectory matters as much as the "
                f"level, since a country moving deeper into a tier is a different story from one "
                f"that has simply always sat there."
            )

    factor_scores = {f: driver_row[f] for f in FACTOR_COLS if pd.notna(driver_row[f])}
    if factor_scores:
        sorted_factors = sorted(factor_scores.items(), key=lambda x: x[1], reverse=True)
        top_risk = FACTOR_LABELS[sorted_factors[0][0]]
        top_strength = FACTOR_LABELS[sorted_factors[-1][0]]
        link_clause = ""
        if events:
            most_recent = sorted(events, key=lambda e: e[0], reverse=True)[0]
            headline = _event_headline(most_recent[1])
            link_clause = (
                f" — consistent with {headline[0].lower()}{headline[1:]} ({most_recent[0]}), "
                f"which is still working through the economy"
            )
        parts.append(
            f"The single largest driver of that score is <b>{top_risk}</b>{link_clause}, while "
            f"<b>{top_strength}</b> stands out as its strongest relative pillar."
        )

    if events:
        recent_events = sorted(events, key=lambda e: e[0], reverse=True)[:2]
        event_phrases = [f"{_event_headline(e[1])[0].lower()}{_event_headline(e[1])[1:]} ({e[0]})" for e in recent_events]
        parts.append("Recent history has been shaped by " + " and ".join(event_phrases) + " — see Key Historical Context below for the full sourced timeline.")

    relevant_conflicts = [c["name"] for c in conflicts if country_code in c["affected"]]
    if relevant_conflicts:
        parts.append(
            f"It is directly exposed to the following live regional flashpoint(s), covered in more "
            f"depth in the Live Conflicts tab: <b>{', '.join(relevant_conflicts)}</b> — a channel of "
            f"risk this annual, backward-looking score cannot yet reflect."
        )
    else:
        parts.append(
            "It is not currently listed as directly exposed to any of the tracked regional flashpoints."
        )

    return " ".join(parts)


def build_regional_brief(scored_df, history_df, conflicts):
    """Synthesizes the current regional snapshot into an analyst-style paragraph:
    the spread, who's moved most and why, and how much of the region sits inside
    a live conflict this year's backward-looking score can't yet capture."""
    parts = []
    valid = scored_df.dropna(subset=["risk_score"])
    n = len(valid)
    avg = valid["risk_score"].mean()
    highest = valid.loc[valid["risk_score"].idxmax()]
    lowest = valid.loc[valid["risk_score"].idxmin()]
    higher_tier_n = (valid["risk_tier"] == "Higher Risk").sum()

    parts.append(
        f"Across the {n} tracked MENASA economies, the composite score averages <b>{avg:.1f}/100</b>, "
        f"spanning <b>{lowest['country']}</b> at {lowest['risk_score']:.1f} on the low end to "
        f"<b>{highest['country']}</b> at {highest['risk_score']:.1f} on the high end. "
        f"<b>{higher_tier_n} of {n}</b> economies currently sit in the Higher Risk tier."
    )

    yoy = valid.dropna(subset=["yoy_change"])
    if not yoy.empty:
        worsened = yoy.loc[yoy["yoy_change"].idxmax()]
        eased = yoy.loc[yoy["yoy_change"].idxmin()]
        if worsened["yoy_change"] > 1.5:
            sentence = (
                f"Year-over-year, <b>{worsened['country']}</b> has moved the most in the wrong "
                f"direction (+{worsened['yoy_change']:.1f} points)"
            )
            if eased["yoy_change"] < -1.5:
                sentence += (
                    f", while <b>{eased['country']}</b> has eased the most ({eased['yoy_change']:.1f} points) "
                    f"— a reminder that this composite moves in both directions, not just downward."
                )
            else:
                sentence += "."
            parts.append(sentence)

    exposed_codes = {code for c in conflicts for code in c["affected"]} & set(valid["country_code"])
    if exposed_codes:
        pct = 100 * len(exposed_codes) / n
        parts.append(
            f"<b>{len(exposed_codes)} of {n}</b> tracked economies ({pct:.0f}%) are directly listed as "
            f"exposed to at least one live regional flashpoint in the Live Conflicts tab below — exposure "
            f"this annual, World Bank-driven score structurally lags, since a conflict that started months "
            f"ago won't move a debt-to-GDP or governance figure until the next reporting cycle catches up."
        )

    return " ".join(parts)


def compute_year_factor_breakdown(long_df, country_code, year):
    """Cross-sectionally normalizes every tracked factor for a single year
    (mirroring compute_scores.py's own per-year methodology exactly, via the
    shared WEIGHTS/HIGHER_IS_RISKIER/normalize_to_risk_0_100 imports) and
    returns {factor: risk_score_0_100_or_None} for one country in that year.
    Used to explain what actually moved between two specific years, rather
    than just showing the composite score's net change."""
    year_slice = long_df[long_df["year"] == year]
    pivot = year_slice.pivot_table(index="country_code", columns="indicator", values="value", aggfunc="first")
    result = {}
    for factor in WEIGHTS:
        if factor not in pivot.columns or country_code not in pivot.index:
            result[factor] = None
            continue
        normalized = normalize_to_risk_0_100(pivot[factor], HIGHER_IS_RISKIER[factor])
        val = normalized.get(country_code)
        result[factor] = None if pd.isna(val) else val
    return result


def build_year_driver_card(long_df, country_code, country_name, year, prior_year):
    """Builds a human-readable explanation of which factors most drove the
    change in a country's composite score between prior_year and year,
    citing the actual raw World Bank figures behind each factor — not a
    generic statement, and not attributed to a data source (e.g. UNCTAD,
    ACLED) this tool doesn't actually pull from. Returns (html_summary, rows)
    where rows is a list of (label, prior_raw, current_raw, unit, risk_delta)
    sorted by absolute contribution to the score change."""
    current_scores = compute_year_factor_breakdown(long_df, country_code, year)
    prior_scores = compute_year_factor_breakdown(long_df, country_code, prior_year)

    raw_current = long_df[(long_df["country_code"] == country_code) & (long_df["year"] == year)].set_index("indicator")["value"]
    raw_prior = long_df[(long_df["country_code"] == country_code) & (long_df["year"] == prior_year)].set_index("indicator")["value"]

    rows = []
    for factor in WEIGHTS:
        cur, prior = current_scores.get(factor), prior_scores.get(factor)
        if cur is None or prior is None:
            continue
        risk_delta = (cur - prior) * WEIGHTS[factor]  # this factor's actual contribution to the composite's move
        label, unit, source = ALL_INDICATOR_LABELS[factor]
        rows.append((label, raw_prior.get(factor), raw_current.get(factor), unit, risk_delta, source))

    rows.sort(key=lambda r: abs(r[4]), reverse=True)

    if not rows:
        return (
            f"Not enough factor-level data is available for both {prior_year} and {year} to break down "
            f"what drove {country_name}'s score that year.",
            [],
        )

    top = rows[:3]
    sentences = []
    for label, prior_val, cur_val, unit, risk_delta, source in top:
        direction = "widened risk" if risk_delta > 0 else "eased risk"
        if pd.notna(prior_val) and pd.notna(cur_val):
            sentences.append(
                f"<b>{label}</b> moved from {_fmt_value_unit(prior_val, unit)} in {prior_year} "
                f"to {_fmt_value_unit(cur_val, unit)} in {year}, contributing "
                f"{abs(risk_delta):.2f} points of {direction} to the composite (source: {source})."
            )
    summary = (
        f"Comparing {country_name}'s reported factors in {prior_year} vs. {year}, the largest contributors "
        f"to the composite score's change were: " + " ".join(sentences)
    )
    return summary, rows


CURRENT_YEAR = datetime.now(timezone.utc).year


def compute_confidence_flag(row, factor_cols):
    """Evaluates ONLY this country's own reported data payload — how many of
    the 10 scored factors it reports, and how recent the least-current one is
    — into a plain confidence label. Never inferred by comparison to other
    countries. If debt-to-GDP specifically came from the IMF WEO fallback
    (tracked in the real debt_to_gdp_source column written by fetch_data.py)
    rather than the World Bank directly, that is named explicitly rather than
    folded silently into a generic "World Bank" claim."""
    factors_used = int(row.get("risk_score_factors_used", 0)) if pd.notna(row.get("risk_score_factors_used")) else 0
    years_reported = [int(row[f"{f}_year"]) for f in factor_cols if pd.notna(row.get(f"{f}_year"))]

    debt_note = ""
    if row.get("debt_to_gdp_source") == "IMF WEO (fallback)":
        debt_note = (
            " Debt-to-GDP specifically is sourced from the IMF World Economic Outlook fallback, "
            "since the World Bank has no figure on file for this country."
        )

    if not years_reported:
        return ("Low Confidence", "#f87171", "No factor-level data has been reported for any of the 10 scored indicators." + debt_note)

    oldest_year = min(years_reported)
    lag = CURRENT_YEAR - oldest_year

    if factors_used >= 9 and lag <= 2:
        return ("High Confidence", "#34d399", f"{factors_used} of 10 factors reported; the least-recent dates to {oldest_year}." + debt_note)
    if factors_used >= 6 and lag <= 4:
        return (
            "Medium Confidence", "#fbbf24",
            f"{factors_used} of 10 factors reported, but at least one dates back to {oldest_year} "
            f"({lag} years behind the current reporting cycle)." + debt_note,
        )
    return (
        "Low Confidence", "#f87171",
        f"Only {factors_used} of 10 factors reported, and/or reporting is stale (oldest: {oldest_year}, "
        f"{lag} years behind) — treat this score cautiously." + debt_note,
    )


def compute_shock_scenario(factor_scores, delta_current_account, delta_inflation, delta_political_stability):
    """Applies user-chosen shocks directly in RISK-SCORE POINTS (the same 0-100
    scale the radar chart and composite already use) to 3 of the 10 scored
    factors, then recomputes the composite with the identical missing-data-aware
    weighted average compute_scores.py uses. This is a transparent points-based
    stress test — it does NOT assert a real-world elasticity between (for
    example) a specific FDI collapse percentage and an inflation outcome; no
    institution publishes a precise mapping like that, so none is invented here.
    Returns None if none of the 3 shockable factors have a baseline score to
    shock in the first place."""
    shocked = dict(factor_scores)
    if "current_account_pct_gdp" in shocked:
        shocked["current_account_pct_gdp"] = min(100, shocked["current_account_pct_gdp"] + delta_current_account)
    if "inflation" in shocked:
        shocked["inflation"] = min(100, shocked["inflation"] + delta_inflation)
    if "political_stability" in shocked:
        shocked["political_stability"] = min(100, shocked["political_stability"] + delta_political_stability)

    if not shocked:
        return None
    available_weights = {f: WEIGHTS[f] for f in shocked}
    total_weight = sum(available_weights.values())
    if total_weight == 0:
        return None
    rescaled = {f: w / total_weight for f, w in available_weights.items()}
    return sum(shocked[f] * rescaled[f] for f in shocked)


# ============================================================
# DATA
# ============================================================
@st.cache_data(ttl=3600)
def load_data():
    """Loads the 4 data files the app is built on, cached for 1 hour so a
    slider drag or tab switch doesn't re-read them from disk on every rerun.
    The background GitHub Action overwrites these files at most nightly, so an
    hour-old cache is never meaningfully stale. Returns None for any file that
    is missing or unreadable rather than raising, so the caller can show a
    clear warning instead of an unhandled traceback."""
    frames = {}
    for key, filename in [
        ("scored", "scored_data.csv"),
        ("history", "scored_history.csv"),
        ("drivers", "driver_data.csv"),
        ("driver_history", "driver_history.csv"),
        ("long_df", "raw_data_long.csv"),
    ]:
        try:
            frames[key] = pd.read_csv(filename)
        except (FileNotFoundError, pd.errors.EmptyDataError, pd.errors.ParserError):
            frames[key] = None
    return frames


_data = load_data()
if any(df is None for df in _data.values()):
    _missing = [k for k, df in _data.items() if df is None]
    st.error(
        f"⚠️ Data files could not be loaded ({', '.join(_missing)} missing or unreadable). "
        "This usually means the background data refresh hasn't produced a valid file yet, or a "
        "file was corrupted mid-write. Please try again shortly, or check the GitHub Actions run "
        "log for the data pipeline.",
        icon="🚨",
    )
    st.stop()

scored, history, drivers, driver_history, long_df = (
    _data["scored"], _data["history"], _data["drivers"], _data["driver_history"], _data["long_df"]
)
TOTAL_COUNTRIES = len(scored)

REQUIRED_COLUMNS = {
    "scored": ["country", "country_code", "risk_score", "risk_tier", "risk_rank", "risk_score_factors_used"],
    "history": ["country", "country_code", "year", "risk_score"],
    "drivers": ["country", "country_code"],
    "driver_history": ["country_code", "year"],
    "long_df": ["country_code", "indicator", "year", "value"],
}
for _name, _df in [("scored", scored), ("history", history), ("drivers", drivers), ("driver_history", driver_history), ("long_df", long_df)]:
    _missing_cols = [c for c in REQUIRED_COLUMNS[_name] if c not in _df.columns]
    if _missing_cols:
        st.error(
            f"⚠️ {_name} data is missing expected column(s): {', '.join(_missing_cols)}. "
            "The data schema may have changed without the app being updated to match. "
            "Showing nothing further rather than risk a confusing partial page.",
            icon="🚨",
        )
        st.stop()

# Verified, working Yahoo Finance tickers for a country's benchmark stock
# index — NOT a guess for every country. Of all 27 tracked countries, only
# these were actually confirmed (via a live yfinance query, checked against
# the ticker's real longName/exchange/currency to rule out an unrelated stock
# accidentally sharing the same symbol) to return genuine, non-trivial
# historical price data. Every other country's exchange (Pakistan, Kuwait,
# Qatar, Jordan, Morocco, Bahrain, Sri Lanka, Oman, Bangladesh, Iraq, Tunisia,
# Egypt, and the rest) either has no public ticker on a free data provider or
# returned empty/single-point data, and is deliberately left out rather than
# shown with fabricated or unreliable coverage.
VERIFIED_STOCK_TICKERS = {
    "IND": ("^NSEI", "NIFTY 50"),
    "ISR": ("^TA125.TA", "TA-125"),
    "SAU": ("^TASI.SR", "TASI"),
}


@st.cache_data(ttl=3600)
def fetch_stock_history(ticker, period="1y"):
    """Fetches real historical closing-price data for a benchmark index via
    yfinance, cached for an hour. Returns None on any failure (network error,
    delisted symbol, empty response) rather than raising — a live market feed
    is one of the least reliable external dependencies this app has, so it
    must degrade to 'not available' rather than crash the page."""
    try:
        hist = yf.Ticker(ticker).history(period=period)
        if hist is None or hist.empty:
            return None
        # Yahoo Finance sometimes appends a trailing row for the current
        # (still in-progress or thinly-traded) session with a NaN Close —
        # drop it rather than let a "nan" leak into the displayed figure.
        hist = hist.dropna(subset=["Close"])
        return hist if not hist.empty else None
    except Exception:
        return None


# The actual span of years present in the data, not a hardcoded range that
# silently goes stale every time fetch_data.py picks up a new year — this
# is used everywhere the UI previously said the fixed string "2010-2024".
DATA_YEAR_RANGE = f"{int(long_df['year'].min())}-{int(long_df['year'].max())}"

# Real, well-known capital-city (plus a few other major metro) coordinates for
# the 27 tracked countries — orientation markers on the two geo maps, not a
# data layer. Standard, stable geographic facts, not something that needs a
# live source citation the way a statistic would.
# Capital/seat-of-government cities -- one per country, always shown with a
# visible text label. Kept separate from MAJOR_CITIES_SECONDARY below so the
# map can label only these by default; doubling every country's label count
# made the Gulf cluster unreadable and blew out the map's footprint on
# narrow/mobile viewports.
MAJOR_CITIES_PRIMARY = {
    "Algiers": (36.75, 3.06), "Cairo": (30.04, 31.24), "Tripoli": (32.89, 13.19),
    "Rabat": (34.02, -6.83), "Tunis": (36.81, 10.18), "Manama": (26.23, 50.59),
    "Kuwait City": (29.38, 47.99), "Muscat": (23.59, 58.41), "Doha": (25.29, 51.53),
    "Riyadh": (24.71, 46.68), "Jeddah": (21.54, 39.17), "Dubai": (25.20, 55.27),
    "Abu Dhabi": (24.45, 54.38), "Amman": (31.95, 35.93), "Beirut": (33.89, 35.50),
    "Damascus": (33.51, 36.29), "Baghdad": (33.31, 44.36), "Jerusalem": (31.78, 35.22),
    "Tel Aviv": (32.09, 34.78), "Gaza City": (31.50, 34.47), "Ramallah": (31.90, 35.20),
    "Tehran": (35.69, 51.39), "Sanaa": (15.37, 44.19), "Kabul": (34.56, 69.21),
    "Islamabad": (33.68, 73.05), "Karachi": (24.86, 67.00), "New Delhi": (28.61, 77.21),
    "Mumbai": (19.08, 72.88), "Dhaka": (23.81, 90.41), "Colombo": (6.93, 79.85),
    "Kathmandu": (27.72, 85.32), "Thimphu": (27.47, 89.64), "Male": (4.17, 73.51),
    "Ankara": (39.93, 32.86), "Khartoum": (15.60, 32.50), "Juba": (4.85, 31.58),
    "Addis Ababa": (9.04, 38.75), "Mogadishu": (2.04, 45.34), "Djibouti City": (11.59, 43.15),
    "Asmara": (15.34, 38.94),
}

# The second, leading commercial/port/population center per country that
# still needed one for ">1 major city per country" coverage -- shown as a
# small dot with the name available on hover only, not a permanent label, to
# keep the map legible instead of doubling every visible text label.
MAJOR_CITIES_SECONDARY = {
    "Oran": (35.70, -0.63), "Alexandria": (31.20, 29.92), "Benghazi": (32.12, 20.07),
    "Casablanca": (33.57, -7.59), "Sfax": (34.74, 10.76), "Muharraq": (26.26, 50.61),
    "Al Ahmadi": (29.08, 48.09), "Salalah": (17.02, 54.09), "Al Wakrah": (25.17, 51.60),
    "Aqaba": (29.53, 35.00), "Sidon": (33.56, 35.37), "Aleppo": (36.20, 37.16),
    "Basra": (30.51, 47.78), "Mashhad": (36.30, 59.61), "Aden": (12.78, 45.02),
    "Herat": (34.34, 62.19), "Chittagong": (22.36, 91.78), "Kandy": (7.29, 80.63),
    "Pokhara": (28.21, 83.99), "Phuntsholing": (26.85, 89.39), "Addu City": (-0.60, 73.08),
    "Istanbul": (41.01, 28.98), "Port Sudan": (19.60, 37.21), "Wau": (7.70, 28.00),
    "Mekelle": (13.50, 39.48), "Hargeisa": (9.56, 44.08), "Ali Sabieh": (11.15, 42.72),
    "Massawa": (15.61, 39.45),
}

# Named seas/gulfs shown as small italic water labels on every regional map,
# the same cartographic convention as the CFR Global Conflict Tracker and
# most professional atlases -- purely orientation, not a data layer.
SEA_LABELS = {
    "Mediterranean Sea": (34.5, 20.0), "Black Sea": (43.0, 35.0),
    "Caspian Sea": (41.5, 51.0), "Red Sea": (20.0, 38.0),
    "Persian Gulf": (26.5, 51.7), "Gulf of Oman": (24.3, 58.8),
    "Gulf of Aden": (12.3, 47.5), "Arabian Sea": (14.0, 65.0),
    "Bay of Bengal": (15.0, 88.0), "Indian Ocean": (-1.0, 72.0),
}

# Major container/energy ports and free-trade economic hubs, shown only on
# the Geo-Economic Interdependence trade map as its own toggleable layer --
# the physical infrastructure the chokepoints and trade arteries actually
# connect, distinct from the political/capital-city markers used elsewhere.
MAJOR_PORTS = {
    "Tanger Med (Morocco)": (35.88, -5.50),
    "Casablanca Port (Morocco)": (33.60, -7.62),
    "Port Said (Egypt)": (31.26, 32.30),
    "Ain Sokhna (Egypt)": (29.60, 32.31),
    "Beirut Port (Lebanon)": (33.90, 35.52),
    "Tripoli Port (Libya)": (32.90, 13.18),
    "Jeddah Islamic Port (Saudi Arabia)": (21.48, 39.17),
    "King Abdullah Port (Saudi Arabia)": (22.53, 39.03),
    "Jebel Ali (UAE)": (25.01, 55.06),
    "Khalifa Port (UAE)": (24.81, 54.65),
    "Hamad Port (Qatar)": (24.75, 51.60),
    "Salalah Port (Oman)": (17.02, 54.09),
    "Duqm Port (Oman)": (19.65, 57.70),
    "Bandar Abbas (Iran)": (27.15, 56.23),
    "Chabahar Port (Iran)": (25.29, 60.62),
    "Gwadar Port (Pakistan)": (25.13, 62.33),
    "Karachi Port (Pakistan)": (24.82, 66.98),
    "Mundra Port (India)": (22.84, 69.72),
    "Nhava Sheva / JNPT (India)": (18.95, 72.95),
    "Colombo Port (Sri Lanka)": (6.95, 79.84),
    "Hambantota Port (Sri Lanka)": (6.12, 81.12),
    "Chittagong Port (Bangladesh)": (22.33, 91.83),
}

# Shared basemap treatment for every regional map: near-black landmass (so
# untracked countries recede into the page background, CFR Global Conflict
# Tracker-style) with a lighter muted slate ocean, so whatever data layer is
# drawn on top -- choropleth fill, conflict markers, chokepoints -- is what
# the eye reads first.
MAP_BASE_STYLE = dict(
    showland=True, landcolor="#0d0d0d",
    showocean=True, oceancolor="#3f4757",
    showlakes=True, lakecolor="#3f4757",
    showcountries=True, countrycolor="rgba(226,232,240,0.45)",
    bgcolor="rgba(0,0,0,0)", showframe=False,
)


def sea_label_trace(lataxis_range=None, lonaxis_range=None):
    """Builds a go.Scattergeo text trace labeling named seas/gulfs, filtered
    to the visible lat/lon window so labels don't render off-canvas."""
    items = list(SEA_LABELS.items())
    if lataxis_range:
        items = [(n, (lat, lon)) for n, (lat, lon) in items if lataxis_range[0] <= lat <= lataxis_range[1]]
    if lonaxis_range:
        items = [(n, (lat, lon)) for n, (lat, lon) in items if lonaxis_range[0] <= lon <= lonaxis_range[1]]
    return go.Scattergeo(
        lat=[v[0] for _, v in items], lon=[v[1] for _, v in items],
        mode="text", text=[f"<i>{n}</i>" for n, _ in items],
        textfont=dict(size=10, color="rgba(226,232,240,0.55)", family="Georgia, serif"),
        hoverinfo="skip", showlegend=False,
    )

# Major rivers shown as thin background lines on every regional map, purely
# for cartographic orientation and visual realism -- like the sea labels,
# these are simplified illustrative waypoints (not a hydrologically precise
# trace) since the point is a recognizable river course at map-wide zoom,
# not surveyed geometry.
MAJOR_RIVERS = {
    "Nile": [(15.6, 32.5), (23.9, 32.9), (26.0, 32.7), (30.0, 31.2), (31.5, 30.8)],
    "Blue Nile": [(12.0, 37.3), (11.22, 35.09), (15.6, 32.5)],
    "Tigris": [(38.5, 39.7), (36.34, 43.13), (33.31, 44.36), (31.0, 47.4)],
    "Euphrates": [(39.0, 38.0), (35.95, 39.02), (35.34, 40.15), (33.42, 43.30), (31.0, 47.4)],
    "Indus": [(34.15, 78.0), (35.3, 75.6), (30.2, 71.5), (27.7, 68.86), (24.8, 67.3)],
}


def river_traces(lataxis_range=None, lonaxis_range=None):
    """Builds a (line, label) pair of go.Scattergeo traces tracing major
    regional rivers, filtered to rivers with at least one waypoint in the
    visible lat/lon window -- decorative geography, like sea_label_trace,
    not a data layer."""
    def _in_range(lat, lon):
        if lataxis_range and not (lataxis_range[0] <= lat <= lataxis_range[1]):
            return False
        if lonaxis_range and not (lonaxis_range[0] <= lon <= lonaxis_range[1]):
            return False
        return True

    lats, lons = [], []
    label_lats, label_lons, label_texts = [], [], []
    for name, points in MAJOR_RIVERS.items():
        if not any(_in_range(lat, lon) for lat, lon in points):
            continue
        if lats:
            lats.append(None)
            lons.append(None)
        for lat, lon in points:
            lats.append(lat)
            lons.append(lon)
        mid_lat, mid_lon = points[len(points) // 2]
        label_lats.append(mid_lat)
        label_lons.append(mid_lon)
        label_texts.append(name)

    line_trace = go.Scattergeo(
        lat=lats, lon=lons, mode="lines",
        line=dict(width=1.2, color="rgba(91,155,213,0.55)"),
        hoverinfo="skip", showlegend=False,
    )
    label_trace = go.Scattergeo(
        lat=label_lats, lon=label_lons, mode="text",
        text=[f"<i>{n}</i>" for n in label_texts],
        textfont=dict(size=9, color="rgba(91,155,213,0.75)", family="Georgia, serif"),
        hoverinfo="skip", showlegend=False,
    )
    return line_trace, label_trace


FACTOR_LABELS = {
    "debt_to_gdp": "Debt (% GDP)",
    "current_account_pct_gdp": "Current Account",
    "reserves_months_imports": "Reserves Cover",
    "gdp_growth": "GDP Growth",
    "inflation": "Inflation",
    "political_stability": "Political Stability",
    "government_effectiveness": "Govt. Effectiveness",
    "rule_of_law": "Rule of Law",
    "regulatory_quality": "Regulatory Quality",
    "control_of_corruption": "Control of Corruption",
}
FACTOR_COLS = list(FACTOR_LABELS.keys())
# Matches compute_scores.py's WEIGHTS exactly -- the default composite is an
# equal-weighted average of all 10 factors, 10% each.
WEIGHTS = {f: 0.10 for f in FACTOR_COLS}


def compute_yoy_attribution(country_code, driver_history_df, latest_year, prior_year):
    """Decomposes a country's year-over-year composite score change into each
    factor's exact point contribution. This is exact, not approximate: since
    the composite is a weighted sum of normalized 0-100 sub-scores, the total
    change is exactly the sum of each factor's (this year's weight x sub-score)
    minus (last year's weight x sub-score) -- rescaled per year the same way
    compute_scores.py rescales weights among whichever factors are non-null
    that year. Returns None if either year is missing from driver_history_df."""
    rows = driver_history_df[driver_history_df["country_code"] == country_code]
    latest_row = rows[rows["year"] == latest_year]
    prior_row = rows[rows["year"] == prior_year]
    if latest_row.empty or prior_row.empty:
        return None
    latest_row, prior_row = latest_row.iloc[0], prior_row.iloc[0]

    def _rescaled_weights(row):
        available = [f for f in FACTOR_COLS if pd.notna(row[f])]
        total = sum(WEIGHTS[f] for f in available)
        return {f: (WEIGHTS[f] / total if total > 0 else 0) for f in available}

    latest_w, prior_w = _rescaled_weights(latest_row), _rescaled_weights(prior_row)
    contributions = []
    for f in FACTOR_COLS:
        latest_term = latest_w.get(f, 0) * latest_row[f] if f in latest_w else 0
        prior_term = prior_w.get(f, 0) * prior_row[f] if f in prior_w else 0
        contributions.append((f, round(latest_term - prior_term, 2)))
    return contributions

RAW_LABELS = {
    "debt_to_gdp": ("Debt to GDP", "%"),
    "current_account_pct_gdp": ("Current Account", "% GDP"),
    "reserves_months_imports": ("Reserves Cover", "months of imports"),
    "gdp_growth": ("GDP Growth", "%"),
    "inflation": ("Inflation", "%"),
    "political_stability": ("Political Stability", "WGI estimate, -2.5 to +2.5"),
    "government_effectiveness": ("Govt. Effectiveness", "WGI estimate, -2.5 to +2.5"),
    "rule_of_law": ("Rule of Law", "WGI estimate, -2.5 to +2.5"),
    "regulatory_quality": ("Regulatory Quality", "WGI estimate, -2.5 to +2.5"),
    "control_of_corruption": ("Control of Corruption", "WGI estimate, -2.5 to +2.5"),
}

# All 13 tracked indicators (the 10 scored factors plus the 3 descriptive
# trade/investment-context indicators), each mapped to a clean display label,
# its real unit, and its ACTUAL source — used by the sub-indicator trend
# dropdown below the radar chart. Every one of these is a genuine World Bank
# WDI or WGI series already being fetched by fetch_data.py; nothing here is
# attributed to a data feed the app doesn't actually pull from.
ALL_INDICATOR_LABELS = {
    "debt_to_gdp": ("Debt (% of GDP)", "%", "World Bank WDI: GC.DOD.TOTL.GD.ZS"),
    "current_account_pct_gdp": ("Current Account (% of GDP)", "% GDP", "World Bank WDI: BN.CAB.XOKA.GD.ZS"),
    "reserves_months_imports": ("Reserves Cover", "months of imports", "World Bank WDI: FI.RES.TOTL.MO"),
    "gdp_growth": ("GDP Growth Rate", "%", "World Bank WDI: NY.GDP.MKTP.KD.ZG"),
    "inflation": ("Inflation", "%", "World Bank WDI: FP.CPI.TOTL.ZG"),
    "political_stability": ("Political Stability & Absence of Violence", "WGI estimate, -2.5 to +2.5", "World Bank WGI: PV.EST"),
    "government_effectiveness": ("Government Effectiveness", "WGI estimate, -2.5 to +2.5", "World Bank WGI: GE.EST"),
    "rule_of_law": ("Rule of Law", "WGI estimate, -2.5 to +2.5", "World Bank WGI: RL.EST"),
    "regulatory_quality": ("Regulatory Quality", "WGI estimate, -2.5 to +2.5", "World Bank WGI: RQ.EST"),
    "control_of_corruption": ("Control of Corruption", "WGI estimate, -2.5 to +2.5", "World Bank WGI: CC.EST"),
    "fdi_net_inflows_pct_gdp": ("Foreign Direct Investment, Net Inflows", "% GDP", "World Bank WDI: BX.KLT.DINV.WD.GD.ZS"),
    "exports_pct_gdp": ("Exports of Goods & Services", "% GDP", "World Bank WDI: NE.EXP.GNFS.ZS"),
    "imports_pct_gdp": ("Imports of Goods & Services", "% GDP", "World Bank WDI: NE.IMP.GNFS.ZS"),
    "gdp_current_usd": ("GDP (Current US$)", "USD", "World Bank WDI: NY.GDP.MKTP.CD"),
    "gdp_per_capita_usd": ("GDP Per Capita (Current US$)", "USD", "World Bank WDI: NY.GDP.PCAP.CD"),
    "total_reserves_usd": ("Total Reserves (Current US$)", "USD", "World Bank WDI: FI.RES.TOTL.CD"),
    "unemployment_rate": ("Unemployment Rate", "%", "World Bank WDI: SL.UEM.TOTL.ZS"),
    "youth_unemployment_rate": ("Youth Unemployment Rate", "%", "World Bank WDI: SL.UEM.1524.ZS"),
    "gini_index": ("Gini Index (Income Inequality)", "index, 0-100", "World Bank WDI: SI.POV.GINI"),
}


def clean_label(raw_key):
    """Defensive fallback: turns a raw snake_case column/indicator key into a
    clean, title-cased display string, for any identifier that reaches the UI
    without an explicit entry in FACTOR_LABELS / ALL_INDICATOR_LABELS. No
    backend column name should ever reach the rendered page verbatim."""
    return raw_key.replace("_", " ").replace("pct", "%").strip().title()


_YEAR_RE = re.compile(r"(19|20)\d{2}")


def _latest_year_in_text(text):
    """Extracts the most recent 4-digit year mentioned in a free-text date/
    period field (e.g. 'December 2022; expanded March 2024' -> 2024,
    '2018-present' -> 2018). Used to sort date-ish lists (Financing
    Arrangements, Economic Sanctions) most-recent-first even though the
    underlying field is free text, not a clean structured date. Returns -1
    (sorts to the bottom of a descending sort) if no year is found, e.g. an
    'N/A' period on a country with no sanctions history."""
    years = [int(m.group()) for m in _YEAR_RE.finditer(text or "")]
    return max(years) if years else -1


def _paragraph_to_bullets(text):
    """Splits a long analyst-style paragraph into sentence-level bullets, so
    a dense wall of prose (e.g. Key Economic Partners) reads as a scannable
    list instead. A '. '/'? '/'! ' boundary split is reliable for this app's
    own written content, which consistently spells out abbreviations (e.g.
    "United States", not "U.S.") rather than using periods mid-sentence."""
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    return [s.strip() for s in sentences if s.strip()]


try:
    with open("last_refreshed.txt") as f:
        LAST_REFRESHED = f.read().strip()
except FileNotFoundError:
    LAST_REFRESHED = "unknown"

# ============================================================
# MASTHEAD
# ============================================================
st.markdown('<div class="tag-label">Risk, Conflict &amp; Trade Intelligence · Full MENASA Coverage</div>', unsafe_allow_html=True)
st.markdown('<div class="masthead-title">MENASA <span>Risk Monitor</span></div>', unsafe_allow_html=True)
st.markdown(
    '<div class="masthead-sub">A composite sovereign risk score for all 34 MENA, South Asia &amp; Horn of Africa economies, '
    'built on live World Bank data across 10 factors spanning economic and governance pillars — paired with '
    'a sourced Live Conflicts tracker, a 4-country Compare tool, and a Geo-Economic Interdependence Dashboard '
    'mapping the region\'s maritime chokepoints, critical-mineral concentration, and commodity markets.</div>',
    unsafe_allow_html=True,
)
st.markdown(
    f'<div style="font-size:0.85rem;color:{TEXT_MUTED};max-width:660px;line-height:1.6;margin-bottom:1rem;'
    f'border-left:2px solid {BORDER};padding-left:0.9rem;">'
    f'Built to turn multilateral-finance research experience (IMF, World Bank) into a reproducible, '
    f'sourced quantitative tool rather than a one-off writeup.</div>',
    unsafe_allow_html=True,
)
st.markdown(f'<div class="stat-sub" style="margin-bottom:1.2rem;">Data last refreshed: {LAST_REFRESHED}</div>', unsafe_allow_html=True)

# ---- System status banner ----
# A genuine status readout, not decoration: it reports the real last-refreshed
# date written by fetch_data.py and flags plainly if the automated pipeline
# looks stalled (>10 days since a scheduled nightly run should have landed),
# rather than always claiming "live" regardless of actual pipeline health.
try:
    _refresh_date = datetime.strptime(LAST_REFRESHED, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    _days_stale = (datetime.now(timezone.utc) - _refresh_date).days
except ValueError:
    _days_stale = None

if _days_stale is None:
    _status_text, _status_color = "Refresh timestamp unavailable", TEXT_MUTED
elif _days_stale <= 2:
    _status_text, _status_color = f"Live Data Pipeline Connected · Synced {_days_stale}d ago", "#34d399"
elif _days_stale <= 10:
    _status_text, _status_color = f"Source Sync Active · Last run {_days_stale}d ago", "#fbbf24"
else:
    _status_text, _status_color = f"Pipeline May Be Stalled · Last run {_days_stale}d ago", "#f87171"

st.markdown(
    f'<div style="display:inline-flex;align-items:center;gap:0.9rem;font-family:\'JetBrains Mono\',monospace;'
    f'font-size:0.74rem;background:rgba(148,163,184,0.06);border:1px solid {BORDER};'
    f'border-radius:20px;padding:0.4rem 1.1rem;margin-bottom:1rem;">'
    f'<span style="color:{_status_color};">● Live data — {_status_text}</span>'
    f'<span style="width:1px;height:0.85rem;background:{BORDER};display:inline-block;"></span>'
    f'<span style="color:{ACCENT2};">● Curated context — not a live feed</span>'
    f'</div>',
    unsafe_allow_html=True,
)

# ============================================================
# AT A GLANCE — a compact strip-plot of all 27 scores, so there's a real
# visual before the first scroll instead of only stat cards and text.
# ============================================================
valid_scores_preview = scored.dropna(subset=["risk_score"])
if not valid_scores_preview.empty:
    st.markdown('<div class="section-tag" style="margin-top:0.2rem;">At A Glance</div>', unsafe_allow_html=True)
    fig_glance = go.Figure()
    for tier, tier_color in TIER_COLORS.items():
        sub = valid_scores_preview[valid_scores_preview["risk_tier"] == tier]
        if sub.empty:
            continue
        fig_glance.add_trace(go.Scatter(
            x=sub["risk_score"], y=[0] * len(sub), mode="markers",
            marker=dict(size=11, color=tier_color, line=dict(width=1, color=BG)),
            text=sub["country"], hovertemplate="<b>%{text}</b>: %{x:.1f}<extra></extra>",
            name=tier,
        ))
    fig_glance.update_layout(
        height=150, margin=dict(t=6, b=60, l=8, r=8),
        xaxis=dict(range=[0, 100], showgrid=False, zeroline=False, tickfont=dict(size=9, color=TEXT_MUTED),
                   title=dict(text="Composite Score (0–100)", font=dict(size=9, color=TEXT_MUTED), standoff=6)),
        yaxis=dict(visible=False, range=[-1, 1]),
        showlegend=True,
        legend=dict(orientation="h", y=-0.75, font=dict(size=9, color=TEXT_MUTED), bgcolor="rgba(0,0,0,0)"),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="JetBrains Mono, monospace"),
    )
    st.plotly_chart(fig_glance, use_container_width=True, config={"displayModeBar": False})

# ============================================================
# TOP-LINE STAT ROW
# ============================================================
valid_scores = scored.dropna(subset=["risk_score"])
highest = valid_scores.iloc[0]
lowest = valid_scores.sort_values("risk_score").iloc[0]

c1, c2, c3, c4 = st.columns(4)
with c1:
    stat_card("Countries Covered", len(scored), "MENA, South Asia & Horn of Africa", accent=ACCENT2)
with c2:
    stat_card("Highest Risk", highest["country"], f"Score {highest['risk_score']:.1f}")
with c3:
    stat_card("Lowest Risk", lowest["country"], f"Score {lowest['risk_score']:.1f}")
with c4:
    stat_card("Regional Average", f"{valid_scores['risk_score'].mean():.1f}", f"Across all {len(scored)}", accent=ACCENT2)

st.markdown(
    f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:0.72rem;color:{TEXT_MUTED};margin-top:0.6rem;">'
    f'Scores are ranked relative to this 34-country MENASA set, not a globally benchmarked index — '
    f'see Methodology.</div>',
    unsafe_allow_html=True,
)

st.markdown("<br>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
    ["Regional Overview", "Country Deep Dive", "Compare Countries", "Live Conflicts",
     "Geo-Economic Interdependence", "Scenario Explorer", "Methodology"]
)

# ================= TAB 1: OVERVIEW =================
with tab1:
    st.markdown('<div class="section-tag">Analyst Brief</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Regional Snapshot</div>', unsafe_allow_html=True)
    regional_brief_text = build_regional_brief(scored, history, LIVE_CONFLICTS)
    st.markdown(f'<div class="narrative-box">{regional_brief_text}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-tag">Geographic Distribution</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Risk Map</div>', unsafe_allow_html=True)

    _hist_years = sorted(history["year"].unique())
    _latest_hist_year = _hist_years[-1]
    selected_map_year = st.select_slider(
        "Year", options=_hist_years, value=_latest_hist_year, key="risk_map_year",
    )
    _is_latest_year = selected_map_year == _latest_hist_year

    if _is_latest_year:
        # The current snapshot (scored_data.csv) can be a few weeks fresher
        # than the last "both pillars reported" year in scored_history.csv,
        # so the latest slider position uses the real current data rather
        # than re-deriving it from history and showing something stale.
        map_df = scored.dropna(subset=["risk_score"]).reset_index(drop=True)
    else:
        map_df = history[history["year"] == selected_map_year].dropna(subset=["risk_score"]).reset_index(drop=True)
        # scored_history.csv doesn't carry a precomputed tier -- bucket it
        # here with the same 33/66 thresholds used everywhere else in the app,
        # purely for the hover tooltip; the color scale itself is continuous
        # and needs no bucketing.
        map_df["risk_tier"] = map_df["risk_score"].apply(
            lambda s: "Higher Risk" if s > 66 else ("Moderate Risk" if s >= 33 else "Lower Risk")
        )
    st.caption(
        f"Showing {'the latest available' if _is_latest_year else int(selected_map_year)} composite scores. "
        f"Drag the slider to see how regional risk evolved from 2010 to {int(_latest_hist_year)}. Earlier years "
        "may show fewer than 34 countries if a country hadn't reported both pillars (economic + governance) "
        "that year — this map never fills a gap with an invented value."
    )

    map_fig = px.choropleth(
        map_df, locations="country_code", locationmode="ISO-3", color="risk_score",
        hover_name="country", hover_data={"country_code": False, "risk_score": ":.1f", "risk_tier": True},
        color_continuous_scale=["#34d399", "#fbbf24", "#f87171"], range_color=(0, 100),
        labels={"risk_score": "Risk Score", "risk_tier": "Risk Tier"},
    )
    # A full-size default colorbar reserves a large, fixed chunk of the
    # figure's width for its title/ticks regardless of container width --
    # on a narrow/mobile viewport that leaves the actual map squeezed into a
    # sliver. A slimmer, shorter bar keeps the map itself the dominant element
    # at any width.
    map_fig.update_coloraxes(colorbar=dict(
        thickness=12, len=0.6, tickfont=dict(size=9, color=TEXT_MUTED),
        title=dict(font=dict(size=10, color=TEXT_MUTED)),
    ))
    _ov_lat_range, _ov_lon_range = [-5, 42], [-12, 100]
    map_fig.update_geos(
        scope="world", lataxis_range=_ov_lat_range, lonaxis_range=_ov_lon_range,
        # The data-driven choropleth fill above this basemap -- the actual
        # analytical layer -- is what the eye reads; untracked countries
        # recede into the near-black landmass so the 27 scored ones pop.
        **MAP_BASE_STYLE,
    )
    map_fig.add_trace(sea_label_trace(_ov_lat_range, _ov_lon_range))
    for _t in river_traces(_ov_lat_range, _ov_lon_range):
        map_fig.add_trace(_t)
    # Capital cities get a small labeled dot for geographic orientation; the
    # second/secondary city per country gets a dot only, name on hover --
    # labeling all 54 cities made the Gulf cluster unreadable and blew out
    # the map's footprint on narrow viewports.
    _city_positions = ["top center", "bottom center", "middle right", "middle left"]
    primary_names = list(MAJOR_CITIES_PRIMARY.keys())
    map_fig.add_trace(go.Scattergeo(
        lat=[c[0] for c in MAJOR_CITIES_PRIMARY.values()], lon=[c[1] for c in MAJOR_CITIES_PRIMARY.values()],
        mode="markers+text",
        marker=dict(size=4, color="rgba(245,245,244,0.9)", line=dict(width=0.5, color="rgba(10,14,20,0.7)")),
        text=primary_names, textposition=[_city_positions[i % 4] for i in range(len(primary_names))],
        textfont=dict(size=8, color="#f5f5f4"),
        hoverinfo="text", showlegend=False,
    ))
    map_fig.add_trace(go.Scattergeo(
        lat=[c[0] for c in MAJOR_CITIES_SECONDARY.values()], lon=[c[1] for c in MAJOR_CITIES_SECONDARY.values()],
        mode="markers", text=list(MAJOR_CITIES_SECONDARY.keys()),
        marker=dict(size=3.5, color="rgba(230,237,243,0.45)", line=dict(width=0.5, color="rgba(10,14,20,0.6)")),
        hoverinfo="text", showlegend=False,
    ))
    map_fig.update_layout(margin=dict(t=10, b=10, l=10, r=10))
    risk_map_click = st.plotly_chart(
        style_chart(map_fig, height=420), use_container_width=True,
        on_select="rerun", selection_mode="points", key="risk_map_select",
    )
    st.caption(
        "Click a country to pre-select it in the Country Deep Dive tab above — small gray dots "
        "mark major cities for geographic orientation only, not a data layer."
    )
    if risk_map_click and risk_map_click.selection and risk_map_click.selection.get("point_indices"):
        clicked_idx = risk_map_click.selection["point_indices"][0]
        if clicked_idx < len(map_df):
            st.session_state["selected_country_from_map"] = map_df.iloc[clicked_idx]["country"]

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(f'<div class="section-tag">All {len(scored)} Ranked</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Risk Ranking</div>', unsafe_allow_html=True)
        chart_df = scored.dropna(subset=["risk_score"]).sort_values("risk_score", ascending=True)
        fig = px.bar(
            chart_df, x="risk_score", y="country", orientation="h",
            color="risk_tier", color_discrete_map=TIER_COLORS, text="risk_score",
            labels={"risk_score": "Risk Score (0-100)", "country": ""},
            custom_data=["country"],
        )
        fig.update_traces(texttemplate="%{text:.1f}", textposition="outside")
        fig.update_layout(showlegend=True, legend_title_text="")
        # A fixed height starves the y-axis of room per country as the tracked
        # set grows -- Plotly then silently thins out tick labels rather than
        # overlapping them, so bars for every country still render but some
        # names go missing. Scaling with the row count keeps one label per bar
        # regardless of how many countries are tracked.
        rank_click = st.plotly_chart(
            style_chart(fig, height=max(560, 22 * len(chart_df))), use_container_width=True,
            on_select="rerun", selection_mode="points", key="risk_rank_select",
        )
        st.caption("Click a bar to pre-select that country in the Country Deep Dive tab above.")
        if rank_click and rank_click.selection and rank_click.selection.get("points"):
            # color="risk_tier" splits this bar chart into one trace per tier,
            # so a raw point_indices lookup against chart_df would silently
            # index into the wrong tier's rows -- explicit customdata (same
            # mechanism as the Geo-Economic map's click handler) sidesteps the
            # multi-trace indexing mismatch entirely, rather than guessing at
            # an undocumented "y" key in Streamlit's selection payload.
            rank_cd = rank_click.selection["points"][0].get("customdata")
            if rank_cd:
                st.session_state["selected_country_from_map"] = rank_cd[0]

    with col2:
        with st.container(border=True):
            st.markdown('<div class="section-tag">Legend</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-title" style="font-size:1rem;">Reading the Scores</div>', unsafe_allow_html=True)
            st.markdown(tier_badge_html("Lower Risk") + " score &lt; 33", unsafe_allow_html=True)
            st.markdown("<br>" + tier_badge_html("Moderate Risk") + " score 33–66", unsafe_allow_html=True)
            st.markdown("<br>" + tier_badge_html("Higher Risk") + " score &gt; 66", unsafe_allow_html=True)
            st.markdown("<br>" + tier_badge_html("Insufficient data") + " &lt; 2 of 10 factors", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        with st.container(border=True):
            st.markdown('<div class="section-tag">By Subregion</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-title" style="font-size:1rem;">Regional Snapshot</div>', unsafe_allow_html=True)
            gulf = scored[scored["country_code"].isin(["SAU", "ARE", "KWT", "QAT", "BHR", "OMN"])]["risk_score"].mean()
            north_africa = scored[scored["country_code"].isin(["DZA", "EGY", "LBY", "MAR", "TUN"])]["risk_score"].mean()
            levant_iraq = scored[scored["country_code"].isin(["JOR", "LBN", "SYR", "ISR", "IRQ", "PSE"])]["risk_score"].mean()
            iran_yemen = scored[scored["country_code"].isin(["IRN", "YEM"])]["risk_score"].mean()
            south_asia = scored[scored["country_code"].isin(["PAK", "BGD", "LKA", "IND", "AFG", "BTN", "MDV", "NPL"])]["risk_score"].mean()
            custom_table(
                [
                    ["Gulf (GCC)", f"{gulf:.1f}"],
                    ["North Africa", f"{north_africa:.1f}"],
                    ["Levant & Iraq", f"{levant_iraq:.1f}"],
                    ["Iran & Yemen", f"{iran_yemen:.1f}"],
                    ["South Asia", f"{south_asia:.1f}"],
                ],
                ["Sub-Region", "Avg. Score"],
            )

        st.markdown("<br>", unsafe_allow_html=True)
        st.info(
            "Iran's score is based on only 7 of 10 factors — debt, current account, and reserves "
            "data are not consistently reported to the World Bank, likely due to sanctions. "
            "Treat that score as lower-confidence.",
            icon="⚠️",
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f'<div class="section-tag">{DATA_YEAR_RANGE}</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Historical Trend</div>', unsafe_allow_html=True)
    trend_countries = st.multiselect(
        "Compare countries over time",
        options=sorted(scored["country"].tolist()),
        default=["Pakistan", "Lebanon", "UAE", "Egypt"],
        label_visibility="collapsed",
    )
    if trend_countries:
        trend_df = history[history["country"].isin(trend_countries)]
        fig2 = px.line(
            trend_df.sort_values("year"), x="year", y="risk_score", color="country",
            markers=True, labels={"risk_score": "Risk Score", "year": "Year"},
            color_discrete_sequence=[ACCENT, "#f87171", "#fbbf24", "#34d399", "#a78bfa", "#fb923c"],
        )
        st.plotly_chart(style_chart(fig2), use_container_width=True)
    else:
        st.caption("Select at least one country to see its risk trend over time.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-tag">Head-to-Head</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Peer Benchmarking Matrix</div>', unsafe_allow_html=True)
    st.markdown(
        "Select two or more countries for a direct side-by-side comparison of composite risk, "
        "latest reported GDP growth, and live conflict exposure."
    )
    peer_countries = st.multiselect(
        "Compare countries head-to-head",
        options=sorted(scored["country"].tolist()),
        default=["Pakistan", "India", "Bangladesh"],
        label_visibility="collapsed",
        key="peer_benchmark_select",
    )
    if len(peer_countries) >= 2:
        peer_rows = []
        for name in peer_countries:
            prow = scored[scored["country"] == name].iloc[0]
            pcode = prow["country_code"]
            gdp_val, gdp_year = prow.get("gdp_growth"), prow.get("gdp_growth_year")
            gdp_display = f"{gdp_val:.1f}% ({int(gdp_year)})" if pd.notna(gdp_val) and pd.notna(gdp_year) else "No data"
            exposed = [c["name"] for c in LIVE_CONFLICTS if pcode in c["affected"]]
            peer_rows.append({
                "Country": name,
                "Composite Score": f"{prow['risk_score']:.1f}" if pd.notna(prow["risk_score"]) else "N/A",
                "Risk Tier": prow["risk_tier"],
                "Regional Rank": f"{int(prow['risk_rank'])} / {len(scored)}" if pd.notna(prow["risk_rank"]) else "N/A",
                "GDP Growth": gdp_display,
                "Active Conflicts": len(exposed),
                "Conflict(s)": ", ".join(exposed) if exposed else "None tracked",
            })
        st.dataframe(pd.DataFrame(peer_rows), use_container_width=True, hide_index=True)
    else:
        st.caption("Select at least two countries above to compare.")

# ================= TAB 2: COUNTRY DEEP DIVE =================
with tab2:
    country_list = scored.sort_values("country")["country"].tolist()
    # Honors a click on the Risk Map (Tab 1) — Streamlit can't force-switch
    # the active tab from a chart click, so this is the honest equivalent:
    # the country is already pre-selected by the time the user clicks over.
    _map_selected_country = st.session_state.get("selected_country_from_map")
    _default_index = country_list.index(_map_selected_country) if _map_selected_country in country_list else 0
    selected = st.selectbox("Select a country", country_list, index=_default_index, label_visibility="collapsed")

    row = scored[scored["country"] == selected].iloc[0]
    driver_row = drivers[drivers["country"] == selected].iloc[0]
    country_code = row["country_code"]
    events = HISTORICAL_CONTEXT.get(country_code, [])

    st.markdown('<div class="section-tag">Analyst Brief</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Country Brief</div>', unsafe_allow_html=True)
    brief_text = build_country_brief(selected, country_code, row, driver_row, events, LIVE_CONFLICTS)
    st.markdown(f'<div class="narrative-box">{brief_text}</div>', unsafe_allow_html=True)

    _factor_scores_for_pdf = {f: driver_row[f] for f in FACTOR_COLS if pd.notna(driver_row[f])}
    _top_risk_factors_for_pdf = [
        (FACTOR_LABELS[f], v) for f, v in sorted(_factor_scores_for_pdf.items(), key=lambda x: x[1], reverse=True)[:3]
    ]
    _conf_label_pdf, _, _conf_detail_pdf = compute_confidence_flag(row, FACTOR_COLS)

    pdf_bytes = generate_country_pdf(
        country_name=selected,
        country_code=country_code,
        row=row.to_dict(),
        brief_text=brief_text,
        ratings=CREDIT_RATINGS.get(country_code),
        trade_profile=COUNTRY_TRADE_PROFILE.get(country_code),
        events=events,
        arrangements=FINANCING_ARRANGEMENTS.get(country_code),
        partner_info=KEY_ECONOMIC_PARTNERS.get(country_code),
        last_refreshed=LAST_REFRESHED,
        top_risk_factors=_top_risk_factors_for_pdf,
        confidence=(_conf_label_pdf, _conf_detail_pdf),
    )
    st.download_button(
        label=f"📄 Generate Executive Report — {selected} (PDF)",
        data=pdf_bytes,
        file_name=f"{selected.replace(' ', '_')}_Sovereign_Risk_Brief.pdf",
        mime="application/pdf",
    )
    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns([1, 2])
    with c1:
        with st.container(border=True):
            st.markdown('<div class="section-tag">Composite Score</div>', unsafe_allow_html=True)
            score_display = f"{row['risk_score']:.1f}" if pd.notna(row["risk_score"]) else "N/A"
            st.markdown(f'<div class="stat-value" style="font-size:2.1rem;">{score_display}</div>', unsafe_allow_html=True)
            st.markdown(tier_badge_html(row["risk_tier"]), unsafe_allow_html=True)
            st.caption(f"Based on {int(row['risk_score_factors_used'])} of 10 factors")

            rank_col, yoy_col = st.columns(2)
            with rank_col:
                st.markdown(
                    f'<div class="stat-label" style="margin-top:0.6rem;">Regional Rank</div>'
                    f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:1.1rem;color:{ACCENT};">'
                    f'{int(row["risk_rank"])} / {len(scored)}</div>',
                    unsafe_allow_html=True,
                )
            with yoy_col:
                if pd.notna(row.get("yoy_change")):
                    yoy = row["yoy_change"]
                    arrow = "▲" if yoy > 0 else ("▼" if yoy < 0 else "—")
                    color = "#f87171" if yoy > 0 else ("#34d399" if yoy < 0 else TEXT_MUTED)
                    st.markdown(
                        f'<div class="stat-label" style="margin-top:0.6rem;">vs {int(row["yoy_prior_year"])}</div>'
                        f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:1.1rem;color:{color};">'
                        f'{arrow} {abs(yoy):.1f}</div>',
                        unsafe_allow_html=True,
                    )

            conf_label, conf_color, conf_detail = compute_confidence_flag(row, FACTOR_COLS)
            st.markdown(
                f'<div class="stat-label" style="margin-top:0.9rem;">Data Integrity</div>'
                f'<span class="tier-badge" style="background:{conf_color}22;color:{conf_color};">{conf_label}</span>',
                unsafe_allow_html=True,
            )
            st.caption(conf_detail)

        st.markdown("<br>", unsafe_allow_html=True)

        with st.container(border=True):
            st.markdown('<div class="section-tag">Sanity Check</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-title" style="font-size:1.05rem;">Actual Credit Ratings</div>', unsafe_allow_html=True)
            ratings = CREDIT_RATINGS.get(country_code)
            if ratings:
                custom_table(
                    [["S&P", ratings["sp"]], ["Moody's", ratings["moodys"]], ["Fitch", ratings["fitch"]]],
                    ["Agency", "Rating"],
                )
                st.caption(
                    "How this tool's own score compares to the real rating agencies — a way to "
                    "sanity-check the composite model against independent professional assessments. "
                    "'Not Rated' means no widely reported rating from these three agencies, common for "
                    "countries without international bond market access."
                )
            else:
                st.caption("No rating data on file.")

        st.markdown("<br>", unsafe_allow_html=True)

        factor_scores = {f: driver_row[f] for f in FACTOR_COLS if pd.notna(driver_row[f])}
        if factor_scores:
            sorted_factors = sorted(factor_scores.items(), key=lambda x: x[1], reverse=True)
            top_risks = sorted_factors[:2]
            top_strength = sorted_factors[-1]
            risk_names = " and ".join(FACTOR_LABELS[f] for f, v in top_risks)
            strength_name = FACTOR_LABELS[top_strength[0]]
            st.markdown(
                f'<div class="narrative-box"><b>Key Drivers</b><br>{selected}\'s risk profile is driven '
                f'primarily by <b>{risk_names}</b>, while <b>{strength_name}</b> is a relative strength.</div>',
                unsafe_allow_html=True,
            )

        if pd.notna(row.get("yoy_change")) and pd.notna(row.get("yoy_latest_year")) and pd.notna(row.get("yoy_prior_year")):
            attribution = compute_yoy_attribution(
                country_code, driver_history, int(row["yoy_latest_year"]), int(row["yoy_prior_year"])
            )
            if attribution:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(
                    f'<div class="section-tag">{int(row["yoy_prior_year"])} → {int(row["yoy_latest_year"])}</div>',
                    unsafe_allow_html=True,
                )
                st.markdown('<div class="section-title" style="font-size:1rem;">What Drove the Change, Point by Point</div>', unsafe_allow_html=True)
                attr_sorted = sorted(attribution, key=lambda x: x[1], reverse=True)
                attr_labels = [FACTOR_LABELS[f] for f, v in attr_sorted]
                attr_values = [v for f, v in attr_sorted]
                fig_attr = go.Figure(go.Bar(
                    x=attr_values, y=attr_labels, orientation="h",
                    marker_color=["#f87171" if v > 0 else "#34d399" for v in attr_values],
                    text=[f"{v:+.1f}" for v in attr_values], textposition="outside",
                ))
                fig_attr.update_layout(
                    xaxis_title="Points contributed to the score change (+ = riskier, − = safer)",
                    yaxis=dict(autorange="reversed"),
                )
                st.plotly_chart(style_chart(fig_attr, height=320), use_container_width=True)
                st.caption(
                    "Exact decomposition, not an estimate: the composite score is a weighted sum of "
                    "10 normalized sub-scores, so each factor's (weight × change in sub-score) sums to "
                    f"precisely the total {row['yoy_change']:+.1f}-point change shown above — using the "
                    "actual rescaled weights each year, the same way the composite itself handles missing data."
                )

    with c2:
        st.markdown('<div class="section-tag">All 10 Factors</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Risk Factor Breakdown</div>', unsafe_allow_html=True)
        radar_factors = [f for f in FACTOR_COLS if pd.notna(driver_row[f])]
        radar_values = [driver_row[f] for f in radar_factors]
        radar_labels = [FACTOR_LABELS[f] for f in radar_factors]
        missing_factors = [f for f in FACTOR_COLS if pd.isna(driver_row[f])]

        if radar_factors:
            # Always plot all 10 axis labels, in FACTOR_COLS order, so a missing
            # factor shows as a visible gap rather than silently shrinking the
            # shape — no value is ever invented to fill it.
            all_labels = [FACTOR_LABELS[f] for f in FACTOR_COLS]
            fig3 = go.Figure()
            fig3.add_trace(go.Scatterpolar(
                r=radar_values + [radar_values[0]],
                theta=radar_labels + [radar_labels[0]],
                fill="toself", fillcolor="rgba(13,148,136,0.14)",
                line=dict(color=ACCENT, width=2),
                name="Reported",
            ))
            if missing_factors:
                fig3.add_trace(go.Scatterpolar(
                    r=[0] * len(missing_factors),
                    theta=[FACTOR_LABELS[f] for f in missing_factors],
                    mode="markers",
                    marker=dict(color="#fbbf24", size=10, symbol="x"),
                    line=dict(color="#fbbf24", dash="dot"),
                    name="Not reported",
                    hovertemplate="%{theta}: not reported to the World Bank — excluded from this country's "
                                  "score, weights rescaled among available factors<extra></extra>",
                ))
            fig3.update_layout(
                polar=dict(
                    bgcolor="rgba(0,0,0,0)",
                    radialaxis=dict(visible=True, range=[0, 100], gridcolor="rgba(148,163,184,0.12)", color=TEXT_MUTED),
                    angularaxis=dict(
                        gridcolor="rgba(148,163,184,0.12)", color=TEXT,
                        categoryorder="array", categoryarray=all_labels,
                        tickfont=dict(size=10),
                    ),
                ),
                showlegend=bool(missing_factors),
                legend=dict(orientation="h", y=-0.1, font=dict(color=TEXT_MUTED, size=10)),
            )
            # A narrower centered sub-column here used to keep this polar
            # chart square on wide desktop screens -- but Streamlit collapses
            # multi-column layouts to full width on narrow viewports anyway,
            # so that extra narrowing only ever helped desktop while actively
            # starving the chart of width on mobile, clipping long angular
            # labels like "Government Effectiveness" at the viewport edge.
            # Using the container's actual width plus a real pixel margin
            # (below) fixes mobile without meaningfully hurting desktop.
            styled_fig3 = style_chart(fig3, height=420)
            # style_chart's default 10px side margin is sized for cartesian
            # charts, where axis labels stay inside the plot -- a radar
            # chart's angular labels sit *outside* the circle and need real
            # room. A fixed pixel margin eats a bigger share of a narrow
            # container (more relative headroom exactly where it's needed)
            # while staying unobtrusive on desktop.
            styled_fig3.update_layout(margin=dict(t=40, b=40, l=105, r=105))
            st.plotly_chart(styled_fig3, use_container_width=True)
            if missing_factors:
                st.caption(
                    f"⚠️ Marked with an amber ✕: {', '.join(FACTOR_LABELS[f] for f in missing_factors)} — "
                    f"not reported to the World Bank for {selected}, not silently assumed or estimated."
                )
        else:
            st.caption("No factor data available for radar chart.")

    st.markdown("<br>", unsafe_allow_html=True)
    gov_col, indicators_col = st.columns([1, 2])

    with gov_col:
        with st.container(border=True):
            st.markdown('<div class="section-tag">State Actors</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-title" style="font-size:1.05rem;">Current Ruling Government</div>', unsafe_allow_html=True)
            gov = CURRENT_GOVERNMENT.get(country_code)
            if gov:
                custom_table(
                    [
                        ["Head of State", gov["head_of_state"]],
                        ["Head of Government", gov["head_of_government"]],
                        ["System Type", gov["system_type"]],
                    ],
                    ["Field", "Detail"],
                )
                if gov.get("notes"):
                    st.caption(gov["notes"])
                if gov.get("sources"):
                    st.markdown(
                        "".join(f'<a class="pill-link" href="{url}" target="_blank" rel="noopener noreferrer">{name} ↗</a>' for name, url in gov["sources"]),
                        unsafe_allow_html=True,
                    )
                st.caption("Verified via live web search as of the research date — not a live feed; leadership can change.")
            else:
                st.caption("No verified leadership data on file for this country yet.")

    with indicators_col:
        with st.container(border=True):
            st.markdown('<div class="section-tag">Beyond The Composite Score</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-title" style="font-size:1.05rem;">Major Development Indicators</div>', unsafe_allow_html=True)
            hdi = HDI_DATA.get(country_code)
            indicator_cells = [
                ("GDP Growth", "gdp_growth", row.get("gdp_growth"), row.get("gdp_growth_year"), "%"),
                ("Inflation", "inflation", row.get("inflation"), row.get("inflation_year"), "%"),
                ("Unemployment", "unemployment_rate", row.get("unemployment_rate"), row.get("unemployment_rate_year"), "%"),
                ("Youth Unemployment", "youth_unemployment_rate", row.get("youth_unemployment_rate"), row.get("youth_unemployment_rate_year"), "%"),
                ("Gini Index", "gini_index", row.get("gini_index"), row.get("gini_index_year"), ""),
            ]
            metric_cols = st.columns(3)
            for i, (label, indicator_key, value, year, suffix) in enumerate(indicator_cells):
                with metric_cols[i % 3]:
                    display = f"{value:.1f}{suffix}" if pd.notna(value) else "No data"
                    sub = f"as of {int(year)}" if pd.notna(year) else ""
                    ind_hist = long_df[
                        (long_df["country_code"] == country_code) & (long_df["indicator"] == indicator_key)
                    ].sort_values("year")
                    spark_vals = ind_hist["value"].dropna().tolist()[-10:]
                    stat_card(label, display, sub, spark=spark_vals if len(spark_vals) >= 2 else None)
                    st.markdown("<br>", unsafe_allow_html=True)
            with metric_cols[2]:
                if hdi:
                    stat_card("HDI (UNDP)", f"{hdi['hdi']:.3f}", f"Rank {hdi['rank']} of 193 ({hdi['year']})")
                else:
                    stat_card("HDI (UNDP)", "No data")
            st.caption(
                "GDP growth/inflation feed the composite score above; unemployment, youth unemployment, "
                "Gini, and HDI are descriptive development context only, not scored inputs. "
                "[Gini coverage](https://data.worldbank.org/indicator/SI.POV.GINI) is real but sparse for "
                "this region — many countries have not reported it in years. HDI is from "
                "[UNDP's Human Development Report](https://hdr.undp.org/data-center/human-development-index) "
                "— a periodic reference figure, not a live pull."
            )

    st.markdown("<br>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown('<div class="section-tag">How Much It Owes &amp; Holds</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title" style="font-size:1.05rem;">Sovereign Debt &amp; Reserves Profile</div>', unsafe_allow_html=True)
        debt_pct = row.get("debt_to_gdp")
        debt_year = row.get("debt_to_gdp_year")
        debt_source = row.get("debt_to_gdp_source")
        gdp_usd = row.get("gdp_current_usd")
        gdp_year = row.get("gdp_current_usd_year")
        reserves_months = row.get("reserves_months_imports")
        reserves_months_year = row.get("reserves_months_imports_year")
        reserves_usd = row.get("total_reserves_usd")
        reserves_usd_year = row.get("total_reserves_usd_year")

        # All 4 stats render independently of each other — a country missing
        # debt data (Libya, Yemen) still gets its reserves figures shown, and
        # vice versa. Nothing here is silently skipped because a neighboring
        # stat happens to be missing.
        debt_cols = st.columns(4)
        with debt_cols[0]:
            if pd.notna(debt_pct):
                stat_card("Debt (% of GDP)", f"{debt_pct:.1f}%", f"as of {int(debt_year)}" if pd.notna(debt_year) else "")
            else:
                stat_card("Debt (% of GDP)", "No data")
        with debt_cols[1]:
            if pd.notna(debt_pct) and pd.notna(gdp_usd):
                approx_debt = debt_pct / 100 * gdp_usd
                year_note = (
                    f"debt {int(debt_year)} × GDP {int(gdp_year)}" if pd.notna(debt_year) and pd.notna(gdp_year) and int(debt_year) != int(gdp_year)
                    else f"as of {int(debt_year)}" if pd.notna(debt_year) else ""
                )
                stat_card("Approx. Total Debt", _fmt_usd(approx_debt), year_note)
            else:
                stat_card("Approx. Total Debt", "No data")
        with debt_cols[2]:
            if pd.notna(reserves_usd):
                stat_card("Foreign Reserves", _fmt_usd(reserves_usd), f"as of {int(reserves_usd_year)}" if pd.notna(reserves_usd_year) else "")
            else:
                stat_card("Foreign Reserves", "No data")
        with debt_cols[3]:
            if pd.notna(reserves_months):
                stat_card("Reserves Cover", f"{reserves_months:.1f} mo.", f"of imports, {int(reserves_months_year)}" if pd.notna(reserves_months_year) else "of imports")
            else:
                stat_card("Reserves Cover", "No data")

        if pd.notna(debt_pct) and pd.notna(gdp_usd) and pd.notna(debt_year) and pd.notna(gdp_year) and int(debt_year) != int(gdp_year):
            st.caption(
                f"⚠️ The dollar debt figure multiplies a {int(debt_year)} debt ratio by {int(gdp_year)} GDP "
                f"(the two indicators' most recent reported years don't match) — treat it as a rough "
                f"approximation, not a precisely reported figure."
            )
        if pd.isna(debt_pct):
            st.caption(
                f"No debt-to-GDP figure is available for {selected} from either the World Bank or the "
                f"IMF WEO fallback — not an oversight, genuinely unreported by both institutions."
            )

        st.markdown(
            "For **who specifically it's borrowed from** (verified IMF/multilateral programs) and "
            "**who else lends to or invests in it** (major bilateral creditors and partners), see "
            "**Financing Arrangements** and **Key Economic Partners** further down this page — a "
            "detailed bilateral debt-instrument matrix (exact loan-by-loan creditor/debtor amounts) "
            "isn't reliably available from any free public source for all 27 tracked countries, so it "
            "isn't fabricated here."
        )

    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("🧪 Geopolitical Shock Tester — simulate a stress scenario", expanded=False):
        st.markdown(
            f"Nudge three of the ten scored risk factors directly, in risk-score points (the same "
            f"0-100 scale the radar chart uses), to see how a stress scenario would move {selected}'s "
            f"composite from its latest reported baseline. This is a transparent **points-based** "
            f"simulation, not a claim about real-world elasticity — no institution publishes a precise "
            f"mapping between (say) an FDI collapse percentage and an inflation outcome, so none is "
            f"invented here."
        )
        shock_col1, shock_col2, shock_col3 = st.columns(3)
        with shock_col1:
            shock_fdi = st.slider(
                "Simulate FDI Collapse → Current Account Stress (+risk pts)", 0, 40, 0,
                key=f"shock_fdi_{country_code}",
            )
        with shock_col2:
            shock_inflation = st.slider(
                "Simulate Inflation Spike (+risk pts)", 0, 40, 0,
                key=f"shock_inflation_{country_code}",
            )
        with shock_col3:
            shock_conflict = st.slider(
                "Simulate Proximity Conflict Event (+risk pts)", 0, 40, 0,
                key=f"shock_conflict_{country_code}",
            )

        simulated_score = None
        if shock_fdi or shock_inflation or shock_conflict:
            simulated_score = compute_shock_scenario(factor_scores, shock_fdi, shock_inflation, shock_conflict)
            if simulated_score is not None and pd.notna(row["risk_score"]):
                delta = simulated_score - row["risk_score"]
                st.markdown(
                    f'<div class="narrative-box">Under this shock, {selected}\'s composite would move from '
                    f'<b>{row["risk_score"]:.1f}</b> to an estimated <b>{simulated_score:.1f}</b> '
                    f'({"+" if delta > 0 else ""}{delta:.1f} points) — shown as the dashed line on the '
                    f'chart below.</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.caption("Not enough factor data available for this country to simulate a shock.")
                simulated_score = None

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f'<div class="section-tag">{DATA_YEAR_RANGE}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{selected}: Risk Score Over Time</div>', unsafe_allow_html=True)
    country_history = history[history["country"] == selected].sort_values("year")
    if not country_history.empty:
        fig4 = px.line(country_history, x="year", y="risk_score", markers=True, labels={"risk_score": "Risk Score", "year": "Year"})
        fig4.update_traces(line_color=ACCENT, marker=dict(color=ACCENT, size=7), name="Reported", showlegend=False)
        if simulated_score is not None and pd.notna(row["risk_score"]):
            # Anchored to row["risk_score"] (the CURRENT composite — latest
            # available value per factor) rather than this chart's own last
            # plotted point, because those are two different, both-legitimate
            # numbers already shown elsewhere on this page (the Composite
            # Score stat card above uses the same "current" figure, which can
            # differ from country_history's last per-YEAR figure since that
            # one requires every factor to come from that single year). The
            # simulation has to start from the same baseline its own narrative
            # text quotes, or the chart and the sentence above it would disagree.
            fig4.add_trace(go.Scatter(
                x=[CURRENT_YEAR, CURRENT_YEAR + 1], y=[row["risk_score"], simulated_score],
                mode="lines+markers", line=dict(color="#fbbf24", dash="dash", width=2),
                marker=dict(color="#fbbf24", size=8, symbol="diamond"),
                name="Simulated (shock applied, from current composite)", showlegend=True,
            ))
            fig4.update_layout(showlegend=True, legend=dict(orientation="h", y=-0.15))
        st.plotly_chart(style_chart(fig4, height=320), use_container_width=True)
        if simulated_score is not None:
            st.caption(
                "The dashed amber segment is a hypothetical simulation from the Shock Tester above, "
                "starting from the current composite score (not necessarily the same figure as this "
                "chart's last plotted year — see Methodology) — not a forecast or trend projection."
            )
    else:
        st.caption("Not enough historical data for a trend line.")

    # ---- Year-over-year factor drill-down ----
    # Lets a user pick a specific year on the trend line above and see, in
    # plain language, which underlying World Bank factors actually moved the
    # composite score that year — not just that it moved.
    if not country_history.empty and len(country_history) >= 2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-tag">Year-by-Year Drivers</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title" style="font-size:1.05rem;">What Drove a Specific Year\'s Score?</div>', unsafe_allow_html=True)
        available_years = sorted(country_history["year"].astype(int).tolist())
        selectable_years = available_years[1:]  # first year has no prior year to compare against
        drill_year = st.selectbox(
            f"Select a year to see what drove {selected}'s score change",
            options=selectable_years,
            index=len(selectable_years) - 1,
            key="year_driver_select",
        )
        prior_year_candidates = [y for y in available_years if y < drill_year]
        if prior_year_candidates:
            prior_year = max(prior_year_candidates)
            summary_html, driver_rows = build_year_driver_card(long_df, country_code, selected, drill_year, prior_year)
            st.markdown(f'<div class="narrative-box">{summary_html}</div>', unsafe_allow_html=True)
            if driver_rows:
                driver_table_rows = [
                    [label, _fmt_value_unit(p, unit) if pd.notna(p) else "No data", _fmt_value_unit(c, unit) if pd.notna(c) else "No data",
                     f"{'+' if d > 0 else ''}{d:.2f} pts ({'more' if d > 0 else 'less'} risk)"]
                    for label, p, c, unit, d, source in driver_rows
                ]
                custom_table(driver_table_rows, ["Factor", f"{prior_year}", f"{drill_year}", "Contribution to Score Change"])
        else:
            st.caption(f"{drill_year} is the earliest year with data — there's no prior year to compare it against.")

    # ---- Sub-indicator historical trend explorer ----
    # Supplements the radar chart (a single-year snapshot across all 10
    # factors) with the full multi-year trend for any ONE indicator the user
    # picks, including the two descriptive trade-context indicators that
    # aren't part of the composite score at all (FDI, exports, imports).
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-tag">Indicator Explorer</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title" style="font-size:1.05rem;">Historical Trend by Indicator</div>', unsafe_allow_html=True)
    indicator_options = list(ALL_INDICATOR_LABELS.keys())
    indicator_choice = st.selectbox(
        "Choose an indicator to see its full historical trend for this country",
        options=indicator_options,
        format_func=lambda k: ALL_INDICATOR_LABELS[k][0],
        key="indicator_explorer_select",
    )
    ind_label, ind_unit, ind_source = ALL_INDICATOR_LABELS[indicator_choice]
    ind_hist = long_df[(long_df["country_code"] == country_code) & (long_df["indicator"] == indicator_choice)].sort_values("year")
    if not ind_hist.empty:
        if ind_unit == "USD":
            # Large-dollar indicators (GDP, reserves) are rescaled to billions
            # for a readable axis; GDP per capita is left in raw dollars, since
            # dividing THAT by a billion would make it unreadably tiny.
            usd_scale, usd_axis_label = (1e9, f"{ind_label}, Billions") if indicator_choice != "gdp_per_capita_usd" else (1, ind_label)
            ind_hist = ind_hist.assign(value=ind_hist["value"] / usd_scale)
            axis_label = usd_axis_label
        else:
            axis_label = f"{ind_label} ({ind_unit})"
        fig_ind = px.line(ind_hist, x="year", y="value", markers=True, labels={"value": axis_label, "year": "Year"})
        fig_ind.update_traces(line_color=ACCENT, marker=dict(color=ACCENT, size=6))
        fig_ind.update_layout(title=dict(text=f"{selected}: {ind_label}", font=dict(size=13)))
        st.plotly_chart(style_chart(fig_ind, height=320), use_container_width=True)
        st.caption(f"Source: {ind_source}")
    else:
        st.caption(f"No historical data available for {ind_label} for {selected}.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-tag">Raw Values</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Underlying Indicators</div>', unsafe_allow_html=True)
    raw_rows = []
    for factor, (label, unit) in RAW_LABELS.items():
        value = row.get(factor)
        year = row.get(f"{factor}_year")
        raw_rows.append([
            label,
            f"{value:.2f}" if pd.notna(value) else "No data",
            unit,
            int(year) if pd.notna(year) else "—",
        ])
    custom_table(raw_rows, ["Indicator", "Value", "Unit", "As Of"])

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-tag">Curated &amp; Sourced</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Key Historical Context</div>', unsafe_allow_html=True)
    if events:
        st.markdown(
            f"The table below traces the major economic, political, and conflict-driven events that "
            f"have shaped {selected}'s risk profile, each fact-checked against the linked primary or "
            f"news source. This is deliberately broader than pure macro data — a debt figure alone "
            f"doesn't explain *why* reserves fell or *why* a currency collapsed; these events do."
        )
        events_by_recency = sorted(events, key=lambda e: e[0], reverse=True)
        sourced_rows = [[str(year), event, (src_name, src_url)] for year, event, src_name, src_url in events_by_recency]
        sourced_table(sourced_rows, ["Year", "Event", "Source"])
        st.caption("Curated highlights fact-checked via web search against primary/news sources as of Aug 2026 — not a live feed.")
    else:
        st.caption("No curated events on file for this country yet.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-tag">What the Economy Runs On</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Key Sectors &amp; Trade Profile</div>', unsafe_allow_html=True)
    trade_profile = COUNTRY_TRADE_PROFILE.get(country_code)
    if trade_profile:
        # An icon-labeled "at a glance" box — quicker to scan than a plain
        # table when the goal is orientation (what does this economy run on?)
        # rather than a precise lookup.
        glance_rows = [
            ("🏭", "Main Sectors & Resources", trade_profile["sectors"]),
            ("📤", "Biggest Exports", trade_profile["exports"]),
            ("📥", "Biggest Imports", trade_profile["imports"]),
            ("🤝", "Leading Trade Partners", trade_profile["partners"]),
        ]
        with st.container(border=True):
            st.markdown('<div class="section-tag">At A Glance</div>', unsafe_allow_html=True)
            for icon, label, detail in glance_rows:
                st.markdown(
                    f'<div style="display:flex;gap:0.7rem;margin-bottom:0.85rem;align-items:flex-start;">'
                    f'<div style="font-size:1.3rem;line-height:1.4;">{icon}</div>'
                    f'<div><div class="stat-label" style="margin-bottom:0.15rem;">{label}</div>'
                    f'<div style="font-size:0.88rem;color:{TEXT};line-height:1.55;">{detail}</div></div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
        st.caption(
            "Compiled from established, stable economic-geography knowledge (the kind found in the "
            "CIA World Factbook and the Observatory of Economic Complexity / UN Comtrade) rather than "
            "a single per-country citation — see Methodology for the full source list. Natural-resource "
            "endowments are folded into Main Sectors (e.g. an oil/gas economy's sector description names "
            "the resource directly) rather than tracked as a separate field. Share figures are "
            "directional, not precise-to-the-decimal statistics."
        )
    else:
        st.caption("No trade/sector profile on file for this country yet.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-tag">Trade &amp; Investment</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Investment &amp; Trade Context</div>', unsafe_allow_html=True)
    st.markdown(
        "Shown as descriptive context only — **not** inputs to the risk score above. Investment and "
        "trade direction aren't unambiguously 'safe' or 'risky' the way a debt ratio is, so they're "
        "kept analytically separate."
    )

    inv_col1, inv_col2 = st.columns([3, 2])
    with inv_col1:
        fdi_hist = long_df[(long_df["country_code"] == country_code) & (long_df["indicator"] == "fdi_net_inflows_pct_gdp")].sort_values("year")
        if not fdi_hist.empty:
            fig5 = px.bar(fdi_hist, x="year", y="value", labels={"value": "FDI Net Inflows (% GDP)", "year": "Year"})
            fig5.update_traces(marker_color=ACCENT)
            fig5.update_layout(title=dict(text="FDI Net Inflows (% GDP)", font=dict(size=13)))
            st.plotly_chart(style_chart(fig5, height=260), use_container_width=True)
        else:
            st.caption("No FDI data available for this country.")

        exports_hist = long_df[(long_df["country_code"] == country_code) & (long_df["indicator"] == "exports_pct_gdp")].sort_values("year")
        imports_hist = long_df[(long_df["country_code"] == country_code) & (long_df["indicator"] == "imports_pct_gdp")].sort_values("year")
        if not exports_hist.empty or not imports_hist.empty:
            fig6 = go.Figure()
            if not exports_hist.empty:
                fig6.add_trace(go.Scatter(x=exports_hist["year"], y=exports_hist["value"], mode="lines+markers", name="Exports (% GDP)", line=dict(color=ACCENT)))
            if not imports_hist.empty:
                fig6.add_trace(go.Scatter(x=imports_hist["year"], y=imports_hist["value"], mode="lines+markers", name="Imports (% GDP)", line=dict(color="#f87171")))
            fig6.update_layout(title=dict(text="Exports vs. Imports (% GDP)", font=dict(size=13)), yaxis_title="% of GDP")
            st.plotly_chart(style_chart(fig6, height=260), use_container_width=True)

            if not exports_hist.empty and not imports_hist.empty:
                latest_exp = exports_hist.iloc[-1]
                latest_imp = imports_hist.iloc[-1]
                if latest_exp["year"] == latest_imp["year"]:
                    balance = latest_exp["value"] - latest_imp["value"]
                    direction = "trade surplus" if balance > 0 else "trade deficit"
                    st.caption(
                        f"Latest available ({int(latest_exp['year'])}): exports {latest_exp['value']:.1f}% "
                        f"of GDP vs. imports {latest_imp['value']:.1f}% — a {abs(balance):.1f} pt "
                        f"{direction} on a goods-and-services basis."
                    )
        else:
            st.caption("No trade (exports/imports) data available for this country.")

    with inv_col2:
        st.markdown('<div class="section-tag">Reference</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title" style="font-size:1.05rem;">Primary Market</div>', unsafe_allow_html=True)
        exchange, index = STOCK_EXCHANGES.get(country_code, ("N/A", "N/A"))
        custom_table([["Exchange", exchange], ["Benchmark Index", index]], ["Field", "Value"])

        if country_code in VERIFIED_STOCK_TICKERS:
            ticker, ticker_label = VERIFIED_STOCK_TICKERS[country_code]
            stock_hist = fetch_stock_history(ticker)
            if stock_hist is not None:
                latest_close = stock_hist["Close"].iloc[-1]
                first_close = stock_hist["Close"].iloc[0]
                pct_change = (latest_close - first_close) / first_close * 100
                fig_stock = px.line(stock_hist.reset_index(), x=stock_hist.index.name or "Date", y="Close")
                fig_stock.update_traces(line_color=ACCENT)
                fig_stock.update_layout(
                    title=dict(text=f"{ticker_label} — 1-Year", font=dict(size=12)),
                    yaxis_title="Index Level",
                )
                st.plotly_chart(style_chart(fig_stock, height=200), use_container_width=True)
                arrow = "▲" if pct_change > 0 else ("▼" if pct_change < 0 else "—")
                st.caption(
                    f"Live via Yahoo Finance ({ticker}): {latest_close:,.1f}, {arrow} {abs(pct_change):.1f}% "
                    f"over the past year. Index levels are unitless (points), not a currency amount."
                )
            else:
                st.caption(f"Live data for {ticker_label} ({ticker}) is temporarily unavailable — reference table above is not live pricing.")
        else:
            st.caption(
                "This exchange has no reliable free live-data ticker — Yahoo Finance either has no listing "
                "for it or returns empty/unreliable history. Reference only, not live pricing."
            )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class=\"section-tag\">Who It's Borrowed From</div>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">Financing Arrangements</div>', unsafe_allow_html=True)
    st.markdown(
        "Verified IMF/multilateral financing arrangements for this country — amount, approval date, "
        "and program length. *Instrument-level Eurobond and bilateral-loan maturity schedules are out "
        "of scope; see Methodology for the full coverage note.*"
    )
    arrangements = FINANCING_ARRANGEMENTS.get(country_code)
    if arrangements:
        arrangements_by_recency = sorted(arrangements, key=lambda a: _latest_year_in_text(a["approved"]), reverse=True)
        arr_rows = [[a["program"], a["amount"], a["approved"], a["status"]] for a in arrangements_by_recency]
        custom_table(arr_rows, ["Program", "Amount", "Approved", "Status"])
    else:
        st.caption("No verified arrangement on file for this country — see Methodology for scope.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-tag">Imposed By Other Countries/Blocs</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Major Economic Sanctions</div>', unsafe_allow_html=True)
    st.markdown(
        "International sanctions this country has faced — who imposed them, why, and their current "
        "status. Where a country has no significant sanctions history, that is stated explicitly rather "
        "than left blank; where a related but distinct mechanism exists (e.g. FATF grey-listing, which "
        "is a financial-transparency watchlist, not a sanction), that distinction is called out."
    )
    sanctions = ECONOMIC_SANCTIONS.get(country_code, [])
    if sanctions:
        sanctions_by_recency = sorted(sanctions, key=lambda s: _latest_year_in_text(s["period"]), reverse=True)
        for s in sanctions_by_recency:
            with st.container(border=True):
                st.markdown(
                    f'<div class="section-tag">{s["status"]}</div>'
                    f'<div class="section-title" style="font-size:1.05rem;">{s["name"]}</div>',
                    unsafe_allow_html=True,
                )
                custom_table(
                    [
                        ["Period", s["period"]],
                        ["Imposed By", s["imposing_body"]],
                        ["Reason", s["reason"]],
                        ["Economic Impact", s["economic_impact"]],
                    ],
                    ["Field", "Detail"],
                )
                if s.get("sources"):
                    st.markdown(
                        "".join(f'<a class="pill-link" href="{url}" target="_blank" rel="noopener noreferrer">{name} ↗</a>' for name, url in s["sources"]),
                        unsafe_allow_html=True,
                    )
            st.markdown("<br>", unsafe_allow_html=True)
    else:
        st.caption("No sanctions data on file for this country yet.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-tag">Who Invests, Who Lends</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Key Economic Partners</div>', unsafe_allow_html=True)
    partner_info = KEY_ECONOMIC_PARTNERS.get(country_code)
    if partner_info:
        bullets = _paragraph_to_bullets(partner_info["summary"])
        bullet_html = "".join(f"<li style='margin-bottom:0.6rem;'>{b}</li>" for b in bullets)
        st.markdown(f'<div class="narrative-box"><ul style="margin:0;padding-left:1.2rem;">{bullet_html}</ul></div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        for name, url in partner_info["sources"]:
            st.markdown(f'<a class="pill-link" href="{url}" target="_blank" rel="noopener noreferrer">{name} ↗</a>', unsafe_allow_html=True)
    else:
        st.caption(
            "No independently verified creditor/investor/trade-partner summary on file for this "
            "country yet — this section is deliberately scoped to cases with solid sourcing rather "
            "than filled in with unverified claims. See Methodology for the full scope note."
        )

# ================= TAB 3: COMPARE COUNTRIES =================
with tab3:
    st.markdown('<div class="section-tag">Side By Side</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Compare Countries</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="masthead-sub" style="margin-bottom:1rem;">Pick up to 4 countries to compare every '
        'structured indicator from the Country Deep Dive side by side — composite score, all 10 risk '
        'factors, macro/development indicators, and credit ratings. Long-form sections (Country Brief, '
        'Key Economic Partners, historical context) stay in the single-country Deep Dive, since dense '
        'prose does not compare cleanly across four countries at once.</div>',
        unsafe_allow_html=True,
    )

    compare_selection = st.multiselect(
        "Select countries to compare (up to 4)", country_list, default=country_list[:2], max_selections=4,
        label_visibility="collapsed",
    )

    if len(compare_selection) < 2:
        st.caption("Select at least 2 countries to compare.")
    else:
        COMPARE_COLORS = ["#0d9488", "#a78bfa", "#2dd4bf", "#f472b6"]
        cmp_rows = [scored[scored["country"] == name].iloc[0] for name in compare_selection]
        cmp_drivers = [drivers[drivers["country"] == name].iloc[0] for name in compare_selection]

        st.markdown('<div class="section-tag">All 10 Factors, Overlaid</div>', unsafe_allow_html=True)
        all_labels = [FACTOR_LABELS[f] for f in FACTOR_COLS]
        fig_cmp = go.Figure()
        for i, (name, drow) in enumerate(zip(compare_selection, cmp_drivers)):
            factors_present = [f for f in FACTOR_COLS if pd.notna(drow[f])]
            if not factors_present:
                continue
            values = [drow[f] for f in factors_present]
            labels = [FACTOR_LABELS[f] for f in factors_present]
            color = COMPARE_COLORS[i % len(COMPARE_COLORS)]
            fig_cmp.add_trace(go.Scatterpolar(
                r=values + [values[0]], theta=labels + [labels[0]],
                fill="toself", fillcolor=color + "22",
                line=dict(color=color, width=2),
                name=name,
            ))
        fig_cmp.update_layout(
            polar=dict(
                bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(visible=True, range=[0, 100], gridcolor="rgba(148,163,184,0.12)", color=TEXT_MUTED),
                angularaxis=dict(
                    gridcolor="rgba(148,163,184,0.12)", color=TEXT,
                    categoryorder="array", categoryarray=all_labels,
                    tickfont=dict(size=10),
                ),
            ),
            showlegend=True,
            legend=dict(orientation="h", y=-0.12, font=dict(color=TEXT_MUTED, size=10)),
        )
        # Same fix as the single-country radar in Country Deep Dive: no extra
        # column narrowing (Streamlit collapses columns to full width on
        # mobile anyway, so it only ever hurt narrow screens) plus a real
        # pixel margin, since angular labels like "Government Effectiveness"
        # sit outside the circle and were getting clipped at the edge.
        styled_fig_cmp = style_chart(fig_cmp, height=460)
        styled_fig_cmp.update_layout(margin=dict(t=40, b=60, l=105, r=105))
        st.plotly_chart(styled_fig_cmp, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown('<div class="section-tag">Headline</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title" style="font-size:1.05rem;">Composite Score &amp; Context</div>', unsafe_allow_html=True)
        headline_rows = [
            ["Composite Score"] + [f"{r['risk_score']:.1f}" if pd.notna(r["risk_score"]) else "N/A" for r in cmp_rows],
            ["Risk Tier"] + [r["risk_tier"] for r in cmp_rows],
            ["Regional Rank"] + [f"{int(r['risk_rank'])} / {len(scored)}" if pd.notna(r["risk_rank"]) else "N/A" for r in cmp_rows],
            ["YoY Change"] + [f"{r['yoy_change']:+.1f}" if pd.notna(r.get("yoy_change")) else "N/A" for r in cmp_rows],
        ]
        custom_table(headline_rows, ["Metric"] + compare_selection)

        st.markdown("<br>", unsafe_allow_html=True)

        def _cmp_cell(r, col, suffix=""):
            v = r.get(col)
            return f"{v:.1f}{suffix}" if pd.notna(v) else "No data"

        st.markdown('<div class="section-tag">State Actors</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title" style="font-size:1.05rem;">Current Ruling Government</div>', unsafe_allow_html=True)
        gov_rows = [
            ["Head of State"] + [CURRENT_GOVERNMENT.get(r["country_code"], {}).get("head_of_state", "No data") for r in cmp_rows],
            ["Head of Government"] + [CURRENT_GOVERNMENT.get(r["country_code"], {}).get("head_of_government", "No data") for r in cmp_rows],
            ["System Type"] + [CURRENT_GOVERNMENT.get(r["country_code"], {}).get("system_type", "No data") for r in cmp_rows],
        ]
        custom_table(gov_rows, ["Field"] + compare_selection)
        st.caption("Verified via live web search as of the research date — not a live feed; leadership can change. See each country's own Deep Dive for full sourcing.")

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown('<div class="section-tag">Beyond The Composite Score</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title" style="font-size:1.05rem;">Macro &amp; Development Indicators</div>', unsafe_allow_html=True)
        macro_rows = [
            ["GDP Growth"] + [_cmp_cell(r, "gdp_growth", "%") for r in cmp_rows],
            ["Inflation"] + [_cmp_cell(r, "inflation", "%") for r in cmp_rows],
            ["Unemployment"] + [_cmp_cell(r, "unemployment_rate", "%") for r in cmp_rows],
            ["Youth Unemployment"] + [_cmp_cell(r, "youth_unemployment_rate", "%") for r in cmp_rows],
            ["Gini Index"] + [_cmp_cell(r, "gini_index") for r in cmp_rows],
            ["HDI (UNDP)"] + [
                f"{HDI_DATA[r['country_code']]['hdi']:.3f}" if r["country_code"] in HDI_DATA else "No data"
                for r in cmp_rows
            ],
            ["GDP (current US$)"] + [
                _fmt_usd(r["gdp_current_usd"]) if pd.notna(r.get("gdp_current_usd")) else "No data" for r in cmp_rows
            ],
            ["GDP per Capita"] + [
                _fmt_usd(r["gdp_per_capita_usd"]) if pd.notna(r.get("gdp_per_capita_usd")) else "No data" for r in cmp_rows
            ],
            ["Current Account (% GDP)"] + [_cmp_cell(r, "current_account_pct_gdp", "%") for r in cmp_rows],
            ["FDI Net Inflows (% GDP)"] + [_cmp_cell(r, "fdi_net_inflows_pct_gdp", "%") for r in cmp_rows],
        ]
        custom_table(macro_rows, ["Metric"] + compare_selection)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown('<div class="section-tag">How Much It Owes &amp; Holds</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title" style="font-size:1.05rem;">Sovereign Debt &amp; Reserves Profile</div>', unsafe_allow_html=True)

        def _cmp_approx_debt(r):
            debt_pct, gdp_usd = r.get("debt_to_gdp"), r.get("gdp_current_usd")
            if pd.isna(debt_pct) or pd.isna(gdp_usd):
                return "No data"
            return _fmt_usd(debt_pct / 100 * gdp_usd)

        debt_rows = [
            ["Debt (% GDP)"] + [_cmp_cell(r, "debt_to_gdp", "%") for r in cmp_rows],
            ["Approx. Total Debt"] + [_cmp_approx_debt(r) for r in cmp_rows],
            ["Foreign Reserves"] + [
                _fmt_usd(r["total_reserves_usd"]) if pd.notna(r.get("total_reserves_usd")) else "No data"
                for r in cmp_rows
            ],
            ["Reserves Cover"] + [_cmp_cell(r, "reserves_months_imports", " mo.") for r in cmp_rows],
        ]
        custom_table(debt_rows, ["Metric"] + compare_selection)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown('<div class="section-tag">Sanity Check</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title" style="font-size:1.05rem;">Actual Credit Ratings</div>', unsafe_allow_html=True)
        rating_rows = []
        for agency, label in [("sp", "S&P"), ("moodys", "Moody's"), ("fitch", "Fitch")]:
            row_vals = []
            for r in cmp_rows:
                ratings = CREDIT_RATINGS.get(r["country_code"])
                row_vals.append(ratings[agency] if ratings else "Not Rated")
            rating_rows.append([label] + row_vals)
        custom_table(rating_rows, ["Agency"] + compare_selection)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown('<div class="section-tag">What The Economy Runs On</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title" style="font-size:1.05rem;">Key Sectors &amp; Trade Profile</div>', unsafe_allow_html=True)
        sector_cols = st.columns(len(compare_selection))
        for name, r, col in zip(compare_selection, cmp_rows, sector_cols):
            with col:
                st.markdown(f'<div class="section-tag">{name}</div>', unsafe_allow_html=True)
                profile = COUNTRY_TRADE_PROFILE.get(r["country_code"])
                if profile:
                    for icon, label, field in [
                        ("🏭", "Main Sectors & Resources", "sectors"),
                        ("📤", "Biggest Exports", "exports"),
                        ("📥", "Biggest Imports", "imports"),
                        ("🤝", "Leading Trade Partners", "partners"),
                    ]:
                        st.markdown(
                            f'<div style="display:flex;gap:0.6rem;margin-bottom:0.85rem;align-items:flex-start;">'
                            f'<div style="font-size:1.1rem;line-height:1.4;">{icon}</div>'
                            f'<div><div class="stat-label" style="margin-bottom:0.15rem;">{label}</div>'
                            f'<div style="font-size:0.82rem;color:{TEXT};line-height:1.5;">{profile[field]}</div></div>'
                            f'</div>',
                            unsafe_allow_html=True,
                        )
                else:
                    st.caption("No trade profile on file.")
        st.caption(
            "Compiled from established, stable economic-geography knowledge rather than a single "
            "per-country citation — see Methodology for the full source list."
        )

# ================= TAB 4: LIVE CONFLICTS =================
with tab4:
    st.markdown('<div class="section-tag">Curated &amp; Sourced, Not a Live Feed</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Live Conflicts &amp; Regional Flashpoints</div>', unsafe_allow_html=True)
    st.markdown(
        "The 10-factor composite score above is built on **annual** World Bank data, which by nature "
        "lags acute, fast-moving events — a war that started two months ago won't yet show up in a "
        "debt-to-GDP or governance figure. This tab is the qualitative complement: the region's most "
        "consequential live conflicts and flashpoints, each mapped to the specific tracked countries "
        "it affects, with sourced detail on market/trade impact. **Curated and fact-checked as of "
        "August 2026 — not a live news feed.** Type and impact classifications below are this project's "
        "own editorial judgment, applying a standard conflict-tracking taxonomy — not a third-party rating."
    )
    st.markdown("<br>", unsafe_allow_html=True)

    code_to_name = dict(zip(scored["country_code"], scored["country"]))

    # Impact-on-tracked-economies severity — deliberately the SAME red/amber/grey
    # family used for country risk tiers elsewhere in this app, since "Impact"
    # is genuinely a severity axis like risk tier is. To avoid recreating the
    # exact color collision this project fixed earlier, it is used ONLY as a
    # small labeled badge here, never as the dominant map/fill color — the map
    # itself stays in the violet/indigo STATUS palette below, which is what a
    # user actually scans across the whole board at a glance.
    IMPACT_COLORS = {"Critical": "#f87171", "Significant": "#fbbf24", "Limited": "#94a3b8"}
    CONFLICT_TYPES = ["Civil War", "Criminal Violence", "Interstate War", "Political Instability", "Sectarian", "Territorial Dispute", "Terrorism", "Unconventional"]
    STATUS_BUCKETS = ["Active / Unresolved", "Ceasefire / Fragile", "Frozen / Stalemated"]

    def _status_bucket(status_text):
        s = status_text.lower()
        if "active" in s or "escalat" in s or "unresolved" in s:
            return "Active / Unresolved"
        if "ceasefire" in s or "fragile" in s or "frozen" in s or "stalemate" in s:
            return "Ceasefire / Fragile"
        return "Frozen / Stalemated"

    for c in LIVE_CONFLICTS:
        c["_status_bucket"] = _status_bucket(c["status"])

    # ---- CFR-style split layout: a narrow filter rail beside the main workspace ----
    filter_col, workspace_col = st.columns([1, 3])

    IMPACT_LEVELS = ["Critical", "Significant", "Limited"]

    with filter_col:
        with st.container(border=True):
            # A "reset" must clear these checkboxes' session_state BEFORE
            # they're instantiated below in this same run — Streamlit raises
            # StreamlitAPIException if a widget's state is written after that
            # widget has already been created in the current script pass. So
            # the reset button (further down) only sets a flag and reruns;
            # this block, which always runs first, is what actually clears
            # the values, on the following run, before the checkboxes exist.
            if st.session_state.get("_reset_conflict_filters_pending"):
                for t in CONFLICT_TYPES:
                    st.session_state[f"ctype_{t}"] = False
                for s in STATUS_BUCKETS:
                    st.session_state[f"cstatus_{s}"] = False
                for i in IMPACT_LEVELS:
                    st.session_state[f"cimpact_{i}"] = False
                st.session_state["_reset_conflict_filters_pending"] = False

            st.markdown('<div class="section-tag">Filter</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-title" style="font-size:1rem;">Conflict Type</div>', unsafe_allow_html=True)
            selected_types = [t for t in CONFLICT_TYPES if st.checkbox(t, key=f"ctype_{t}")]

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="section-title" style="font-size:1rem;">Status</div>', unsafe_allow_html=True)
            # A small colored dot per option, CFR-style, using Streamlit's
            # built-in markdown color annotations (a fixed named palette, not
            # arbitrary hex) — the closest match to this tab's own violet/
            # indigo/grey status palette that a checkbox label can render.
            STATUS_DOT = {"Active / Unresolved": "violet", "Ceasefire / Fragile": "blue", "Frozen / Stalemated": "gray"}
            selected_statuses = [s for s in STATUS_BUCKETS if st.checkbox(f":{STATUS_DOT[s]}[●] {s}", key=f"cstatus_{s}")]

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="section-title" style="font-size:1rem;">Impact on Tracked Economies</div>', unsafe_allow_html=True)
            IMPACT_DOT = {"Critical": "red", "Significant": "orange", "Limited": "gray"}
            selected_impacts = [i for i in IMPACT_LEVELS if st.checkbox(f":{IMPACT_DOT[i]}[●] {i}", key=f"cimpact_{i}")]

            if selected_types or selected_statuses or selected_impacts:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Reset filters", key="reset_conflict_filters"):
                    st.session_state["_reset_conflict_filters_pending"] = True
                    st.rerun()

    def _passes_conflict_filters(c):
        if selected_types and c["type"] not in selected_types:
            return False
        if selected_statuses and c["_status_bucket"] not in selected_statuses:
            return False
        if selected_impacts and c["impact"] not in selected_impacts:
            return False
        return True

    matching_names = {c["name"] for c in LIVE_CONFLICTS if _passes_conflict_filters(c)}

    # Representative point per conflict for the map below — a single lat/lon
    # standing in for what is often a multi-country or border-spanning event,
    # not a claim about an exact front line.
    with workspace_col:
        CONFLICT_COORDS = {
            "2026 Iran-Israel-US War": (35.6892, 51.3890),
            "Red Sea Shipping Crisis & Houthi-Saudi Blockade": (12.6, 43.4),
            "Gaza War Aftermath & Fragile Ceasefire": (31.5, 34.47),
            "Syria's Post-Assad Transition": (33.51, 36.28),
            "Sudan Civil War": (15.5, 32.55),
            "Israel-Hezbollah War & Lebanon Front": (33.37, 35.48),
            "Libya's Rival Governments Standoff": (31.2, 16.6),
            "2026 Pakistan-Afghanistan War": (34.0, 70.0),
            "India-Pakistan Kashmir Crisis": (34.08, 74.80),
            "Balochistan Insurgency & CPEC Attacks": (25.13, 62.33),
            "Iran-Aligned Militia Attacks on US Forces in Iraq": (33.31, 44.36),
            "Egypt-Ethiopia Nile Dam (GERD) Dispute": (11.22, 35.09),
            "Western Sahara Conflict & Algeria-Morocco Rupture": (27.15, -13.20),
        }
        # Deliberately a distinct cool (violet/indigo) palette, not the warm
        # green/amber/red used for risk-tier severity elsewhere in this app —
        # a conflict being "Active" and a country being "Higher Risk" are two
        # different metrics, and sharing red for both would visually conflate them.
        STATUS_COLORS = {"active": "#a855f7", "ceasefire": "#818cf8", "frozen": "#7d8aa0"}

        def _status_color(status_text):
            s = status_text.lower()
            if "active" in s or "escalat" in s or "unresolved" in s:
                return STATUS_COLORS["active"]
            if "ceasefire" in s or "fragile" in s or "frozen" in s or "stalemate" in s:
                return STATUS_COLORS["ceasefire"]
            return STATUS_COLORS["frozen"]

        st.markdown('<div class="section-tag">Map View</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title" style="font-size:1.05rem;">Conflict Map</div>', unsafe_allow_html=True)
        map_conflicts = [c for c in LIVE_CONFLICTS if c["name"] in CONFLICT_COORDS]
        if map_conflicts:
            lats = [CONFLICT_COORDS[c["name"]][0] for c in map_conflicts]
            lons = [CONFLICT_COORDS[c["name"]][1] for c in map_conflicts]
            colors = [_status_color(c["status"]) for c in map_conflicts]
            # Non-matching conflicts fade to near-invisible rather than being
            # removed outright, so the map's geography stays legible while
            # filtering — the same "dim, don't delete" pattern as the artifact.
            opacities = [0.9 if c["name"] in matching_names else 0.08 for c in map_conflicts]
            # Territorial disputes (Kashmir, GERD, Western Sahara) get a
            # distinct diamond marker — these are contested zones/borders
            # rather than an armed conflict with a clear combat front, so a
            # different shape lets them read as a different kind of flashpoint
            # at a glance, without needing a separate legend-free color.
            symbols = ["diamond" if c["type"] == "Territorial Dispute" else "circle" for c in map_conflicts]
            # A short, CFR-style hover pill — just the name and status — since
            # the full actor/impact/country detail already lives one click
            # away in the card below; a cluttered hover box competes with,
            # rather than complements, that fuller read.
            hover_texts = [f"<b>{c['name']}</b><br>{c['status']}<br><i>Click for full detail ↓</i>" for c in map_conflicts]
            conflict_map_fig = go.Figure()
            # When a conflict is focused (clicked, or arrived via cross-nav),
            # shade the full territory of every country it lists as
            # "affected" — a direct, CFR Global-Conflict-Tracker-style answer
            # to "who's in this conflict", not just a dot at the capital. Drawn
            # first so the conflict/city markers layer on top of the fill.
            _focused = st.session_state.get("focused_conflict")
            _focused_conflict_obj = next((c for c in map_conflicts if c["name"] == _focused), None)
            if _focused_conflict_obj:
                _aff_codes = [code for code in _focused_conflict_obj.get("affected", []) if code in COUNTRY_CAPITAL_COORDS]
                if _aff_codes:
                    conflict_map_fig.add_trace(go.Choropleth(
                        locations=_aff_codes, locationmode="ISO-3", z=[1] * len(_aff_codes),
                        colorscale=[[0, "rgba(240,180,41,0.55)"], [1, "rgba(240,180,41,0.55)"]],
                        showscale=False, marker_line_color="#f0b429", marker_line_width=1.5,
                        text=[f"{code_to_name.get(code, code)} — party to {_focused}" for code in _aff_codes],
                        hoverinfo="text",
                    ))
            conflict_map_fig.add_trace(go.Scattergeo(
                lat=lats, lon=lons, mode="markers",
                marker=dict(size=14, color=colors, opacity=opacities, symbol=symbols, line=dict(width=1, color="#0a0e14")),
                text=hover_texts, hoverinfo="text",
                hoverlabel=dict(bgcolor=colors, font=dict(color="#0a0e14", size=12)),
            ))
            _city_positions = ["top center", "bottom center", "middle right", "middle left"]
            _cf_primary_names = list(MAJOR_CITIES_PRIMARY.keys())
            conflict_map_fig.add_trace(go.Scattergeo(
                lat=[c[0] for c in MAJOR_CITIES_PRIMARY.values()], lon=[c[1] for c in MAJOR_CITIES_PRIMARY.values()],
                mode="markers+text", text=_cf_primary_names,
                marker=dict(size=4, color="rgba(245,245,244,0.9)", line=dict(width=0.5, color="rgba(10,14,20,0.7)")),
                textposition=[_city_positions[i % 4] for i in range(len(_cf_primary_names))],
                textfont=dict(size=8, color="#f5f5f4"),
                hoverinfo="text", showlegend=False,
            ))
            conflict_map_fig.add_trace(go.Scattergeo(
                lat=[c[0] for c in MAJOR_CITIES_SECONDARY.values()], lon=[c[1] for c in MAJOR_CITIES_SECONDARY.values()],
                mode="markers", text=list(MAJOR_CITIES_SECONDARY.keys()),
                marker=dict(size=3.5, color="rgba(230,237,243,0.45)", line=dict(width=0.5, color="rgba(10,14,20,0.6)")),
                hoverinfo="text", showlegend=False,
            ))
            _cf_lat_range, _cf_lon_range = [-5, 42], [-18, 100]
            conflict_map_fig.add_trace(sea_label_trace(_cf_lat_range, _cf_lon_range))
            for _t in river_traces(_cf_lat_range, _cf_lon_range):
                conflict_map_fig.add_trace(_t)
            conflict_map_fig.update_geos(
                scope="world", lataxis_range=_cf_lat_range, lonaxis_range=_cf_lon_range,
                # Same near-black/slate basemap as the Risk Map — muted and distinct from
                # this map's own violet/indigo conflict-status markers, so the markers
                # are what stands out.
                **MAP_BASE_STYLE,
            )
            conflict_map_fig.update_layout(margin=dict(t=10, b=10, l=10, r=10), showlegend=False)
            map_click = st.plotly_chart(
                style_chart(conflict_map_fig, height=380), use_container_width=True,
                on_select="rerun", selection_mode="points", key="conflict_map_select",
            )
            st.caption(
                "🟣 Active/unresolved · 🔵 Ceasefire/fragile · ⚪ Frozen or stalemated · "
                "◆ Contested territory (Kashmir, GERD, Western Sahara) vs ● other flashpoints — "
                "hover a node for a quick name/status popup, or **click a marker to shade every affected "
                "country on the map** (amber fill) **and jump to that conflict's full detail below**. "
                "One point per conflict; a single marker stands "
                "in for what is often a multi-country or border-spanning event. Each conflict card below "
                "also has clickable **affected-economy pills** — click one to pre-select that country in "
                "the Country Deep Dive tab above (Streamlit can't force-switch tabs from here, so it's "
                "ready the moment you click over)."
            )
            # Clicking a marker on the map re-runs the app with a selection payload;
            # translate that point index back to a conflict name and remember it in
            # session state so the matching card below can float to the top and
            # auto-expand — the closest honest equivalent of "jump to that section"
            # Streamlit's tab/expander model supports, since there's no native
            # cross-widget DOM anchor-scroll on a chart click event.
            if map_click and map_click.selection and map_click.selection.get("point_indices"):
                clicked_idx = map_click.selection["point_indices"][0]
                if clicked_idx < len(map_conflicts):
                    st.session_state["focused_conflict"] = map_conflicts[clicked_idx]["name"]
        st.markdown("<br>", unsafe_allow_html=True)

        focused_name = st.session_state.get("focused_conflict")
        visible_conflicts = [c for c in LIVE_CONFLICTS if c["name"] in matching_names]
        if focused_name:
            visible_conflicts.sort(key=lambda c: c["name"] != focused_name)
            if focused_name in matching_names:
                st.info(f"📍 Jumped here from the map: **{focused_name}**. Scroll down for the rest, or click a different marker above.", icon="📍")

        st.markdown(
            f'<div class="section-tag">Showing {len(visible_conflicts)} of {len(LIVE_CONFLICTS)} Tracked Flashpoints</div>',
            unsafe_allow_html=True,
        )

        if not visible_conflicts:
            st.info("No conflicts match the selected filters — try clearing a filter group on the left.", icon="🔍")

        for i, conflict in enumerate(visible_conflicts):
            is_focused = conflict["name"] == focused_name
            with st.container(border=True):
                # ---- Always-visible compact header: status/type/impact
                # badges, name, affected countries, and a one-sentence
                # takeaway — enough to understand the conflict at a glance
                # without reading a wall of text. ----
                impact_color = IMPACT_COLORS[conflict["impact"]]
                st.markdown(
                    f'<div style="display:flex;gap:0.4rem;flex-wrap:wrap;margin-bottom:0.3rem;">'
                    f'<span class="tier-badge" style="background:rgba(168,85,247,0.14);color:#c4b5fd;">{conflict["status"]}</span>'
                    f'<span class="tier-badge" style="background:{impact_color}22;color:{impact_color};">Impact: {conflict["impact"]}</span>'
                    f'<span class="tier-badge" style="background:rgba(148,163,184,0.14);color:{TEXT_MUTED};">{conflict["type"]}</span>'
                    f'</div>'
                    f'<div class="section-title" style="font-size:1.2rem;">{conflict["name"]}</div>',
                    unsafe_allow_html=True,
                )
                affected_names = [code_to_name.get(c, c) for c in conflict["affected"]]
                # Each affected-country pill is clickable — same "pre-select in
                # Country Deep Dive" cross-navigation as the Risk Map click,
                # since Streamlit can't force-switch the active tab from here.
                _jump_key = "country_jump_" + re.sub(r"[^a-z0-9]+", "_", conflict["name"].lower())
                jumped_country = st.pills(
                    f"Affected economies — {conflict['name']}", affected_names,
                    selection_mode="single", key=_jump_key, label_visibility="collapsed",
                )
                if jumped_country and st.session_state.get("selected_country_from_map") != jumped_country:
                    # This tab (4) runs *after* Country Deep Dive (tab 2) in
                    # script order, so setting session_state alone wouldn't
                    # take effect until the pass after next — an immediate
                    # rerun makes the pre-select land on this same click. The
                    # inequality check stops that rerun from looping forever,
                    # since the pill stays selected across reruns.
                    st.session_state["selected_country_from_map"] = jumped_country
                    st.rerun()
                if is_focused:
                    # CFR-style clean field/value rows for the specific
                    # conflict a user just clicked on the map — a spotlight
                    # treatment closer to that map's own popup card, layered
                    # on top of (not replacing) this app's usual badge style.
                    custom_table(
                        [
                            ["Type", conflict["type"]],
                            ["Impact on Tracked Economies", conflict["impact"]],
                            ["Status", conflict["status"]],
                        ],
                        ["Field", "Detail"],
                    )
                takeaway = _event_headline(conflict["summary"], max_len=200)
                if not takeaway.endswith((".", "…")):
                    takeaway += "."
                st.markdown(f'<div class="narrative-box">{takeaway}</div>', unsafe_allow_html=True)

                if conflict.get("stats"):
                    st.markdown("<br>", unsafe_allow_html=True)
                    stat_cols = st.columns(len(conflict["stats"]))
                    for col, (label, value) in zip(stat_cols, conflict["stats"]):
                        with col:
                            st.markdown(
                                f'<div class="stat-label" style="font-size:0.58rem;">{label}</div>'
                                f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:1rem;color:{ACCENT};font-weight:700;">{value}</div>',
                                unsafe_allow_html=True,
                            )

                # ---- Full detail, collapsed by default — the dense material
                # (full summary, market impact, actors, sources) lives here
                # instead of always being on screen. ----
                with st.expander("Full summary, market impact & sources", expanded=is_focused):
                    if conflict.get("groups"):
                        st.markdown(
                            f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:0.78rem;color:{TEXT_MUTED};margin-bottom:0.8rem;">'
                            f'<b style="color:{ACCENT};">Groups Involved:</b> {conflict["groups"]}</div>',
                            unsafe_allow_html=True,
                        )
                    st.markdown(f'<div class="narrative-box"><b>Summary</b><br>{conflict["summary"]}</div>', unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown(f'<div class="narrative-box"><b>Market &amp; Trade Impact</b><br>{conflict["market_impact"]}</div>', unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown(
                        "".join(f'<a class="pill-link" href="{url}" target="_blank" rel="noopener noreferrer">{name} ↗</a>' for name, url in conflict["sources"]),
                        unsafe_allow_html=True,
                    )
            if i < len(visible_conflicts) - 1:
                st.markdown("<br>", unsafe_allow_html=True)

# ================= TAB 5: GEO-ECONOMIC INTERDEPENDENCE =================
GEO_RISK_COLOR = {"Low": "#34d399", "Moderate": "#fbbf24", "High": "#f87171", "Critical": "#dc2626"}
BLOC_COLOR = {
    "GCC": "#0d9488", "OPEC": "#f472b6", "BRICS+": "#2dd4bf",
    "Arab League": "#a78bfa", "SAARC": "#fbbf24", "Non-aligned / OECD": TEXT_MUTED,
}

with tab5:
    st.markdown('<div class="section-tag">Global Trade Structure</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Geo-Economic Interdependence Dashboard</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="masthead-sub" style="margin-bottom:1rem;">How MENASA connects to the rest of the global '
        'economy through maritime chokepoints, critical-mineral supply concentration, and a small set of '
        'corporate gatekeepers whose capacity constraints ripple through world trade. A structural/context '
        'layer — descriptive, not part of the composite risk score elsewhere in this app.</div>',
        unsafe_allow_html=True,
    )

    geo_sub1, geo_sub2, geo_sub3, geo_sub4 = st.tabs(
        ["\U0001F5FA\uFE0F Trade Map", "\U0001F4CA Structural Matrix", "\U0001F4B9 Resource Benchmarks", "\U0001F3E2 Corporate Gatekeepers"]
    )

    with geo_sub1:
        with st.expander("Map Layers", expanded=True):
            lcol1, lcol2, lcol3 = st.columns(3)
            with lcol1:
                show_infra = st.checkbox("Hard Infrastructure (chokepoints)", value=True, key="geo_show_infra")
            with lcol2:
                show_friction = st.checkbox("Trade Arteries / Friction Points", value=True, key="geo_show_friction")
            with lcol3:
                show_alliances = st.checkbox("Legal Trade Alliances (GCC, BRICS+, ASEAN, EU)", value=False, key="geo_show_alliances")
            lcol4, lcol5, lcol6 = st.columns(3)
            with lcol4:
                show_countries = st.checkbox("MENASA Country Alliances (all 27)", value=True, key="geo_show_countries")
            with lcol5:
                show_fabs = st.checkbox("Advanced Semiconductor Fabs", value=False, key="geo_show_fabs")
            with lcol6:
                show_ports = st.checkbox("Major Ports & Economic Hubs", value=True, key="geo_show_ports")

        st.markdown('<div class="section-tag">Chokepoints &amp; Trade Arteries</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title" style="font-size:1.05rem;">Interactive Trade Map</div>', unsafe_allow_html=True)

        fig_geo = go.Figure()

        if show_friction:
            # Each artery's line color/width reflects the highest real risk_level
            # among the chokepoints it actually transits (sourced in
            # MARITIME_CHOKEPOINTS), rather than a single flat color for all
            # three routes -- a rerouted/blockaded corridor should read as more
            # exposed than a normal one, using data already in the app.
            _risk_rank = {"Low": 0, "Moderate": 1, "High": 2, "Critical": 3}
            for route in TRADE_ARTERIES:
                route_risk = max(
                    (MARITIME_CHOKEPOINTS[k]["risk_level"] for k in route["chokepoints"] if k in MARITIME_CHOKEPOINTS),
                    key=lambda r: _risk_rank.get(r, 0), default="Moderate",
                )
                route_color = GEO_RISK_COLOR.get(route_risk, ACCENT)
                path_lons = [p[1] for p in route["path"]]
                path_lats = [p[0] for p in route["path"]]
                fig_geo.add_trace(go.Scattergeo(
                    lon=path_lons, lat=path_lats,
                    mode="lines", line=dict(width=1.5 + _risk_rank.get(route_risk, 0) * 0.6, color=route_color, dash="dot"),
                    opacity=0.65, hoverinfo="text",
                    text=f"{route['name']} — exposure: {route_risk}", showlegend=False,
                ))
                # Small endpoint markers at both ends of the path make the
                # dotted line read as a bounded corridor rather than an
                # arbitrary trail (Plotly's geo lines have no arrowhead support).
                fig_geo.add_trace(go.Scattergeo(
                    lon=[path_lons[0], path_lons[-1]], lat=[path_lats[0], path_lats[-1]],
                    mode="markers", marker=dict(size=6, symbol="circle-open", color=route_color, line=dict(width=1.5)),
                    opacity=0.85, hoverinfo="skip", showlegend=False,
                ))

        if show_alliances:
            for bloc_name, bloc in TRADE_ALLIANCES.items():
                fig_geo.add_trace(go.Scattergeo(
                    lon=[bloc["centroid"][1]], lat=[bloc["centroid"][0]],
                    mode="markers+text", text=[bloc_name], textposition="bottom center",
                    marker=dict(size=10, color="rgba(148,163,184,0.5)", symbol="square"),
                    hovertemplate=f"<b>{bloc_name}</b><br>{', '.join(bloc['members'][:6])}…<extra></extra>",
                    showlegend=False,
                ))

        if show_countries:
            # Group by primary_bloc so the legend shows one entry per bloc rather
            # than 27 individual country entries.
            by_bloc = {}
            for code, alliance in MENASA_COUNTRY_ALLIANCES.items():
                by_bloc.setdefault(alliance["primary_bloc"], []).append(code)
            country_names = dict(zip(scored["country_code"], scored["country"]))
            for bloc_name, codes in by_bloc.items():
                # customdata carries ["country", <name>, <memberships>] -- the
                # literal "country" tag lets the click handler below tell this
                # trace apart from the chokepoint trace's ["<key>", <risk>]
                # customdata, since both are 2+/3-element lists otherwise
                # indistinguishable by shape alone.
                fig_geo.add_trace(go.Scattergeo(
                    lon=[COUNTRY_CAPITAL_COORDS[c][1] for c in codes if c in COUNTRY_CAPITAL_COORDS],
                    lat=[COUNTRY_CAPITAL_COORDS[c][0] for c in codes if c in COUNTRY_CAPITAL_COORDS],
                    text=[country_names.get(c, c) for c in codes if c in COUNTRY_CAPITAL_COORDS],
                    customdata=[["country", country_names.get(c, c), ", ".join(MENASA_COUNTRY_ALLIANCES[c]["memberships"])]
                                for c in codes if c in COUNTRY_CAPITAL_COORDS],
                    mode="markers+text", textposition="top center", textfont=dict(size=9),
                    marker=dict(size=9, color=BLOC_COLOR.get(bloc_name, TEXT_MUTED), line=dict(width=1, color=BG)),
                    hovertemplate="<b>%{text}</b><br>%{customdata[2]}<extra></extra>",
                    name=bloc_name, showlegend=True,
                ))

        if show_fabs:
            fabs = SEMICONDUCTOR_SUBDIVISIONS["advanced_sub7nm"]["fabs"]
            fig_geo.add_trace(go.Scattergeo(
                lon=[f["lon"] for f in fabs], lat=[f["lat"] for f in fabs],
                text=[f"{f['company']} — {f['site']}" for f in fabs],
                mode="markers", marker=dict(size=11, color="#0d9488", symbol="diamond", line=dict(width=1, color=BG)),
                hovertemplate="<b>%{text}</b><br>Advanced (sub-7nm) fab<extra></extra>",
                name="Advanced Fabs", showlegend=True,
            ))

        if show_ports:
            port_names = list(MAJOR_PORTS.keys())
            fig_geo.add_trace(go.Scattergeo(
                lon=[MAJOR_PORTS[k][1] for k in port_names],
                lat=[MAJOR_PORTS[k][0] for k in port_names],
                text=port_names, mode="markers",
                marker=dict(size=8, color=ACCENT2, symbol="hexagon", line=dict(width=1, color=BG)),
                hovertemplate="<b>%{text}</b><extra></extra>",
                name="Major Ports & Hubs", showlegend=True,
            ))

        if show_infra:
            cp_keys = list(MARITIME_CHOKEPOINTS.keys())
            fig_geo.add_trace(go.Scattergeo(
                lon=[MARITIME_CHOKEPOINTS[k]["lon"] for k in cp_keys],
                lat=[MARITIME_CHOKEPOINTS[k]["lat"] for k in cp_keys],
                text=[MARITIME_CHOKEPOINTS[k]["name"] for k in cp_keys],
                mode="markers+text", textposition="top center",
                marker=dict(
                    size=18,
                    color=[GEO_RISK_COLOR.get(MARITIME_CHOKEPOINTS[k]["risk_level"], TEXT_MUTED) for k in cp_keys],
                    line=dict(width=1.5, color=BG), symbol="circle",
                ),
                customdata=[["chokepoint", k, MARITIME_CHOKEPOINTS[k]["risk_level"]] for k in cp_keys],
                hovertemplate="<b>%{text}</b><br>Risk: %{customdata[2]}<extra></extra>",
                name="Chokepoints",
            ))

        _geo_lat_range, _geo_lon_range = [-10, 60], [-20, 130]
        fig_geo.add_trace(sea_label_trace(_geo_lat_range, _geo_lon_range))
        for _t in river_traces(_geo_lat_range, _geo_lon_range):
            fig_geo.add_trace(_t)
        fig_geo.update_geos(
            scope="world", projection_type="natural earth",
            lataxis_range=_geo_lat_range, lonaxis_range=_geo_lon_range,
            **MAP_BASE_STYLE,
        )
        fig_geo.update_layout(
            showlegend=show_countries or show_fabs or show_ports or show_infra,
            legend=dict(orientation="h", y=-0.05, font=dict(color=TEXT_MUTED, size=10), bgcolor="rgba(0,0,0,0)"),
        )

        geo_select = st.plotly_chart(
            style_chart(fig_geo, height=480), use_container_width=True,
            on_select="rerun", selection_mode="points", key="geoeconomic_map_select",
        )

        # Best-effort map-click filtering: a click on the chokepoint trace sets
        # session_state directly; a click on a country dot instead pre-selects
        # that country for the Country Deep Dive tab (same cross-navigation
        # pattern as the Risk Map). The customdata's own first element tags
        # which trace a click landed on, since both traces carry 2+/3-element
        # customdata otherwise indistinguishable by shape alone. The selectbox
        # just below is the reliable, always-available way to drive the
        # chokepoint filter, since multi-trace geo-chart click targeting is
        # inherently less robust than a single-trace map.
        if geo_select and geo_select.selection and geo_select.selection.get("points"):
            for pt in geo_select.selection["points"]:
                cd = pt.get("customdata")
                if not cd:
                    continue
                if cd[0] == "chokepoint":
                    st.session_state["geo_selected_chokepoint"] = cd[1]
                elif cd[0] == "country" and st.session_state.get("selected_country_from_map") != cd[1]:
                    # This tab (5) also runs after Country Deep Dive (tab 2) in
                    # script order -- same immediate-rerun fix as the Live
                    # Conflicts pills, guarded the same way against looping.
                    st.session_state["selected_country_from_map"] = cd[1]
                    st.rerun()

        st.caption(
            "Click a chokepoint marker, or use the dropdown below, to filter the Corporate Gatekeepers table "
            "to firms most exposed to it. Click a country dot to pre-select it in the Country Deep Dive tab "
            "above. Trade-artery line color and thickness reflect the highest sourced risk level among the "
            "chokepoints each route transits — routing is illustrative, not precise shipping-lane geometry; "
            "alliance and port/hub markers are simple annotations, not a scored dataset."
        )

        st.markdown("<br>", unsafe_allow_html=True)

        with st.expander("Chokepoint Briefing — what's actually happening at each one right now"):
            for key, cp in MARITIME_CHOKEPOINTS.items():
                st.markdown(
                    f'<div class="narrative-box" style="margin-bottom:0.9rem;"><b>{cp["name"]}</b> '
                    f'<span class="tier-badge" style="background:{GEO_RISK_COLOR.get(cp["risk_level"], TEXT_MUTED)}22;'
                    f'color:{GEO_RISK_COLOR.get(cp["risk_level"], TEXT_MUTED)};margin-left:0.4rem;">{cp["risk_level"]}</span>'
                    f'<br><br>{cp["notes"]}<br><br><i>{cp["annual_cargo_throughput"]}</i></div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    "".join(f'<a class="pill-link" href="{url}" target="_blank" rel="noopener noreferrer">{name} ↗</a>' for name, url in cp["sources"]),
                    unsafe_allow_html=True,
                )
                st.markdown("<br>", unsafe_allow_html=True)

        with st.expander("Deeper Verification Notes — semiconductor node tiers, energy flow granularity, UNCTAD"):
            st.caption(
                "A follow-up research pass checked whether more granular breakdowns (sour vs. sweet crude "
                "flow, a current TSMC-vs-Samsung sub-7nm split, a published semiconductor HHI) actually "
                "exist publicly. Several don't — stated here honestly as 'Data Pending Verification' rather "
                "than invented, per this project's core rule against fabricated or simulated figures."
            )
            sub7 = SEMICONDUCTOR_SUBDIVISIONS["advanced_sub7nm"]
            legacy = SEMICONDUCTOR_SUBDIVISIONS["mature_legacy_node"]
            st.markdown(
                f'<div class="narrative-box" style="margin-bottom:0.9rem;"><b>Advanced (Sub-7nm) Foundry</b>'
                f'<br><br>{sub7["note"]}</div>', unsafe_allow_html=True,
            )
            st.markdown(
                "".join(f'<a class="pill-link" href="{url}" target="_blank" rel="noopener noreferrer">{name} ↗</a>' for name, url in sub7["sources"]),
                unsafe_allow_html=True,
            )
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(
                f'<div class="narrative-box" style="margin-bottom:0.9rem;"><b>Mature/Legacy-Node Foundry</b> '
                f'— China: {legacy["china_share_2021_pct"]:.0f}% (2021) → {legacy["china_share_2030_projected_pct"]:.0f}% (2030 projected)'
                f'<br><br>{legacy["note"]}</div>', unsafe_allow_html=True,
            )
            st.markdown(
                "".join(f'<a class="pill-link" href="{url}" target="_blank" rel="noopener noreferrer">{name} ↗</a>' for name, url in legacy["sources"]),
                unsafe_allow_html=True,
            )
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f'<div class="narrative-box" style="margin-bottom:0.9rem;"><b>Semiconductor HHI</b><br><br>{SEMICONDUCTOR_SUBDIVISIONS["hhi_status"]}</div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(
                f'<div class="narrative-box" style="margin-bottom:0.9rem;"><b>Hormuz: Crude Grade &amp; LNG Flow</b>'
                f'<br><br>{ENERGY_FLOW_GRANULARITY["hormuz_crude_grade_note"]}<br><br>'
                f'<b>Post-war LNG status:</b> {ENERGY_FLOW_GRANULARITY["hormuz_lng_status"]["post_war_status"]}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                "".join(f'<a class="pill-link" href="{url}" target="_blank" rel="noopener noreferrer">{name} ↗</a>' for name, url in ENERGY_FLOW_GRANULARITY["hormuz_lng_status"]["sources"]),
                unsafe_allow_html=True,
            )

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(
                f'<div class="narrative-box"><b>UNCTAD Review of Maritime Transport</b><br><br>{UNCTAD_RMT_2025["edition"]}'
                f'<br><br>Global seaborne trade: <b>{UNCTAD_RMT_2025["global_seaborne_trade_2024_million_tons"]:,} million tons</b> in 2024 '
                f'(+{UNCTAD_RMT_2025["global_seaborne_trade_2024_growth_pct"]}% y/y). Ton-miles grew '
                f'+{UNCTAD_RMT_2025["ton_miles_growth_2024_pct"]}% — nearly 3x volume growth, reflecting Cape of Good Hope rerouting. '
                f'UNCTAD\'s own figure: Suez transit ran roughly {abs(UNCTAD_RMT_2025["suez_transit_vs_2023_pct"])}% below 2023 averages as of May 2025.'
                f'<br><br><i>Forward-looking (UNCTAD\'s own projection, not an observed outturn):</i> overall maritime trade growth of '
                f'{UNCTAD_RMT_2025["projections_labeled_as_projection_not_fact"]["2025_overall_growth_pct"]}% in 2025.</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                "".join(f'<a class="pill-link" href="{url}" target="_blank" rel="noopener noreferrer">{name} ↗</a>' for name, url in UNCTAD_RMT_2025["sources"]),
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)

    with geo_sub2:
        # ---- Component 2: Multi-Indicator Interdependence Matrix ----
        st.markdown('<div class="section-tag">The Structural Picture</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Multi-Indicator Interdependence Matrix</div>', unsafe_allow_html=True)

        mcol1, mcol2, mcol3 = st.columns(3)
        with mcol1:
            with st.container(border=True):
                st.markdown('<div class="section-tag">Supply Chain Concentration</div>', unsafe_allow_html=True)
                for key, m in CRITICAL_MINERAL_DEPENDENCIES.items():
                    share = m["global_market_share_pct"]
                    display = f"{share:.0f}%" if share is not None else "Unconfirmed"
                    sub = f"{m['dominant_country']} share" if share is not None else f"{m['dominant_country']} — sources don't reconcile, see notes"
                    stat_card(m["mineral"], display, sub)
                    st.markdown("<br>", unsafe_allow_html=True)
                st.caption("IEA/USGS don't publish a formal HHI for these specific commodities — market share is shown as the concentration signal instead of an invented HHI number.")
        with mcol2:
            with st.container(border=True):
                st.markdown('<div class="section-tag">Chokepoint Vulnerability</div>', unsafe_allow_html=True)
                for key, cp in MARITIME_CHOKEPOINTS.items():
                    if cp["latency_delay_days"] is not None:
                        value = f"{cp['latency_delay_days']:.0f}d added transit"
                    else:
                        value = "Effectively closed"
                    stat_card(cp["name"], value, f"Risk: {cp['risk_level']}")
                    st.markdown("<br>", unsafe_allow_html=True)
                st.caption("Hormuz shows no delay figure because it's a closure/blockade as of August 2026, not a rerouting scenario — see the map notes below.")
        with mcol3:
            with st.container(border=True):
                st.markdown('<div class="section-tag">Resource Sovereignty Buffers</div>', unsafe_allow_html=True)
                st.caption("How much slack exists outside the dominant supplier — lower share = more buffer.")
                buffer_rows = []
                for key, m in sorted(
                    CRITICAL_MINERAL_DEPENDENCIES.items(),
                    key=lambda kv: -(kv[1]["global_market_share_pct"] or 0),
                ):
                    share = m["global_market_share_pct"]
                    if share is None:
                        buffer_rows.append([m["mineral"], "Unconfirmed", "See notes"])
                        continue
                    tier = "Critical" if share >= 80 else ("High" if share >= 60 else ("Moderate" if share >= 40 else "Low"))
                    buffer_rows.append([m["mineral"], f"{share:.0f}%", tier])
                custom_table(buffer_rows, ["Mineral", "Share", "Concentration"])

        st.markdown("<br>", unsafe_allow_html=True)

        with st.expander("Mineral Concentration Context & Sources"):
            for key, m in CRITICAL_MINERAL_DEPENDENCIES.items():
                st.markdown(
                    f'<div class="narrative-box" style="margin-bottom:0.9rem;"><b>{m["mineral"]}</b> '
                    f'({m["dominant_country"]})<br><br>{m["context"]}</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    "".join(f'<a class="pill-link" href="{url}" target="_blank" rel="noopener noreferrer">{name} ↗</a>' for name, url in m["sources"]),
                    unsafe_allow_html=True,
                )
                st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

    with geo_sub3:
        # ---- Component 2b: Resource Benchmarks ----
        st.markdown('<div class="section-tag">What It Trades On, What It\'s Worth</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Resource Benchmarks</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="masthead-sub" style="margin-bottom:1rem;">Eight resources central to MENASA trade exposure — real exchange/benchmark, '
            'a sourced 2025-2026 price narrative, and the 5 largest companies in each. Live price history is only shown for the 3 resources with a real '
            'tradable futures ticker (Crude Oil, Natural Gas, Gold); the other 5 trade via bulk contracts or LME assessment rather than a public futures '
            'feed this app can pull, so their pricing is presented as sourced text instead of a fabricated chart.</div>',
            unsafe_allow_html=True,
        )
        resource_key = st.selectbox(
            "Select a resource", list(RESOURCE_BENCHMARKS.keys()),
            format_func=lambda k: RESOURCE_BENCHMARKS[k]["label"], key="geo_resource_select",
        )
        resource = RESOURCE_BENCHMARKS[resource_key]

        rcol1, rcol2 = st.columns([2, 1])
        with rcol1:
            if resource["yfinance_ticker"]:
                price_hist = fetch_stock_history(resource["yfinance_ticker"], period="5y")
                if price_hist is not None:
                    fig_res = go.Figure()
                    fig_res.add_trace(go.Scatter(
                        x=price_hist.index, y=price_hist["Close"], mode="lines",
                        line=dict(color=ACCENT, width=2), fill="tozeroy", fillcolor=ACCENT_DIM,
                    ))
                    st.plotly_chart(style_chart(fig_res, height=280), use_container_width=True)
                    st.caption(f"Real 5-year price history, ticker {resource['yfinance_ticker']} (live Yahoo Finance pull, cached hourly) — not a simulated or illustrative series.")
                else:
                    st.caption("Live price feed temporarily unavailable — Yahoo Finance is one of the least reliable external dependencies this app has.")
            else:
                st.caption(f"No live chart shown: {resource['label']} has no standard exchange-traded futures contract (see benchmark note) — a chart here would misrepresent bulk/contract pricing as if it were a continuous market feed.")
        with rcol2:
            st.markdown(
                f'<div class="narrative-box"><b>Benchmark</b><br>{resource["benchmark"]}</div>',
                unsafe_allow_html=True,
            )

        st.markdown(
            f'<div class="narrative-box" style="margin-top:0.8rem;"><b>Why the price has moved (2025-2026)</b><br>{resource["price_narrative"]}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            "".join(f'<a class="pill-link" href="{url}" target="_blank" rel="noopener noreferrer">{name} ↗</a>' for name, url in resource["sources"]),
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f'<div class="section-tag" style="font-size:0.9rem;">Top 5 Companies — {resource["label"]}</div>', unsafe_allow_html=True)
        top5_rows = [[c["company"], c["hq_location"], c["position"]] for c in resource["top_companies"]]
        custom_table(top5_rows, ["Company", "HQ Location", "Market Position"])
        st.caption("Sourced individually per company — hover isn't available in a plain table, so see the citation pills above for the resource-level sources; company-specific sources are in the underlying dataset.")

        st.markdown("<br>", unsafe_allow_html=True)

    with geo_sub4:
        # ---- Component 3: Corporate Infrastructure Gatekeepers ----
        st.markdown('<div class="section-tag">Who Controls The Bottleneck</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Corporate Infrastructure Gatekeepers</div>', unsafe_allow_html=True)

        filter_options = ["All"] + [MARITIME_CHOKEPOINTS[k]["name"] for k in MARITIME_CHOKEPOINTS] + \
                         [m["mineral"] for m in CRITICAL_MINERAL_DEPENDENCIES.values()]
        _default_filter = "All"
        _geo_sel = st.session_state.get("geo_selected_chokepoint")
        if _geo_sel and _geo_sel in MARITIME_CHOKEPOINTS:
            _default_filter = MARITIME_CHOKEPOINTS[_geo_sel]["name"]
        fcol, scol = st.columns([1, 1])
        with fcol:
            gatekeeper_filter = st.selectbox(
                "Filter by chokepoint or mineral dependency", filter_options,
                index=filter_options.index(_default_filter) if _default_filter in filter_options else 0,
            )
        with scol:
            gatekeeper_search = st.text_input("🔍 Filter by company, sector, or HQ", key="geo_gatekeeper_search")

        if gatekeeper_filter == "All":
            filtered_gatekeepers = CORPORATE_GATEKEEPERS
        else:
            cp_key_match = next((k for k, v in MARITIME_CHOKEPOINTS.items() if v["name"] == gatekeeper_filter), None)
            min_key_match = next((k for k, v in CRITICAL_MINERAL_DEPENDENCIES.items() if v["mineral"] == gatekeeper_filter), None)
            filtered_gatekeepers = [
                g for g in CORPORATE_GATEKEEPERS
                if (cp_key_match and cp_key_match in g["related_chokepoints"])
                or (min_key_match and min_key_match in g["related_minerals"])
            ]

        if gatekeeper_search.strip():
            needle = gatekeeper_search.strip().lower()
            filtered_gatekeepers = [
                g for g in filtered_gatekeepers
                if needle in g["company"].lower() or needle in g["hq_location"].lower() or needle in g["sector"].lower()
            ]

        if filtered_gatekeepers:
            gk_df = pd.DataFrame([
                {
                    "Company": g["company"],
                    "HQ Location": g["hq_location"],
                    "Sector": g["sector"],
                    "Market Share %": f"{g['market_share_pct']:.0f}%" if g["market_share_pct"] is not None else "Unconfirmed",
                    "Dependency Note": g["dependency_note"],
                    "Source": g["source"][0],
                }
                for g in filtered_gatekeepers
            ])
            st.dataframe(gk_df, use_container_width=True, hide_index=True)
        else:
            st.caption("No gatekeeper firms tagged to this filter yet.")

        st.caption(
            "Market Share % refers to each firm's share of its specific dominant niche (see Dependency Note), "
            "not overall company revenue. Read-only reference table — not editable, since it reflects sourced "
            "institutional data rather than user input."
        )

# ================= TAB 6: SCENARIO EXPLORER =================
SHOCK_PRESETS = {
    "Red Sea / Shipping Shock": {
        "weights": {
            "debt_to_gdp": 5, "current_account_pct_gdp": 20, "reserves_months_imports": 20,
            "gdp_growth": 10, "inflation": 15, "political_stability": 15,
            "government_effectiveness": 5, "rule_of_law": 5, "regulatory_quality": 0, "control_of_corruption": 5,
        },
        "rationale": (
            "Models a Bab el-Mandeb/Suez shipping disruption: overweights current account, reserves, "
            "and inflation (higher import costs pass through fast) and political stability (conflict-adjacent "
            "risk), while de-emphasizing longer-run institutional-quality factors that a shipping shock "
            "doesn't move on its own."
        ),
    },
    "Commodity Price Cycle": {
        "weights": {
            "debt_to_gdp": 15, "current_account_pct_gdp": 25, "reserves_months_imports": 15,
            "gdp_growth": 20, "inflation": 10, "political_stability": 5,
            "government_effectiveness": 5, "rule_of_law": 0, "regulatory_quality": 0, "control_of_corruption": 5,
        },
        "rationale": (
            "Models an oil/commodity terms-of-trade swing: overweights current account and GDP growth "
            "(the two factors a commodity cycle hits hardest and fastest for both exporters and importers), "
            "with debt sustainability following behind and governance factors weighted down."
        ),
    },
    "Capital Flight / Sudden Stop": {
        "weights": {
            "debt_to_gdp": 20, "current_account_pct_gdp": 10, "reserves_months_imports": 25,
            "gdp_growth": 5, "inflation": 5, "political_stability": 15,
            "government_effectiveness": 10, "rule_of_law": 5, "regulatory_quality": 0, "control_of_corruption": 5,
        },
        "rationale": (
            "Models an investor-confidence sudden stop: overweights reserves cover and debt sustainability "
            "(what a fleeing investor actually checks first) plus political and institutional stability, "
            "since capital flight is a confidence event more than a growth or inflation one."
        ),
    },
}

with tab6:
    st.markdown('<div class="section-tag">Interactive Reweighting</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Scenario Explorer</div>', unsafe_allow_html=True)
    st.markdown(
        "The default methodology weights all 10 factors equally (10% each). Adjust the sliders "
        "below to model a different risk appetite — e.g. a bank focused purely on debt "
        "sustainability, or a consultancy weighting governance more heavily — and watch the "
        "ranking update live. This does not change the saved default score anywhere else in the app."
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-tag">Geopolitical Shock Tester</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title" style="font-size:1.05rem;">Load a Shock Scenario</div>', unsafe_allow_html=True)
    preset_choice = st.selectbox(
        "Load a preset scenario",
        ["Custom / Manual"] + list(SHOCK_PRESETS.keys()),
        label_visibility="collapsed",
        key="preset_choice",
    )
    if preset_choice != st.session_state.get("_applied_preset"):
        if preset_choice in SHOCK_PRESETS:
            for f, w in SHOCK_PRESETS[preset_choice]["weights"].items():
                st.session_state[f"w_{f}"] = w
        st.session_state["_applied_preset"] = preset_choice
        st.rerun()

    if preset_choice in SHOCK_PRESETS:
        st.caption(SHOCK_PRESETS[preset_choice]["rationale"])

    st.markdown("<br>", unsafe_allow_html=True)

    slider_cols = st.columns(2)
    custom_weights = {}
    for i, (factor, label) in enumerate(FACTOR_LABELS.items()):
        with slider_cols[i % 2]:
            slider_key = f"w_{factor}"
            slider_kwargs = {"key": slider_key}
            if slider_key not in st.session_state:
                slider_kwargs["value"] = 10
            custom_weights[factor] = st.slider(label, 0, 100, **slider_kwargs)

    total_w = sum(custom_weights.values())
    st.markdown(f'<div class="stat-sub">Total weight: {total_w}% {"✓" if total_w == 100 else "(auto-normalized to 100%)"}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-tag">Live Result</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Re-Ranked Under Your Weights</div>', unsafe_allow_html=True)

    if total_w > 0:
        norm_weights = {f: w / total_w for f, w in custom_weights.items()}
        scenario_scores = []
        for _, drow in drivers.iterrows():
            available = {f: drow[f] for f in FACTOR_COLS if pd.notna(drow[f]) and norm_weights[f] > 0}
            if not available:
                scenario_scores.append(None)
                continue
            avail_w = {f: norm_weights[f] for f in available}
            tw = sum(avail_w.values())
            rescaled = {f: w / tw for f, w in avail_w.items()}
            score = sum(available[f] * rescaled[f] for f in available)
            scenario_scores.append(round(score, 1))

        scenario_df = drivers[["country"]].copy()
        scenario_df["scenario_score"] = scenario_scores
        scenario_df = scenario_df.dropna(subset=["scenario_score"]).sort_values("scenario_score", ascending=True)

        fig6 = px.bar(
            scenario_df, x="scenario_score", y="country", orientation="h",
            labels={"scenario_score": "Scenario Risk Score (0-100)", "country": ""},
            custom_data=["country"],
        )
        fig6.update_traces(marker_color=ACCENT)
        # Same fixed-vs-scaling-height fix as the Regional Overview ranking:
        # without enough vertical room per bar, Plotly quietly drops some
        # y-axis country labels rather than overlapping them.
        scenario_click = st.plotly_chart(
            style_chart(fig6, height=max(560, 22 * len(scenario_df))), use_container_width=True,
            on_select="rerun", selection_mode="points", key="scenario_rank_select",
        )
        st.caption("Click a bar to pre-select that country in the Country Deep Dive tab above.")
        if scenario_click and scenario_click.selection and scenario_click.selection.get("points"):
            # Explicit customdata (same mechanism as the Geo-Economic map's
            # click handler) rather than an undocumented "y" key.
            scenario_cd = scenario_click.selection["points"][0].get("customdata")
            # Tab 6 runs after Country Deep Dive (tab 2) in script order -- same
            # guarded-rerun fix as the Live Conflicts pills and Geo-Economic map.
            if scenario_cd and st.session_state.get("selected_country_from_map") != scenario_cd[0]:
                st.session_state["selected_country_from_map"] = scenario_cd[0]
                st.rerun()
    else:
        st.caption("Set at least one factor weight above zero to see a ranking.")

# ================= TAB 7: METHODOLOGY =================
with tab7:
    st.markdown("<div class=\"section-tag\">How It's Built</div>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">Methodology</div>', unsafe_allow_html=True)
    st.markdown(
        "Each country is scored **0–100** (100 = highest risk) on a weighted composite "
        "of 10 factors across two pillars, weighted equally at 10% by default — adjustable "
        "live in the Scenario Explorer tab:"
    )
    sourced_table(
        [
            ["Debt (% of GDP)", "Economic", "10%", ("World Bank WDI: GC.DOD.TOTL.GD.ZS", "https://data.worldbank.org/indicator/GC.DOD.TOTL.GD.ZS")],
            ["Current Account (% of GDP)", "Economic", "10%", ("World Bank WDI: BN.CAB.XOKA.GD.ZS", "https://data.worldbank.org/indicator/BN.CAB.XOKA.GD.ZS")],
            ["Reserves (months of imports)", "Economic", "10%", ("World Bank WDI: FI.RES.TOTL.MO", "https://data.worldbank.org/indicator/FI.RES.TOTL.MO")],
            ["GDP Growth", "Economic", "10%", ("World Bank WDI: NY.GDP.MKTP.KD.ZG", "https://data.worldbank.org/indicator/NY.GDP.MKTP.KD.ZG")],
            ["Inflation", "Economic", "10%", ("World Bank WDI: FP.CPI.TOTL.ZG", "https://data.worldbank.org/indicator/FP.CPI.TOTL.ZG")],
            ["Political Stability", "Governance", "10%", ("World Bank WGI: PV.EST", "https://databank.worldbank.org/metadataglossary/worldwide-governance-indicators/series/PV.EST")],
            ["Government Effectiveness", "Governance", "10%", ("World Bank WGI: GE.EST", "https://databank.worldbank.org/metadataglossary/worldwide-governance-indicators/series/GE.EST")],
            ["Rule of Law", "Governance", "10%", ("World Bank WGI: RL.EST", "https://databank.worldbank.org/metadataglossary/worldwide-governance-indicators/series/RL.EST")],
            ["Regulatory Quality", "Governance", "10%", ("World Bank WGI: RQ.EST", "https://databank.worldbank.org/metadataglossary/worldwide-governance-indicators/series/RQ.EST")],
            ["Control of Corruption", "Governance", "10%", ("World Bank WGI: CC.EST", "https://databank.worldbank.org/metadataglossary/worldwide-governance-indicators/series/CC.EST")],
        ],
        ["Factor", "Pillar", "Weight", "Source"],
    )
    st.caption(
        "All 10 factors are pulled live from the World Bank's public API (WDI = World Development "
        "Indicators, WGI = Worldwide Governance Indicators) — the same underlying database the IMF, "
        "credit rating agencies, and academic researchers use as a baseline. Click any source link "
        "above to see the indicator's full definition and country coverage on the World Bank's own site."
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.info(
        "**This is a relative ranking within this 34-country sample — not an absolute, "
        "globally-benchmarked index.** Every factor is min-max normalized against only the other "
        "33 tracked MENASA economies for that same year, not against the full ~190-country UN "
        "membership. A 'Lower Risk' score here means lower risk *relative to this specific regional "
        "pool* — it does not mean the country would also rank as low-risk against, say, Western "
        "Europe or East Asia. Comparing scores or tiers to any country outside this 34-country set "
        "(including via the credit-rating comparison elsewhere in this app, which draws on actual "
        "global agency ratings) requires that caveat in mind.",
        icon="📐",
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-tag">Context Only</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title" style="font-size:1.1rem;">Investment/Trade Context Indicators</div>', unsafe_allow_html=True)
    sourced_table(
        [
            ["FDI Net Inflows (% GDP)", ("World Bank WDI: BX.KLT.DINV.WD.GD.ZS", "https://data.worldbank.org/indicator/BX.KLT.DINV.WD.GD.ZS")],
            ["Exports of Goods & Services (% GDP)", ("World Bank WDI: NE.EXP.GNFS.ZS", "https://data.worldbank.org/indicator/NE.EXP.GNFS.ZS")],
            ["Imports of Goods & Services (% GDP)", ("World Bank WDI: NE.IMP.GNFS.ZS", "https://data.worldbank.org/indicator/NE.IMP.GNFS.ZS")],
            ["GDP (Current US$)", ("World Bank WDI: NY.GDP.MKTP.CD", "https://data.worldbank.org/indicator/NY.GDP.MKTP.CD")],
            ["GDP Per Capita (Current US$)", ("World Bank WDI: NY.GDP.PCAP.CD", "https://data.worldbank.org/indicator/NY.GDP.PCAP.CD")],
            ["Total Reserves (Current US$)", ("World Bank WDI: FI.RES.TOTL.CD", "https://data.worldbank.org/indicator/FI.RES.TOTL.CD")],
        ],
        ["Indicator", "Source"],
    )
    st.markdown(
        "Each factor is **min-max normalized to 0–100** relative to the other countries "
        "in the sample. If a country is missing a factor, that factor is dropped and the "
        "remaining weights are **rescaled proportionally** — missing data is never silently "
        "treated as \"safe.\" FDI (net inflows, % GDP) is tracked separately in each country's "
        "profile as descriptive investment context — it is intentionally **not** part of the "
        "risk score, since investment direction is not unambiguously a risk signal."
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-tag">Scope Notes</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Known Limitations</div>', unsafe_allow_html=True)
    st.markdown(
        """
- **Debt-to-GDP coverage is sparse** for several Gulf states and conflict/sanctions-affected
  countries — only 31 of 34 report it consistently, even after the IMF World Economic Outlook
  fallback fills some World Bank gaps.
- **Iran's score is lower-confidence** — only 7 of 10 factors are available, likely due to
  sanctions limiting fiscal data reporting.
- **The composite score is annual and backward-looking** — it will not reflect an event from the
  last few months (e.g. the February 2026 Iran war) until World Bank data catches up. See the
  Live Conflicts tab for the qualitative, currently-relevant complement to this gap.
- **Historical context is curated, not live** — the event list in each country's Deep Dive tab
  and the Live Conflicts tab were hand-researched and fact-checked via web search as of August
  2026, not pulled from a live news feed. They highlight major events but are not exhaustive.
- **Financing Arrangements now cover all 34 countries explicitly** — either a verified IMF/
  multilateral program (amount, approval date, status), or a sourced explanation of why none
  exists (net-creditor Gulf states with no IMF borrowing, or sanctions/arrears-blocked cases like
  Iran and Syria). Instrument-level bond/loan maturity schedules (a true "debt rollover wall") are
  still out of scope entirely — that needs a specialized debt database (Bloomberg, the IMF's
  sovereign debt investor relations portal, or national debt management offices), not a research
  pass over public web sources.
- **Key Economic Partners and Trade/Sector Profiles cover all 34 countries in comparable depth**
  — each entry now runs 5-8 sourced sentences covering creditors, major foreign investors, key
  allies/rivals, and at least one named recent (2024-2026) development, backed by 4-6 cited
  sources per country. Where a claim cites a specific figure or date, that figure has a named
  source; general economic structure (e.g. "Kuwait relies on oil exports") reflects well-
  established economic geography rather than requiring a single citation.
- **Major Economic Sanctions covers all 34 countries** — either the verified sanctions regimes a
  country has faced (imposing body, reason, current status, and economic impact where a real
  figure exists), or an explicit statement that none was found, rather than an empty section.
  FATF grey-listing (a financial-transparency watchlist) is deliberately distinguished from an
  actual sanction where relevant (e.g. Pakistan). This is a snapshot as of the research date, not
  a live feed — a sanctions regime can be imposed, modified, or lifted at any time (Syria's 2025
  sanctions rollback after Assad's fall is a recent example already reflected here).
- Weights are a transparent, reasonable starting point — not a backtested or econometrically
  validated model. Research/screening tool, not investment advice.
- **Built with AI assistance**, under the author's direction — both the code and the qualitative
  research were drafted with an AI assistant and fact-checked against the named sources shown
  throughout, each independently verifiable at the link given.
"""
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-tag">Rigor, Honestly Scoped</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Toward a Statistically Validated Model</div>', unsafe_allow_html=True)
    st.markdown(
        "Equal weighting is a deliberate starting point, not a claim that all 10 factors matter "
        "equally in reality. A real validation pass would run in two directions: **(1) redundancy** "
        "— principal component analysis across the 10 factors to check for multicollinearity (Government "
        "Effectiveness and Control of Corruption, both WGI dimensions, are the likeliest candidates to "
        "be capturing overlapping variance rather than independent signal), and **(2) predictive "
        "validity** — backtesting the composite score's year-over-year direction against realized "
        "sovereign actions (S&P/Moody's/Fitch upgrades and downgrades, actual defaults or restructurings) "
        "to test whether the score moved ahead of the event rather than merely alongside it, and, for the "
        "handful of these 34 economies with tradable sovereign debt, correlating the score against "
        "CDS spreads or bond yields as an independent, market-implied check.\n\n"
        "Neither the full PCA pass nor CDS/bond-yield correlation is done here, and that's a scope "
        "choice, not an oversight: true statistical backtesting needs point-in-time data vintages (the "
        "score as it would have looked *at the time*, not recomputed with data revised since), which the "
        "World Bank's API doesn't expose and this project doesn't warehouse; and reliable market pricing "
        "simply doesn't exist for most of these economies. This tool optimizes for transparency and "
        "reproducibility — anyone can see exactly why a score is what it is — over a fitted model whose "
        "weights would be harder to explain and easier to overfit on a region with this few, this "
        "volatile, historical observations.\n\n"
        "A lighter-weight check *is* possible with the data already on hand, though: did the score's own "
        "history actually move in the right direction around real, well-documented crises? That's what "
        "the section below tests."
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-tag">Did It Actually Work?</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Historical Validation Against Known Crises</div>', unsafe_allow_html=True)
    st.markdown(
        "Six well-documented, unambiguous crises, checked against this project's own historical scores "
        "(2010-2024) with no cherry-picking of only the successes — including one clear miss below. "
        "This tests direction and timing only: did the score rise (or fall) in the right year, not "
        "whether the exact magnitude is calibrated correctly."
    )

    VALIDATION_CASES = [
        {
            "code": "SYR", "label": "Syria — civil war escalation", "mark_years": [2011, 2012],
            "verdict_type": "success",
            "verdict": "The score jumped **+31.8 points in a single year** (2011→2012) — exactly when the "
                       "uprising escalated into full civil war. The sharpest, most immediate capture of any "
                       "case tested here: registered in the same year it happened, not with a lag.",
        },
        {
            "code": "LKA", "label": "Sri Lanka — 2022 economic collapse & default", "mark_years": [2022],
            "verdict_type": "success",
            "verdict": "The 2022 collapse (fuel/food shortages, mass protests, the president's ouster) shows "
                       "as a **+9.3 point jump in exactly that year** — and the recovery is captured too: the "
                       "score fell in both 2023 and 2024 as the 2023 IMF program took hold. Both the crisis "
                       "and the stabilization land in the correct years.",
        },
        {
            "code": "AFG", "label": "Afghanistan — 2021 Taliban takeover", "mark_years": [2021],
            "verdict_type": "success",
            "verdict": "The August 2021 regime change shows as a **+9.9 point jump in the same calendar "
                       "year** — a same-year capture of a sudden political shock, not a lagged one.",
        },
        {
            "code": "LBN", "label": "Lebanon — 2019-2023 financial collapse", "mark_years": [2019, 2020, 2021],
            "verdict_type": "lag",
            "verdict": "Protests began October 2019, but the score barely moved that year (it actually dipped "
                       "slightly). The real deterioration shows up starting **2020 and climbs every year "
                       "through 2023** — a real, sustained, correctly-directional capture of one of the worst "
                       "peacetime collapses in modern history, but with **roughly a one-year lag** from the "
                       "crisis's actual onset.",
        },
        {
            "code": "PAK", "label": "Pakistan — 2022-2023 balance-of-payments crisis", "mark_years": [2022, 2023],
            "verdict_type": "lag",
            "verdict": "The crisis built through 2022, but the score barely moved that year (+0.6). The bulk "
                       "of the increase (**+5.5**) landed in **2023**, the year the IMF program was actually "
                       "signed and the crisis was most acute — again roughly a one-year lag, followed by a "
                       "correct improvement in 2024 as the program took hold.",
        },
        {
            "code": "EGY", "label": "Egypt — 2022-2023 currency crisis", "mark_years": [2022, 2023],
            "verdict_type": "miss",
            "verdict": "**The clearest miss.** Egypt's currency crisis — the EGP devalued sharply multiple "
                       "times starting in 2022, with the IMF program expanded twice — barely registers: the "
                       "score actually *fell* in 2022, the crisis's most acute year. None of the 10 tracked "
                       "factors is an exchange-rate indicator by design (see the Economic/Macro gaps this "
                       "audit already surfaces), and that gap shows up directly here rather than being papered "
                       "over.",
        },
    ]
    VERDICT_COLOR = {"success": "#34d399", "lag": "#fbbf24", "miss": "#f87171"}
    VERDICT_TAG = {"success": "SAME-YEAR CAPTURE", "lag": "~1-YEAR LAG", "miss": "MISSED"}

    for case in VALIDATION_CASES:
        case_hist = history[history["country_code"] == case["code"]].sort_values("year")
        if case_hist.empty:
            continue
        vcol1, vcol2 = st.columns([1, 1])
        with vcol1:
            fig_val = go.Figure(go.Scatter(
                x=case_hist["year"], y=case_hist["risk_score"],
                mode="lines+markers", line=dict(color=ACCENT, width=2), marker=dict(size=5),
            ))
            for y in case["mark_years"]:
                if y in case_hist["year"].values:
                    fig_val.add_vline(x=y, line_dash="dot", line_color=VERDICT_COLOR[case["verdict_type"]], opacity=0.6)
            fig_val.update_layout(
                yaxis=dict(range=[0, 100], title="Risk Score"), xaxis=dict(title=None), showlegend=False,
            )
            st.plotly_chart(style_chart(fig_val, height=260), use_container_width=True)
        with vcol2:
            st.markdown(
                f'<span class="tier-badge" style="background:{VERDICT_COLOR[case["verdict_type"]]}22;'
                f'color:{VERDICT_COLOR[case["verdict_type"]]};">{VERDICT_TAG[case["verdict_type"]]}</span>'
                f'<div class="section-title" style="font-size:0.95rem;margin-top:0.4rem;">{case["label"]}</div>'
                f'<div class="narrative-box" style="margin-top:0.5rem;">{case["verdict"]}</div>',
                unsafe_allow_html=True,
            )
        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        "**Overall:** of these 6 cases, 3 captured the crisis in the same calendar year it happened "
        "(Syria, Sri Lanka, Afghanistan), 2 captured it correctly but roughly a year late (Lebanon, "
        "Pakistan) — consistent with this being annual, backward-looking data, not a live feed — and 1 "
        "missed it substantially (Egypt), specifically because no tracked factor captures exchange-rate "
        "shocks. That's exactly the kind of test a composite index should go through before anyone treats "
        "it as more than what it claims to be: a transparent screening tool, not an early-warning system."
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-tag">Beyond World Bank &amp; IMF</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Additional Sources Used</div>', unsafe_allow_html=True)
    st.markdown(
        "The 10-factor risk score is built primarily on World Bank data, with IMF World Economic "
        "Outlook debt figures used as an automatic fallback for the 13 countries where the World Bank "
        "has no debt-to-GDP figure on file (see below) — for consistency and reproducibility. The "
        "qualitative layers — Historical Context, Live Conflicts, Key Economic Partners, Trade/Sector "
        "Profiles, and Credit Ratings — draw on a much broader set of reputable sources, reflecting "
        "how real political risk research actually works: no single database covers conflict "
        "dynamics, trade relationships, credit ratings, *and* fiscal data at once."
    )
    custom_table(
        [
            ["News & wire services", "Reuters, Bloomberg, Al Jazeera, Associated Press, Times of Israel, France24, Middle East Eye"],
            ["Think tanks & policy research", "Brookings Institution, Council on Foreign Relations (CFR) Global Conflict Tracker, Center for Strategic and International Studies (CSIS), Carnegie Endowment, Atlantic Council, International Crisis Group, Belfer Center (Harvard), Chatham House, Stimson Center, Washington Institute, Soufan Center"],
            ["Government & multilateral bodies", "IMF press releases and World Economic Outlook database, US Congress.gov (CRS reports), UK House of Commons Library, UN Security Council Report, UNHCR/OCHA"],
            ["Encyclopedic reference", "Wikipedia (used as a starting point and cross-checked against primary sources, not a sole source), Britannica"],
            ["Economic/trade data", "CIA World Factbook, Observatory of Economic Complexity (OEC), UN Comtrade, EIA (energy)"],
            ["Credit rating agencies", "S&P Global Ratings, Moody's Ratings, Fitch Ratings (via countryeconomy.com aggregation, cross-checked against individual agency press coverage)"],
        ],
        ["Category", "Examples Used"],
    )
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        "".join(f'<a class="pill-link" href="{url}" target="_blank" rel="noopener noreferrer">{name} ↗</a>' for name, url in CREDIT_RATINGS_SOURCES),
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-tag">Sources</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Data &amp; Code</div>', unsafe_allow_html=True)
    st.markdown(
        '<a class="pill-link" href="https://data.worldbank.org/" target="_blank">World Bank Data ↗</a>'
        '<a class="pill-link" href="https://github.com/rafaywaqar2004-lang/overeign-risk-index" target="_blank">GitHub Repo ↗</a>',
        unsafe_allow_html=True,
    )

# ============================================================
# FOOTER
# ============================================================
st.markdown(
    '<div class="site-footer">Built by Muhammad Rafay Waqar &nbsp;·&nbsp; '
    '<a href="https://rafaywaqar2004-lang.github.io/rafaywaqar-portfolio/" target="_blank">portfolio</a> &nbsp;·&nbsp; '
    '<a href="https://github.com/rafaywaqar2004-lang/overeign-risk-index" target="_blank">source</a> &nbsp;·&nbsp; '
    "not investment advice.</div>",
    unsafe_allow_html=True,
)
