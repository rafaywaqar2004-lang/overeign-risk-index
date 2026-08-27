import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from context_data import HISTORICAL_CONTEXT, STOCK_EXCHANGES

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
    }}

    h1, h2, h3 {{ font-family: 'Inter', sans-serif !important; }}

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
        line-height: 1.6;
        margin-bottom: 1.4rem;
    }}
    .section-tag {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.66rem;
        font-weight: 500;
        letter-spacing: 0.05em;
        color: {ACCENT};
        margin-bottom: 0.35rem;
    }}
    .section-tag::before {{ content: "// "; opacity: 0.6; }}
    .section-title {{
        font-family: 'Inter', sans-serif;
        font-size: 1.3rem;
        font-weight: 700;
        color: {TEXT};
        margin-bottom: 1rem;
        letter-spacing: -0.01em;
    }}

    /* ---- stat cards ---- */
    .stat-card {{
        background: {SURFACE};
        border: 1px solid {BORDER};
        border-left: 2px solid {ACCENT};
        border-radius: 2px;
        padding: 1rem 1.25rem;
        height: 100%;
    }}
    .stat-label {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.62rem;
        font-weight: 500;
        letter-spacing: 0.09em;
        text-transform: uppercase;
        color: {TEXT_MUTED};
        margin-bottom: 0.5rem;
    }}
    .stat-value {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.65rem;
        font-weight: 700;
        color: {TEXT};
        line-height: 1.1;
    }}
    .stat-sub {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.76rem;
        color: {ACCENT};
        margin-top: 0.4rem;
    }}

    /* ---- narrative callout ---- */
    .narrative-box {{
        background: {ACCENT_DIM};
        border-left: 2px solid {ACCENT};
        padding: 1rem 1.3rem;
        font-size: 0.9rem;
        line-height: 1.65;
        color: {TEXT};
        border-radius: 0 2px 2px 0;
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
        padding: 0.28rem 0.65rem;
        border-radius: 2px;
        margin-top: 0.4rem;
    }}

    /* ---- custom html table ---- */
    .custom-table {{
        width: 100%;
        border-collapse: collapse;
        font-size: 0.85rem;
        margin-bottom: 1rem;
    }}
    .custom-table th {{
        text-align: left;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.64rem;
        font-weight: 500;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: {ACCENT};
        border-bottom: 1px solid {BORDER};
        padding: 0.6rem 0.8rem;
    }}
    .custom-table td {{
        padding: 0.6rem 0.8rem;
        border-bottom: 1px solid rgba(255,255,255,0.04);
        color: {TEXT};
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.82rem;
    }}
    .custom-table tr:last-child td {{ border-bottom: none; }}
    .custom-table tr:hover td {{ background: rgba(34,211,238,0.04); }}

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
        padding: 0.55rem 1.1rem;
        border-radius: 2px;
        text-decoration: none !important;
        margin-right: 0.75rem;
        margin-bottom: 0.5rem;
    }}

    /* ---- streamlit widget overrides ---- */
    [data-testid="stTabs"] button[role="tab"] {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.76rem;
        font-weight: 500;
        letter-spacing: 0.04em;
    }}
    [data-testid="stAlert"] {{
        background: {ACCENT_DIM} !important;
        border-left: 2px solid {ACCENT} !important;
        border-radius: 0 2px 2px 0 !important;
    }}
    [data-testid="stVerticalBlockBorderWrapper"] {{
        border-color: {BORDER} !important;
        border-radius: 2px !important;
    }}
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
st.markdown('<div class="tag-label">SOVEREIGN-RISK/v2 · MENA &amp; SOUTH ASIA</div>', unsafe_allow_html=True)
st.markdown('<div class="masthead-title">Sovereign Risk <span>Scorecard</span></div>', unsafe_allow_html=True)
st.markdown(
    '<div class="masthead-sub">A composite risk score for 15 MENA &amp; South Asia economies, '
    'built on live World Bank data across 10 factors spanning economic and governance pillars, '
    'with curated historical context and a live scenario-weighting explorer.</div>',
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
    stat_card("Regional Average", f"{valid_scores['risk_score'].mean():.1f}", "Across all 15")

st.markdown("<br>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["REGIONAL_OVERVIEW", "COUNTRY_DEEP_DIVE", "SCENARIO_EXPLORER", "METHODOLOGY"])

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
        st.markdown('<div class="section-tag">RANKED_ALL_15</div>', unsafe_allow_html=True)
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
            gulf = scored[scored["country_code"].isin(["SAU", "ARE", "KWT", "QAT"])]["risk_score"].mean()
            south_asia = scored[scored["country_code"].isin(["PAK", "BGD", "LKA"])]["risk_score"].mean()
            levant = scored[scored["country_code"].isin(["JOR", "LBN", "IRQ"])]["risk_score"].mean()
            custom_table(
                [["Gulf States", f"{gulf:.1f}"], ["South Asia", f"{south_asia:.1f}"], ["Levant", f"{levant:.1f}"]],
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
    st.markdown('<div class="section-tag">2015_2024</div>', unsafe_allow_html=True)
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
                    f'{int(row["risk_rank"])} / 15</div>',
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
    st.markdown(f'<div class="section-tag">2015_2024</div>', unsafe_allow_html=True)
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
    st.markdown('<div class="section-tag">CURATED_NOT_LIVE</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Key Historical Context</div>', unsafe_allow_html=True)
    country_code = row["country_code"]
    events = HISTORICAL_CONTEXT.get(country_code, [])
    if events:
        event_html = '<table class="custom-table"><thead><tr><th>Year</th><th>Event</th></tr></thead><tbody>'
        for year, event in events:
            event_html += f"<tr><td style='white-space:nowrap;'>{year}</td><td>{event}</td></tr>"
        event_html += "</tbody></table>"
        st.markdown(event_html, unsafe_allow_html=True)
        st.caption("Curated highlights fact-checked against IMF/news sources as of Aug 2026 — not a live feed.")
    else:
        st.caption("No curated events on file for this country yet.")

    st.markdown("<br>", unsafe_allow_html=True)
    inv_col1, inv_col2 = st.columns([3, 2])
    with inv_col1:
        st.markdown('<div class="section-tag">FDI_NET_INFLOWS</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Investment Context</div>', unsafe_allow_html=True)
        fdi_hist = long_df[(long_df["country_code"] == country_code) & (long_df["indicator"] == "fdi_net_inflows_pct_gdp")].sort_values("year")
        if not fdi_hist.empty:
            fig5 = px.bar(fdi_hist, x="year", y="value", labels={"value": "FDI Net Inflows (% GDP)", "year": "Year"})
            fig5.update_traces(marker_color=ACCENT)
            st.plotly_chart(style_chart(fig5, height=280), use_container_width=True)
            st.caption(
                "Foreign direct investment, net inflows as % of GDP (World Bank). Shown as descriptive "
                "context, not a risk-score input — investment direction isn't unambiguously 'safe' or 'risky.'"
            )
        else:
            st.caption("No FDI data available for this country.")
    with inv_col2:
        st.markdown('<div class="section-tag">REFERENCE</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Primary Market</div>', unsafe_allow_html=True)
        exchange, index = STOCK_EXCHANGES.get(country_code, ("N/A", "N/A"))
        custom_table([["Exchange", exchange], ["Benchmark Index", index]], ["Field", "Value"])
        st.caption("Reference only — not live pricing.")

# ================= TAB 3: SCENARIO EXPLORER =================
with tab3:
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

# ================= TAB 4: METHODOLOGY =================
with tab4:
    st.markdown('<div class="section-tag">HOW_ITS_BUILT</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Methodology</div>', unsafe_allow_html=True)
    st.markdown(
        "Each country is scored **0–100** (100 = highest risk) on a weighted composite "
        "of 10 factors across two pillars, weighted equally at 10% by default — adjustable "
        "live in the Scenario Explorer tab:"
    )
    custom_table(
        [
            ["Debt (% of GDP)", "Economic", "10%", "World Bank WDI"],
            ["Current Account (% of GDP)", "Economic", "10%", "World Bank WDI"],
            ["Reserves (months of imports)", "Economic", "10%", "World Bank WDI"],
            ["GDP Growth", "Economic", "10%", "World Bank WDI"],
            ["Inflation", "Economic", "10%", "World Bank WDI"],
            ["Political Stability", "Governance", "10%", "World Bank WGI"],
            ["Government Effectiveness", "Governance", "10%", "World Bank WGI"],
            ["Rule of Law", "Governance", "10%", "World Bank WGI"],
            ["Regulatory Quality", "Governance", "10%", "World Bank WGI"],
            ["Control of Corruption", "Governance", "10%", "World Bank WGI"],
        ],
        ["Factor", "Pillar", "Weight", "Source"],
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
    st.markdown('<div class="section-tag">V3</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Known Limitations</div>', unsafe_allow_html=True)
    st.markdown(
        """
- **Debt-to-GDP coverage is sparse** for Gulf states and Iran — only 6 of 15 countries report
  it consistently to the World Bank. A future improvement would add IMF World Economic Outlook
  debt data as a fallback source.
- **Iran's score is lower-confidence** — only 7 of 10 factors are available, likely due to
  sanctions limiting fiscal data reporting.
- **Historical context is curated, not live** — the event list in each country's Deep Dive tab
  was hand-researched and fact-checked as of August 2026, not pulled from a live news feed.
  It highlights major events but is not exhaustive.
- Weights are a transparent, reasonable starting point — not a backtested or econometrically
  validated model. Research/screening tool, not investment advice.
"""
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
