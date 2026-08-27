import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Sovereign Risk Scorecard", page_icon="🌍", layout="wide")

df = pd.read_csv("scored_data.csv")

st.title("Sovereign Risk Scorecard")
st.caption(
    "MENA & South Asia | Built on public IMF/World Bank data · "
    "Methodology: weighted composite of debt-to-GDP, current account balance, "
    "reserves, and political stability (World Bank WGI)"
)

tier_colors = {
    "Lower Risk": "#2e7d32",
    "Moderate Risk": "#c9a227",
    "Higher Risk": "#b3261e",
    "Insufficient data": "#9e9e9e",
}

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Risk Ranking")
    chart_df = df.dropna(subset=["risk_score"]).sort_values("risk_score", ascending=True)
    fig = px.bar(
        chart_df,
        x="risk_score",
        y="country",
        orientation="h",
        color="risk_tier",
        color_discrete_map=tier_colors,
        text="risk_score",
        labels={"risk_score": "Risk Score (0-100)", "country": ""},
    )
    fig.update_traces(texttemplate="%{text:.1f}", textposition="outside")
    fig.update_layout(showlegend=True, height=500)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Legend")
    st.markdown("🟢 **Lower Risk** — score < 33")
    st.markdown("🟡 **Moderate Risk** — score 33-66")
    st.markdown("🔴 **Higher Risk** — score > 66")
    st.markdown("⚪ **Insufficient data** — fewer than 2 factors available")
    st.info(
        "Iran's score is based on only 1 of 4 factors — debt and current account "
        "data are not reported to the World Bank, likely due to sanctions. "
        "Treat that score as low-confidence.",
        icon="⚠️",
    )

st.divider()
st.subheader("Full Data")
display_df = df[
    ["country", "risk_score", "risk_tier", "risk_score_factors_used",
     "debt_to_gdp", "current_account_pct_gdp", "reserves_months_imports", "political_stability"]
].rename(columns={
    "risk_score_factors_used": "factors available (of 4)",
    "debt_to_gdp": "debt to GDP (%)",
    "current_account_pct_gdp": "current account (% GDP)",
    "reserves_months_imports": "reserves (months of imports)",
    "political_stability": "political stability (-2.5 to +2.5)",
})
st.dataframe(display_df, use_container_width=True, hide_index=True)

st.divider()
st.caption(
    "Data: World Bank World Development Indicators & Worldwide Governance Indicators, "
    "pulled via public API. Not investment advice."
)
