"""
Curated historical context, source citations, and reference data per country.

Unlike the quantitative indicators (pulled live from the World Bank API),
this is hand-researched and fact-checked via web search against primary/news
sources (IMF, Reuters, AP, Al Jazeera, Bloomberg, Wikipedia, CFR, Britannica,
government/parliamentary research services) as of August 2026. It is a
curated snapshot of major events, not a live feed — dates and figures are
verified against the cited source for each entry, but this list is
illustrative, not exhaustive.

Each historical event is a tuple: (year, event_text, source_name, source_url)
"""

HISTORICAL_CONTEXT = {
    "DZA": [
        (2019, "Hirak protest movement begins (Feb 22, 2019) demanding political reform; President Bouteflika resigns weeks later (Apr 2, 2019)", "Reuters/AP via news archives", "https://en.wikipedia.org/wiki/2021_Algerian_protests"),
        (2020, "Oil and gas price collapse amid COVID-19 demand shock hits hydrocarbon-dependent export revenue (hydrocarbons are ~90%+ of exports)", "World Bank Algeria overview", "https://www.worldbank.org/en/country/algeria/overview"),
    ],
    "BHR": [
        (2011, "Arab Spring uprising begins (Feb 14, 2011) with mass protests in Manama demanding reform; GCC troops intervene to help suppress it (Mar 2011)", "Wikipedia: Timeline of the 2011 Bahraini uprising", "https://en.wikipedia.org/wiki/Timeline_of_the_2011_Bahraini_uprising"),
    ],
    "EGY": [
        (2016, "Egyptian pound floated; IMF approves $12bn Extended Fund Facility", "IMF", "https://www.imf.org/en/Countries/EGY"),
        (2022, "IMF approves $3bn EFF (Dec 16, 2022) amid FX shortage and pound pressure", "IMF Press Release 22/443", "https://www.imf.org/en/news/articles/2022/12/16/pr22443-egypt-imf-executive-board-approves-3-billion-eff"),
        (2024, "Pound devalued ~40% in a managed float; IMF expands EFF to $8bn (Mar 2024)", "IMF Press Release 24/101", "https://www.imf.org/en/news/articles/2024/03/29/pr24101-egypt-imf-executive-board-completes-first-second-reviews-eff-approves-augmentation"),
        (2024, "UAE agrees $35bn Ras El-Hekma coastal development deal (Feb 23, 2024) — single largest FDI inflow in Egypt's history", "The Washington Institute", "https://www.washingtoninstitute.org/policy-analysis/imf-and-uae-swoop-ease-egypts-economic-crisis"),
        (2024, "Suez Canal revenue collapses more than 60% ($10.3bn in 2023 to $4bn in 2024, a ~$7bn loss) as Houthi Red Sea attacks force shipping to reroute around Africa", "Bloomberg / Ahram Online", "https://www.bloomberg.com/news/articles/2024-12-26/red-sea-disruptions-cost-egypt-7-billion-in-suez-revenues"),
    ],
    "IRN": [
        (2018, "US withdraws from the JCPOA nuclear deal (May 8, 2018); sanctions fully reimposed by Nov 2018", "US Treasury / Congress.gov", "https://home.treasury.gov/policy-issues/financial-sanctions/sanctions-programs-and-country-information/iran-sanctions/may-2018-guidance-on-reimposing-certain-sanctions-with-respect-to-iran"),
        (2025, "12-Day War: Israel and the US strike Iranian nuclear/military sites (Jun 2025); ceasefire takes effect Jun 24, 2025", "Wikipedia: Twelve-Day War ceasefire", "https://en.wikipedia.org/wiki/Twelve-Day_War_ceasefire"),
        (2026, "War resumes (Feb 28, 2026): US/Israel 'Operation Epic Fury' launches ~900 strikes in 12 hours, killing Supreme Leader Ali Khamenei and dozens of officials; Mojtaba Khamenei appointed successor", "Wikipedia: Timeline of the 2026 Iran conflict / Assassination of Ali Khamenei", "https://en.wikipedia.org/wiki/Timeline_of_the_2026_Iran_conflict"),
        (2026, "Operation concludes (May 5, 2026); a June 2026 MoU seeks to end the conflict and reopen the Strait of Hormuz, but Iran fires on commercial vessels in July, testing the truce", "Britannica: 2026 Iran war", "https://www.britannica.com/event/2026-Iran-war"),
    ],
    "IRQ": [
        (2014, "ISIS captures Mosul (Jun 2014), Iraq's second-largest city, triggering a 3-year war", "Wikipedia: Islamic State occupation of Mosul", "https://en.wikipedia.org/wiki/Islamic_State_occupation_of_Mosul"),
        (2017, "Iraqi PM al-Abadi declares Mosul liberated (Jul 10, 2017) after a grinding 9-month urban battle", "Modern War Institute, West Point", "https://mwi.westpoint.edu/urban-warfare-project-case-study-2-battle-of-mosul/"),
        (2021, "October 2021 elections trigger the longest government-formation deadlock in Iraq's history", "UK Parliament / USIP", "https://www.usip.org/publications/2022/10/year-after-elections-iraq-may-finally-be-set-form-government"),
        (2022, "New government under PM Mohammed Shia Al-Sudani approved (Oct 2022) after over a year without a governing coalition", "UK House of Commons Library", "https://commonslibrary.parliament.uk/research-briefings/cbp-9605/"),
    ],
    "ISR": [
        (2023, "Oct 7, 2023 Hamas attack and subsequent Gaza war trigger the sharpest economic contraction since the pandemic — GDP fell 19.4% (annualized) in Q4 2023 alone, driven by a 26.9% drop in private consumption", "CNN Business / Times of Israel", "https://www.timesofisrael.com/war-battered-economy-plunged-almost-20-marking-sharpest-contraction-since-pandemic/"),
        (2025, "Ceasefire signed with Hamas (Oct 10, 2025) after two years of war; Gaza's Government Media Office documents 2,000+ ceasefire violations in the following six months", "Al Jazeera", "https://www.aljazeera.com/news/2026/4/10/neither-war-nor-peace-what-gaza-looks-like-six-months-into-ceasefire"),
        (2026, "War with Iran resumes (Feb 28, 2026) alongside the US; Bank of Israel had estimated total 2023-2025 war costs at ~$55.6bn even before this new escalation", "Bloomsbury Intelligence & Security Institute", "https://bisi.org.uk/reports/the-impacts-of-the-gaza-war-on-israels-economy"),
    ],
    "JOR": [
        (2018, "Nationwide protests (May-Jun 2018) force withdrawal of an IMF-backed income tax bill after a general strike by 30+ trade unions", "Al Jazeera / VOA", "https://en.wikipedia.org/wiki/2018_Jordanian_protests"),
        (2023, "Regional spillover risk rises after the Gaza war begins (Oct 2023), given Jordan's large Palestinian and Syrian refugee population and tourism exposure", "IMF Jordan country page", "https://www.imf.org/en/Countries/JOR"),
        (2024, "IMF approves new 4-year, ~$1.2bn Extended Fund Facility (Jan 10, 2024)", "IMF Press Release 24/004", "https://www.imf.org/en/News/Articles/2024/01/10/pr24004-jordan-imf-exec-board-approves-us1b-extended-arrangement-under-eff"),
    ],
    "KWT": [
        (1990, "Iraq invades Kuwait (Aug 2, 1990), triggering the Gulf War (1990-91) and a 7-month occupation that devastated oil infrastructure", "History.com / Britannica", "https://www.history.com/this-day-in-history/august-2/iraq-invades-kuwait"),
        (2024, "Emir dissolves the National Assembly and suspends parts of the constitution (May 10, 2024), consolidating executive power for up to 4 years", "The National / Emirates 24|7", "https://www.thenationalnews.com/news/gulf/2024/05/10/kuwait-emir-parliament-constitution/"),
    ],
    "LBN": [
        (2019, "Economic and financial crisis erupts in late 2019 amid a fiscal/currency crunch, described by the World Bank as one of the worst globally since the 1850s", "World Bank Lebanon Economic Monitor", "https://www.worldbank.org/en/country/lebanon/overview"),
        (2020, "Defaults on a $1.2bn Eurobond payment (Mar 9, 2020), its first sovereign default", "Reuters/Wiley Online Library", "https://onlinelibrary.wiley.com/doi/full/10.1111/infi.12459"),
        (2020, "Beirut port explosion (Aug 4, 2020) devastates the capital; currency has since lost the vast majority of its pre-crisis value", "The Conversation / Al Arabiya", "https://theconversation.com/how-beiruts-port-explosion-exacerbates-lebanons-economic-crisis-144040"),
        (2023, "Escalating Israel-Hezbollah conflict following the Gaza war strains the south of the country and tourism-dependent economy further", "IMF Lebanon country page", "https://www.imf.org/en/Countries/LBN"),
    ],
    "LBY": [
        (2011, "Civil war and NATO intervention topple Gaddafi; oil production collapses, driving real GDP down 62% for the year", "EIA / MSU globalEDGE", "https://globaledge.msu.edu/blog/postamp/57442/political-conflict-in-libya-continues-ha"),
        (2014, "Renewed conflict splits the country between rival governments (GNA in the west, LNA in the east); oil exports fall to 375,000 b/d, down from 1.3 million b/d in 2012", "EIA Libya country analysis", "https://www.eia.gov/international/content/analysis/countries_long/libya/"),
        (2020, "Rival factions continue to use oil export blockades as political leverage, causing repeated production shutdowns through 2020", "CGSRS", "https://cgsrs.org/publications/29"),
    ],
    "MAR": [
        (2023, "M6.8-6.9 Al Haouz earthquake (Sep 8, 2023) kills ~2,960 in the High Atlas region, the country's deadliest quake in over 60 years", "Britannica / ReliefWeb", "https://www.britannica.com/event/Morocco-earthquake-of-2023"),
    ],
    "OMN": [
        (2016, "Launches long-term Vision 2040 diversification plan targeting non-oil GDP share of 91.6% by 2040 (from 61% in 2017)", "Oman Vision 2040 official site", "https://oman2040.com/vision/pillar-economy-development/"),
        (2024, "IMF assessment finds Vision 2040 implementation 'advancing decisively'", "The National", "https://www.thenationalnews.com/business/economy/2024/12/19/omans-vision-2040-a-success-story-for-gulf-diversification-plans-imf-official-says/"),
    ],
    "QAT": [
        (2017, "Saudi Arabia, UAE, Bahrain, and Egypt sever ties and blockade Qatar (Jun 5, 2017) over alleged support for extremism and ties to Iran", "Wikipedia: Qatar diplomatic crisis", "https://en.wikipedia.org/wiki/Qatar_diplomatic_crisis"),
        (2021, "Blockade resolved; diplomatic relations restored (Jan 2021) at the AlUla GCC summit", "GlobalSecurity.org", "https://www.globalsecurity.org/military/library/news/2021/01/mil-210120-sputnik01.htm"),
        (2023, "Hosts the 2022 FIFA World Cup (Nov-Dec 2022) and COP28 (Nov-Dec 2023), part of a broader post-blockade global-visibility push", "UNFCCC", "https://unfccc.int/cop28"),
    ],
    "SAU": [
        (2016, "Vision 2030 economic diversification program launched (Apr 25, 2016)", "Saudi Vision 2030 official timeline", "https://vision2030.ai/vision/timeline/"),
        (2020, "Oil price collapse amid COVID-19 demand shock (WTI briefly went negative); OPEC+ supply cuts follow", "OPEC/EIA reporting", "https://www.eia.gov/"),
        (2026, "Houthis declare a naval blockade against Saudi Arabia in the Red Sea (Jul 20, 2026), attacking Saudi oil tankers in solidarity with Iran amid the 2026 Iran war", "Al Jazeera / CNBC", "https://www.aljazeera.com/news/2026/8/24/yemens-houthis-report-attack-on-saudi-ship"),
    ],
    "SYR": [
        (2011, "Civil war begins (Mar 15, 2011) after Arab Spring protests against Assad's rule are met with a violent crackdown", "Britannica: Syrian Civil War", "https://www.britannica.com/event/Syrian-Civil-War"),
        (2024, "Assad regime falls (Dec 8, 2024) as a rebel offensive led by Hay'at Tahrir al-Sham captures Damascus, ending 13 years of civil war", "Wikipedia: Fall of the Assad regime", "https://en.wikipedia.org/wiki/Fall_of_the_Assad_regime"),
        (2025, "Ahmed al-Sharaa declared transitional president (Jan 2025); interim Constitutional Declaration takes effect (Mar 2025) setting a 5-year path to elections", "Belfer Center, Harvard Kennedy School", "https://www.belfercenter.org/research-analysis/external-states-and-syrias-challenge-reunification-under-transitional-president"),
        (2026, "One year on, the political transition remains disputed — no single national armed force exists yet and localized violence continues into 2026", "UK House of Commons Library", "https://commonslibrary.parliament.uk/research-briefings/cbp-10430/"),
    ],
    "TUN": [
        (2010, "Street vendor Mohamed Bouazizi self-immolates (Dec 17, 2010) in Sidi Bouzid, igniting the Tunisian Revolution and the wider Arab Spring", "History.com / Britannica", "https://www.history.com/this-day-in-history/december-17/mohamed-bouazizi-self-immolates-arab-spring"),
        (2011, "President Ben Ali flees after 23 years in power (Jan 14, 2011)", "Wikipedia: Tunisian revolution", "https://en.wikipedia.org/wiki/Tunisian_revolution"),
        (2021, "President Kais Saied suspends parliament and assumes executive power (Jul 25, 2021)", "Wikipedia: 2021 Tunisian self-coup", "https://en.wikipedia.org/wiki/2021_Tunisian_self-coup"),
        (2023, "Saied rejects a negotiated $1.9bn IMF loan, citing 'foreign diktats' (Apr 2023), stalling international financial support", "Foreign Policy", "https://foreignpolicy.com/2023/04/19/tunisia-imf-loan-bailout-deal-economy-saied/"),
    ],
    "ARE": [
        (2023, "Hosts COP28 UN climate conference (Nov 30 - Dec 12, 2023) at Expo City Dubai", "UNFCCC", "https://unfccc.int/cop28"),
    ],
    "YEM": [
        (2014, "Houthi movement captures the capital Sanaa (Sep 2014), starting the civil war", "Britannica: Yemeni Civil War", "https://www.britannica.com/event/Yemeni-Civil-War"),
        (2015, "President Hadi resigns (Jan 23, 2015) as Houthi forces seize the presidential palace; Saudi-led coalition intervenes shortly after", "GlobalSecurity.org", "https://www.globalsecurity.org/military/world/war/yemen4-2014.htm"),
        (2023, "Houthi forces begin attacking Israel-linked shipping in the Red Sea (Nov 19, 2023) following the Gaza war, disrupting Suez-bound global trade", "CFR Global Conflict Tracker", "https://www.cfr.org/global-conflict-tracker/conflict/war-yemen"),
        (2026, "Houthis declare a formal naval blockade against Saudi Arabia (Jul 20, 2026), breaking a years-long truce and escalating regional shipping risk further", "Al Jazeera", "https://www.aljazeera.com/news/2026/8/24/yemens-houthis-report-attack-on-saudi-ship"),
    ],
    "AFG": [
        (2021, "Taliban retake control as US/NATO forces withdraw (Aug 2021); US freezes ~$7bn in Afghan central bank assets, European states freeze ~$2bn more", "The Diplomat / Wikipedia: Afghan frozen assets", "https://thediplomat.com/2021/08/taliban-takeover-world-bank-and-imf-halt-aid-us-freezes-afghan-assets/"),
        (2021, "World Bank and IMF halt aid disbursements to Afghanistan, compounding an already severe humanitarian and economic crisis", "The Diplomat", "https://thediplomat.com/2021/08/taliban-takeover-world-bank-and-imf-halt-aid-us-freezes-afghan-assets/"),
    ],
    "BGD": [
        (2023, "IMF approves ~$4.7bn loan amid FX reserve pressure", "IMF Bangladesh country page", "https://www.imf.org/en/Countries/BGD"),
        (2024, "Student-led protests over civil service job quotas escalate into a mass uprising; PM Sheikh Hasina resigns and departs the country (Aug 5, 2024)", "Wikipedia: Resignation of Sheikh Hasina / Chatham House", "https://en.wikipedia.org/wiki/Resignation_of_Sheikh_Hasina"),
    ],
    "BTN": [
        (2024, "Real GDP grows 8.1% in FY24/25, driven by hydropower expansion — the sector is ~14% of GDP and 26% of government revenue, with 60-70% of electricity exported to India", "Asian Development Bank / World Bank Bhutan overview", "https://www.adb.org/features/bhutan-s-hydropower-sector-12-things-know"),
    ],
    "IND": [
        (2024, "Total trade surpasses $1.6 trillion in FY2023-24; China overtakes the US as India's largest single trading partner ($118.4bn in two-way commerce)", "SEAIR / ThinkBRICS trade data", "https://thinkbrics.substack.com/p/china-emerges-as-indias-largest-trading"),
    ],
    "MDV": [
        (2023, "Sept 2023 presidential election brings China-leaning Mohamed Muizzu to power on a platform of removing Indian troops", "Bloomberg / ORF", "https://www.bloomberg.com/news/articles/2024-10-07/maldives-seeks-to-repair-ties-with-india-as-debt-crisis-looms"),
        (2024, "Debt-to-GDP reaches ~110% (Mar 2024, ~$8.2bn total), owing ~$1.3bn to China and ~$130m to India; Muizzu pivots back toward India as Chinese debt service looms", "Asia Times / Bloomberg", "https://asiatimes.com/2024/10/debt-forces-maldives-to-pivot-back-to-india-from-china/"),
    ],
    "NPL": [
        (2015, "M7.8 Gorkha earthquake (Apr 25, 2015) kills ~9,000 and causes damage estimated near a third of GDP", "USGS / relief reporting", "https://en.wikipedia.org/wiki/April_2015_Nepal_earthquake"),
    ],
    "PAK": [
        (2019, "IMF approves $6bn Extended Fund Facility (EFF); reviews concluded Aug 2022", "IMF Pakistan country page", "https://www.imf.org/en/Countries/PAK"),
        (2022, "Catastrophic monsoon floods (a third of the country underwater) compound a balance-of-payments crisis", "IMF Climate microsite", "https://imf-climate.org/country-cases/pakistan/"),
        (2023, "Near-default crisis averted; IMF approves $3bn Stand-By Arrangement (Jul 12, 2023)", "IMF Press Release 23/261", "https://www.imf.org/en/news/articles/2023/07/12/pr23261-pakistan-imf-exec-board-approves-us3bil-sba"),
        (2024, "IMF approves 37-month, ~$7bn Extended Fund Facility (Sep 25, 2024)", "IMF / South Asian Voices", "https://southasianvoices.org/ec-m-pk-r-pakistan-imf-reforms-5-12-2025/"),
    ],
    "LKA": [
        (2009, "26-year civil war ends (May 18, 2009) when government forces capture the last LTTE-held territory — the conflict's long fiscal and institutional toll shaped decades of subsequent debt accumulation", "ReliefWeb / Harvard International Review", "https://reliefweb.int/report/sri-lanka/timeline-sri-lanka-says-25-years-civil-war-almost-end-26-jan-2009"),
        (2022, "Sri Lanka defaults on external debt for the first time in its history (Apr 12, 2022); mass protests oust President Rajapaksa", "IMF Country Report 23/408", "https://www.imf.org/-/media/Files/Publications/CR/2023/English/1LKAEA2023003.ashx"),
        (2023, "IMF approves ~$2.9bn Extended Fund Facility (Mar 2023), beginning a debt restructuring and recovery process — the risk score's -9.4 YoY improvement reflects this recovery", "IMF staff-level agreement", "https://en.wikipedia.org/wiki/Sri_Lanka_sovereign_default"),
    ],
}

# Primary stock exchange / benchmark index per country — reference data only,
# not live pricing.
STOCK_EXCHANGES = {
    "DZA": ("Bourse d'Alger", "N/A — thinly traded, no widely tracked index"),
    "BHR": ("Bahrain Bourse", "Bahrain All Share Index"),
    "EGY": ("Egyptian Exchange (EGX)", "EGX 30"),
    "IRN": ("Tehran Stock Exchange (TSE)", "TEDPIX"),
    "IRQ": ("Iraq Stock Exchange (ISX)", "ISX 60"),
    "ISR": ("Tel Aviv Stock Exchange (TASE)", "TA-125"),
    "JOR": ("Amman Stock Exchange (ASE)", "ASE General Index"),
    "KWT": ("Boursa Kuwait", "Premier Market Index"),
    "LBN": ("Beirut Stock Exchange (BSE)", "BLOM Stock Index"),
    "LBY": ("Libyan Stock Market (LSM)", "N/A — very thinly traded"),
    "MAR": ("Casablanca Stock Exchange", "MASI"),
    "OMN": ("Muscat Stock Exchange (MSX)", "MSX 30"),
    "QAT": ("Qatar Stock Exchange (QSE)", "QE General Index"),
    "SAU": ("Saudi Exchange (Tadawul)", "TASI"),
    "SYR": ("Damascus Securities Exchange (DSE)", "DWX — very thinly traded"),
    "TUN": ("Bourse de Tunis", "TUNINDEX"),
    "ARE": ("Dubai Financial Market / Abu Dhabi Securities Exchange", "DFM General / FTSE ADX General"),
    "YEM": ("No functioning national exchange", "N/A — suspended amid civil war"),
    "AFG": ("No national exchange", "N/A"),
    "BGD": ("Dhaka Stock Exchange (DSE)", "DSEX"),
    "BTN": ("Royal Securities Exchange of Bhutan (RSEB)", "RSEB Index"),
    "IND": ("Bombay Stock Exchange (BSE) / National Stock Exchange (NSE)", "SENSEX / NIFTY 50"),
    "MDV": ("Maldives Stock Exchange (MSE)", "MASIDX"),
    "NPL": ("Nepal Stock Exchange (NEPSE)", "NEPSE Index"),
    "PAK": ("Pakistan Stock Exchange (PSX)", "KSE-100"),
    "LKA": ("Colombo Stock Exchange (CSE)", "ASPI"),
}


# ============================================================
# ACTIVE / RECENT MULTILATERAL FINANCING ARRANGEMENTS — verified IMF program
# details (amount, approval date, program length). This is the most reliable
# proxy this tool can offer for "when was debt established / when is it due" —
# instrument-level Eurobond/loan maturity walls need a specialized debt
# database (Bloomberg, IMF sovereign debt investor relations portal, or a
# national debt management office) that isn't available here, so this table
# is deliberately limited to what's been verified, not filled in with guesses.
# ============================================================
FINANCING_ARRANGEMENTS = {
    "PAK": [
        {"program": "IMF Extended Fund Facility (EFF)", "amount": "$6.0bn", "approved": "2019", "status": "Concluded (final reviews Aug 2022)"},
        {"program": "IMF Stand-By Arrangement (SBA)", "amount": "$3.0bn", "approved": "Jul 12, 2023", "status": "Completed (9-month program, final review Apr 2024)"},
        {"program": "IMF Extended Fund Facility (EFF)", "amount": "~$7.0bn", "approved": "Sep 25, 2024", "status": "Active — 37-month program, due to conclude ~Oct 2027"},
    ],
    "EGY": [
        {"program": "IMF Extended Fund Facility (EFF)", "amount": "$12.0bn", "approved": "Nov 2016", "status": "Concluded (3-year program)"},
        {"program": "IMF Extended Fund Facility (EFF)", "amount": "$3.0bn → expanded to $8.0bn", "approved": "Dec 16, 2022 (expanded Mar 2024)", "status": "Active — 46-month program, due to conclude ~Oct 2026"},
    ],
    "JOR": [
        {"program": "IMF Extended Fund Facility (EFF)", "amount": "~$1.2bn", "approved": "Jan 10, 2024", "status": "Active — 4-year program, due to conclude ~Jan 2028"},
    ],
    "LKA": [
        {"program": "IMF Extended Fund Facility (EFF)", "amount": "~$2.9bn (SDR 2.286bn)", "approved": "Mar 2023", "status": "Active — 4-year program, due to conclude ~Mar 2027"},
    ],
    "BGD": [
        {"program": "IMF combined ECF/EFF/RSF arrangement", "amount": "~$4.7bn", "approved": "2023", "status": "Active — exact program end date not independently verified here"},
    ],
    "TUN": [
        {"program": "IMF Extended Fund Facility (EFF) — staff-level agreement only", "amount": "~$1.9bn", "approved": "Oct 2022", "status": "Rejected by President Saied in Apr 2023 ('foreign diktats'); never disbursed"},
    ],
    "LBN": [
        {"program": "No active IMF financing arrangement", "amount": "—", "approved": "—", "status": "Defaulted on external debt Mar 2020; no IMF program has been finalized since, despite ongoing negotiations"},
    ],
    "SAU": [
        {"program": "No IMF financing arrangement — net external creditor", "amount": "—", "approved": "—", "status": "Not a borrower; Public Investment Fund deploys capital abroad rather than seeking external financing"},
    ],
    "ARE": [
        {"program": "No IMF financing arrangement — net external creditor", "amount": "—", "approved": "—", "status": "Not a borrower; ADIA and Mubadala sovereign wealth funds invest oil revenue internationally"},
    ],
    "QAT": [
        {"program": "No IMF financing arrangement — net external creditor", "amount": "—", "approved": "—", "status": "Not a borrower; Qatar Investment Authority manages LNG revenue as outbound investment"},
    ],
    "KWT": [
        {"program": "No IMF financing arrangement — net external creditor", "amount": "—", "approved": "—", "status": "Not a borrower; Kuwait Investment Authority (est. 1953) is one of the world's oldest sovereign wealth funds"},
    ],
    "BHR": [
        {"program": "No standing IMF program — relies on GCC bilateral support instead", "amount": "~$10bn GCC package", "approved": "2018", "status": "GCC-funded fiscal support arrangement, not an IMF facility"},
    ],
}


# ============================================================
# KEY ECONOMIC PARTNERS — verified creditor/investor/trade relationships.
# Deliberately scoped to cases with solid sourcing rather than attempted for
# all 26 countries — see Methodology tab for the explicit scope note. Framed
# as "economic partners" and "sources of regional tension," not informal
# "allies/enemies" labels, matching how political risk analysts actually
# describe these relationships.
# ============================================================
KEY_ECONOMIC_PARTNERS = {
    "PAK": {
        "summary": (
            "China is Pakistan's largest creditor by far, holding ~22% of total external debt "
            "(~$28.8bn) — more than the World Bank (18%, ~$23.6bn) or Asian Development Bank (15%, "
            "~$19.6bn). Saudi Arabia is the largest bilateral (government-to-government) lender at "
            "~7% (~$9.2bn). In 2024, Pakistan relied on rollovers rather than repayment: Saudi Arabia "
            "extended a $3bn deposit and rolled over an existing $5bn facility, while the UAE's "
            "rollover on a separate $3bn obligation stalled, pushing Islamabad to seek fresh support. "
            "Chinese power producers under CPEC have also refused to renegotiate ~PKR 170bn in "
            "late-payment surcharges, leaving ~PKR 423bn in unpaid dues to 18 CPEC power plants — a "
            "live source of financing friction distinct from the sovereign debt itself."
        ),
        "sources": [
            ("The Print: China becomes Pakistan's biggest creditor", "https://theprint.in/go-to-pakistan/china-pakistans-biggest-creditor-never-ending-loop-debt/2388995/"),
            ("Bloomberg: Pakistan Secures Debt Extension Assurances From China, UAE", "https://www.bloomberg.com/news/articles/2024-08-06/pakistan-secures-debt-extension-assurances-from-china-uae"),
            ("Outlook India: Pakistan Faces Fresh Debt Blow as Chinese Power Firms Refuse Concessions", "https://www.outlookindia.com/international/pakistan-faces-fresh-debt-blow-as-chinese-power-firms-refuse-concessions"),
        ],
    },
    "LKA": {
        "summary": (
            "Sri Lanka's post-default bilateral debt is concentrated in China, India, and Japan. An "
            "Official Creditors Committee (OCC), co-chaired by India, France, and Japan, was formed "
            "April 13, 2023 to coordinate restructuring talks. A Memorandum of Understanding signed "
            "June 26, 2024 restructured $5.8bn of bilateral debt via slashed interest rates and longer "
            "repayment schedules, saving Sri Lanka an estimated $5bn — one of the clearest examples in "
            "this dataset of a country's YoY risk-score improvement (-9.4) being traceable to a named, "
            "dated financial event."
        ),
        "sources": [
            ("The Diplomat: Sri Lanka Reaches Debt Restructuring Deal", "https://thediplomat.com/2024/06/sri-lanka-reaches-debt-restructuring-deal-with-bilateral-creditors-including-china-and-india/"),
            ("VOA: Sri Lanka to save $5bn from bilateral debt deal", "https://www.voanews.com/a/sri-lanka-to-save-5bn-from-bilateral-debt-deal-/7681898.html"),
            ("Al Jazeera: Japan, India, France form common platform for Sri Lanka creditors", "https://www.aljazeera.com/news/2023/4/14/japan-india-france-form-common-platform-for-sri-lanka-creditors"),
        ],
    },
    "MDV": {
        "summary": (
            "The Maldives is caught between its two largest creditors: China (~$1.3bn owed) and India "
            "(~$130m owed), against a debt-to-GDP ratio of ~110% (~$8.2bn total, Mar 2024). President "
            "Muizzu was elected in Sept 2023 on a China-leaning platform pledging to remove Indian "
            "troops, but by 2024 was pivoting back toward India as Chinese debt-service obligations "
            "came due — a clear illustration of how creditor concentration shapes foreign policy "
            "alignment in real time, not just abstractly."
        ),
        "sources": [
            ("Bloomberg: Maldives Pivots Back Toward India to Ease China Debt Squeeze", "https://www.bloomberg.com/news/articles/2024-10-07/maldives-seeks-to-repair-ties-with-india-as-debt-crisis-looms"),
            ("Asia Times: Debt forces Maldives to pivot back to India from China", "https://asiatimes.com/2024/10/debt-forces-maldives-to-pivot-back-to-india-from-china/"),
        ],
    },
    "EGY": {
        "summary": (
            "Gulf states (UAE, Saudi Arabia, Qatar) are Egypt's most consequential economic backers, "
            "typically via central bank deposits and direct investment rather than bond-market lending. "
            "The clearest recent example is the UAE's $35bn Ras El-Hekma coastal development deal (Feb "
            "2024) — the largest single FDI inflow in Egyptian history — struck at the same moment the "
            "IMF expanded its EFF to $8bn, illustrating how Gulf capital and IMF financing have moved "
            "in tandem to backstop Egypt's currency and reserves."
        ),
        "sources": [
            ("The Washington Institute: The IMF and UAE Swoop In to Ease Egypt's Economic Crisis", "https://www.washingtoninstitute.org/policy-analysis/imf-and-uae-swoop-ease-egypts-economic-crisis"),
            ("The National: Egypt finalises $8bn deal with IMF", "https://www.thenationalnews.com/business/economy/2024/03/06/egypt-imf-currency-egyptian-pound-record-low/"),
        ],
    },
    "QAT": {
        "summary": (
            "Qatar's most consequential regional relationship dynamic was the 2017-2021 blockade by "
            "Saudi Arabia, the UAE, Bahrain, and Egypt over alleged support for extremism and ties to "
            "Iran — a rare case of a Gulf Cooperation Council member being economically isolated by its "
            "own bloc-mates. Relations fully normalized at the Jan 2021 AlUla summit, and Qatar has "
            "since used LNG export revenue and high-visibility hosting (2022 World Cup, COP28) to "
            "rebuild regional standing."
        ),
        "sources": [
            ("Wikipedia: Qatar diplomatic crisis", "https://en.wikipedia.org/wiki/Qatar_diplomatic_crisis"),
            ("GlobalSecurity.org: Egypt and Qatar restore diplomatic ties", "https://www.globalsecurity.org/military/library/news/2021/01/mil-210120-sputnik01.htm"),
        ],
    },
    "JOR": {
        "summary": (
            "The United States is Jordan's single most important economic partner outside of trade: "
            "roughly $1.45-1.82bn in annual US foreign aid (FY2024) makes Jordan one of the largest "
            "recipients of US assistance worldwide relative to its size, underwriting a meaningful "
            "share of the government budget. Trade-wise, Jordan's Qualifying Industrial Zones (QIZs) "
            "allow duty-free garment exports to the US, a arrangement tied directly to the peace treaty "
            "with Israel and regional economic integration."
        ),
        "sources": [
            ("USAFacts: US foreign aid to Jordan", "https://usafacts.org/answers/how-much-foreign-aid-does-the-us-provide/countries/jordan/"),
            ("Congress.gov CRS: Jordan — Background and U.S. Relations", "https://www.congress.gov/crs-product/RL33546"),
        ],
    },
    "ISR": {
        "summary": (
            "The United States is Israel's dominant strategic and economic partner. Baseline US "
            "military aid runs ~$3.8bn/year under a standing Memorandum of Understanding, but wartime "
            "supplementals pushed total US military assistance to at least $16.3bn between October "
            "2023 and 2025 — including an $8.7bn supplemental package in April 2024 alone. This scale "
            "of external military financing is functionally unique in this dataset; no other tracked "
            "country receives comparable single-country backing."
        ),
        "sources": [
            ("Congress.gov CRS: U.S. Foreign Aid to Israel", "https://www.congress.gov/crs-product/RL33222"),
            ("Statista: U.S. military aid to Israel 2025", "https://www.statista.com/statistics/1625044/us-military-aid-to-israel/"),
            ("CFR: U.S. Aid to Israel in Four Charts", "https://www.cfr.org/articles/us-aid-israel-four-charts"),
        ],
    },
    "DZA": {
        "summary": (
            "Algeria's most consequential economic relationship is with Europe via natural gas, not "
            "debt. After Russia's 2022 invasion of Ukraine, Italy moved aggressively to cut its "
            "reliance on Russian gas, and Eni (Italy), alongside Occidental (US) and TotalEnergies "
            "(France), signed a $4bn production-sharing deal with state firm Sonatrach in July 2022, "
            "with volumes through the Transmed pipeline rising toward 9 billion cubic meters/year by "
            "2023-24. This has made Algeria one of Europe's most strategically important gas suppliers "
            "practically overnight, a rare case of a geopolitical shock (the Ukraine war) directly "
            "reshaping a tracked country's trade profile."
        ),
        "sources": [
            ("Al Jazeera: Algeria's growing importance to Italy", "https://www.aljazeera.com/news/2022/6/9/algerias-growing-importance-to-italy"),
            ("Al Jazeera: Eni inks deal to boost Algerian gas imports", "https://www.aljazeera.com/economy/2022/5/26/italys-power-giant-eni-inks-deal-to-boost-algerian-gas-imports"),
            ("France24: Italy PM signs Algeria gas deals to reduce Russia reliance", "https://amp.france24.com/en/live-news/20220411-italy-pm-signs-algeria-gas-deals-to-reduce-russia-reliance"),
        ],
    },
    "BHR": {
        "summary": (
            "Bahrain's economy is functionally an extension of Saudi Arabia's: it is physically "
            "connected via the King Fahd Causeway, refines significant volumes of Saudi crude, and "
            "relies on Gulf Cooperation Council financial backing (a $10bn GCC support package was "
            "extended in 2018 to help stabilize its finances after a debt scare). This makes Bahrain's "
            "sovereign risk profile unusually dependent on the health of its much larger neighbor rather "
            "than standing fully on its own economic base."
        ),
        "sources": [
            ("Reuters coverage of the 2018 Gulf support package for Bahrain (general reference)", "https://en.wikipedia.org/wiki/Economy_of_Bahrain"),
        ],
    },
    "IRN": {
        "summary": (
            "China is overwhelmingly Iran's most important economic lifeline, buying the large majority "
            "of Iran's sanctioned oil exports — often at a discount, shipped via a 'shadow fleet' of "
            "tankers designed to obscure origin and evade Western sanctions enforcement. This single "
            "relationship is what has allowed Iran's economy to avoid total collapse under sanctions "
            "since 2018, but it also leaves Iran's export revenue almost entirely hostage to Chinese "
            "demand and to how aggressively the US enforces secondary sanctions on that trade."
        ),
        "sources": [
            ("Reuters/Reuters-style reporting on Iran-China shadow fleet oil trade (general reference)", "https://en.wikipedia.org/wiki/Sanctions_against_Iran"),
        ],
    },
    "IRQ": {
        "summary": (
            "Iraq's reconstruction and energy sectors are increasingly financed and built by Chinese "
            "firms under 'oil-for-reconstruction' arrangements, while Iraq remains dependent on "
            "neighboring Iran for a meaningful share of its electricity and natural gas supply — a "
            "dependency the US has repeatedly pressured Baghdad to reduce via sanctions-waiver "
            "brinkmanship. This dual exposure (Chinese capital, Iranian energy) sits awkwardly "
            "alongside Iraq's continued security relationship with the United States."
        ),
        "sources": [
            ("CFR/Reuters-style reporting on Iraq's Iran energy dependency (general reference)", "https://www.cfr.org/global-conflict-tracker/conflict/political-instability-iraq"),
        ],
    },
    "LBY": {
        "summary": (
            "Libya's oil-export economy is deeply tied to Italy's Eni, the dominant foreign operator of "
            "Libyan oil and gas fields since the Gaddafi era. Politically, Libya's civil-conflict "
            "factions each have distinct foreign backers: Turkey supports the Tripoli-based GNU with "
            "military and construction contracts, while the UAE and Russia have backed Haftar's LNA in "
            "the east — meaning Libya's fractured domestic politics are mirrored by fractured, "
            "competing foreign patronage."
        ),
        "sources": [
            ("GIS Reports: Libya's fractures drift toward permanence", "https://www.gisreportsonline.com/r/libyas-divisions-harden/"),
        ],
    },
    "MAR": {
        "summary": (
            "France is Morocco's most important economic patron, and the relationship deepened sharply "
            "in 2024 when France formally recognized Moroccan sovereignty over Western Sahara — a "
            "major diplomatic win for Rabat — accompanied by roughly 22 new economic and trade "
            "agreements spanning high-speed rail, energy, agriculture, and infrastructure investment, "
            "some of it explicitly directed into Western Sahara itself. The move strained France's "
            "parallel relationship with Algeria, illustrating how Morocco's and Algeria's competing "
            "claims over the territory ripple into their separate relationships with European powers."
        ),
        "sources": [
            ("France24: France backs Morocco's autonomy plan for disputed Western Sahara", "https://www.france24.com/en/france/20240730-france-backs-morocco-s-autonomy-plan-for-disputed-western-sahara"),
            ("Atlantic Council: France has sided with Morocco on the Western Sahara", "https://www.atlanticcouncil.org/blogs/new-atlanticist/france-has-sided-with-morocco-on-the-western-sahara-how-might-algeria-respond/"),
            ("Al Jazeera: EU-Morocco trade deals in Western Sahara ruled invalid", "https://www.aljazeera.com/news/2024/10/4/eu-morocco-trade-deals-in-western-sahara-ruled-invalid-rabat-claims-bias"),
        ],
    },
    "OMN": {
        "summary": (
            "China has committed roughly $10.7bn (via a Chinese-led consortium and an Asian "
            "Infrastructure Investment Bank loan) to build an industrial city inside the Duqm Special "
            "Economic Zone, a flagship Belt and Road-linked project positioning Oman as a potential "
            "alternative shipping route that bypasses the Strait of Hormuz entirely — a strategically "
            "significant hedge given the 2026 Iran-Israel-US war's Hormuz-related shipping risk. Not "
            "every planned Chinese project at Duqm has proceeded on schedule, with some delayed or "
            "scaled back for commercial reasons."
        ),
        "sources": [
            ("Carnegie Endowment: Duqm at the Crossroads", "https://carnegieendowment.org/sada/2026/03/duqm-at-the-crossroads-omans-strategic-port-and-its-role-in-vision-2040"),
            ("CSIS: Dire Straits — China's Push to Secure Its Energy Interests in the Middle East", "https://features.csis.org/hiddenreach/china-middle-east-military-facility/"),
        ],
    },
    "SAU": {
        "summary": (
            "China is Saudi Arabia's single largest oil customer, a relationship Riyadh has "
            "deliberately deepened even as it maintains its longstanding US security partnership — a "
            "hedging strategy visible across the Gulf. As a major net creditor rather than a debtor, "
            "Saudi Arabia's key 'financing arrangement' is outbound, not inbound: its Public Investment "
            "Fund (PIF) is one of the world's largest sovereign wealth funds, deploying capital abroad "
            "(including into US and European markets) rather than seeking external financing."
        ),
        "sources": [
            ("EIA / general reference on Saudi-China oil trade", "https://www.eia.gov/international/analysis/country/SAU"),
        ],
    },
    "SYR": {
        "summary": (
            "Post-Assad Syria's reconstruction is a live bidding ground for regional influence: Turkey "
            "has moved fastest with construction and infrastructure contracts under the new "
            "transitional government, while Gulf states (particularly Qatar) have signaled reconstruction "
            "investment interest contingent on the transition stabilizing. Western sanctions relief "
            "remains only partially unwound, which continues to constrain the international financing "
            "Syria would need for a full rebuild after 13 years of civil war."
        ),
        "sources": [
            ("Belfer Center: External States and Syria's Challenge of Reunification", "https://www.belfercenter.org/research-analysis/external-states-and-syrias-challenge-reunification-under-transitional-president"),
        ],
    },
    "TUN": {
        "summary": (
            "The European Union — led by France, Italy, and Germany — accounts for roughly 70%+ of "
            "Tunisia's trade, making it by far Tunisia's most consequential economic relationship, "
            "ahead of any single creditor. This EU dependency is also a source of leverage: EU "
            "migration-management funding (tied to Tunisia's role as a departure point for migrants "
            "crossing to Italy) has become intertwined with broader economic support discussions, "
            "layered on top of the unresolved IMF standoff described above."
        ),
        "sources": [
            ("General EU-Tunisia trade relationship reference", "https://policy.trade.ec.europa.eu/eu-trade-relationships-country-and-region/countries-and-regions/tunisia_en"),
        ],
    },
    "ARE": {
        "summary": (
            "Like Saudi Arabia and Qatar, the UAE is a net capital exporter, not an aid or loan "
            "recipient — Abu Dhabi's ADIA and Mubadala sovereign wealth funds are among the world's "
            "largest, investing UAE oil wealth into global markets. Dubai's re-export economy makes "
            "China and India its largest trading partners by volume, while the 2020 Abraham Accords "
            "opened a fast-growing new trade and investment channel with Israel."
        ),
        "sources": [
            ("General reference on UAE sovereign wealth funds and Abraham Accords trade", "https://en.wikipedia.org/wiki/Abraham_Accords"),
        ],
    },
    "YEM": {
        "summary": (
            "Yemen's internationally recognized government has been financially sustained largely by "
            "Saudi Arabia and the UAE since the Saudi-led coalition intervened in 2015, while the "
            "Houthi-controlled north receives military and financial backing from Iran. This split "
            "external patronage mirrors the country's territorial division and is a direct driver of "
            "the near-total import dependency (~90% of food) noted in its trade profile above."
        ),
        "sources": [
            ("CFR Global Conflict Tracker: Yemen", "https://www.cfr.org/global-conflict-tracker/conflict/war-yemen"),
        ],
    },
    "AFG": {
        "summary": (
            "With ~$7bn in central bank assets frozen by the US and a further ~$2bn frozen by European "
            "states since the 2021 Taliban takeover, Afghanistan has no meaningful access to its own "
            "reserves or to World Bank/IMF financing. China has emerged as the most active new economic "
            "actor, pursuing mining agreements (copper, and reported interest in lithium and rare "
            "earths) with the Taliban government, though large-scale extraction has been slow to "
            "materialize given security and infrastructure constraints."
        ),
        "sources": [
            ("The Diplomat: Taliban Takeover — World Bank and IMF Halt Aid", "https://thediplomat.com/2021/08/taliban-takeover-world-bank-and-imf-halt-aid-us-freezes-afghan-assets/"),
            ("Wikipedia: Afghan frozen assets", "https://en.wikipedia.org/wiki/Afghan_frozen_assets"),
        ],
    },
    "BGD": {
        "summary": (
            "The US and EU are Bangladesh's dominant export markets by far, as the destination for the "
            "overwhelming majority of its ready-made garment exports, while China is its largest import "
            "source (machinery and raw materials for that same garment industry). This creates a "
            "structural dependency on Western consumer demand for its single largest export earner, "
            "layered on top of the 2023 IMF loan and 2024 political upheaval already noted above."
        ),
        "sources": [
            ("World Bank Bangladesh overview (general reference)", "https://www.worldbank.org/en/country/bangladesh/overview"),
        ],
    },
    "BTN": {
        "summary": (
            "Bhutan's economy is almost entirely oriented around a single relationship: India is both "
            "its dominant export market (via hydropower electricity sales) and its dominant import "
            "source, with the Indian rupee even accepted alongside Bhutan's own currency domestically. "
            "This is one of the most concentrated bilateral economic relationships in this entire "
            "dataset — there is no meaningful 'second partner' to speak of."
        ),
        "sources": [
            ("ADB: Bhutan's Hydropower Sector — 12 Things to Know", "https://www.adb.org/features/bhutan-s-hydropower-sector-12-things-know"),
        ],
    },
    "IND": {
        "summary": (
            "India's trade relationships are genuinely diversified rather than concentrated: the United "
            "States is its single largest overall trading partner, while China is its largest source of "
            "imports (a politically uncomfortable dependency given the two countries' border tensions "
            "and strategic rivalry). India is also increasingly an outbound investor and creditor in "
            "its own region — for instance building the Chabahar port in Iran and extending financing "
            "to Maldives and Sri Lanka — making it one of the few tracked countries acting as both a "
            "aid recipient's neighbor and a regional financier in its own right."
        ),
        "sources": [
            ("ThinkBRICS: China Emerges as India's Largest Trading Partner", "https://thinkbrics.substack.com/p/china-emerges-as-indias-largest-trading"),
        ],
    },
    "NPL": {
        "summary": (
            "Nepal sits at the center of an India-China competition for influence: India remains "
            "overwhelmingly dominant in trade and is the primary destination for labor migration "
            "underpinning Nepal's remittance economy, while China has pushed Belt and Road-linked "
            "infrastructure financing as a competing avenue of influence. Nepal's landlocked geography "
            "between the two giants leaves it with limited practical alternatives to this dual "
            "dependency."
        ),
        "sources": [
            ("General reference on Nepal's India/China balancing", "https://en.wikipedia.org/wiki/Foreign_relations_of_Nepal"),
        ],
    },
    "KWT": {
        "summary": (
            "Like Saudi Arabia, the UAE, and Qatar, Kuwait is a net creditor to the world rather than a "
            "borrower: the Kuwait Investment Authority — one of the oldest and largest sovereign wealth "
            "funds globally, established in 1953 — invests oil revenue into international markets "
            "rather than seeking external financing. Its crude oil sales flow predominantly to Asian "
            "buyers (China, India, South Korea, Japan), while its domestic politics remain shaped by "
            "recurring friction between the Emir and an elected National Assembly, most recently "
            "resolved by the Emir's 2024 dissolution of parliament noted above."
        ),
        "sources": [
            ("General reference on the Kuwait Investment Authority", "https://en.wikipedia.org/wiki/Kuwait_Investment_Authority"),
        ],
    },
    "LBN": {
        "summary": (
            "Lebanon is a striking case of lost external patronage: Gulf states that historically "
            "propped up Lebanon's economy and banking sector largely withdrew financial support after "
            "the 2019-2020 collapse, frustrated by the entrenched sectarian political system's failure "
            "to enact reform. France retains a historical patron role (colonial-era ties and periodic "
            "diplomatic mediation) but has not stepped in with financing at the scale of the crisis. "
            "With no active IMF program (see Financing Arrangements above) and no major bilateral "
            "backer stepping in, Lebanon is unusually short of external anchors for a country in this "
            "much distress — a key reason it sits at the top of the risk ranking."
        ),
        "sources": [
            ("World Bank Lebanon Economic Monitor (general reference)", "https://www.worldbank.org/en/country/lebanon/overview"),
        ],
    },
}


# ============================================================
# COUNTRY TRADE & SECTOR PROFILES — main economic sectors, top exports,
# top imports, and leading trade partners for all 26 tracked countries.
# Compiled from well-established, stable economic-geography knowledge
# (the kind found in the CIA World Factbook and the Observatory of
# Economic Complexity / UN Comtrade) rather than a single per-country
# citation — see the Methodology tab for the full source list. Figures
# describing shares (e.g. "~90% of exports") are directional, not
# precise-to-the-decimal statistics.
# ============================================================
COUNTRY_TRADE_PROFILE = {
    "DZA": {"sectors": "Hydrocarbons (oil & gas), agriculture", "exports": "Crude oil, natural gas/LNG (pipeline to Europe)", "imports": "Machinery, food, consumer goods", "partners": "Italy, France, Spain, China"},
    "BHR": {"sectors": "Oil refining, aluminum smelting (Alba), financial services/banking hub, tourism", "exports": "Refined petroleum, aluminum", "imports": "Crude oil (for refining), machinery", "partners": "Saudi Arabia, US, China"},
    "EGY": {"sectors": "Suez Canal transit fees, tourism, natural gas, textiles, agriculture, remittances", "exports": "Petroleum products, natural gas, textiles/garments, fruits & vegetables", "imports": "Wheat (top global importer), machinery, vehicles, fuel", "partners": "EU, US, China, Gulf states (investment/remittances)"},
    "IRN": {"sectors": "Oil & gas, petrochemicals, agriculture, mining", "exports": "Crude oil (mainly to China), petrochemicals, pistachios, carpets", "imports": "Machinery, foodstuffs, consumer goods", "partners": "China (dominant oil buyer), Iraq, UAE, Turkey, Russia"},
    "IRQ": {"sectors": "Oil (~90%+ of government revenue and exports), agriculture", "exports": "Crude oil (Basra terminals, Kurdistan pipeline)", "imports": "Refined fuel, food, machinery, vehicles", "partners": "China (major oil buyer), India, Turkey, Iran"},
    "ISR": {"sectors": "High-tech/software, pharmaceuticals, diamonds, defense industry, advanced agriculture", "exports": "High-tech equipment/software, pharmaceuticals, polished diamonds, defense/military equipment", "imports": "Raw materials, military equipment, energy, rough diamonds, consumer goods", "partners": "United States (dominant), EU, China, India, UAE (post-Abraham Accords)"},
    "JOR": {"sectors": "Phosphates & potash mining, tourism, pharmaceuticals, textiles (QIZ), remittances, US aid", "exports": "Potash, phosphates, pharmaceuticals, garments (duty-free to US via QIZ)", "imports": "Crude oil/fuel, machinery, food", "partners": "United States (QIZ trade + aid), Saudi Arabia, Iraq, India"},
    "KWT": {"sectors": "Oil (~90% of exports), sovereign wealth management (Kuwait Investment Authority)", "exports": "Crude oil", "imports": "Machinery, vehicles, food", "partners": "China, India, South Korea, Japan"},
    "LBN": {"sectors": "Historically banking/finance (collapsed since 2019), remittances, agriculture, tourism", "exports": "Jewelry, base metals, limited agricultural goods", "imports": "Petroleum, vehicles, consumer goods, machinery (heavily import-dependent)", "partners": "Gulf states, EU, China"},
    "LBY": {"sectors": "Oil (near-total dependence — government revenue and exports)", "exports": "Crude oil almost exclusively", "imports": "Food, machinery, consumer goods, fuel (damaged domestic refining capacity)", "partners": "Italy (major oil buyer, ENI), China, Turkey, UAE"},
    "MAR": {"sectors": "Phosphates (world's largest reserves, OCP Group), automotive manufacturing, textiles, agriculture, tourism, aerospace", "exports": "Phosphates/fertilizers, automobiles & auto parts, textiles, citrus", "imports": "Crude oil, machinery, wheat", "partners": "EU — France and Spain dominant, United States (FTA)"},
    "OMN": {"sectors": "Oil & gas, logistics/ports (Duqm), fisheries, developing tourism", "exports": "Crude oil, natural gas/LNG, refined petroleum", "imports": "Machinery, vehicles, food", "partners": "China (major oil buyer), UAE, India"},
    "QAT": {"sectors": "LNG (one of the world's largest exporters), oil, financial services, sovereign wealth fund (QIA)", "exports": "LNG, crude oil/condensates, petrochemicals", "imports": "Machinery, food, vehicles", "partners": "Japan, South Korea, China, India"},
    "SAU": {"sectors": "Oil (Saudi Aramco, world's largest exporter), petrochemicals, Vision 2030 tourism/entertainment diversification", "exports": "Crude oil, petrochemicals, plastics", "imports": "Machinery, vehicles, food, electronics", "partners": "China (largest oil buyer), Japan, India, South Korea, US"},
    "SYR": {"sectors": "Pre-war: oil, agriculture, textiles; post-civil-war economy devastated, reconstruction-dependent", "exports": "Olive oil and limited agricultural goods (formal exports minimal)", "imports": "Virtually everything given reconstruction needs, fuel", "partners": "Turkey (growing influence), Gulf states (reconstruction investment interest), Qatar"},
    "TUN": {"sectors": "Tourism, textiles/garments (EU-oriented manufacturing), phosphates, olive oil, automotive components", "exports": "Textiles/garments, olive oil (major global exporter), phosphates/fertilizers, auto parts", "imports": "Crude oil, machinery, wheat", "partners": "EU — France, Italy, Germany dominant (~70%+ of trade), Libya"},
    "ARE": {"sectors": "Oil (Abu Dhabi), Dubai re-export/logistics hub, tourism, financial services, real estate", "exports": "Crude oil, re-exported goods (gold, electronics, machinery), petrochemicals", "imports": "Gold, diamonds, machinery, vehicles (much for re-export)", "partners": "China, India, Saudi Arabia, Japan"},
    "YEM": {"sectors": "Pre-war oil/gas (largely halted), agriculture (qat, coffee — Yemen is coffee's historical origin), fishing", "exports": "Minimal — crude oil when operational, coffee, dried fish", "imports": "Food (~90% import-dependent — a major humanitarian vulnerability), fuel, medicine", "partners": "Saudi Arabia (aid/imports), UAE, historically China (oil)"},
    "AFG": {"sectors": "Agriculture (fruits, nuts; opium poppy historically dominant), untapped mining potential (copper, lithium, rare earths), aid/remittance-dependent", "exports": "Dried fruits & nuts, carpets, some minerals", "imports": "Food, fuel, machinery (heavily import-dependent)", "partners": "Pakistan, Iran, China (growing mining interest)"},
    "BGD": {"sectors": "Ready-made garments (~80%+ of export earnings, world's 2nd-largest garment exporter), remittances, agriculture, pharmaceuticals", "exports": "Garments/textiles (dominant), leather goods, jute, frozen shrimp/fish", "imports": "Raw cotton, machinery, fuel, food", "partners": "US, EU (garment buyers), China (largest import source)"},
    "BTN": {"sectors": "Hydropower (exported to India), tourism (high-value, low-volume model), agriculture, cement", "exports": "Electricity (hydropower), ferrosilicon, cement, cardamom", "imports": "Fuel, machinery, vehicles, food", "partners": "India (overwhelmingly dominant for both exports and imports)"},
    "IND": {"sectors": "IT/software services, pharmaceuticals ('pharmacy of the world'), textiles, agriculture, automotive, petroleum refining", "exports": "Refined petroleum, pharmaceuticals, IT services, textiles/garments, gems & jewelry, engineering goods", "imports": "Crude oil, gold, electronics, coal", "partners": "United States (largest trade partner), China (largest import source), UAE, Saudi Arabia"},
    "MDV": {"sectors": "Tourism (resorts, roughly a third of GDP), fishing (tuna)", "exports": "Fish/tuna products (frozen and canned)", "imports": "Virtually everything — food, fuel, construction materials, consumer goods", "partners": "Thailand, UAE, India, China (imports); Europe/UK (tourism source markets)"},
    "NPL": {"sectors": "Agriculture, remittances (~25%+ of GDP — among the world's most remittance-dependent economies), tourism, developing hydropower", "exports": "Carpets, garments, pashmina/textiles, tea, cardamom", "imports": "Petroleum products, machinery, gold, vehicles", "partners": "India (overwhelmingly dominant), China (growing infrastructure ties)"},
    "PAK": {"sectors": "Textiles/garments (dominant export sector), agriculture, remittances, cement, growing IT/freelance services", "exports": "Textiles/garments (~55%+ of exports), rice, leather goods, sporting goods", "imports": "Petroleum/fuel, machinery, palm oil, chemicals", "partners": "US/EU (garment markets), China (CPEC-linked, largest import source), Saudi Arabia/UAE (remittances, oil)"},
    "LKA": {"sectors": "Tea, garments/textiles, tourism, remittances, rubber/coconut products", "exports": "Garments/textiles (dominant), tea, rubber products, spices", "imports": "Petroleum, textile raw materials, machinery, food", "partners": "US/EU (garment markets), India, China (imports, infrastructure ties)"},
}


# ============================================================
# LIVE / ONGOING CONFLICTS — the major current regional flashpoints,
# each tagged with which of the 26 tracked countries it affects most
# directly. Curated and fact-checked as of August 2026, not a live feed.
# ============================================================
LIVE_CONFLICTS = [
    {
        "name": "2026 Iran-Israel-US War",
        "status": "Active / unresolved",
        "stats": [
            ("Strikes in Operation Epic Fury", "~900 in 12 hours (Feb 28, 2026)"),
            ("School strike casualties", "~170 killed, Minab"),
            ("Duration of active operations", "Feb 28 - May 5, 2026"),
            ("US military aid to Israel since Oct 2023", "$16.3bn+"),
        ],
        "groups": "Israel Defense Forces, United States military, Islamic Revolutionary Guard Corps (IRGC), Iran's Assembly of Experts (Khamenei succession)",
        "affected": ["IRN", "ISR", "SAU", "QAT", "ARE", "KWT", "BHR", "OMN", "IRQ"],
        "summary": (
            "The single largest live risk event in the region. A June 2025 ceasefire ending the "
            "'Twelve-Day War' between Israel and Iran held for eight months before collapsing. On "
            "February 28, 2026, the US and Israel launched Operation Epic Fury — roughly 900 strikes "
            "in 12 hours against Iranian nuclear, missile, and military targets. The strikes killed "
            "Supreme Leader Ali Khamenei and dozens of senior officials; a strike near a naval base in "
            "Minab also killed ~170 people at an adjacent girls' school. Iran's Assembly of Experts "
            "appointed Khamenei's son, Mojtaba Khamenei, as successor. Active operations concluded "
            "May 5, 2026, and a June 2026 memorandum of understanding sought to end the conflict and "
            "reopen the Strait of Hormuz — but Iran fired on three commercial vessels on July 6-7, "
            "testing the truce and prompting further US strikes. Core disputes over Iran's nuclear "
            "program, the Strait of Hormuz, and sanctions relief remain unresolved."
        ),
        "market_impact": (
            "The Strait of Hormuz carries roughly a fifth of global oil supply; any sustained closure "
            "or harassment of shipping there threatens Gulf oil/gas export revenue directly (Saudi "
            "Arabia, UAE, Qatar, Kuwait, Oman, Bahrain) and global energy prices broadly. Iran's own "
            "economy — already running on 7 of 10 tracked risk factors due to sanctions-driven data "
            "gaps — faces a further collapse in institutional continuity following the leadership "
            "assassination. Brookings analysis notes a second-order effect: the war has diverted US "
            "diplomatic attention and energy away from the Gaza ceasefire process entirely, worsening "
            "conditions on the ground there even as headline hostilities in Gaza have wound down."
        ),
        "sources": [
            ("Wikipedia: Timeline of the 2026 Iran conflict", "https://en.wikipedia.org/wiki/Timeline_of_the_2026_Iran_conflict"),
            ("Britannica: 2026 Iran war", "https://www.britannica.com/event/2026-Iran-war"),
            ("CFR Global Conflict Tracker", "https://www.cfr.org/global-conflict-tracker/conflict/confrontation-between-united-states-and-iran"),
            ("UK House of Commons Library", "https://commonslibrary.parliament.uk/research-briefings/cbp-10521/"),
            ("Brookings: The road to the Israel-Iran war", "https://www.brookings.edu/articles/the-road-to-the-israel-iran-war/"),
            ("Brookings: The cycle of violence — from Israel-Palestine to Iran and back", "https://www.brookings.edu/articles/the-cycle-of-violence-from-israel-palestine-to-iran-and-back/"),
        ],
    },
    {
        "name": "Red Sea Shipping Crisis & Houthi-Saudi Blockade",
        "status": "Active, re-escalating",
        "stats": [
            ("Egypt's Suez Canal revenue, 2023 vs 2024", "$10.3bn → $4bn (-61%)"),
            ("Estimated 2024 revenue loss", "~$7bn"),
            ("Ships transiting Suez, 2023 vs 2024", "26,000+ → 13,213 (-50%)"),
            ("Houthi attacks on shipping by Oct 2024", "190+"),
        ],
        "groups": "Houthi movement / Ansar Allah (Iran-aligned), Saudi-led coalition, Egyptian Suez Canal Authority",
        "affected": ["YEM", "EGY", "SAU", "ARE", "QAT", "ISR"],
        "summary": (
            "Houthi forces began attacking Israel-linked shipping in the Red Sea in November 2023 "
            "following the Gaza war, in what Bloomberg called the biggest disruption to global trade "
            "since the COVID-19 pandemic. Attacks paused briefly after the October 2025 Gaza ceasefire, "
            "then resumed alongside the February 2026 Iran-Israel-US war. On July 20, 2026, the Houthis "
            "declared a formal naval blockade against Saudi Arabia, framing it as retaliation for a "
            "Saudi 'siege' on Yemen and breaking a years-long civil-war truce. Attacks on commercial "
            "shipping continued into August 2026, including a Saudi oil tanker off Yanbu and a lethal "
            "strike killing six on a cargo ship on August 11."
        ),
        "market_impact": (
            "Egypt's Suez Canal revenue — historically ~2% of its GDP — fell over 60% in 2024 alone "
            "(from $10.3bn to $4bn, a ~$7bn loss) as shippers rerouted around Africa's Cape of Good "
            "Hope, adding 10-14 days and significant fuel cost per voyage. A widening blockade against "
            "Saudi Arabia threatens Gulf oil-export shipping lanes directly, not just Israel-linked "
            "traffic, broadening the economic exposure well beyond the original scope of the attacks."
        ),
        "sources": [
            ("Bloomberg: How Houthi Red Sea Ship Attacks Upended Global Trade", "https://www.bloomberg.com/news/articles/2025-05-01/how-houthi-red-sea-ship-attacks-upended-global-trade"),
            ("Bloomberg: Red Sea Disruptions Cost Egypt $7 Billion", "https://www.bloomberg.com/news/articles/2024-12-26/red-sea-disruptions-cost-egypt-7-billion-in-suez-revenues"),
            ("Al Jazeera: Houthis report attack on Saudi tanker", "https://www.aljazeera.com/news/2026/8/24/yemens-houthis-report-attack-on-saudi-ship"),
            ("UN Security Council Report, Jul 2026 Monthly Forecast", "https://www.securitycouncilreport.org/monthly-forecast/2026-07/the-red-sea.php"),
        ],
    },
    {
        "name": "Gaza War Aftermath & Fragile Ceasefire",
        "status": "Ceasefire holding but repeatedly violated",
        "stats": [
            ("War duration before ceasefire", "~2 years (Oct 2023 - Oct 2025)"),
            ("Ceasefire violations documented, 6 months in", "2,000+"),
            ("Palestinian deaths over the war", "72,000+"),
            ("Israel's Q4 2023 GDP contraction (annualized)", "-19.4%"),
            ("Bank of Israel est. total war cost, 2023-2025", "~$55.6bn"),
        ],
        "groups": "Hamas, Israel Defense Forces, US-brokered mediation team",
        "affected": ["ISR", "EGY", "JOR", "LBN"],
        "summary": (
            "The Gaza war, triggered by the October 7, 2023 Hamas attack, ran nearly two years before "
            "an Israel-Hamas ceasefire was signed on October 10, 2025 under a US-brokered 20-point plan. "
            "Six months in, Gaza's Government Media Office had documented over 2,000 ceasefire "
            "violations, including Israeli airstrikes and incursions across a newly established "
            "'Yellow Line' separating zones of control. Implementation of the plan's second phase has "
            "stalled, and the humanitarian situation in Gaza remains described by observers as "
            "catastrophic even under the nominal ceasefire."
        ),
        "market_impact": (
            "Israel's economy contracted 19.4% (annualized) in Q4 2023 alone at the war's peak, with "
            "the Bank of Israel estimating total 2023-2025 war costs near $55.6bn. Jordan and Egypt "
            "both carry tourism and refugee-related exposure to any renewed escalation, and Lebanon's "
            "southern border remains a live flashpoint via Hezbollah."
        ),
        "sources": [
            ("Al Jazeera: What Gaza looks like six months into 'ceasefire'", "https://www.aljazeera.com/news/2026/4/10/neither-war-nor-peace-what-gaza-looks-like-six-months-into-ceasefire"),
            ("Times of Israel: War-battered economy plunged almost 20%", "https://www.timesofisrael.com/war-battered-economy-plunged-almost-20-marking-sharpest-contraction-since-pandemic/"),
            ("J Street: Nine Months In — Assessing the Gaza Ceasefire", "https://jstreet.org/nine-months-in-assessing-the-status-of-the-gaza-ceasefire/"),
            ("Brookings: What could the Israel-Gaza deal mean for the Middle East?", "https://www.brookings.edu/articles/what-could-the-israel-gaza-deal-mean-for-the-middle-east/"),
        ],
    },
    {
        "name": "Syria's Post-Assad Transition",
        "status": "Fragile, ongoing",
        "stats": [
            ("Civil war duration before Assad's fall", "13 years (2011-2024)"),
            ("Rebel offensive to capture Damascus", "~11 days"),
            ("Transition timeline set by interim constitution", "5 years to elections"),
            ("World Bank reconstruction cost estimate, Oct 2025", "$216bn (range $140-345bn)"),
            ("Share of pre-conflict capital stock destroyed", "~1/3"),
            ("Investment commitments attracted in 2025", "$28bn (incl. $14bn MOUs at Aug 2025 Damascus ceremony)"),
            ("Registered Syrian refugees remaining in Jordan, Apr 2026", "~411,760 (down sharply from pre-2025)"),
            ("Lebanon-to-Syria cross-border return movements by Jun 22, 2026", "464,562+"),
        ],
        "groups": "Hay'at Tahrir al-Sham (HTS) / transitional government under Ahmed al-Sharaa, remnant Assad-era militias, Kurdish SDF",
        "affected": ["SYR", "LBN", "JOR", "IRQ"],
        "summary": (
            "The Assad regime fell on December 8, 2024 after a rapid rebel offensive led by Hay'at "
            "Tahrir al-Sham captured Damascus, ending a 13-year civil war. Ahmed al-Sharaa was declared "
            "transitional president in January 2025, and an interim constitutional declaration took "
            "effect in March 2025, setting out a 5-year path to elections. One year on, the transition "
            "remains disputed — no single national armed force yet exists, and localized violence "
            "(including renewed hostilities from March 2026) has continued. On the sanctions side, "
            "Washington repealed the Caesar Act via the FY2026 National Defense Authorization Act in "
            "December 2025 and the EU has lifted most broad-based economic restrictions from the Assad "
            "era, though targeted sanctions on regime-linked individuals and heavy compliance risk for "
            "banks and contractors remain — meaning sanctions relief is real but partial, not a clean "
            "reopening."
        ),
        "market_impact": (
            "The World Bank's October 2025 assessment put Syria's reconstruction need at roughly $216bn "
            "(a range of $140-345bn, which the Bank itself calls a likely underestimate; Syrian officials "
            "have cited figures as high as $600-900bn), with infrastructure alone accounting for 48% of "
            "the roughly $108bn in direct physical damage assessed so far. Investors have moved faster "
            "than the sanctions picture might suggest — Syria drew about $28bn in investment commitments "
            "in 2025, including $14bn in MOUs signed at a single August 2025 Damascus ceremony, led by "
            "Turkey ($11bn in energy/infrastructure), Saudi Arabia ($6.4bn), and the UAE ($800m for "
            "Tartus port development) — though MOUs are non-binding and actual disbursement will take "
            "years. For neighbors, the fiscal picture is now shifting: the World Bank estimates hosting "
            "Syrian refugees costs Lebanon's economy roughly $1.5bn a year, but returns have accelerated "
            "sharply since renewed Lebanon-Syria border hostilities began March 2, 2026 (464,562+ "
            "cross-border movements by late June), and Jordan's registered Syrian refugee population has "
            "fallen to roughly 411,760 by April 2026. That easing of the refugee-hosting burden is "
            "genuine relief for Lebanon's and Jordan's budgets, but the 2026 regional refugee response "
            "plan is itself operating on a $2.8bn ask — already cut 40% from 2025 — leaving those still "
            "displaced, and the returnees rebuilding inside Syria, with materially less international "
            "support than a year earlier."
        ),
        "sources": [
            ("Wikipedia: Fall of the Assad regime", "https://en.wikipedia.org/wiki/Fall_of_the_Assad_regime"),
            ("Belfer Center, Harvard Kennedy School", "https://www.belfercenter.org/research-analysis/external-states-and-syrias-challenge-reunification-under-transitional-president"),
            ("UK House of Commons Library: Syria one year after Assad", "https://commonslibrary.parliament.uk/research-briefings/cbp-10430/"),
            ("World Bank: Syria's Post-Conflict Reconstruction Costs Estimated at $216 Billion", "https://www.worldbank.org/en/news/press-release/2025/10/21/syria-s-post-conflict-reconstruction-costs-estimated-at-216-billion"),
            ("The Arab Weekly: Syria hopes for full lifting of US sanctions to push ahead with $216bn reconstruction", "https://thearabweekly.com/syria-hopes-full-lifting-us-sanctions-push-ahead-216-billion-reconstruction"),
            ("EUAA: Syria Country Focus — Impact on Civilian Population, Returns Abroad", "https://www.euaa.europa.eu/coi/syria/2025/country-focus/45-impact-violence-civilian-population/456-returns-abroad"),
        ],
    },
    {
        "name": "Sudan Civil War (regional spillover)",
        "status": "Active — not a tracked country, but a major regional shock",
        "stats": [
            ("People requiring humanitarian assistance (early war)", "~25 million"),
            ("Forcibly displaced", "~12 million"),
            ("Refugees fleeing across borders", "3 million+"),
            ("Sudanese refugees hosted by Egypt (incl. unregistered)", "~1.2 million"),
            ("Registered with UNHCR in Egypt, as of Jan 2025", "890,000+"),
            ("Newly arrived Sudanese children out of school (UNICEF/World Bank)", "54%"),
            ("Refugee families left without cash assistance after 2025 funding cuts", "~50,000 families / 164,000 people"),
        ],
        "groups": "Sudanese Armed Forces (SAF) under Abdul Fattah al-Burhan, Rapid Support Forces (RSF) under Mohamed Hamdan Dagalo",
        "affected": ["EGY"],
        "summary": (
            "Though Sudan is outside this tool's 26-country MENASA tracking scope, its civil war "
            "(erupted Apr 15, 2023, between the Sudanese Armed Forces and the Rapid Support Forces after "
            "a power struggle following their joint 2021 coup) is one of the world's largest displacement "
            "crises — roughly 12 million people forcibly displaced, with over 3 million fleeing across "
            "borders. Egypt has become the single largest host, sheltering an estimated 1.2 million "
            "Sudanese, of whom more than 890,000 were formally registered with UNHCR as of January 2025 "
            "(the remainder informal). A UNICEF/World Bank socioeconomic assessment found 54% of newly "
            "arrived Sudanese children are out of school, and UNHCR was forced to cut monthly cash "
            "assistance in 2025, leaving roughly 50,000 vulnerable refugee families — about 164,000 "
            "people — without reliable means to cover rent or food, pushing more of the burden onto "
            "Egypt's already-strained public services and informal labor market."
        ),
        "market_impact": (
            "The refugee influx lands directly on top of Egypt's own currency and Suez Canal-driven "
            "fragility rather than in isolation: absorbing over a million additional residents strains "
            "subsidized bread, fuel, and school places at the exact moment Egypt's government is trying "
            "to hold the line on IMF-mandated subsidy reform, and the largely informal Sudanese labor "
            "market participation adds downward pressure on already-low wages in Egypt's informal sector. "
            "Because international humanitarian funding for the Sudan response has been cut rather than "
            "expanded through 2025, more of this cost is being absorbed directly by Egyptian host "
            "communities and the state rather than offset by donor aid — a slow-burn fiscal drag layered "
            "on top of Egypt's debt and reserves picture that shows up nowhere in a single macro indicator."
        ),
        "sources": [
            ("Wikipedia: Sudanese civil war (2023-present)", "https://en.wikipedia.org/wiki/Sudanese_civil_war_(2023%E2%80%93present)"),
            ("Wikipedia: Humanitarian impact of the Sudanese civil war", "https://en.wikipedia.org/wiki/Humanitarian_impact_of_the_Sudanese_civil_war_(2023%E2%80%93present)"),
            ("UNHCR: Egypt Sudan Situation — Country Socioeconomic Profile, Jan 2025", "https://data.unhcr.org/en/documents/download/114065"),
            ("Development Action Platform: Egypt — Sudan Regional Crisis", "https://developmentactionrefugees.org/country-responses/egypt"),
        ],
    },
    {
        "name": "Israel-Hezbollah War & Lebanon Front",
        "status": "Ceasefire re-established Apr 2026, fragile",
        "stats": [
            ("Killed in Lebanon by mid-April 2026", "2,000+"),
            ("Displaced in Lebanon", "1 million+"),
            ("First ceasefire withdrawal window", "60 days (from Nov 27, 2024)"),
            ("Time between ceasefires", "~1 year, 5 months"),
        ],
        "groups": "Hezbollah (Iran-aligned), Israel Defense Forces, Lebanese Armed Forces, US/French mediators",
        "affected": ["LBN", "ISR"],
        "summary": (
            "A parallel front to the Gaza war: Hezbollah opened fire on northern Israel on Oct 8, 2023 "
            "in solidarity with Hamas, escalating into a full Israeli air and ground campaign across "
            "Lebanon by late 2024. A US/France-brokered ceasefire took effect Nov 27, 2024, requiring "
            "Hezbollah to withdraw north of the Litani River and Israel to withdraw from southern "
            "Lebanon — but both sides missed key provisions, and Israel struck Lebanon almost daily "
            "even under the 'ceasefire.' The truce effectively collapsed when the Feb 2026 Iran-Israel-"
            "US war broke out and Hezbollah resumed firing on Israel in retaliation for Khamenei's "
            "killing. A new ceasefire was reached Apr 16, 2026, but by that point the conflict had "
            "killed over 2,000 people in Lebanon and displaced more than 1 million."
        ),
        "market_impact": (
            "Lebanon's economy — already the most distressed in this dataset (rank 1 of 26, no active "
            "IMF program, defaulted since 2020) — has absorbed further destruction of housing, "
            "agriculture, and infrastructure across its south, on top of a currency and banking "
            "collapse that predates the war entirely. Reconstruction financing needs compound an "
            "already-unresolved sovereign debt problem."
        ),
        "sources": [
            ("Wikipedia: 2024 Israel-Lebanon ceasefire agreement", "https://en.wikipedia.org/wiki/2024_Israel%E2%80%93Lebanon_ceasefire_agreement"),
            ("Wikipedia: 2026 Israel-Lebanon ceasefire", "https://en.wikipedia.org/wiki/2026_Israel%E2%80%93Lebanon_ceasefire"),
            ("Al Jazeera: What we know about the Israel-Lebanon ceasefire", "https://www.aljazeera.com/news/2026/4/17/what-we-know-about-the-israel-lebanon-ceasefire"),
            ("International Crisis Group: Reinforcing the Shaky Israel-Lebanon Ceasefire", "https://www.crisisgroup.org/cmt/middle-east-north-africa/east-mediterranean-mena/lebanon-israelpalestine-united-states/reinforcing-shaky-israel-lebanon-ceasefire"),
        ],
    },
    {
        "name": "Libya's Rival Governments Standoff",
        "status": "Frozen stalemate, no resolution in sight",
        "stats": [
            ("2011 real GDP decline (civil war year)", "-62%"),
            ("Oil exports, 2012 vs 2014", "1.3 million b/d → 375,000 b/d"),
            ("Oil production during worst 2011 fighting", "as low as 22,000 b/d"),
            ("Years the political split has persisted", "12+ (since 2014)"),
        ],
        "groups": "Government of National Unity (GNU, Tripoli, PM Abdul Hamid Dbeibah), Government of National Stability (GNS, east, PM Osama Hamad), Libyan National Army (LNA, Gen. Khalifa Haftar), House of Representatives (HoR)",
        "affected": ["LBY"],
        "summary": (
            "Libya remains split between the UN-recognized GNU in Tripoli and the eastern GNS, backed "
            "by Haftar's LNA and the Tobruk-based House of Representatives. A 2020 ceasefire between "
            "the two sides continues to technically hold — there's been no return to nationwide "
            "fighting — but the parties remain deadlocked over election legislation that would "
            "reunify the country's governance. As of mid-2026, neither side has the military strength "
            "to unify Libya outright, but both have enough financial and armed leverage to block any "
            "settlement that threatens their position, producing a durable frozen conflict rather than "
            "an active war."
        ),
        "market_impact": (
            "This political split is the direct cause of the oil-export volatility that has plagued "
            "Libya since 2014, when rival factions began using oil terminal blockades as bargaining "
            "leverage, repeatedly cutting exports from over 1.3 million barrels/day (2012) to as low "
            "as 375,000 b/d. With nearly 100% of Libya's exports and government revenue tied to oil, "
            "this factional standoff is functionally the country's entire sovereign risk profile."
        ),
        "sources": [
            ("Security Council Report: Libya, August 2026 Monthly Forecast", "https://www.securitycouncilreport.org/monthly-forecast/2026-08/libya-69.php"),
            ("Wikipedia: Government of National Stability", "https://en.wikipedia.org/wiki/Government_of_National_Stability"),
            ("GIS Reports: Libya's fractures drift toward permanence", "https://www.gisreportsonline.com/r/libyas-divisions-harden/"),
        ],
    },
    {
        "name": "2026 Pakistan-Afghanistan War",
        "status": "Active, following Feb 2026 escalation",
        "stats": [
            ("Pakistani soldiers killed, Oct 2025 clash", "23+"),
            ("Afghan soldiers killed, Oct 2025 clash", "9+"),
            ("Cross-border offensive date", "Feb 26, 2026"),
            ("Pakistani counter-strike date", "Feb 27, 2026 (Kabul, Kandahar)"),
        ],
        "groups": "Tehreek-e-Taliban Pakistan (TTP), Islamic State — Khorasan Province (ISIS-K), Afghan Taliban government forces, Pakistani military",
        "affected": ["PAK", "AFG"],
        "summary": (
            "Pakistan has long accused the Afghan Taliban government of harboring the Tehreek-e-Taliban "
            "Pakistan (TTP), a separate militant group waging an insurgency inside Pakistan since 2021. "
            "Tensions turned into open warfare in October 2025 after a Pakistani airstrike on a TTP "
            "leader in Kabul triggered retaliatory Afghan strikes that killed at least 23 Pakistani "
            "soldiers — the deadliest clash between the two since the Taliban's 2021 takeover. A tenuous "
            "ceasefire followed, but on February 26, 2026, Afghan forces launched a cross-border "
            "offensive, and Pakistan responded the next day with coordinated air and ground strikes on "
            "Kabul, Kandahar, and other Afghan cities, targeting TTP and ISIS-K camps. A March 16, 2026 "
            "Pakistani strike on what was reportedly a drug rehabilitation facility killed and injured "
            "hundreds."
        ),
        "market_impact": (
            "This directly threatens Pakistan's fragile post-2024-EFF stabilization by diverting fiscal "
            "resources to military operations and disrupting the Pakistan-Afghanistan border trade "
            "corridor. For Afghanistan — already isolated by frozen central bank assets and halted "
            "World Bank/IMF aid since 2021 — the conflict compounds an economy with almost no formal "
            "financial buffers left to absorb further shocks."
        ),
        "sources": [
            ("Wikipedia: 2026 Afghanistan-Pakistan war", "https://en.wikipedia.org/wiki/2026_Afghanistan%E2%80%93Pakistan_conflict"),
            ("Britannica: Afghanistan-Pakistan Conflict 2025-2026", "https://www.britannica.com/topic/Afghanistan-Pakistan-Conflict-2025"),
            ("CFR Global Conflict Tracker: Violent Extremism in South Asia", "https://www.cfr.org/global-conflict-tracker/conflict/war-afghanistan"),
        ],
    },
    {
        "name": "India-Pakistan Kashmir Crisis",
        "status": "Ceasefire since May 2025, relations still frozen",
        "stats": [
            ("Killed in Pahalgam attack (trigger)", "26"),
            ("Civilians killed in Pakistani retaliation, Poonch", "16"),
            ("Time from attack to ceasefire", "18 days (Apr 22 - May 10, 2025)"),
            ("Most serious confrontation since", "1971 war"),
        ],
        "groups": "Indian Armed Forces, Pakistani Armed Forces, Kashmir-based militant groups",
        "affected": ["IND", "PAK"],
        "summary": (
            "The gunmen killing of 26 people at Pahalgam in Indian-administered Kashmir on April 22, "
            "2025 triggered the most serious India-Pakistan military confrontation since 1971. On the "
            "night of May 6-7, 2025, India struck targets in both Pakistan-administered Kashmir and "
            "Pakistan's own territory; Pakistan's army retaliated the next day with strikes on Poonch, "
            "Jammu, killing 16 civilians. A ceasefire was announced May 10, 2025, but the underlying "
            "dispute remains unresolved — India suspended the decades-old Indus Waters Treaty and "
            "commercial flights between the two countries stayed disrupted well into 2026."
        ),
        "market_impact": (
            "The suspended Indus Waters Treaty is a direct water-security risk for Pakistan's "
            "agriculture-dependent economy, since the Indus system irrigates the bulk of its farmland. "
            "For India, the crisis is a smaller relative shock given its far larger and more "
            "diversified economy, but it adds to South Asia's broader risk premium and keeps two "
            "nuclear-armed states in a state of unresolved military tension."
        ),
        "sources": [
            ("Wikipedia: 2025 India-Pakistan crisis", "https://en.wikipedia.org/wiki/2025_India%E2%80%93Pakistan_crisis"),
            ("CSIS: What Led to the Recent Crisis Between India and Pakistan?", "https://www.csis.org/analysis/what-led-recent-crisis-between-india-and-pakistan"),
            ("Stimson Center: Four Days in May — The India-Pakistan Crisis of 2025", "https://www.stimson.org/2025/four-days-in-may-the-india-pakistan-crisis-of-2025/"),
            ("UK House of Commons Library: Kashmir — Renewed India-Pakistan tensions", "https://commonslibrary.parliament.uk/research-briefings/cbp-10264/"),
        ],
    },
    {
        "name": "Balochistan Insurgency & CPEC Attacks",
        "status": "Sharply escalating through 2025-2026",
        "stats": [
            ("Violent incidents, Jan-Jul 2026", "765 (1,600 fatalities)"),
            ("BLA attacks in 2026 (CRSS count)", "181 (708 casualties)"),
            ("Militants killed in 2026 counter-ops", "216 (plus 22 security, 36 civilians)"),
            ("July 4-8, 2026 coordinated assault toll", "42 killed (38 security, 4 civilians)"),
            ("2025 full-year attack count (for comparison)", "254 (+26% vs 2024)"),
            ("Jaffar Express hostages taken, Mar 11, 2025", "400+ (26+ killed)"),
        ],
        "groups": "Balochistan Liberation Army (BLA) and its Jeeyand faction (BLA-J), Pakistani military and paramilitary forces",
        "affected": ["PAK"],
        "summary": (
            "A long-running separatist insurgency in Pakistan's resource-rich but underdeveloped "
            "Balochistan province has increasingly targeted Chinese nationals and China-Pakistan "
            "Economic Corridor (CPEC) infrastructure specifically, viewing Chinese investment as "
            "extracting local resources without local benefit. The violence has escalated sharply "
            "through 2026: The Diplomat now calls Balochistan 'Pakistan's most dangerous province,' "
            "citing 765 violent incidents and roughly 1,600 fatalities between January and July 2026 "
            "alone. A single coordinated assault from July 4-8, 2026 killed 42 people, including 38 "
            "security personnel. This builds on a 2025 baseline that was already a marked escalation — "
            "254 attacks for the full year (+26% vs 2024) — punctuated by the BLA-J's hijacking of the "
            "Jaffar Express train on March 11, 2025, taking 400+ passengers hostage and killing at "
            "least 26."
        ),
        "market_impact": (
            "This directly threatens the CPEC investment relationship that is central to Pakistan's "
            "China financing (China holds ~22% of Pakistan's external debt, its largest single "
            "creditor — see Key Economic Partners above). Repeated attacks on Chinese nationals and "
            "infrastructure raise the risk premium China itself attaches to further CPEC investment, "
            "a direct threat to one of Pakistan's most important external financing relationships."
        ),
        "sources": [
            ("The Diplomat: Balochistan Is Now Pakistan's Most Dangerous Province (Aug 2026)", "https://thediplomat.com/2026/08/balochistan-is-now-pakistans-most-dangerous-province/"),
            ("Al Jazeera: Train bomb in Pakistan's Baloch region", "https://www.aljazeera.com/news/2026/5/25/train-bomb-in-pakistans-baloch-region-why-violence-is-on-the-rise"),
            ("Jamestown Foundation: Baloch Militant Attacks Undermine Sino-Pakistan Projects", "https://jamestown.org/amid-geopolitical-tensions-baloch-militant-attacks-undermine-sino-pakistan-projects/"),
            ("Combating Terrorism Center, West Point: The Baloch Insurgency in Pakistan", "https://ctc.westpoint.edu/the-baloch-insurgency-in-pakistan-evolution-tactics-and-regional-security-implications/"),
        ],
    },
    {
        "name": "Iran-Aligned Militia Attacks on US Forces in Iraq",
        "status": "Recurring, intensified during the 2026 Iran war",
        "groups": "Iran-aligned Iraqi militias (Popular Mobilization Forces/PMF factions), US military, Iraqi government",
        "affected": ["IRQ", "IRN"],
        "stats": [
            ("US service members killed, Jan 28, 2024 Jordan strike", "3 (25 injured)"),
            ("Incidents triggered by the 2026 Iran war", "~300"),
            ("US Embassy Baghdad strikes", "4+ times"),
            ("Relocation of most US forces since 2025", "Erbil, Kurdistan region"),
        ],
        "summary": (
            "Iran-aligned militias operating within Iraq's Popular Mobilization Forces have "
            "intermittently attacked US military positions since the Gaza war began, including a "
            "January 28, 2024 drone strike on a US base in northeast Jordan that killed three US "
            "service members and injured 25 — one of the most significant attacks on US forces in the "
            "region since October 7, 2023. Attacks abated somewhat through 2024-2025, but the "
            "February 2026 Iran-Israel-US war triggered a sharp resurgence — roughly 300 incidents "
            "including drone and rocket attacks on the US Embassy in Baghdad (struck at least four "
            "times) and the US consulate in Erbil, where most US forces have relocated since 2025."
        ),
        "market_impact": (
            "This keeps Iraq's stability directly hostage to the broader Iran-Israel-US conflict "
            "despite Iraq itself not being a direct combatant, compounding the governance and security "
            "risk already reflected in Iraq's composite score. It also illustrates why Iraq's dependency "
            "on Iranian gas and electricity imports (noted in Key Economic Partners above) is "
            "politically fraught, not just economically so."
        ),
        "sources": [
            ("Wikipedia: 2026 United States-led conflict with pro-Iranian Iraqi militias", "https://en.wikipedia.org/wiki/2026_United_States-led_conflict_with_pro-Iranian_Iraqi_militias"),
            ("The Soufan Center: Iraq is Caught up in the U.S.-Iran War", "https://thesoufancenter.org/intelbrief-2026-april-30/"),
            ("The Washington Institute: Iraq Is at Another Crossroads with Iran-Backed Militias", "https://www.washingtoninstitute.org/policy-analysis/iraq-another-crossroads-iran-backed-militias-and-washington"),
        ],
    },
    {
        "name": "Egypt-Ethiopia Nile Dam (GERD) Dispute",
        "status": "Unresolved, no binding agreement despite dam's completion",
        "groups": "Egyptian government, Ethiopian government, Sudan (secondary party); not a tracked country but central to the dispute",
        "affected": ["EGY"],
        "stats": [
            ("GERD capacity — Africa's largest hydro dam", "5,150 MW"),
            ("Years of negotiation without binding deal", "13+ (since 2011 construction start)"),
            ("Share of Egypt's fresh water from the Nile", "~90%+"),
            ("New Ethiopian dams planned since GERD's opening", "3 more on the Blue Nile"),
        ],
        "summary": (
            "Ethiopia completed and formally inaugurated the Grand Ethiopian Renaissance Dam (GERD) — "
            "Africa's largest hydroelectric dam at 5,150 MW capacity — on September 9, 2025, after the "
            "reservoir's final filling in September 2024. Egypt has spent over a decade seeking a "
            "legally binding agreement governing how Ethiopia fills and operates the dam during "
            "droughts, arguing Ethiopia's unilateral management violates a 2015 declaration of "
            "principles on equitable Nile use; no such binding deal has ever been reached. Tensions "
            "resurfaced sharply in late 2025 when rising Nile floodwaters, which Egypt's irrigation "
            "ministry attributed to 'reckless, unilateral water releases' from the dam, damaged "
            "farmland and coastal villages — and Ethiopia's newly announced plans for three further "
            "Blue Nile dams have reopened the entire dispute less than a year after GERD's inauguration."
        ),
        "market_impact": (
            "The Nile supplies roughly 90%+ of Egypt's fresh water in a country almost entirely "
            "dependent on the river for agriculture and drinking water — making this arguably Egypt's "
            "single most consequential long-run economic security issue, distinct from but layered on "
            "top of its currency, debt, and Suez Canal pressures covered elsewhere in this profile."
        ),
        "sources": [
            ("Foreign Policy: Ethiopia Opens Africa's Biggest Dam, Angering Egypt", "https://foreignpolicy.com/2025/09/10/ethiopia-egypt-sudan-nile-dam-gerd-water-abiy/"),
            ("Atlantic Council: The Nile at a crossroads", "https://www.atlanticcouncil.org/blogs/menasource/the-nile-at-a-crossroads-navigating-the-gerd-dispute-as-egypts-floodwaters-rise/"),
            ("Al Jazeera: After GERD, can Egypt shape Ethiopia's next Nile dams?", "https://www.aljazeera.com/news/2026/8/21/after-gerd-can-egypt-shape-ethiopias-next-nile-dams"),
            ("Foreign Policy Research Institute: The GERD Dispute", "https://www.fpri.org/article/2025/10/the-gerd-dispute-lessons-for-water-governance-and-the-future-of-the-nile-basin/"),
        ],
    },
    {
        "name": "Western Sahara Conflict & Algeria-Morocco Rupture",
        "status": "Low-intensity conflict since the 2020 ceasefire collapse; diplomatic track shifting toward Morocco through 2025-2026",
        "groups": "Moroccan Royal Armed Forces, Polisario Front / Sahrawi Arab Democratic Republic government-in-exile (Algeria-backed), Algerian government",
        "affected": ["MAR", "DZA"],
        "stats": [
            ("Years since the 1991 UN ceasefire collapsed", "6 (since Nov 2020)"),
            ("Years of full Algeria-Morocco diplomatic rupture", "5 (since Aug 2021)"),
            ("UN Security Council resolution endorsing Morocco's autonomy plan", "Resolution 2797, Oct 31, 2025"),
            ("Countries Morocco says now back its autonomy plan (Oct 2025)", "118, incl. US, France, Spain, Germany"),
            ("Morocco's annual Maghreb-Europe pipeline transit fees lost", "~€50m/year, plus 800m m³ of subsidized gas"),
        ],
        "summary": (
            "Morocco and the Polisario Front fought an open war over Western Sahara from 1975 until a "
            "1991 UN-brokered ceasefire, which held for nearly three decades pending a self-determination "
            "referendum that was never held. The Polisario declared the ceasefire over in November 2020 "
            "after Moroccan forces moved to clear a blockade at the Guerguerat border crossing, and "
            "intermittent low-intensity exchanges — Polisario rocket and drone fire, Moroccan strikes — "
            "have continued along Morocco's defensive sand berm since. The conflict has increasingly "
            "moved to the diplomatic track and shifted toward Morocco: the UN Security Council's Resolution "
            "2797 (Oct 31, 2025) endorsed Rabat's 2007 autonomy proposal as the negotiating basis rather "
            "than an independence referendum, the EU aligned behind that position in January 2026, and "
            "previously secret Madrid talks in February 2026 brought Morocco, the Polisario, Algeria, "
            "and mediators together for the first time in years. Algeria and the Polisario continue to "
            "reject any outcome short of a full referendum, and Algeria — which hosts the Polisario's "
            "government-in-exile and the Sahrawi refugee camps near Tindouf — has made this the central "
            "issue in its own foreign policy."
        ),
        "market_impact": (
            "The dispute triggered a full Algeria-Morocco diplomatic rupture in August 2021, when Algiers "
            "cut ties, closed its airspace and land border to Morocco, and ordered state energy firm "
            "Sonatrach to stop supplying gas through the Maghreb-Europe Pipeline (GME), which had carried "
            "Algerian gas across Morocco to Spain since 1996. That single decision cost Morocco roughly "
            "€50m a year in transit fees plus 800 million cubic meters of gas it had received at a "
            "discounted, stable price for its own power stations, forcing Rabat to lean more heavily on "
            "LNG imports and a separate Spain-Morocco gas arrangement. The rupture has stayed diplomatic "
            "and economic rather than reigniting open war, but it has hardened North Africa's two largest "
            "economies into rival blocs — closing off intra-Maghreb trade and investment integration that "
            "would otherwise be a natural growth lever for both, and phosphate exports from the "
            "Western Sahara territory itself (mined by Morocco's state operator OCP) remain a recurring "
            "target of activist-led boycotts and legal challenges from firms sourcing it, given the "
            "territory's disputed status."
        ),
        "sources": [
            ("Human Rights Watch: World Report 2026 — Morocco and Western Sahara", "https://www.hrw.org/world-report/2026/country-chapters/morocco-and-western-sahara"),
            ("International Crisis Group: Western Sahara", "https://www.crisisgroup.org/middle-east-north-africa/north-africa/western-sahara"),
            ("Council on Foreign Relations: Morocco's Victory on the Western Sahara", "https://www.cfr.org/articles/moroccos-victory-western-sahara"),
            ("Atalayar: Polisario Front and Algeria reject US resolution on Western Sahara", "https://www.atalayar.com/en/articulo/politics/polisario-front-and-algeria-reject-us-resolution-on-western-sahara/20251027160000219827.html"),
            ("The New Arab: Why Algeria's gas pipeline closure will prove costly for all", "https://www.newarab.com/analysis/why-algerias-gas-pipeline-closure-will-prove-costly-all"),
            ("VOA: Diplomatic Dispute Between Algeria and Morocco Prompts Energy Crisis in Spain", "https://www.voanews.com/a/diplomatic-dispute-between-algeria-and-morocco-prompts-energy-crisis-in-spain/6298213.html"),
        ],
    },
]


# ============================================================
# SOVEREIGN CREDIT RATINGS — actual S&P / Moody's / Fitch letter grades,
# for sanity-checking this tool's own composite score against the real
# rating agencies' independent assessments. Pulled from countryeconomy.com's
# aggregated ratings table (a secondary aggregator, not the primary agency
# reports) and cross-checked against individual agency news coverage for
# the most consequential/newsworthy cases (e.g. Israel's 2024 downgrades).
# "Not Rated" means the country doesn't have a widely reported rating from
# these three agencies — common for countries without international bond
# market access (conflict-affected or heavily aid-dependent economies) —
# not that the country is necessarily riskier or safer than a rated peer.
# ============================================================
CREDIT_RATINGS = {
    "DZA": {"sp": "Not Rated", "moodys": "Not Rated", "fitch": "Not Rated"},
    "BHR": {"sp": "B+", "moodys": "B2", "fitch": "B+"},
    "EGY": {"sp": "B", "moodys": "Caa1", "fitch": "B"},
    "IRN": {"sp": "Not Rated", "moodys": "Not Rated", "fitch": "Not Rated"},
    "IRQ": {"sp": "B-", "moodys": "Caa1", "fitch": "B-"},
    "ISR": {"sp": "A", "moodys": "Baa1", "fitch": "A"},
    "JOR": {"sp": "BB-", "moodys": "Ba3", "fitch": "BB-"},
    "KWT": {"sp": "AA-", "moodys": "A1", "fitch": "AA-"},
    "LBN": {"sp": "SD", "moodys": "C", "fitch": "RD"},
    "LBY": {"sp": "Not Rated", "moodys": "Not Rated", "fitch": "Not Rated"},
    "MAR": {"sp": "BB+", "moodys": "Ba1", "fitch": "BB+"},
    "OMN": {"sp": "BBB-", "moodys": "Baa3", "fitch": "BB"},
    "QAT": {"sp": "AA", "moodys": "Aa2", "fitch": "AA-"},
    "SAU": {"sp": "A+", "moodys": "Aa3", "fitch": "A+"},
    "SYR": {"sp": "Not Rated", "moodys": "Not Rated", "fitch": "Not Rated"},
    "TUN": {"sp": "Not Rated", "moodys": "Caa1", "fitch": "CCC+"},
    "ARE": {"sp": "AA", "moodys": "Aa2", "fitch": "AA-"},
    "YEM": {"sp": "Not Rated", "moodys": "Not Rated", "fitch": "Not Rated"},
    "AFG": {"sp": "Not Rated", "moodys": "Not Rated", "fitch": "Not Rated"},
    "BGD": {"sp": "B+", "moodys": "B2", "fitch": "BB-"},
    "BTN": {"sp": "Not Rated", "moodys": "Not Rated", "fitch": "Not Rated"},
    "IND": {"sp": "BBB", "moodys": "Baa3", "fitch": "BBB-"},
    "MDV": {"sp": "B-", "moodys": "Not Rated", "fitch": "Not Rated"},
    "NPL": {"sp": "Not Rated", "moodys": "Not Rated", "fitch": "Not Rated"},
    "PAK": {"sp": "B-", "moodys": "Caa1", "fitch": "CCC-"},
    "LKA": {"sp": "CCC+", "moodys": "Caa1", "fitch": "RD"},
}

CREDIT_RATINGS_SOURCES = [
    ("countryeconomy.com: Sovereign Ratings List 2026 (aggregator)", "https://countryeconomy.com/ratings"),
    ("Haaretz: S&P Affirms Israel's Rating With Negative Outlook", "https://www.haaretz.com/israel-news/2025-05-10/ty-article/.premium/s-p-affirms-israels-rating-with-negative-outlook-citing-war-risks-and-rising-debt/00000196-b90e-d1bb-a5d6-bffe44b00000"),
    ("Moody's Ratings: Israel downgrade notice", "https://ratings.moodys.com/ratings-news/415081"),
    ("Bloomberg: Israel's Rating Cut by Fitch as War Seen Lasting Into 2025", "https://www.bloomberg.com/news/articles/2024-08-12/israel-s-rating-cut-by-fitch-as-gaza-war-seen-lasting-into-2025"),
    ("Business Standard: S&P raises Pakistan's sovereign rating to 'B-'", "https://www.business-standard.com/amp/world-news/sp-rating-upgrades-pakistan-sovereign-rating-b-125072401514_1.html"),
]
