import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Sovereign Risk Scorecard", page_icon="🌍", layout="wide")

scored = pd.read_csv("scored_data.csv")
history = pd.read_csv("scored_history.csv")
drivers = pd.read_csv("driver_data.csv")

FACTOR_LABELS = {
    "debt_to_gdp": "Debt (% GDP)",
    "current_account_pct_gdp": "Current Account",
    "reserves_months_imports": "Reserves Cover",
    "gdp_growth": "GDP Growth",
    "inflation": "Inflation",
    "political_stability": "Political Stability",
    "government_effectiveness": "Govt. Effectiveness",
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
}

tier_colors = {
    "Lower Risk": "#2e7d32",
    "Moderate Risk": "#c9a227",
    "Higher Risk": "#b3261e",
    "Insufficient data": "#9e9e9e",
}

st.title("Sovereign Risk Scorecard")
st.caption(
    "MENA & South Asia · 15 economies · 7-factor composite across economic and "
    "governance pillars · Built on public IMF/World Bank data"
)

# ---------------- TOP-LINE METRICS ----------------
valid_scores = scored.dropna(subset=["risk_score"])
m1, m2, m3, m4 = st.columns(4)
m1.metric("Countries Covered", len(scored))
m2.metric("Highest Risk", f"{valid_scores.iloc[0]['country']}", f"{valid_scores.iloc[0]['risk_score']:.1f}")
lowest = valid_scores.sort_values("risk_score").iloc[0]
m3.metric("Lowest Risk", f"{lowest['country']}", f"{lowest['risk_score']:.1f}")
m4.metric("Regional Average", f"{valid_scores['risk_score'].mean():.1f}")

tab1, tab2, tab3 = st.tabs(["📊 Regional Overview", "🔎 Country Deep Dive", "📋 Methodology & Data"])

# ================= TAB 1: OVERVIEW =================
with tab1:
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Risk Ranking")
        chart_df = scored.dropna(subset=["risk_score"]).sort_values("risk_score", ascending=True)
        fig = px.bar(
            chart_df, x="risk_score", y="country", orientation="h",
            color="risk_tier", color_discrete_map=tier_colors, text="risk_score",
            labels={"risk_score": "Risk Score (0-100)", "country": ""},
        )
        fig.update_traces(texttemplate="%{text:.1f}", textposition="outside")
        fig.update_layout(height=560, showlegend=True, legend_title_text="")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Legend")
        st.markdown("🟢 **Lower Risk** — score < 33")
        st.markdown("🟡 **Moderate Risk** — score 33-66")
        st.markdown("🔴 **Higher Risk** — score > 66")
        st.markdown("⚪ **Insufficient data** — fewer than 2 of 7 factors available")
        st.divider()
        st.subheader("Regional Snapshot")
        gulf = scored[scored["country_code"].isin(["SAU", "ARE", "KWT", "QAT"])]["risk_score"].mean()
        south_asia = scored[scored["country_code"].isin(["PAK", "BGD", "LKA"])]["risk_score"].mean()
        levant = scored[scored["country_code"].isin(["JOR", "LBN", "IRQ"])]["risk_score"].mean()
        st.markdown(f"**Gulf states avg:** {gulf:.1f}")
        st.markdown(f"**South Asia avg:** {south_asia:.1f}")
        st.markdown(f"**Levant avg:** {levant:.1f}")
        st.info(
            "Iran's score is based on only 4 of 7 factors — debt, current account, "
            "and reserves data are not consistently reported to the World Bank, "
            "likely due to sanctions. Treat that score as lower-confidence.",
            icon="⚠️",
        )

    st.divider()
    st.subheader("Historical Trend (2015-2024)")
    trend_countries = st.multiselect(
        "Compare countries over time",
        options=sorted(scored["country"].tolist()),
        default=["Pakistan", "Lebanon", "UAE", "Egypt"],
    )
    if trend_countries:
        trend_df = history[history["country"].isin(trend_countries)]
        fig2 = px.line(
            trend_df.sort_values("year"), x="year", y="risk_score", color="country",
            markers=True, labels={"risk_score": "Risk Score", "year": "Year"},
        )
        fig2.update_layout(height=420)
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.caption("Select at least one country to see its risk trend over time.")

# ================= TAB 2: COUNTRY DEEP DIVE =================
with tab2:
    country_list = scored.sort_values("country")["country"].tolist()
    selected = st.selectbox("Select a country", country_list)

    row = scored[scored["country"] == selected].iloc[0]
    driver_row = drivers[drivers["country"] == selected].iloc[0]

    c1, c2 = st.columns([1, 2])
    with c1:
        st.metric("Composite Risk Score", f"{row['risk_score']:.1f}" if pd.notna(row["risk_score"]) else "N/A", row["risk_tier"])
        st.caption(f"Based on {int(row['risk_score_factors_used'])} of 7 factors")

        # ---- Narrative generation ----
        factor_scores = {f: driver_row[f] for f in FACTOR_COLS if pd.notna(driver_row[f])}
        if factor_scores:
            sorted_factors = sorted(factor_scores.items(), key=lambda x: x[1], reverse=True)
            top_risks = sorted_factors[:2]
            top_strength = sorted_factors[-1]
            risk_names = " and ".join(FACTOR_LABELS[f] for f, v in top_risks)
            strength_name = FACTOR_LABELS[top_strength[0]]
            st.markdown(
                f"**Key drivers:** {selected}'s risk profile is driven primarily by "
                f"**{risk_names}**, while **{strength_name}** is a relative strength."
            )

    with c2:
        st.subheader("Risk Factor Breakdown")
        radar_factors = [f for f in FACTOR_COLS if pd.notna(driver_row[f])]
        radar_values = [driver_row[f] for f in radar_factors]
        radar_labels = [FACTOR_LABELS[f] for f in radar_factors]

        if radar_factors:
            fig3 = go.Figure()
            fig3.add_trace(go.Scatterpolar(
                r=radar_values + [radar_values[0]],
                theta=radar_labels + [radar_labels[0]],
                fill="toself", fillcolor="rgba(201,168,76,0.25)",
                line=dict(color="#c9a84c"),
            ))
            fig3.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                showlegend=False, height=400,
            )
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.caption("No factor data available for radar chart.")

    st.divider()
    st.subheader(f"{selected}: Risk Score Over Time")
    country_history = history[history["country"] == selected].sort_values("year")
    if not country_history.empty:
        fig4 = px.line(country_history, x="year", y="risk_score", markers=True)
        fig4.update_traces(line_color="#c9a84c")
        fig4.update_layout(height=320)
        st.plotly_chart(fig4, use_container_width=True)
    else:
        st.caption("Not enough historical data for a trend line.")

    st.divider()
    st.subheader("Underlying Raw Indicators")
    raw_rows = []
    for factor, (label, unit) in RAW_LABELS.items():
        value = row.get(factor)
        year = row.get(f"{factor}_year")
        raw_rows.append({
            "Indicator": label,
            "Value": f"{value:.2f}" if pd.notna(value) else "No data",
            "Unit": unit,
            "As of": int(year) if pd.notna(year) else "—",
        })
    st.dataframe(pd.DataFrame(raw_rows), use_container_width=True, hide_index=True)

# ================= TAB 3: METHODOLOGY =================
with tab3:
    st.subheader("Methodology")
    st.markdown(
        """
Each country is scored **0-100** (100 = highest risk) on a weighted composite
of 7 factors across two pillars:
"""
    )
    weights_table = pd.DataFrame([
        {"Factor": "Debt (% of GDP)", "Pillar": "Economic", "Weight": "20%", "Source": "World Bank WDI"},
        {"Factor": "Current Account (% of GDP)", "Pillar": "Economic", "Weight": "15%", "Source": "World Bank WDI"},
        {"Factor": "Reserves (months of imports)", "Pillar": "Economic", "Weight": "15%", "Source": "World Bank WDI"},
        {"Factor": "GDP Growth", "Pillar": "Economic", "Weight": "10%", "Source": "World Bank WDI"},
        {"Factor": "Inflation", "Pillar": "Economic", "Weight": "10%", "Source": "World Bank WDI"},
        {"Factor": "Political Stability", "Pillar": "Governance", "Weight": "20%", "Source": "World Bank WGI"},
        {"Factor": "Government Effectiveness", "Pillar": "Governance", "Weight": "10%", "Source": "World Bank WGI"},
    ])
    st.dataframe(weights_table, use_container_width=True, hide_index=True)

    st.markdown(
        """
Each factor is **min-max normalized to 0-100** relative to the other countries
in the sample (for that same year, when building the historical trend). If a
country is missing a factor, that factor is dropped for that country and the
remaining weights are **rescaled proportionally** — missing data is never
silently treated as "safe."
"""
    )

    st.subheader("Known Limitations (v2)")
    st.markdown(
        """
- **Debt-to-GDP coverage is sparse** for Gulf states and Iran in the World
  Bank's WDI dataset — only 6 of 15 countries report it consistently. A v3
  improvement would pull IMF World Economic Outlook debt data as a fallback
  source for fuller coverage.
- **Iran's score is lower-confidence** — only 4 of 7 factors are available,
  likely due to sanctions limiting what fiscal data gets reported.
- Weights are a transparent, reasonable starting point — not a backtested or
  econometrically validated model. Treat this as a research/screening tool,
  not investment advice.
"""
    )

    st.subheader("Data & Code")
    st.markdown(
        "- Data: [World Bank World Development Indicators & Worldwide Governance Indicators](https://data.worldbank.org/)\n"
        "- Source code: [GitHub](https://github.com/rafaywaqar2004-lang/overeign-risk-index)\n"
        "- Not investment advice."
    )
