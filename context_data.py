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
            "assassination."
        ),
        "sources": [
            ("Wikipedia: Timeline of the 2026 Iran conflict", "https://en.wikipedia.org/wiki/Timeline_of_the_2026_Iran_conflict"),
            ("Britannica: 2026 Iran war", "https://www.britannica.com/event/2026-Iran-war"),
            ("CFR Global Conflict Tracker", "https://www.cfr.org/global-conflict-tracker/conflict/confrontation-between-united-states-and-iran"),
            ("UK House of Commons Library", "https://commonslibrary.parliament.uk/research-briefings/cbp-10521/"),
        ],
    },
    {
        "name": "Red Sea Shipping Crisis & Houthi-Saudi Blockade",
        "status": "Active, re-escalating",
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
        ],
    },
    {
        "name": "Syria's Post-Assad Transition",
        "status": "Fragile, ongoing",
        "affected": ["SYR", "LBN", "JOR", "IRQ"],
        "summary": (
            "The Assad regime fell on December 8, 2024 after a rapid rebel offensive led by Hay'at "
            "Tahrir al-Sham captured Damascus, ending a 13-year civil war. Ahmed al-Sharaa was declared "
            "transitional president in January 2025, and an interim constitutional declaration took "
            "effect in March 2025, setting out a 5-year path to elections. One year on, the transition "
            "remains disputed — no single national armed force yet exists, and localized violence has "
            "continued into 2026."
        ),
        "market_impact": (
            "Syria's own reconstruction need is enormous after 13 years of civil war, but the "
            "transition's fragility also carries spillover risk for neighboring Lebanon, Jordan, and "
            "Iraq, all of which hosted large Syrian refugee populations and share long, historically "
            "porous borders."
        ),
        "sources": [
            ("Wikipedia: Fall of the Assad regime", "https://en.wikipedia.org/wiki/Fall_of_the_Assad_regime"),
            ("Belfer Center, Harvard Kennedy School", "https://www.belfercenter.org/research-analysis/external-states-and-syrias-challenge-reunification-under-transitional-president"),
            ("UK House of Commons Library: Syria one year after Assad", "https://commonslibrary.parliament.uk/research-briefings/cbp-10430/"),
        ],
    },
    {
        "name": "Sudan Civil War (regional spillover)",
        "status": "Active — not a tracked country, but a major regional shock",
        "affected": ["EGY"],
        "summary": (
            "Though Sudan is outside this tool's 26-country MENASA tracking scope, its civil war "
            "(erupted Apr 15, 2023, between the Sudanese Armed Forces and the Rapid Support Forces) is "
            "one of the world's largest displacement crises — roughly 12 million people forcibly "
            "displaced, with over 3 million fleeing across borders. Egypt has become the primary host, "
            "sheltering more than 1 million Sudanese refugees, a meaningful fiscal and social strain "
            "layered on top of Egypt's own currency and Suez Canal-driven pressures."
        ),
        "market_impact": (
            "Refugee-hosting costs and informal-labor-market strain in Egypt compound its existing "
            "balance-of-payments fragility, even though Sudan itself isn't a scored country here."
        ),
        "sources": [
            ("Wikipedia: Sudanese civil war (2023-present)", "https://en.wikipedia.org/wiki/Sudanese_civil_war_(2023%E2%80%93present)"),
            ("Wikipedia: Humanitarian impact of the Sudanese civil war", "https://en.wikipedia.org/wiki/Humanitarian_impact_of_the_Sudanese_civil_war_(2023%E2%80%93present)"),
        ],
    },
]
