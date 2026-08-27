import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from context_data import HISTORICAL_CONTEXT, STOCK_EXCHANGES, LIVE_CONFLICTS, FINANCING_ARRANGEMENTS, KEY_ECONOMIC_PARTNERS, COUNTRY_TRADE_PROFILE, CREDIT_RATINGS, CREDIT_RATINGS_SOURCES
from pdf_export import generate_country_pdf

st.set_page_config(page_title="Sovereign Risk Scorecard", page_icon="📡", layout="wide")

# ============================================================
# DESIGN SYSTEM — "Analyst Terminal": dark, data-dense, monospace
# numerals, cyan accent. Deliberately distinct from the portfolio's
# editorial navy/gold/serif identity — this is a standalone product.
# ============================================================
BG = "#0a0e14"
SURFACE = "#111826"
SURFACE_ALT = "#161d2c"
BORDER = "rgba(148,163,184,0.14)"
ACCENT = "#22d3ee"
ACCENT_DIM = "rgba(34,211,238,0.10)"
TEXT = "#e6edf3"
TEXT_MUTED = "#7d8aa0"
TIER_COLORS = {
    "Lower Risk": "#34d399",
    "Moderate Risk": "#fbbf24",
    "Higher Risk": "#f87171",
    "Insufficient data": "#64748b",
}

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', -apple-system, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }}

    h1, h2, h3 {{ font-family: 'Inter', sans-serif !important; }}

    /* subtle depth instead of a flat background */
    [data-testid="stAppViewContainer"] > .main {{
        background: radial-gradient(ellipse 1400px 800px at 50% -10%, rgba(34,211,238,0.05), transparent),
                    linear-gradient(180deg, {BG} 0%, #0c1119 100%);
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
        font-size: 2.5rem;
        font-weight: 800;
        color: {TEXT};
        line-height: 1.1;
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
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.66rem;
        font-weight: 500;
        letter-spacing: 0.06em;
        color: {ACCENT};
        opacity: 0.85;
        margin-bottom: 0.4rem;
    }}
    .section-tag::before {{ content: "// "; opacity: 0.55; }}
    .section-title {{
        font-family: 'Inter', sans-serif;
        font-size: 1.3rem;
        font-weight: 700;
        color: {TEXT};
        margin-bottom: 1.1rem;
        letter-spacing: -0.01em;
    }}

    /* ---- stat cards ---- */
    .stat-card {{
        background: linear-gradient(160deg, {SURFACE_ALT} 0%, {SURFACE} 100%);
        border: 1px solid {BORDER};
        border-left: 3px solid {ACCENT};
        border-radius: 12px;
        padding: 1.15rem 1.4rem;
        height: 100%;
        box-shadow: 0 4px 16px rgba(0,0,0,0.24);
        transition: transform 0.18s ease, box-shadow 0.18s ease;
    }}
    .stat-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.32);
    }}
    .stat-label {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.62rem;
        font-weight: 500;
        letter-spacing: 0.09em;
        text-transform: uppercase;
        color: {TEXT_MUTED};
        margin-bottom: 0.55rem;
    }}
    .stat-value {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.65rem;
        font-weight: 700;
        color: {TEXT};
        line-height: 1.15;
    }}
    .stat-sub {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.76rem;
        color: {ACCENT};
        margin-top: 0.45rem;
    }}

    /* ---- narrative callout ---- */
    .narrative-box {{
        background: linear-gradient(135deg, {ACCENT_DIM} 0%, rgba(34,211,238,0.04) 100%);
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
        border-bottom: 1px solid rgba(255,255,255,0.04);
        color: {TEXT};
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.82rem;
        transition: background 0.12s ease;
    }}
    .custom-table tr:last-child td {{ border-bottom: none; }}
    .custom-table tr:hover td {{ background: rgba(34,211,238,0.05); }}

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
        box-shadow: 0 2px 10px rgba(34,211,238,0.18);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }}
    .pill-link:hover {{
        transform: translateY(-1px);
        box-shadow: 0 4px 16px rgba(34,211,238,0.3);
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


def stat_card(label, value, sub=None):
    sub_html = f'<div class="stat-sub">{sub}</div>' if sub else ""
    st.markdown(
        f'<div class="stat-card"><div class="stat-label">{label}</div>'
        f'<div class="stat-value">{value}</div>{sub_html}</div>',
        unsafe_allow_html=True,
    )


def custom_table(rows, headers):
    html = '<table class="custom-table"><thead><tr>'
    html += "".join(f"<th>{h}</th>" for h in headers)
    html += "</tr></thead><tbody>"
    for row in rows:
        html += "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>"
    html += "</tbody></table>"
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
    )
    fig.update_xaxes(gridcolor="rgba(148,163,184,0.10)", zerolinecolor="rgba(148,163,184,0.16)")
    fig.update_yaxes(gridcolor="rgba(148,163,184,0.10)", zerolinecolor="rgba(148,163,184,0.16)")
    return fig


def sourced_table(rows, headers):
    """Like custom_table, but the last column of each row is rendered as a link."""
    html = '<table class="custom-table"><thead><tr>'
    html += "".join(f"<th>{h}</th>" for h in headers)
    html += "</tr></thead><tbody>"
    for row in rows:
        cells = row[:-1]
        source_name, source_url = row[-1]
        html += "<tr>" + "".join(f"<td>{c}</td>" for c in cells)
        html += f'<td><a href="{source_url}" target="_blank" rel="noopener noreferrer" style="color:{ACCENT};">{source_name} ↗</a></td></tr>'
    html += "</tbody></table>"
    st.markdown(html, unsafe_allow_html=True)


def build_country_brief(country_name, country_code, row, driver_row, events, conflicts):
    """Synthesizes score + trajectory + top historical events + conflict exposure
    into a flowing analyst-style paragraph that explains *why* the score is what
    it is and *where it's headed*, rather than stating disconnected facts."""
    parts = []

    score = row.get("risk_score")
    tier = row.get("risk_tier", "").lower()
    rank = row.get("risk_rank")
    n_countries = 26
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
            link_clause = (
                f" — consistent with {most_recent[1][0].lower()}{most_recent[1][1:]} ({most_recent[0]}), "
                f"which is still working through the economy"
            )
        parts.append(
            f"The single largest driver of that score is <b>{top_risk}</b>{link_clause}, while "
            f"<b>{top_strength}</b> stands out as its strongest relative pillar."
        )

    if events:
        recent_events = sorted(events, key=lambda e: e[0], reverse=True)[:2]
        event_phrases = [f"{e[1][0].lower()}{e[1][1:]} ({e[0]})" for e in recent_events]
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


# ============================================================
# DATA
# ============================================================
scored = pd.read_csv("scored_data.csv")
history = pd.read_csv("scored_history.csv")
drivers = pd.read_csv("driver_data.csv")
long_df = pd.read_csv("raw_data_long.csv")

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

try:
    with open("last_refreshed.txt") as f:
        LAST_REFRESHED = f.read().strip()
except FileNotFoundError:
    LAST_REFRESHED = "unknown"

# ============================================================
# MASTHEAD
# ============================================================
st.markdown('<div class="tag-label">SOVEREIGN-RISK/v4 · FULL MENASA COVERAGE</div>', unsafe_allow_html=True)
st.markdown('<div class="masthead-title">Sovereign Risk <span>Scorecard</span></div>', unsafe_allow_html=True)
st.markdown(
    '<div class="masthead-sub">A composite risk score for all 26 MENA &amp; South Asia economies, '
    'built on live World Bank data across 10 factors spanning economic and governance pillars, '
    'with curated and sourced historical context, a live scenario-weighting explorer, and a '
    'dedicated tracker for the region\'s most consequential live conflicts.</div>',
    unsafe_allow_html=True,
)
st.markdown(f'<div class="stat-sub" style="margin-bottom:1.2rem;">DATA_LAST_REFRESHED: {LAST_REFRESHED}</div>', unsafe_allow_html=True)

# ============================================================
# TOP-LINE STAT ROW
# ============================================================
valid_scores = scored.dropna(subset=["risk_score"])
highest = valid_scores.iloc[0]
lowest = valid_scores.sort_values("risk_score").iloc[0]

c1, c2, c3, c4 = st.columns(4)
with c1:
    stat_card("Countries Covered", len(scored), "MENA + South Asia")
with c2:
    stat_card("Highest Risk", highest["country"], f"Score {highest['risk_score']:.1f}")
with c3:
    stat_card("Lowest Risk", lowest["country"], f"Score {lowest['risk_score']:.1f}")
with c4:
    stat_card("Regional Average", f"{valid_scores['risk_score'].mean():.1f}", "Across all 26")

st.markdown("<br>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["REGIONAL_OVERVIEW", "COUNTRY_DEEP_DIVE", "LIVE_CONFLICTS", "SCENARIO_EXPLORER", "METHODOLOGY"])

# ================= TAB 1: OVERVIEW =================
with tab1:
    st.markdown('<div class="section-tag">GEOGRAPHIC_DISTRIBUTION</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Risk Map</div>', unsafe_allow_html=True)
    map_df = scored.dropna(subset=["risk_score"])
    map_fig = px.choropleth(
        map_df, locations="country_code", locationmode="ISO-3", color="risk_score",
        hover_name="country", hover_data={"country_code": False, "risk_score": ":.1f", "risk_tier": True},
        color_continuous_scale=["#34d399", "#fbbf24", "#f87171"], range_color=(0, 100),
        labels={"risk_score": "Risk Score"},
    )
    map_fig.update_geos(
        scope="world", lataxis_range=[-5, 42], lonaxis_range=[-12, 100],
        bgcolor="rgba(0,0,0,0)", showcountries=True, countrycolor="rgba(148,163,184,0.25)",
        showland=True, landcolor="#161d2c", showocean=True, oceancolor="#0a0e14",
        showframe=False,
    )
    map_fig.update_layout(margin=dict(t=10, b=10, l=10, r=10))
    st.plotly_chart(style_chart(map_fig, height=420), use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown('<div class="section-tag">RANKED_ALL_26</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Risk Ranking</div>', unsafe_allow_html=True)
        chart_df = scored.dropna(subset=["risk_score"]).sort_values("risk_score", ascending=True)
        fig = px.bar(
            chart_df, x="risk_score", y="country", orientation="h",
            color="risk_tier", color_discrete_map=TIER_COLORS, text="risk_score",
            labels={"risk_score": "Risk Score (0-100)", "country": ""},
        )
        fig.update_traces(texttemplate="%{text:.1f}", textposition="outside")
        fig.update_layout(showlegend=True, legend_title_text="")
        st.plotly_chart(style_chart(fig, height=560), use_container_width=True)

    with col2:
        with st.container(border=True):
            st.markdown('<div class="section-tag">LEGEND</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-title" style="font-size:1rem;">Reading the Scores</div>', unsafe_allow_html=True)
            st.markdown(tier_badge_html("Lower Risk") + " score &lt; 33", unsafe_allow_html=True)
            st.markdown("<br>" + tier_badge_html("Moderate Risk") + " score 33–66", unsafe_allow_html=True)
            st.markdown("<br>" + tier_badge_html("Higher Risk") + " score &gt; 66", unsafe_allow_html=True)
            st.markdown("<br>" + tier_badge_html("Insufficient data") + " &lt; 2 of 10 factors", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        with st.container(border=True):
            st.markdown('<div class="section-tag">BY_SUBREGION</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-title" style="font-size:1rem;">Regional Snapshot</div>', unsafe_allow_html=True)
            gulf = scored[scored["country_code"].isin(["SAU", "ARE", "KWT", "QAT", "BHR", "OMN"])]["risk_score"].mean()
            north_africa = scored[scored["country_code"].isin(["DZA", "EGY", "LBY", "MAR", "TUN"])]["risk_score"].mean()
            levant_iraq = scored[scored["country_code"].isin(["JOR", "LBN", "SYR", "ISR", "IRQ"])]["risk_score"].mean()
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
    st.markdown('<div class="section-tag">2010_2024</div>', unsafe_allow_html=True)
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

# ================= TAB 2: COUNTRY DEEP DIVE =================
with tab2:
    country_list = scored.sort_values("country")["country"].tolist()
    selected = st.selectbox("Select a country", country_list, label_visibility="collapsed")

    row = scored[scored["country"] == selected].iloc[0]
    driver_row = drivers[drivers["country"] == selected].iloc[0]
    country_code = row["country_code"]
    events = HISTORICAL_CONTEXT.get(country_code, [])

    st.markdown('<div class="section-tag">ANALYST_BRIEF</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Country Brief</div>', unsafe_allow_html=True)
    brief_text = build_country_brief(selected, country_code, row, driver_row, events, LIVE_CONFLICTS)
    st.markdown(f'<div class="narrative-box">{brief_text}</div>', unsafe_allow_html=True)

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
    )
    st.download_button(
        label=f"Download {selected} Brief (PDF)",
        data=pdf_bytes,
        file_name=f"{selected.replace(' ', '_')}_Sovereign_Risk_Brief.pdf",
        mime="application/pdf",
    )
    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns([1, 2])
    with c1:
        with st.container(border=True):
            st.markdown('<div class="section-tag">COMPOSITE_SCORE</div>', unsafe_allow_html=True)
            score_display = f"{row['risk_score']:.1f}" if pd.notna(row["risk_score"]) else "N/A"
            st.markdown(f'<div class="stat-value" style="font-size:2.1rem;">{score_display}</div>', unsafe_allow_html=True)
            st.markdown(tier_badge_html(row["risk_tier"]), unsafe_allow_html=True)
            st.caption(f"Based on {int(row['risk_score_factors_used'])} of 10 factors")

            rank_col, yoy_col = st.columns(2)
            with rank_col:
                st.markdown(
                    f'<div class="stat-label" style="margin-top:0.6rem;">Regional Rank</div>'
                    f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:1.1rem;color:{ACCENT};">'
                    f'{int(row["risk_rank"])} / 26</div>',
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

        st.markdown("<br>", unsafe_allow_html=True)

        with st.container(border=True):
            st.markdown('<div class="section-tag">SANITY_CHECK</div>', unsafe_allow_html=True)
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
                f'<div class="narrative-box"><b>KEY_DRIVERS</b><br>{selected}\'s risk profile is driven '
                f'primarily by <b>{risk_names}</b>, while <b>{strength_name}</b> is a relative strength.</div>',
                unsafe_allow_html=True,
            )

    with c2:
        st.markdown('<div class="section-tag">ALL_10_FACTORS</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Risk Factor Breakdown</div>', unsafe_allow_html=True)
        radar_factors = [f for f in FACTOR_COLS if pd.notna(driver_row[f])]
        radar_values = [driver_row[f] for f in radar_factors]
        radar_labels = [FACTOR_LABELS[f] for f in radar_factors]

        if radar_factors:
            fig3 = go.Figure()
            fig3.add_trace(go.Scatterpolar(
                r=radar_values + [radar_values[0]],
                theta=radar_labels + [radar_labels[0]],
                fill="toself", fillcolor="rgba(34,211,238,0.18)",
                line=dict(color=ACCENT, width=2),
            ))
            fig3.update_layout(
                polar=dict(
                    bgcolor="rgba(0,0,0,0)",
                    radialaxis=dict(visible=True, range=[0, 100], gridcolor="rgba(148,163,184,0.12)", color=TEXT_MUTED),
                    angularaxis=dict(gridcolor="rgba(148,163,184,0.12)", color=TEXT),
                ),
                showlegend=False,
            )
            st.plotly_chart(style_chart(fig3, height=380), use_container_width=True)
        else:
            st.caption("No factor data available for radar chart.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f'<div class="section-tag">2010_2024</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{selected}: Risk Score Over Time</div>', unsafe_allow_html=True)
    country_history = history[history["country"] == selected].sort_values("year")
    if not country_history.empty:
        fig4 = px.line(country_history, x="year", y="risk_score", markers=True)
        fig4.update_traces(line_color=ACCENT, marker=dict(color=ACCENT, size=7))
        st.plotly_chart(style_chart(fig4, height=320), use_container_width=True)
    else:
        st.caption("Not enough historical data for a trend line.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-tag">RAW_VALUES</div>', unsafe_allow_html=True)
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
    st.markdown('<div class="section-tag">CURATED_AND_SOURCED</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Key Historical Context</div>', unsafe_allow_html=True)
    if events:
        st.markdown(
            f"The table below traces the major economic, political, and conflict-driven events that "
            f"have shaped {selected}'s risk profile, each fact-checked against the linked primary or "
            f"news source. This is deliberately broader than pure macro data — a debt figure alone "
            f"doesn't explain *why* reserves fell or *why* a currency collapsed; these events do."
        )
        sourced_rows = [[str(year), event, (src_name, src_url)] for year, event, src_name, src_url in events]
        sourced_table(sourced_rows, ["Year", "Event", "Source"])
        st.caption("Curated highlights fact-checked via web search against primary/news sources as of Aug 2026 — not a live feed.")
    else:
        st.caption("No curated events on file for this country yet.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-tag">WHAT_THE_ECONOMY_RUNS_ON</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Key Sectors &amp; Trade Profile</div>', unsafe_allow_html=True)
    trade_profile = COUNTRY_TRADE_PROFILE.get(country_code)
    if trade_profile:
        custom_table(
            [
                ["Main Sectors", trade_profile["sectors"]],
                ["Biggest Exports", trade_profile["exports"]],
                ["Biggest Imports", trade_profile["imports"]],
                ["Leading Trade Partners", trade_profile["partners"]],
            ],
            ["Category", "Detail"],
        )
        st.caption(
            "Compiled from established, stable economic-geography knowledge (the kind found in the "
            "CIA World Factbook and the Observatory of Economic Complexity / UN Comtrade) rather than "
            "a single per-country citation — see Methodology for the full source list. Share figures "
            "are directional, not precise-to-the-decimal statistics."
        )
    else:
        st.caption("No trade/sector profile on file for this country yet.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-tag">TRADE_AND_INVESTMENT</div>', unsafe_allow_html=True)
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
        st.markdown('<div class="section-tag">REFERENCE</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title" style="font-size:1.05rem;">Primary Market</div>', unsafe_allow_html=True)
        exchange, index = STOCK_EXCHANGES.get(country_code, ("N/A", "N/A"))
        custom_table([["Exchange", exchange], ["Benchmark Index", index]], ["Field", "Value"])
        st.caption("Reference only — not live pricing.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-tag">WHO_ITS_BORROWED_FROM</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Financing Arrangements</div>', unsafe_allow_html=True)
    st.markdown(
        "Verified IMF/multilateral financing arrangements for this country — amount, approval date, "
        "and program length. *Instrument-level Eurobond and bilateral-loan maturity schedules are out "
        "of scope; see Methodology for the full coverage note.*"
    )
    arrangements = FINANCING_ARRANGEMENTS.get(country_code)
    if arrangements:
        arr_rows = [[a["program"], a["amount"], a["approved"], a["status"]] for a in arrangements]
        custom_table(arr_rows, ["Program", "Amount", "Approved", "Status"])
    else:
        st.caption("No verified arrangement on file for this country — see Methodology for scope.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-tag">WHO_INVESTS_WHO_LENDS</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Key Economic Partners</div>', unsafe_allow_html=True)
    partner_info = KEY_ECONOMIC_PARTNERS.get(country_code)
    if partner_info:
        st.markdown(f'<div class="narrative-box">{partner_info["summary"]}</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        for name, url in partner_info["sources"]:
            st.markdown(f'<a class="pill-link" href="{url}" target="_blank" rel="noopener noreferrer">{name} ↗</a>', unsafe_allow_html=True)
    else:
        st.caption(
            "No independently verified creditor/investor/trade-partner summary on file for this "
            "country yet — this section is deliberately scoped to cases with solid sourcing rather "
            "than filled in with unverified claims. See Methodology for the full scope note."
        )

# ================= TAB 3: LIVE CONFLICTS =================
with tab3:
    st.markdown('<div class="section-tag">CURATED_AND_SOURCED_NOT_LIVE_FEED</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Live Conflicts &amp; Regional Flashpoints</div>', unsafe_allow_html=True)
    st.markdown(
        "The 10-factor composite score above is built on **annual** World Bank data, which by nature "
        "lags acute, fast-moving events — a war that started two months ago won't yet show up in a "
        "debt-to-GDP or governance figure. This tab is the qualitative complement: the region's most "
        "consequential live conflicts and flashpoints, each mapped to the specific tracked countries "
        "it affects, with sourced detail on market/trade impact. **Curated and fact-checked as of "
        "August 2026 — not a live news feed**, and ranked here roughly by breadth of economic impact "
        "across tracked countries."
    )
    st.markdown("<br>", unsafe_allow_html=True)

    code_to_name = dict(zip(scored["country_code"], scored["country"]))

    for i, conflict in enumerate(LIVE_CONFLICTS):
        with st.container(border=True):
            st.markdown(
                f'<div class="section-tag">{conflict["status"].upper()}</div>'
                f'<div class="section-title" style="font-size:1.25rem;">{conflict["name"]}</div>',
                unsafe_allow_html=True,
            )
            affected_names = [code_to_name.get(c, c) for c in conflict["affected"]]
            st.markdown(
                "<div style='margin-bottom:0.8rem;'>" +
                "".join(f'<span class="tier-badge" style="background:rgba(34,211,238,0.12);color:{ACCENT};margin-right:0.4rem;">{n}</span>' for n in affected_names) +
                "</div>",
                unsafe_allow_html=True,
            )
            if conflict.get("groups"):
                st.markdown(
                    f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:0.78rem;color:{TEXT_MUTED};margin-bottom:0.8rem;">'
                    f'<b style="color:{ACCENT};">GROUPS INVOLVED:</b> {conflict["groups"]}</div>',
                    unsafe_allow_html=True,
                )
            st.markdown(f'<div class="narrative-box"><b>SUMMARY</b><br>{conflict["summary"]}</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f'<div class="narrative-box"><b>MARKET_&amp;_TRADE_IMPACT</b><br>{conflict["market_impact"]}</div>', unsafe_allow_html=True)
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
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(
                "".join(f'<a class="pill-link" href="{url}" target="_blank" rel="noopener noreferrer">{name} ↗</a>' for name, url in conflict["sources"]),
                unsafe_allow_html=True,
            )
        if i < len(LIVE_CONFLICTS) - 1:
            st.markdown("<br>", unsafe_allow_html=True)

# ================= TAB 4: SCENARIO EXPLORER =================
with tab4:
    st.markdown('<div class="section-tag">INTERACTIVE_REWEIGHTING</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Scenario Explorer</div>', unsafe_allow_html=True)
    st.markdown(
        "The default methodology weights all 10 factors equally (10% each). Adjust the sliders "
        "below to model a different risk appetite — e.g. a bank focused purely on debt "
        "sustainability, or a consultancy weighting governance more heavily — and watch the "
        "ranking update live. This does not change the saved default score anywhere else in the app."
    )
    st.markdown("<br>", unsafe_allow_html=True)

    slider_cols = st.columns(2)
    custom_weights = {}
    for i, (factor, label) in enumerate(FACTOR_LABELS.items()):
        with slider_cols[i % 2]:
            custom_weights[factor] = st.slider(label, 0, 100, 10, key=f"w_{factor}")

    total_w = sum(custom_weights.values())
    st.markdown(f'<div class="stat-sub">Total weight: {total_w}% {"✓" if total_w == 100 else "(auto-normalized to 100%)"}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-tag">LIVE_RESULT</div>', unsafe_allow_html=True)
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
        )
        fig6.update_traces(marker_color=ACCENT)
        st.plotly_chart(style_chart(fig6, height=560), use_container_width=True)
    else:
        st.caption("Set at least one factor weight above zero to see a ranking.")

# ================= TAB 5: METHODOLOGY =================
with tab5:
    st.markdown('<div class="section-tag">HOW_ITS_BUILT</div>', unsafe_allow_html=True)
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
    st.markdown('<div class="section-tag">CONTEXT_ONLY</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title" style="font-size:1.1rem;">Investment/Trade Context Indicators</div>', unsafe_allow_html=True)
    sourced_table(
        [
            ["FDI Net Inflows (% GDP)", ("World Bank WDI: BX.KLT.DINV.WD.GD.ZS", "https://data.worldbank.org/indicator/BX.KLT.DINV.WD.GD.ZS")],
            ["Exports of Goods & Services (% GDP)", ("World Bank WDI: NE.EXP.GNFS.ZS", "https://data.worldbank.org/indicator/NE.EXP.GNFS.ZS")],
            ["Imports of Goods & Services (% GDP)", ("World Bank WDI: NE.IMP.GNFS.ZS", "https://data.worldbank.org/indicator/NE.IMP.GNFS.ZS")],
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
    st.markdown('<div class="section-tag">V4</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Known Limitations</div>', unsafe_allow_html=True)
    st.markdown(
        """
- **Debt-to-GDP coverage is sparse** for several Gulf states and conflict/sanctions-affected
  countries — only 11 of 26 report it consistently to the World Bank. A future improvement would
  add IMF World Economic Outlook debt data as a fallback source.
- **Iran's score is lower-confidence** — only 7 of 10 factors are available, likely due to
  sanctions limiting fiscal data reporting.
- **The composite score is annual and backward-looking** — it will not reflect an event from the
  last few months (e.g. the February 2026 Iran war) until World Bank data catches up. See the
  Live Conflicts tab for the qualitative, currently-relevant complement to this gap.
- **Historical context is curated, not live** — the event list in each country's Deep Dive tab
  and the Live Conflicts tab were hand-researched and fact-checked via web search as of August
  2026, not pulled from a live news feed. They highlight major events but are not exhaustive.
- **Financing Arrangements coverage is partial by design** — 12 of 26 countries have a verified
  IMF/multilateral arrangement or explicit "net creditor" note on file. The rest simply weren't
  independently confirmed in this research pass, rather than assumed to have none. Instrument-level
  bond/loan maturity schedules (a true "debt rollover wall") are out of scope entirely — that needs
  a specialized debt database (Bloomberg, the IMF's sovereign debt investor relations portal, or
  national debt management offices), not a research pass over public web sources.
- **Key Economic Partners and Trade/Sector Profiles now cover all 26 countries**, but at varying
  depth — some entries (Pakistan, Sri Lanka, Egypt) are backed by multiple named, dated sources;
  others rely more on general reference material where a specific news event wasn't available.
  Where a claim cites a specific figure or date, that figure has a named source; general economic
  structure (e.g. "Kuwait relies on oil exports") reflects well-established economic geography
  rather than requiring a single citation.
- Weights are a transparent, reasonable starting point — not a backtested or econometrically
  validated model. Research/screening tool, not investment advice.
"""
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-tag">BEYOND_WORLD_BANK_AND_IMF</div>', unsafe_allow_html=True)
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
    st.markdown('<div class="section-tag">SOURCES</div>', unsafe_allow_html=True)
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
    '<div class="site-footer">BUILT_BY: Muhammad Rafay Waqar &nbsp;·&nbsp; '
    '<a href="https://rafaywaqar2004-lang.github.io/rafaywaqar-portfolio/" target="_blank">portfolio</a> &nbsp;·&nbsp; '
    '<a href="https://github.com/rafaywaqar2004-lang/overeign-risk-index" target="_blank">source</a> &nbsp;·&nbsp; '
    "not investment advice.</div>",
    unsafe_allow_html=True,
)
