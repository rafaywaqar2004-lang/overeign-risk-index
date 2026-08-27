"""
Curated historical context and reference data per country.

Unlike the quantitative indicators (pulled live from the World Bank API),
this is hand-researched and fact-checked against primary/news sources
(IMF press releases, Reuters, AP, major think tanks) as of August 2026.
It is a curated snapshot of major events, not a live feed — dates and
figures are verified, but this list is illustrative, not exhaustive.
"""

HISTORICAL_CONTEXT = {
    "PAK": [
        (2019, "IMF approves $6bn Extended Fund Facility (EFF); reviews concluded Aug 2022"),
        (2022, "Catastrophic monsoon floods (a third of the country underwater) compound a balance-of-payments crisis"),
        (2023, "Near-default crisis averted; IMF approves $3bn Stand-By Arrangement (Jul 12, 2023)"),
        (2024, "IMF approves 37-month, ~$7bn Extended Fund Facility (Sep 25, 2024)"),
    ],
    "EGY": [
        (2016, "Egyptian pound floated; IMF approves $12bn Extended Fund Facility"),
        (2022, "IMF approves $3bn EFF (Dec 16, 2022) amid FX shortage and pound pressure"),
        (2024, "Pound devalued ~40% in a managed float; IMF expands EFF to $8bn (Mar 2024)"),
        (2024, "UAE agrees $35bn Ras El-Hekma coastal development deal (Feb 23, 2024) — single largest FDI inflow in Egypt's history"),
    ],
    "MAR": [
        (2023, "M6.8-6.9 Al Haouz earthquake (Sep 8, 2023) kills ~2,960; High Atlas region devastated"),
    ],
    "TUN": [
        (2021, "President Kais Saied suspends parliament and assumes executive power (Jul 25, 2021)"),
        (2023, "Saied rejects a negotiated $1.9bn IMF loan, citing 'foreign diktats' (Apr 2023), stalling international support"),
    ],
    "DZA": [
        (2019, "Hirak protest movement begins (Feb 22, 2019); President Bouteflika resigns weeks later (Apr 2, 2019)"),
    ],
    "JOR": [
        (2024, "IMF approves new 4-year, ~$1.2bn Extended Fund Facility (Jan 10, 2024)"),
        (2023, "Regional spillover risk rises after the Gaza war begins (Oct 2023), given Jordan's large refugee population and tourism exposure"),
    ],
    "SAU": [
        (2016, "Vision 2030 economic diversification program launched (Apr 25, 2016)"),
        (2020, "Oil price collapse amid COVID-19 demand shock; OPEC+ supply cuts follow"),
    ],
    "ARE": [
        (2023, "Hosts COP28 UN climate conference (Nov 30 - Dec 12, 2023)"),
    ],
    "IRN": [
        (2018, "US withdraws from the JCPOA nuclear deal (May 8, 2018); sanctions fully reimposed by Nov 2018"),
    ],
    "BGD": [
        (2023, "IMF approves ~$4.7bn loan amid FX reserve pressure"),
        (2024, "Student-led protests over job quotas escalate into a mass uprising; PM Sheikh Hasina resigns and departs the country (Aug 5, 2024)"),
    ],
    "LKA": [
        (2022, "Sri Lanka defaults on external debt for the first time in its history (Apr 12, 2022); mass protests oust President Rajapaksa"),
        (2023, "IMF approves ~$2.9bn Extended Fund Facility (Mar 2023), beginning a debt restructuring and recovery process"),
    ],
    "IRQ": [
        (2021, "October 2021 elections are followed by a record-length government formation deadlock"),
        (2022, "New government under PM Mohammed Shia Al-Sudani approved (Oct 2022) after over a year without a governing coalition"),
    ],
    "LBN": [
        (2020, "Defaults on a $1.2bn Eurobond payment (Mar 9, 2020), its first sovereign default"),
        (2020, "Beirut port explosion (Aug 4, 2020) devastates the capital; currency has since lost the vast majority of its pre-crisis value"),
    ],
    "KWT": [
        (2024, "Emir dissolves the National Assembly and suspends parts of the constitution (May 10, 2024), consolidating executive power"),
    ],
    "QAT": [
        (2017, "Saudi Arabia, UAE, Bahrain, and Egypt sever ties and blockade Qatar (Jun 5, 2017)"),
        (2021, "Blockade resolved; diplomatic relations restored (Jan 2021)"),
    ],
}

# Primary stock exchange / benchmark index per country — reference data only,
# not live pricing.
STOCK_EXCHANGES = {
    "PAK": ("Pakistan Stock Exchange (PSX)", "KSE-100"),
    "EGY": ("Egyptian Exchange (EGX)", "EGX 30"),
    "MAR": ("Casablanca Stock Exchange", "MASI"),
    "TUN": ("Bourse de Tunis", "TUNINDEX"),
    "DZA": ("Bourse d'Alger", "N/A — thinly traded, no widely tracked index"),
    "JOR": ("Amman Stock Exchange (ASE)", "ASE General Index"),
    "SAU": ("Saudi Exchange (Tadawul)", "TASI"),
    "ARE": ("Dubai Financial Market / Abu Dhabi Securities Exchange", "DFM General / FTSE ADX General"),
    "IRN": ("Tehran Stock Exchange (TSE)", "TEDPIX"),
    "BGD": ("Dhaka Stock Exchange (DSE)", "DSEX"),
    "LKA": ("Colombo Stock Exchange (CSE)", "ASPI"),
    "IRQ": ("Iraq Stock Exchange (ISX)", "ISX 60"),
    "LBN": ("Beirut Stock Exchange (BSE)", "BLOM Stock Index"),
    "KWT": ("Boursa Kuwait", "Premier Market Index"),
    "QAT": ("Qatar Stock Exchange (QSE)", "QE General Index"),
}
