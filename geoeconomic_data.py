"""
Geo-Economic Interdependence dataset: maritime chokepoints, critical-mineral
concentration, and the corporate "gatekeepers" whose capacity constraints
ripple through global trade. A structural/context layer -- descriptive, not
part of the composite risk score computed elsewhere in this app.

Verified via live web search as of August 2026 (Suez Canal Authority, gCaptain,
Lloyd's List, Bloomberg/CNN/Al Jazeera/CNBC, IEA Global Critical Minerals
Outlook, USGS Mineral Commodity Summaries). Fields left as None are genuinely
unreconciled across sources as of the research date -- the honest range or
caveat lives in the adjacent notes/context field rather than a fabricated
single number. "risk_level" on each chokepoint is this project's own editorial
characterization, not a third-party rating, the same way Live Conflicts'
type/impact fields are its own classification.
"""

# Real, stable capital/major-city coordinates for the 27 tracked countries --
# matches the same values used for MAJOR_CITIES in app.py.
COUNTRY_CAPITAL_COORDS = {
    "DZA": (36.75, 3.06), "BHR": (26.23, 50.59), "EGY": (30.04, 31.24),
    "IRN": (35.69, 51.39), "IRQ": (33.31, 44.36), "ISR": (31.78, 35.22),
    "JOR": (31.95, 35.93), "KWT": (29.38, 47.99), "LBN": (33.89, 35.50),
    "LBY": (32.89, 13.19), "MAR": (34.02, -6.83), "OMN": (23.59, 58.41),
    "PSE": (31.90, 35.20), "QAT": (25.29, 51.53), "SAU": (24.71, 46.68),
    "SYR": (33.51, 36.29), "TUN": (36.81, 10.18), "ARE": (24.45, 54.38),
    "YEM": (15.37, 44.19), "AFG": (34.56, 69.21), "BGD": (23.81, 90.41),
    "BTN": (27.47, 89.64), "IND": (28.61, 77.21), "MDV": (4.17, 73.51),
    "NPL": (27.72, 85.32), "PAK": (33.68, 73.05), "LKA": (6.93, 79.85),
    "TUR": (39.9334, 32.8597), "SDN": (15.6, 32.5), "SSD": (4.8517, 31.5825),
    "ETH": (9.0359, 38.7525), "SOM": (2.03917, 45.34194), "DJI": (11.5944, 43.1480),
    "ERI": (15.33583, 38.94111),
}

# Real, stable multilateral-alliance memberships for each tracked country.
# "primary_bloc" drives the map color; "memberships" lists everything for the
# tooltip/table. Ambiguous or dormant memberships are labeled as such rather
# than presented as clean-cut, current facts (e.g. SAARC hasn't held a summit
# since 2014 amid India-Pakistan tensions; Saudi Arabia's BRICS+ accession was
# invited in 2024 but has never been confirmed).
MENASA_COUNTRY_ALLIANCES = {
    "DZA": {"memberships": ["OPEC", "Arab League"], "primary_bloc": "OPEC"},
    "BHR": {"memberships": ["GCC", "OPEC+ (non-OPEC participant)", "Arab League"], "primary_bloc": "GCC"},
    "EGY": {"memberships": ["Arab League", "BRICS+ (2024 member)", "D-8"], "primary_bloc": "BRICS+"},
    "IRN": {"memberships": ["OPEC", "BRICS+ (2024 member)"], "primary_bloc": "OPEC"},
    "IRQ": {"memberships": ["OPEC", "Arab League"], "primary_bloc": "OPEC"},
    "ISR": {"memberships": ["OECD"], "primary_bloc": "Non-aligned / OECD"},
    "JOR": {"memberships": ["Arab League"], "primary_bloc": "Arab League"},
    "KWT": {"memberships": ["GCC", "OPEC", "Arab League"], "primary_bloc": "GCC"},
    "LBN": {"memberships": ["Arab League"], "primary_bloc": "Arab League"},
    "LBY": {"memberships": ["OPEC", "Arab League"], "primary_bloc": "OPEC"},
    "MAR": {"memberships": ["Arab League"], "primary_bloc": "Arab League"},
    "OMN": {"memberships": ["GCC", "OPEC+ (non-OPEC participant)", "Arab League"], "primary_bloc": "GCC"},
    "PSE": {"memberships": ["Arab League"], "primary_bloc": "Arab League"},
    "QAT": {"memberships": ["GCC", "Arab League"], "primary_bloc": "GCC"},  # Left OPEC Jan 2019
    "SAU": {"memberships": ["GCC", "OPEC", "Arab League", "BRICS+ (invited 2024, accession unconfirmed)"], "primary_bloc": "GCC"},
    "SYR": {"memberships": ["Arab League (reinstated May 2023 after 12-year suspension)"], "primary_bloc": "Arab League"},
    "TUN": {"memberships": ["Arab League"], "primary_bloc": "Arab League"},
    "ARE": {"memberships": ["GCC", "OPEC", "Arab League", "BRICS+ (2024 member)"], "primary_bloc": "GCC"},
    "YEM": {"memberships": ["Arab League"], "primary_bloc": "Arab League"},
    "AFG": {"memberships": ["SAARC (dormant since 2014)"], "primary_bloc": "SAARC"},
    "BGD": {"memberships": ["SAARC (dormant since 2014)", "D-8"], "primary_bloc": "SAARC"},
    "BTN": {"memberships": ["SAARC (dormant since 2014)"], "primary_bloc": "SAARC"},
    "IND": {"memberships": ["SAARC (dormant since 2014)", "BRICS (founding member)"], "primary_bloc": "BRICS+"},
    "MDV": {"memberships": ["SAARC (dormant since 2014)"], "primary_bloc": "SAARC"},
    "NPL": {"memberships": ["SAARC (dormant since 2014)"], "primary_bloc": "SAARC"},
    "PAK": {"memberships": ["SAARC (dormant since 2014)", "D-8"], "primary_bloc": "SAARC"},
    "LKA": {"memberships": ["SAARC (dormant since 2014)"], "primary_bloc": "SAARC"},
    "TUR": {"memberships": ["NATO (member since 1952)", "OECD (founding member, 1961)", "G20", "EU Customs Union (since 1995)", "EU accession candidate (since 1999, talks frozen since 2018)", "OIC", "Organization of Turkic States"], "primary_bloc": "NATO"},
    "SDN": {"memberships": ["Arab League", "African Union (membership suspended since October 2021 coup)"], "primary_bloc": "Arab League"},
    "SSD": {"memberships": ["African Union (since independence, 2011)", "East African Community (acceded 2016)", "IGAD (since 2011)"], "primary_bloc": "IGAD / EAC"},
    "ETH": {"memberships": ["African Union (headquarters host)", "IGAD", "BRICS+ (joined January 1, 2024)", "COMESA"], "primary_bloc": "African Union / IGAD"},
    "SOM": {"memberships": ["Arab League (joined 1974)", "African Union", "IGAD (founding member)", "East African Community (joined November 2023)"], "primary_bloc": "Arab League"},
    "DJI": {"memberships": ["Arab League", "African Union", "IGAD (headquartered in Djibouti City)", "OIC"], "primary_bloc": "Arab League / African Union"},
    "ERI": {"memberships": ["African Union", "Arab League (observer status only, since 2003)", "Not an IGAD member (withdrew December 2025)"], "primary_bloc": "African Union / Horn of Africa"},
}

MARITIME_CHOKEPOINTS = {
    "suez_canal": {
        "name": "Suez Canal",
        "lat": 30.5, "lon": 32.35,
        # Sources conflict sharply depending on the exact week in 2026 cited: gCaptain
        # (mid-Aug 2026, citing the Suez Canal Authority) reports ~39/day over the prior
        # 4 weeks, called the "highest level in 2+ years" but still 41% below pre-crisis;
        # a separate 2026 gCaptain piece cites traffic "60% below normal despite 100 days
        # without Houthi attacks." Pre-crisis (2023) baseline was ~72-74/day.
        "daily_transit_volume": None,
        "annual_cargo_throughput": "SCA reported +5.8% transits, +16% tonnage, +18.5% revenue YoY for H1 FY2025/26 -- full-year absolute TEU/tonnage not independently confirmed.",
        "latency_delay_days": 12.0,
        "risk_level": "High",
        "notes": (
            "Traffic collapsed after Houthi Red Sea attacks began late 2023 and has only "
            "partially recovered. The October 2025 Gaza ceasefire brought the first sustained "
            "lull in Houthi activity, and the Suez Canal Authority reported its strongest "
            "monthly vessel-return rate (229 vessels in October 2025) since the crisis began. "
            "But 2026 reporting is contradictory on how far recovery has actually gone -- some "
            "accounts describe an 8-month traffic high in mid-August 2026, others describe "
            "traffic still stalled 60% below normal. Container lines (Maersk-Hapag Gemini "
            "network, CMA CGM on select escorted sailings) are cautiously testing returns; "
            "most Asia-Europe cargo still routes via the Cape of Good Hope as of August 2026."
        ),
        "sources": [
            ("gCaptain -- Suez Canal Traffic Stalls at 60% Below Normal Despite 100 Days Without Houthi Attacks", "https://gcaptain.com/suez-canal-traffic-stalls-at-60-below-normal-despite-100-days-without-houthi-attacks/"),
            ("Lloyd's List Intelligence -- Red Sea Brief: 20 August 2026", "https://www.lloydslistintelligence.com/resources/blog/red-sea-brief-20-august-2026"),
            ("gCaptain -- Red Sea Shipping Faces Uncertain Future as Houthi Ceasefire Brings Hope and Caution", "https://gcaptain.com/red-sea-shipping-faces-uncertain-future-as-houthi-ceasefire-brings-hope-and-caution/"),
            ("Maritime News -- Suez Canal Recovery: Traffic Up, Revenues Rise in 2026", "https://www.maritimenews.com/suez-canal/suez-canal-traffic-strong-recovery"),
        ],
    },
    "bab_el_mandeb": {
        "name": "Bab el-Mandeb Strait",
        "lat": 12.58, "lon": 43.33,
        "daily_transit_volume": None,
        "annual_cargo_throughput": "~7.4 million barrels/day of petroleum transiting as of June 2026 (~7% of global oil output) -- approximate, single-source estimate.",
        "latency_delay_days": 12.0,
        "risk_level": "Critical",
        "notes": (
            "Houthi attacks here drove the original 2023-2024 diversion crisis, and the October "
            "2025 Gaza ceasefire brought a real lull. But 2026 has seen renewed escalation "
            "distinct from the Gaza track: the Houthis declared a naval blockade of Saudi Arabia "
            "in July 2026, and on August 12, 2026 an attack on the Egyptian-owned vessel Tihamah "
            "killed six -- the first Houthi-linked shipping deaths since the separate US-Israel "
            "war on Iran began February 28, 2026. This strait's risk is now compounding with the "
            "near-closure of the Strait of Hormuz and the Qatar LNG facility strikes (see "
            "Corporate Gatekeepers), making it the most acutely volatile of the three chokepoints "
            "as of August 2026."
        ),
        "sources": [
            ("Al Jazeera -- Six killed in Houthi attack on Bab al-Mandeb ship (Aug 12, 2026)", "https://www.aljazeera.com/news/2026/8/12/six-killed-in-houthi-attack-on-bab-al-mandeb-ship-yemens-government-says"),
            ("Al Jazeera -- Yemen's Houthis declare naval blockade of Saudi Arabia (Jul 20, 2026)", "https://www.aljazeera.com/news/2026/7/20/yemens-houthis-declare-naval-blockade-of-saudi-arabia-what-to-know"),
            ("CNBC -- Houthis deploy missiles and drones to attack ships in southern Red Sea", "https://www.cnbc.com/2026/07/22/houthis-red-sea-bab-el-mandeb-saudi-oil-iran.html"),
            ("S&P Global -- Factbox: Red Sea transits in renewed focus following Houthi attacks", "https://www.spglobal.com/energy/en/news-research/latest-news/shipping/070925-factbox-red-sea-transits-in-renewed-focus-following-houthis-first-attacks-in-2025"),
        ],
    },
    "strait_of_hormuz": {
        "name": "Strait of Hormuz",
        "lat": 26.57, "lon": 56.25,
        "daily_transit_volume": None,
        "annual_cargo_throughput": "~14.6 million bbl/day (Q1 2026, EIA), down from ~20.4M bbl/day a year earlier; effectively near-zero commercial flow reported as of Aug 5, 2026, with a brief partial recovery during a temporary US-Iran MoU that later expired.",
        "latency_delay_days": None,  # Not a rerouting/delay scenario -- this is closure/blockade, a different disruption type than Suez/Bab el-Mandeb.
        "risk_level": "Critical",
        "notes": (
            "The most dramatic development of the three chokepoints, reflecting a real shooting "
            "war, not a rerouting inconvenience. The US-Israel war on Iran (started Feb 28, 2026) "
            "triggered a collapse in Hormuz transits: roughly 90% of traffic diverted immediately, "
            "rising above 95% once Iran threatened ships directly, and Iran has since fired on "
            "dozens of tankers attempting transit. By August 5, 2026 the strait was described as "
            "'effectively closed to commercial shipping.' A temporary US-Iran MoU briefly nearly "
            "tripled flows before expiring around August 20, 2026, still far below pre-war levels. "
            "Normally ~20% of global oil and a large share of global LNG (much of it Qatari) "
            "transits here; Iran has also directly struck QatarEnergy's Ras Laffan/Mesaieed LNG "
            "facilities (see Corporate Gatekeepers), knocking out roughly 17% of Qatar's LNG export "
            "capacity for an estimated 3-5 years."
        ),
        "sources": [
            ("Bloomberg -- Hormuz Oil Flows Fell Nearly 30% Last Quarter, EIA Says", "https://www.bloomberg.com/news/articles/2026-05-13/hormuz-oil-flows-fell-nearly-30-last-quarter-eia-says"),
            ("CNN -- Wait... how much oil is actually leaving the Persian Gulf?", "https://www.cnn.com/2026/08/17/business/oil-market-strait-of-hormuz-trump"),
            ("Al Jazeera -- Oil flows nearly tripled before US-Iran MoU expired", "https://www.aljazeera.com/economy/2026/8/20/oil-flows-nearly-tripled-before-us-iran-mou-expired"),
            ("U.S. EIA -- Today in Energy", "https://www.eia.gov/todayinenergy/detail.php?id=61002"),
        ],
    },
}

CRITICAL_MINERAL_DEPENDENCIES = {
    "natural_graphite": {
        "mineral": "Natural Graphite (mine production & processing)",
        "dominant_country": "China",
        "global_market_share_pct": 78.0,
        "context": (
            "IEA characterizes graphite refining/processing (spheronization into battery-grade "
            "anode material) as even more concentrated than mining -- China controls over 90% of "
            "global graphite refining capacity, versus ~78% of raw mine production. China has "
            "layered export permit requirements on graphite since December 2023. Western "
            "diversification (Syrah Resources, Novonix, Anovion) remains small relative to Chinese "
            "processing scale as of 2026."
        ),
        "sources": [
            ("USGS -- Mineral Commodity Summaries 2025: Graphite (Natural)", "https://pubs.usgs.gov/periodicals/mcs2025/mcs2025-graphite.pdf"),
            ("IEA -- Global Critical Minerals Outlook 2025, Executive Summary", "https://www.iea.org/reports/global-critical-minerals-outlook-2025/executive-summary"),
        ],
    },
    "rare_earth_refining": {
        "mineral": "Rare Earth Elements (refining/separation)",
        "dominant_country": "China",
        "global_market_share_pct": 90.0,
        "context": (
            "IEA's Global Critical Minerals Outlook describes rare earth refining as among the "
            "most concentrated of all critical mineral markets -- refining/separation "
            "concentration (90%+) runs meaningfully higher than mine-production concentration "
            "(~69% per USGS 2025). China has used rare earth export licensing as explicit "
            "trade-war leverage in 2024-2026. MP Materials (USA) and Lynas (Australia/Malaysia) "
            "are the main Western/allied diversification plays, but their combined separation "
            "capacity remains a small fraction of China's."
        ),
        "sources": [
            ("IEA -- Global Critical Minerals Outlook 2025, Regional Snapshots", "https://www.iea.org/reports/global-critical-minerals-outlook-2025/regional-snapshots"),
            ("USGS -- Mineral Commodity Summaries 2025: Rare Earths", "https://pubs.usgs.gov/periodicals/mcs2025/mcs2025-rare-earths.pdf"),
        ],
    },
    "cobalt_drc": {
        "mineral": "Cobalt (mine production)",
        "dominant_country": "DRC",
        "global_market_share_pct": 75.0,  # USGS ~76%; some 2025/26 estimates ~72-74% as Indonesia scales up -- midpoint of the ~74-76% range.
        "context": (
            "The DRC's dominance is deepening in price terms even as its share edges down "
            "slightly: DRC export restrictions (a 2024 export ban, then a 2025 quota regime) "
            "drove cobalt prices up roughly 130% per IEA's 2026 outlook, since alternative supply "
            "(chiefly Indonesia, now the #2 producer at roughly 10%) hasn't offset DRC policy "
            "shifts. This is a supply-chain risk distinct from simple market-share concentration "
            "-- policy at a single dominant supplier moves global battery/EV input prices directly."
        ),
        "sources": [
            ("USGS -- Mineral Commodity Summaries 2025: Cobalt", "https://pubs.usgs.gov/periodicals/mcs2025/mcs2025-cobalt.pdf"),
            ("IEA -- Global Critical Minerals Outlook 2026, Outlook", "https://www.iea.org/reports/global-critical-minerals-outlook-2026/outlook"),
        ],
    },
    "nickel_refining_indonesia": {
        "mineral": "Nickel (refining/processing)",
        "dominant_country": "Indonesia",
        # Sources disagree materially (37% vs ~45-62%), unclear whether higher figures measure
        # refined-nickel share vs. mined-ore share, or blend different product classes. No single
        # reconciled current-year figure found -- left as None rather than picking one.
        "global_market_share_pct": None,
        "context": (
            "Indonesia's refined-nickel share grew fast (IEA: 23% to 37% between 2020-2023) on "
            "the back of its 2020 raw-ore export ban, which forced smelting onshore. More recent "
            "trade press cites materially higher figures (45-62%) for 2024-2025, but these could "
            "not be reconciled to one authoritative current IEA/USGS number -- treat any single "
            "percentage as approximate. A distinct wrinkle: despite hosting the majority of world "
            "refining capacity, Indonesian firms reportedly own only around 10% of that capacity "
            "-- most of it is Chinese-financed and Chinese-operated smelting sited in Indonesia, "
            "which complicates a simple 'country dominance' framing."
        ),
        "sources": [
            ("IEA -- Global Critical Minerals Outlook 2025, Executive Summary", "https://www.iea.org/reports/global-critical-minerals-outlook-2025/executive-summary"),
            ("C4ADS -- Refining Power", "https://c4ads.org/commentary/refining-power/"),
        ],
    },
}

CORPORATE_GATEKEEPERS = [
    {
        "company": "TSMC", "hq_location": "Taiwan", "sector": "Advanced Hardware",
        "market_share_pct": 90.0,
        "dependency_note": (
            "Share of leading-edge (sub-7nm) foundry capacity; overall pure-play foundry share "
            "separately reported at 72.3% (Q1 2026). Near-monopoly on fabrication for Nvidia, "
            "Apple, AMD, Qualcomm. Arizona and Kumamoto (Japan) fabs partially diversify geography, "
            "but the most advanced nodes remain concentrated in Taiwan."
        ),
        "related_chokepoints": [], "related_minerals": [],
        "source": ("TrendForce data via Semiecosystem/Counterpoint Research", "https://marklapedus.substack.com/p/tsmc-gains-foundry-share-in-q1-26"),
    },
    {
        "company": "ASML", "hq_location": "Netherlands", "sector": "Advanced Hardware",
        "market_share_pct": 100.0,
        "dependency_note": (
            "Sole global supplier of EUV lithography systems (100% of EUV specifically; ~94% of "
            "overall lithography equipment). Every sub-7nm chip on Earth is printed on ASML "
            "equipment; High-NA EUV extends the moat into the 2nm/1.4nm era with no credible "
            "near-term rival."
        ),
        "related_chokepoints": [], "related_minerals": [],
        "source": ("Finimize / ASML company disclosures", "https://finimize.com/content/asmlf-asset-snapshot"),
    },
    {
        "company": "Nvidia", "hq_location": "United States", "sector": "Advanced Hardware",
        "market_share_pct": 80.0,
        "dependency_note": (
            "Estimated share of AI accelerator/data-center GPU revenue, 2026 (credible range "
            "across trackers: 75-87%). Deep CUDA software lock-in; AMD (~5-7%) and hyperscaler "
            "custom silicon (Google TPU, Amazon Trainium) remain small by comparison."
        ),
        "related_chokepoints": [], "related_minerals": [],
        "source": ("Silicon Analysts -- NVIDIA AI GPU Market Share 2026", "https://siliconanalysts.com/analysis/nvidia-ai-accelerator-market-share-2024-2026"),
    },
    {
        "company": "Saudi Aramco", "hq_location": "Saudi Arabia", "sector": "Energy",
        "market_share_pct": 10.0,
        "dependency_note": (
            "~10% of global crude production (~10.1M bpd of ~102M bpd global), under OPEC+ "
            "coordination; among the world's largest proven reserves (~260-270B barrels, from a "
            "secondary aggregator -- flagged for primary-source verification). World's lowest-cost "
            "large-scale producer and OPEC+'s de facto swing producer."
        ),
        "related_chokepoints": ["strait_of_hormuz"], "related_minerals": [],
        "source": ("Vision2030.ai (secondary aggregator, flagged for primary-source verification)", "https://vision2030.ai/encyclopedia/saudi-arabia-oil-reserves/"),
    },
    {
        "company": "QatarEnergy", "hq_location": "Qatar", "sector": "Energy",
        "market_share_pct": 18.7,
        "dependency_note": (
            "18.7% is Qatar's pre-strike full-year-2025 share of global LNG exports (world's #2 "
            "LNG exporter). MAJOR 2026 DEVELOPMENT: Iranian strikes on Ras Laffan/Mesaieed in "
            "March 2026 knocked out roughly 17% of Qatar's LNG capacity -- QatarEnergy's own CEO "
            "says repairs will take 3-5 years, and the company has declared force majeure on "
            "long-term contracts to Italy, Belgium, South Korea, and China. Read the 18.7% figure "
            "as a pre-strike baseline, not current effective capacity."
        ),
        "related_chokepoints": ["strait_of_hormuz"], "related_minerals": [],
        "source": ("The Peninsula Qatar -- Qatar strengthens LNG leadership as exports reach record high in 2025", "https://thepeninsulaqatar.com/article/30/07/2026/qatar-strengthens-lng-leadership-as-exports-reach-record-high-in-2025"),
    },
    {
        "company": "Maersk", "hq_location": "Denmark", "sector": "Logistics & Shipping",
        "market_share_pct": 13.7,
        "dependency_note": (
            "Share of global container shipping capacity, May 2026 -- a 20-year low for Maersk, "
            "having ceded the #1 spot to MSC (21.5-21.6%). Maersk has shifted from a capacity-"
            "leadership strategy to an 'integrator' logistics model via the Gemini Cooperation "
            "alliance with Hapag-Lloyd, prioritizing reliability over fleet size."
        ),
        "related_chokepoints": ["suez_canal", "bab_el_mandeb"], "related_minerals": [],
        "source": ("IndexBox -- MSC Sets New Industry Benchmark with 21.6% Global Container Capacity Share (May 2026)", "https://www.indexbox.io/blog/msc-reaches-record-216-global-container-market-share-surpassing-maersks-historic-high/"),
    },
    {
        "company": "China Northern Rare Earth Group", "hq_location": "China", "sector": "Critical Minerals",
        # Neither IEA nor USGS publishes a clean company-level % of China's national rare earth
        # output. What is verifiable: it holds the largest single mining-quota allocation among
        # China's state-consolidated RE groups. Left as None rather than an invented %.
        "market_share_pct": None,
        "dependency_note": (
            "World's largest rare earth mining company by volume, anchored on the Bayan Obo "
            "deposit in Inner Mongolia. Awarded an 80,900-tonne mining quota (2025 first batch, "
            "+34.4% YoY) -- industry estimates put this around 45-50% of China's national quota, "
            "but that percentage is not independently confirmed against a primary official source. "
            "Controls a major share of upstream light rare earth supply feeding global magnet, EV, "
            "and defense supply chains."
        ),
        "related_chokepoints": [], "related_minerals": ["rare_earth_refining"],
        "source": ("Yicai Global -- China Northern Rare Earth Group Keeps Top Position as MIIT Releases First Quota List", "https://www.yicaiglobal.com/news/china-northern-rare-earth-group-keeps-top-position-as-miit-releases-first-quota-list"),
    },
    {
        "company": "Vale", "hq_location": "Brazil", "sector": "Critical Minerals",
        "market_share_pct": 18.0,
        "dependency_note": (
            "Approximate share of global seaborne iron ore trade, 2024/2025 estimates (range "
            "cited: 17-19%) -- the 'Big Four' (Vale, Rio Tinto, BHP, Fortescue) together control "
            "roughly 70-80% of seaborne supply. Vale's high-grade Brazilian ore (Carajás/S11D) is "
            "disproportionately important for green-steel/DRI-grade feedstock; ore quality/grade "
            "is geologically fixed, limiting how easily this dependency can be diversified away. "
            "The 17-19% figure came from secondary market commentary rather than a single named "
            "primary report -- treat as approximate."
        ),
        "related_chokepoints": [], "related_minerals": [],
        "source": ("Rio Times Online -- Iron Ore Markets Latam", "https://www.riotimesonline.com/iron-ore-markets-latam-saturday-august-22-2026/"),
    },
]

# Simplified great-circle-ish waypoints for the trade-artery overlay -- these
# are illustrative routing paths (MENASA to Europe / East Asia), not precise
# shipping-lane geometry.
TRADE_ARTERIES = [
    {"name": "Asia → Europe via Suez", "chokepoints": ["bab_el_mandeb", "suez_canal"],
     "path": [(1.3, 103.8), (12.58, 43.33), (30.5, 32.35), (36.1, 5.3), (51.9, 4.5)]},
    {"name": "Persian Gulf → Asia (energy exports)", "chokepoints": ["strait_of_hormuz"],
     "path": [(26.2, 50.6), (26.57, 56.25), (5.3, 100.3), (1.3, 103.8), (31.2, 121.5)]},
    {"name": "Persian Gulf → Europe (energy exports)", "chokepoints": ["strait_of_hormuz", "bab_el_mandeb", "suez_canal"],
     "path": [(26.2, 50.6), (26.57, 56.25), (12.58, 43.33), (30.5, 32.35), (36.1, 5.3), (43.3, 5.4)]},
]

# Real, stable membership facts (not a scored/sourced-figure claim the way the
# datasets above are) -- shown as a simple map annotation layer only.
TRADE_ALLIANCES = {
    "GCC": {"members": ["Saudi Arabia", "UAE", "Qatar", "Kuwait", "Bahrain", "Oman"],
            "centroid": (24.5, 51.0)},
    "BRICS+": {"members": ["Brazil", "Russia", "India", "China", "South Africa", "Egypt",
                            "Ethiopia", "Iran", "UAE"],
               "centroid": (20.0, 50.0),
               "note": "Saudi Arabia was invited to join in 2024 but its accession status has "
                       "remained unresolved/unconfirmed -- deliberately not listed as a member."},
    "ASEAN": {"members": ["Indonesia", "Malaysia", "Philippines", "Thailand", "Vietnam",
                           "Singapore", "Brunei", "Cambodia", "Laos", "Myanmar"],
              "centroid": (10.0, 106.0)},
    "EU": {"members": ["Germany", "France", "Italy", "Spain", "Netherlands", "and 22 others"],
           "centroid": (50.0, 10.0)},
}


# ============================================================
# RESOURCE_BENCHMARKS -- top-5 companies, real benchmark/exchange, and a
# sourced 2025-2026 price narrative for eight resources central to MENASA
# trade exposure. "yfinance_ticker" is set only where a real, live-fetchable
# futures ticker exists (Brent, Henry Hub, Gold) -- the app charts real
# historical prices for those three rather than describing them in text.
# Cobalt/Nickel trade on the LME, which isn't reliably available via
# yfinance, and phosphates/graphite/REE have no standard exchange contract
# at all (priced via bulk contract/specialist assessments instead) -- all
# five are context-only, same treatment as CRITICAL_MINERAL_DEPENDENCIES.
# ============================================================

RESOURCE_BENCHMARKS = {
    "crude_oil": {
        "label": "Crude Oil",
        "yfinance_ticker": "BZ=F",
        "benchmark": "Brent Crude (ICE Futures) and WTI (NYMEX/CME) -- the two global price references; OPEC+ national producers set output policy but don't set a single official price.",
        "price_narrative": (
            "Brent spiked to ~$109/bbl in Q1 2026 when the Feb 28 US-Israel-Iran war collapsed "
            "Strait of Hormuz transit (~20% of global seaborne oil), then fell back under $70 after "
            "the strait reopened mid-June 2026. The EIA sharply raised its 2026 average forecast "
            "from $58 to $79/bbl in the aftermath, while some bank forecasts (Goldman Sachs) stayed "
            "lower (~$56) assuming the war premium fades. BloombergNEF sees only a modest ~$4/bbl "
            "residual war premium as of mid-2026. Underlying non-war fundamentals (US shale growth, "
            "OPEC+ spare capacity) had been pushing toward oversupply before the war."
        ),
        "sources": [
            ("EIA / Yahoo Finance -- Oil Shock Lifts EIA Price Outlook", "https://finance.yahoo.com/news/oil-shock-lifts-eia-price-173000464.html"),
            ("BloombergNEF -- Oil Can Hit $91/bbl in Late 2026", "https://about.bnef.com/insights/commodities/oil-can-hit-91-a-barrel-in-late-2026-on-iran-disruption/"),
            ("Gulf News -- Brent spikes to $109 amid Iran-US-Israel war", "https://gulfnews.com/business/energy/brent-crude-oil-price-spikes-to-1071-amid-iran-us-israel-war-1.500467933"),
        ],
        "top_companies": [
            {"company": "Saudi Aramco", "hq_location": "Saudi Arabia", "position": "#1 producer, ~12.9 million boe/d total hydrocarbon output (FY2025); largest crude producer in the world, state-controlled", "source": ("Aramco FY2025 results / Visual Capitalist", "https://www.visualcapitalist.com/visualizing-saudi-aramcos-massive-oil-reserves/")},
            {"company": "ExxonMobil", "hq_location": "USA", "position": "Largest non-state-owned producer, record ~4.3 million boe/d (2024-2025), ~3.3 million bbl/d liquids", "source": ("Statista -- ExxonMobil net liquids production", "https://www.statista.com/statistics/1032515/exxonmobil-net-liquids-production-worldwide/")},
            {"company": "Chevron", "hq_location": "USA", "position": "Major US producer, guided 6-8% output growth in 2025 over 2024, driven by ~10% Permian Basin growth", "source": ("Chevron 10-K FY2025 / Fortune", "https://fortune.com/2025/10/31/exxon-chevron-shell-oil-production-global-supply-glut-exploration-opec-output/")},
            {"company": "PetroChina", "hq_location": "China", "position": "Record 4.736 million boe/d in 2025 (oil+gas combined) -- oil-equivalent figure, not pure crude, flagged for comparability", "source": ("PetroChina 2025 annual results reporting", "https://farmonaut.com/mining/top-20-oil-companies-in-the-world-2026-update")},
            {"company": "Rosneft", "hq_location": "Russia", "position": "Russia's largest producer/exporter (~19.9% of Russian crude exports by value, 2025); precise current bbl/d unreconciled post-sanctions -- flagged as approximate", "source": ("Aggregated trade data reporting", "https://tradeint.com/insights/top-10-crude-oil-exporting-countries/")},
        ],
    },
    "natural_gas_lng": {
        "label": "Natural Gas / LNG",
        "yfinance_ticker": "NG=F",
        "benchmark": "No single global LNG futures benchmark. Henry Hub (NYMEX/CME) prices US domestic gas feedstock; JKM (Japan-Korea Marker, ICE) prices spot Asian LNG cargoes; TTF (ICE Endex) prices European gas. LNG itself is largely sold via long-term bilateral contracts indexed to these markers.",
        "price_narrative": (
            "Qatar's LNG export capacity was cut roughly 17% after Feb-March 2026 strikes on the "
            "Ras Laffan and Mesaieed complexes during the US-Israel-Iran war, with production "
            "'almost completely halted' at points in March 2026. This pushed Asian buyers toward US "
            "and other suppliers, and 2025 already saw a landmark shift with US LNG exports "
            "outpacing Qatar's for the first time. JKM and European TTF prices rose on the loss of "
            "Qatari cargoes since Qatar could not be quickly substituted. New US capacity (Golden "
            "Pass LNG, ExxonMobil/QatarEnergy JV, first train 2026) is easing some tightness into "
            "H2 2026."
        ),
        "sources": [
            ("EnergyNow -- Qatar loses LNG export capacity for years after strikes", "https://energynews.pro/en/qatar-loses-lng-export-capacity-for-years-after-strikes"),
            ("EnergyNow -- US LNG exports outpace Qatar", "https://energy-oil-gas.com/news/us-lng-exports-outpace-qatar-in-landmark-year-for-natural-gas/"),
            ("EnergyNow -- Little US LNG producers can do to replace lost Qatari cargoes", "https://energynow.com/2026/03/there-is-little-us-lng-producers-can-do-to-immediately-replace-lost-qatari-cargoes/"),
        ],
        "top_companies": [
            {"company": "QatarEnergy", "hq_location": "Qatar", "position": "World's largest LNG supplier by operational capacity, 55.8 mtpa (2024 baseline); capacity cut ~17% by the Feb-2026 war strikes", "source": ("Statista / EnergyNow", "https://www.statista.com/statistics/859126/largest-lng-exporting-companies-by-capacity")},
            {"company": "Cheniere Energy", "hq_location": "USA", "position": "#2 globally, ~44.5-46 mtpa operational capacity; Sabine Pass is the world's largest single liquefaction platform", "source": ("BlackRidge Research -- Top 15 LNG Companies", "https://www.blackridgeresearch.com/blog/list-of-global-top-liquefied-natural-gas-lng-companies-manufacturers-producers-operators-suppliers-in-the-world")},
            {"company": "Shell", "hq_location": "United Kingdom/Netherlands", "position": "#3 globally by LNG supply/trading volume, large integrated portfolio", "source": ("BlackRidge Research", "https://www.blackridgeresearch.com/blog/list-of-global-top-liquefied-natural-gas-lng-companies-manufacturers-producers-operators-suppliers-in-the-world")},
            {"company": "TotalEnergies", "hq_location": "France", "position": "#1 exporter of US LNG specifically, shipping >19 mtpa (2025); targeting 50 mtpa across global portfolio", "source": ("TotalEnergies USA corporate release", "https://corporate.totalenergies.us/totalenergies-largest-exporter-us-liquefied-natural-gas-lng")},
            {"company": "ExxonMobil", "hq_location": "USA", "position": "Major integrated LNG portfolio (Golden Pass JV with QatarEnergy, PNG, Mozambique, Guyana); exact global mtpa ranking vs. peers not precisely reconciled", "source": ("Aggregated industry reporting", "https://energydigital.com/top10/top-10-lng-companies")},
        ],
    },
    "gold": {
        "label": "Gold",
        "yfinance_ticker": "GC=F",
        "benchmark": "LBMA Gold Price (London Bullion Market Association twice-daily auction) is the global spot reference; COMEX gold futures (CME Group) is the primary tradable futures benchmark.",
        "price_narrative": (
            "Gold gained an extraordinary 64% in 2025, setting over 50 record highs, then surged "
            "past $5,000/oz in January 2026 and above $5,100 shortly after -- confirming the "
            "safe-haven thesis held (and intensified) through the Feb 2026 US-Israel-Iran war. The "
            "rally is distinguished by record central-bank buying (China alone added to a 14-month "
            "buying streak, >2,303 tonnes reserves) and ETF inflows hitting record AUM, alongside "
            "trade-tension-driven diversification away from US Treasuries. Total 2025 demand topped "
            "5,000 tonnes, with investment demand up ~84% year-on-year."
        ),
        "sources": [
            ("Gold.org -- Gold Demand Trends 2026", "https://www.gold.org/goldhub/research/gold-demand-trends"),
            ("Bullion Trading LLC -- Gold Price Record High 2026", "https://bulliontradingllc.com/blog/gold-price-5000-record-high-2026-drivers/"),
            ("Yahoo Finance -- Gold demand hits record levels, central banks buy at 'eye-watering' pace", "https://finance.yahoo.com/news/gold-demand-hits-record-levels-as-central-banks-buy-at-eye-watering-pace-205945413.html"),
        ],
        "top_companies": [
            {"company": "Newmont Corporation", "hq_location": "USA", "position": "#1 gold miner, 5.47 million oz produced in 2025", "source": ("MINING.COM -- Ranked: Top 10 gold mining companies of 2025", "https://www.mining.com/ranked-top-10-gold-mining-companies-of-2025/")},
            {"company": "Agnico Eagle Mines", "hq_location": "Canada", "position": "#2, 3.44 million oz in 2025, overtook Barrick for second place", "source": ("MINING.COM", "https://www.mining.com/ranked-top-10-gold-mining-companies-of-2025/")},
            {"company": "Barrick Mining Corporation", "hq_location": "Canada", "position": "#3, 3.03 million oz in 2025; renamed from Barrick Gold Corporation in May 2025", "source": ("Barrick.com / MINING.COM", "https://www.barrick.com/English/news/news-details/2025/barrick-mining-corporation/default.aspx")},
            {"company": "Zijin Mining Group", "hq_location": "China", "position": "#4, surged into the top tier with a 35% production increase in 2025", "source": ("MINING.COM", "https://www.mining.com/ranked-top-10-gold-mining-companies-of-2025/")},
            {"company": "Gold Fields", "hq_location": "South Africa", "position": "#5, 18% production jump in 2025 on operational improvements", "source": ("MINING.COM", "https://www.mining.com/ranked-top-10-gold-mining-companies-of-2025/")},
        ],
    },
    "phosphates": {
        "label": "Phosphates",
        "yfinance_ticker": None,
        "benchmark": "No standard exchange-traded futures contract. Priced via bulk/spot contract references -- chiefly the Morocco FOB phosphate rock benchmark and DAP/MAP price assessments from agencies like Argus FMB, CRU, and Fertecon.",
        "price_narrative": (
            "Phosphate rock held broadly stable near $150-158/tonne FOB Morocco through 2025-2026. "
            "DAP prices rallied through Q1-Q3 2025 (from ~$0.64/kg to a Q3 peak of ~$0.79/kg) on "
            "Chinese export restrictions, aggressive Indian procurement, and tight inventories, "
            "before easing ~7% in Q4 2025 as demand cooled and Morocco's OCP plus Saudi Arabia's "
            "Ma'aden kept supply flowing. A global sulfur shortage (a key input) is also pushing "
            "costs up. Morocco/OCP's reserve dominance gives it structural pricing power but it "
            "hasn't triggered a supply-restriction price shock the way DRC cobalt or Chinese rare "
            "earths have."
        ),
        "sources": [
            ("Morocco World News -- Morocco's phosphate sector holds steady", "https://www.moroccoworldnews.com/2026/03/282882/moroccos-phosphate-sector-holds-steady-despite-global-fertilizer-market-pressure/"),
            ("ExpertMarketResearch -- DAP Price Trend 2026", "https://www.expertmarketresearch.com/price-forecast/dap-price-trends"),
            ("ExpertMarketResearch -- Phosphate Rock Price Trend 2026", "https://www.expertmarketresearch.com/price-forecast/phosphate-rock-price-trends"),
        ],
        "top_companies": [
            {"company": "OCP Group", "hq_location": "Morocco", "position": "#1 -- controls 68% of world's phosphate rock reserves per USGS (Jan 2025); other estimates range 70-75%, unreconciled; ~13.5% of global phosphate product market revenue, >2x nearest competitor", "source": ("USGS-sourced reporting via OCP Group", "https://en.wikipedia.org/wiki/OCP_Group")},
            {"company": "Nutrien Ltd.", "hq_location": "Canada", "position": "Top-5 global producer, major DAP/MAP producer and marketer", "source": ("Discovery Alert -- Phosphate fertilizers 2025 market dynamics", "https://discoveryalert.com.au/phosphate-fertilizers-2025-market-dynamics-morocco/")},
            {"company": "The Mosaic Company", "hq_location": "USA", "position": "Top-5 global producer of concentrated phosphate and potash crop nutrients", "source": ("Mosaic Co. FY2025/2026 SEC filings", "https://www.sec.gov/Archives/edgar/data/1285785/000119312526158446/d37864dars.pdf")},
            {"company": "PhosAgro", "hq_location": "Russia", "position": "Top-5 global producer of phosphate fertilizers (MAP, DAP, specialty grades)", "source": ("Industry aggregated reporting", "https://www.gminsights.com/industry-analysis/phosphate-rock-market")},
            {"company": "Ma'aden (Saudi Arabian Mining Co.)", "hq_location": "Saudi Arabia", "position": "Top-5 global phosphate rock/fertilizer producer, rapidly expanding capacity alongside OCP", "source": ("Global market insights aggregation", "https://www.gminsights.com/industry-analysis/phosphate-rock-market")},
        ],
    },
    "natural_graphite": {
        "label": "Natural Graphite",
        "yfinance_ticker": None,
        "benchmark": "No standard exchange-traded futures contract. Priced via bulk contracts and specialist price assessments (Benchmark Mineral Intelligence, Fastmarkets).",
        "price_narrative": (
            "China controls ~75-80% of natural graphite mining and 90%+ of anode processing, "
            "leverage it has used repeatedly since Dec 2023 -- most recently expanding export "
            "licensing to artificial graphite in Nov 2025, alongside standing US anti-dumping duties "
            "of 93.5% on Chinese anode material. China temporarily eased end-user verification for "
            "US-bound shipments in Nov 2025 (through Nov 27, 2026), easing near-term supply anxiety "
            "but leaving structural risk unresolved past that date. Prices diverged regionally in "
            "2025: North America rose ~5.2% on tariff-driven scarcity while Northeast Asia fell "
            "~17.7% on chronic oversupply -- a genuinely bifurcated, not single, global price."
        ),
        "sources": [
            ("Crux Investor -- China's temporary easing of graphite export controls", "https://www.cruxinvestor.com/posts/chinas-temporary-easing-of-graphite-export-controls-the-shifting-global-supply-outlook-for-battery-materials"),
            ("Metals-Hub -- Graphite Supply Chain in 2026", "https://www.metals-hub.com/en/blog/graphite-supply-chain/"),
            ("Investing News Network -- Graphite Market Trends H1 2026", "https://investingnews.com/daily/resource-investing/battery-metals-investing/graphite-investing/graphite-forecast/"),
        ],
        "top_companies": [
            {"company": "BTR New Material Group", "hq_location": "China", "position": "China's largest natural+synthetic graphite anode material producer", "source": ("Critical Minerals News", "https://critical-minerals-news.com/top-10-graphite-mining-companies-2026/")},
            {"company": "Sinosteel Corporation", "hq_location": "China", "position": "One of China's largest natural graphite mining groups", "source": ("Industry aggregated reporting", "https://www.zdnaturalgraphite.com/top-7-global-natural-graphite-mines-ranked-by-capacity/")},
            {"company": "Syrah Resources", "hq_location": "Australia (Balama mine, Mozambique)", "position": "Operates the world's largest single graphite mine outside China; 67,000 tonnes produced in 2025", "source": ("Syrah Resources Dec 2025 production report", "https://mining.com.au/breaking-the-graphite-bottleneck/")},
            {"company": "Nouveau Monde Graphite", "hq_location": "Canada", "position": "Largest Western pure-play, most integrated mine-to-anode supply chain; US$645M funding (May 2026) for Matawinie Mine phase 2, targeting 106,000 tpa", "source": ("Investing News Network", "https://investingnews.com/top-graphite-miners-asx")},
            {"company": "Nacional de Grafite", "hq_location": "Brazil", "position": "One of the largest non-Chinese natural graphite producers historically; exact current global rank vs. mid-tier producers not precisely reconciled -- flagged as lower-confidence", "source": ("Industry sector overview", "https://www.researchandmarkets.com/articles/key-companies-in-graphite")},
        ],
    },
    "rare_earth_elements": {
        "label": "Rare Earth Elements",
        "yfinance_ticker": None,
        "benchmark": "No standard global futures exchange. Priced via specialist OTC assessments (Fastmarkets, Argus, Shanghai Metals Market) and increasingly bespoke government-backed price floors (e.g. MP Materials' 10-year $110/kg NdPr floor with the US government).",
        "price_narrative": (
            "China has layered rare earth and magnet export licensing restrictions since Dec 2023, "
            "expanding controls on April 4, 2025 to cover downstream magnets and adding five more "
            "elements in Oct 2025 -- causing Chinese REE exports to plunge 74.3% y/y in May 2025 at "
            "the peak of disruption. NdPr prices rose from ~$53/kg in Jan 2026 to ~$125/kg by "
            "mid-2026 (+136% YTD). Heavy rare earths spiked even harder: dysprosium oxide to "
            "~$1,450/kg and terbium oxide to ~$4,500/kg by May 2026, up from single digits "
            "pre-restriction. These bottlenecks are expected to persist through 2026."
        ),
        "sources": [
            ("S&P Global -- Rare earth supply bottlenecks set to persist in 2026", "https://www.spglobal.com/energy/en/news-research/latest-news/metals/012726-rare-earth-supply-bottlenecks-set-to-persist-in-2026"),
            ("The Oregon Group -- Rare Earth prices surge as China keeps export restrictions", "https://theoregongroup.com/commodities/rare-earths/rare-earth-prices-surge-as-china-keeps-export-restrictions/"),
            ("CSIS -- China's new rare earth and magnet restrictions", "https://www.csis.org/analysis/chinas-new-rare-earth-and-magnet-restrictions-threaten-us-defense-supply-chains"),
        ],
        "top_companies": [
            {"company": "China Northern Rare Earth Group", "hq_location": "China", "position": "#1 globally, ~40% of global supply, projected 58,800 tonnes output in 2026", "source": ("Voronoi App -- Top 10 Rare Earth Miners & Refiners by Market Cap", "https://www.voronoiapp.com/investing/Top-10-Rare-Earth-Miners--Refiners-by-Market-Capitalization-6180")},
            {"company": "China Rare Earth Group", "hq_location": "China", "position": "Second major Chinese state-consolidated producer; Chinese state-backed entities together hold ~85-90% of global processing capacity", "source": ("Aggregated industry analysis", "https://rare-earth-mining.com/top-10-rare-earth-mining-companies/")},
            {"company": "MP Materials", "hq_location": "USA", "position": "Largest rare earth producer in the Western Hemisphere (Mountain Pass, California); 10-year $110/kg NdPr price floor from the US government", "source": ("MP Materials SEC 10-K FY2025", "https://www.sec.gov/Archives/edgar/data/1801368/000180136826000008/mp-20251231.htm")},
            {"company": "Lynas Rare Earths", "hq_location": "Australia", "position": "Largest producer of separated rare earths outside China; Mt Weld mine + Malaysia processing, targeting 12,000 tpa NdPr at full ramp", "source": ("rare-earth-mining.com competitor analysis", "https://rare-earth-mining.com/lynas-rare-earths-competitors/")},
            {"company": "Shenghe Resources", "hq_location": "China", "position": "Major Chinese rare earth processing and trading company, part of the trio dominating most global processing capacity", "source": ("Aggregated industry analysis", "https://rare-earth-mining.com/top-10-rare-earth-mineral-processing-companies/")},
        ],
    },
    "cobalt": {
        "label": "Cobalt",
        "yfinance_ticker": None,
        "benchmark": "LME Cobalt (London Metal Exchange futures contract, also assessed via Fastmarkets MB) is the standard tradable benchmark.",
        "price_narrative": (
            "The DRC's 2024 cobalt export ban followed by a 2025 quota system (covering 2025-2027) "
            "drove cobalt prices up roughly 130-160% -- from ~$20,000/tonne in Feb 2025 to over "
            "$56,000-57,000/tonne by Jan-mid-2026, a 4-year high. The DRC's 2026 export quota is set "
            "at 96,600 tonnes (87,000t pro-rata plus 9,600t discretionary reserve) -- roughly half "
            "of 2024 production levels. Fastmarkets still projects a ~10,700-tonne supply deficit "
            "for 2026, meaning further tightness is likely even as the acute shortage phase passes."
        ),
        "sources": [
            ("Fastmarkets -- Dried-up feedstock pipeline sends cobalt prices soaring", "https://www.fastmarkets.com/insights/dried-up-feedstock-pipeline-cobalt-prices-soaring-2025-deficit/"),
            ("Benchmark Source -- DRC to lift cobalt export ban and impose quotas through 2027", "https://source.benchmarkminerals.com/article/drc-to-lift-cobalt-export-ban-and-impose-quotas-through-2027"),
            ("Ecofin Agency -- Cobalt export quotas and copper supply risks", "https://www.ecofinagency.com/news-industry/2101-52126-cobalt-export-quotas-and-copper-supply-risks-shape-drc-revenue-outlook"),
        ],
        "top_companies": [
            {"company": "China Molybdenum Co. (CMOC)", "hq_location": "China (DRC operations)", "position": "#1 globally, 114,165 tonnes mined in 2024, 2025 guidance 100,000-120,000 tonnes", "source": ("Critical Minerals News -- Top 10 Cobalt Producers", "https://critical-minerals-news.com/top-10-cobalt-producers/")},
            {"company": "Glencore", "hq_location": "Switzerland (DRC operations: Mutanda, KCC)", "position": "Major top-5 DRC cobalt producer, part of the group supplying >70% of global demand alongside CMOC and Gecamines", "source": ("Farmonaut -- Biggest Cobalt Mining Companies & Mines 2025", "https://farmonaut.com/mining/biggest-cobalt-mining-companies-mines-2025")},
            {"company": "Eurasian Resources Group (ERG)", "hq_location": "Luxembourg/Kazakhstan (DRC operations)", "position": "Operates Metalkol RTR in DRC, an advanced tailings-reprocessing project; top-tier DRC cobalt producer", "source": ("Farmonaut aggregation", "https://farmonaut.com/mining/top-cobalt-mining-companies-2026-key-trends-updates")},
            {"company": "Vale", "hq_location": "Brazil", "position": "Top-10 global cobalt producer as a byproduct of nickel operations (Voisey's Bay, Indonesia assets)", "source": ("Vale SEC 6-K filings FY2025", "https://www.sec.gov/Archives/edgar/data/917851/000129281425004048/vale20251119_6k.htm")},
            {"company": "Huayou Cobalt", "hq_location": "China", "position": "Major integrated cobalt miner/refiner, part of the Chinese trio dominating both mining and refining stages", "source": ("Farmonaut -- Top Chinese & US Cobalt Mining Companies 2026", "https://farmonaut.com/mining/top-chinese-us-cobalt-mining-companies-2026")},
        ],
    },
    "nickel": {
        "label": "Nickel",
        "yfinance_ticker": None,
        "benchmark": "LME Nickel (London Metal Exchange futures contract) is the standard tradable benchmark.",
        "price_narrative": (
            "Nickel fell to near four-year lows (~$14,550/tonne) in Nov 2025 on weak stainless-steel "
            "and battery demand plus ample Indonesian-driven supply, then rallied sharply -- to "
            ">$17,000/t by Feb 11, 2026 and a 1.5-year high of $18,950/t on Jan 29, 2026 -- as "
            "Indonesia signaled sharply lower 2026 mining quotas (260-270 million wmt vs. 379 "
            "million wmt in 2025, some reports suggesting an even tighter 190-200 million tonnes). "
            "This is the mirror image of the graphite/cobalt story: Indonesia's ~45-50% global "
            "mine-production share means its quota policy, not a supply shock, is now the dominant "
            "price lever, deliberately used to prop up prices amid a structural surplus."
        ),
        "sources": [
            ("Mining.com -- Nickel price jumps as Indonesia's top mine cuts output", "https://www.mining.com/nickel-price-jumps-as-indonesias-top-mine-cuts-output/"),
            ("Benchmark Source -- Indonesia announces significantly lower nickel RKAB quotas", "https://source.benchmarkminerals.com/article/indonesia-announces-significantly-lower-nickel-rkab-quotas"),
            ("ING Think -- Nickel still capped by surplus", "https://think.ing.com/articles/nickel-still-capped-by-surplus/"),
        ],
        "top_companies": [
            {"company": "MMC Norilsk Nickel (Nornickel)", "hq_location": "Russia", "position": "#1, 198,521 tonnes produced in 2025; 2026 guidance 193,000-203,000 tonnes", "source": ("Mining.com -- Nornickel sees 2026 output in line with previous year", "https://www.mining.com/web/nornickel-sees-2026-nickel-output-broadly-in-line-with-previous-year/")},
            {"company": "Vale", "hq_location": "Brazil", "position": "#2, 177,000 tonnes in 2025 (Onca Puma 2nd furnace + Voisey's Bay ramp-up); 2026 guidance 175,000-200,000 tonnes", "source": ("Vale SEC 6-K FY2025", "https://www.sec.gov/Archives/edgar/data/917851/000129281426000367/vale20260212_6k2.htm")},
            {"company": "Tsingshan Holding Group", "hq_location": "China (Indonesia operations)", "position": "World's largest nickel pig iron/ferronickel producer, ~300,000 tonne ferronickel capacity", "source": ("Jakarta Post -- Tsingshan slashes local nickel pig iron output", "https://www.thejakartapost.com/business/2025/06/05/tsingshan-slashes-local-nickel-pig-iron-output-amid-profit-squeeze.html")},
            {"company": "Harita Nickel (PT Trimegah Bangun Persada)", "hq_location": "Indonesia", "position": "Major Indonesian HPAL/nickel producer; ranking vs. other Indonesian smelter groups by exact tonnage not precisely reconciled -- flagged as approximate", "source": ("Industry sector aggregation", "https://greenstocksresearch.com/nickel-stocks/")},
            {"company": "Jinchuan Group", "hq_location": "China", "position": "China's largest integrated nickel miner/refiner domestically; top-10 global producer", "source": ("Global Growth Insights -- Top 9 Nickel Companies 2026", "https://www.globalgrowthinsights.com/blog/nickel-companies-1171")},
        ],
    },
}


# ============================================================
# Deeper sub-asset verification pass (semiconductor node tiers, energy flow
# granularity, UNCTAD topline figures). Where a genuinely granular figure
# (e.g. a sour/sweet crude split per chokepoint, a current TSMC-vs-Samsung
# sub-7nm-specific %, or a published semiconductor HHI) does not actually
# exist in any public source as of this research pass, that is stated
# explicitly as "Data Pending Verification" rather than derived/estimated --
# per this project's rule against fabricated or simulated figures.
# ============================================================

SEMICONDUCTOR_SUBDIVISIONS = {
    "advanced_sub7nm": {
        "label": "Advanced (Sub-7nm) Foundry",
        "note": (
            "No current, sourced, company-level sub-7nm-specific % split between TSMC and Samsung "
            "is published anywhere -- Data Pending Verification for that specific number. What is "
            "real and sourced: TSMC's own wafer-revenue mix (Q4 2025) is 36% 5nm, 24-28% 3nm, 14% "
            "7nm; Samsung's 2nm (SF2) line reported 55-60% yield as of Nov 2025 with mass production "
            "starting 2025-2026. A 2021 BCG/SIA report is the closest authoritative concentration "
            "source (near-monopoly of sub-10nm capacity sitting with Taiwan/South Korea) but it's "
            "dated, describes sub-10nm not sub-7nm, and splits by country rather than by company --  "
            "used here only as historical qualitative context, not a current numeric split."
        ),
        "fabs": [
            {"company": "TSMC", "site": "Hsinchu Science Park, Taiwan", "lat": 24.77, "lon": 121.07},
            {"company": "TSMC", "site": "Tainan / Southern Taiwan Science Park (Fab 18, 2nm/3nm)", "lat": 23.10, "lon": 120.28},
            {"company": "TSMC", "site": "Arizona, USA (Fab 21)", "lat": 33.67, "lon": -112.10},
            {"company": "TSMC", "site": "Kumamoto, Japan (JASM)", "lat": 32.82, "lon": 130.83},
            {"company": "Samsung", "site": "Pyeongtaek, South Korea", "lat": 36.99, "lon": 127.09},
        ],
        "sources": [
            ("TrendForce -- TSMC/Samsung foundry revenue and node mix reporting, Q4 2025", "https://marklapedus.substack.com/p/tsmc-gains-foundry-share-in-q1-26"),
            ("SIA/BCG -- Strengthening the Global Semiconductor Supply Chain in an Uncertain Era (2021)", "https://www.semiconductors.org/"),
        ],
    },
    "mature_legacy_node": {
        "label": "Mature/Legacy-Node Foundry",
        "china_share_2021_pct": 22.0,
        "china_share_2030_projected_pct": 53.0,
        "note": (
            "China's mature-node (typically >28nm) capacity share is real and sourced: 22% of "
            "global legacy-node capacity in 2021, projected to reach 53% by 2030. Total mainland "
            "12-inch foundry capacity (ex-memory/IDM) is ~1.2M wafers/month as of end-2025, ~1.5M "
            "projected for 2026. SMIC and Hua Hong are the two established leaders, with Nexchip "
            "(China's #3 foundry) expanding and reportedly filing for a Hong Kong listing (April "
            "2026). South Asia has near-zero confirmed leading-edge or legacy fab capacity -- "
            "India's fabs (e.g. Tata/PSMC Dholera) remain pre-production as of August 2026 and are "
            "not yet contributing to global capacity figures."
        ),
        "leaders": [
            {"company": "SMIC", "hq_location": "China", "position": "Acquired remaining 49% of SMIC North for $5.7B; guiding ~40,000 additional 12-inch-equivalent wafers/month by end-2026"},
            {"company": "Hua Hong Semiconductor", "hq_location": "China", "position": "Absorbed Shanghai Huali Microelectronics ($1.2B), adding 38,000 12-inch wafers/month at 65nm"},
            {"company": "Nexchip", "hq_location": "China", "position": "China's #3 foundry, expanding capacity, reportedly filing for a Hong Kong listing (TrendForce, April 2026)"},
        ],
        "sources": [
            ("TrendForce-linked analysis via Notebookcheck -- China mature-node capacity share", "https://www.notebookcheck.net/"),
            ("Tianxia Gongchang / TrendForce -- China 12-inch foundry capacity reporting", "https://www.trendforce.com/"),
        ],
    },
    "hhi_status": (
        "No authoritative HHI for global semiconductor foundry capacity has been published by SIA, "
        "BCG, McKinsey, or IEA as of this research pass. Rather than compute and display a "
        "self-derived HHI as if it were a confirmed third-party indicator, this figure is marked "
        "Data Pending Verification and omitted from any 'confirmed baseline indicator' display."
    ),
}

ENERGY_FLOW_GRANULARITY = {
    "hormuz_crude_grade_note": (
        "No public source (EIA, IEA, Kpler, Vortexa, S&P Global) splits Strait of Hormuz transit "
        "volume by crude grade (sour vs. sweet) -- Data Pending Verification for any percentage "
        "split. The honest qualitative fact: Gulf crude transiting Hormuz is predominantly "
        "medium-to-heavy SOUR grades (Arab Light ~33.3 deg API/1.96% sulfur; Basrah Medium/Heavy "
        "~24-28 deg API/3-4% sulfur). Light-sweet benchmark grades (Brent, WTI, West African crudes) "
        "largely don't transit MENASA chokepoints at all -- they move via the Atlantic/North Sea. "
        "So 'sour vs. sweet at Hormuz' isn't really a split to report -- Hormuz flow is sour-crude-"
        "dominant by definition."
    ),
    "hormuz_oil_breakdown_h1_2025": {
        "total_bbl_d": 20_900_000, "crude_and_condensate_bbl_d": 15_000_000, "refined_products_bbl_d": 5_500_000,
        "source": ("EIA -- Today in Energy (World Oil Transit Chokepoints)", "https://www.eia.gov/todayinenergy/detail.php?id=61002"),
    },
    "hormuz_lng_status": {
        "pre_war_baseline": "10-11 billion cubic feet/day, ~20% of global LNG trade; Qatar alone shipped >112 bcm LNG in 2025, ~93% via Hormuz.",
        "post_war_status": (
            "Data Pending Verification -- no aggregate bcf/d figure has been published for the "
            "post-February-2026-war period. The real, currently-tracked indicator is vessel-transit "
            "counts, not volume: zero LNG carrier transits between July 11-29, 2026; 21 LNG "
            "carriers counted inside the Gulf as of August 5, 2026 (13 ballast, 5 laden, 4 berthed). "
            "Oman-Iran talks on a temporary joint navigation corridor were still in progress as of "
            "August 25, 2026."
        ),
        "sources": [
            ("Lloyd's List Intelligence -- Strait of Hormuz Brief: 5 August 2026", "https://www.lloydslistintelligence.com/"),
            ("Kpler -- No LNG tankers cross Strait of Hormuz since July 11", "https://www.kpler.com/"),
        ],
    },
}

UNCTAD_RMT_2025 = {
    "edition": "Review of Maritime Transport 2025 (\"Staying the Course in Turbulent Waters\"), released 24 September 2025 -- the most recent real edition; no 2026 edition exists yet as of August 2026.",
    "global_seaborne_trade_2024_million_tons": 12720,
    "global_seaborne_trade_2024_growth_pct": 2.2,
    "ton_miles_growth_2024_pct": 5.9,
    "average_voyage_haul_nm": {"2018": 4831, "2024": 5245},
    "suez_transit_vs_2023_pct": -70,  # "approximately 70% below 2023 averages as of May 2025" -- UNCTAD's own figure
    "projections_labeled_as_projection_not_fact": {
        "2025_overall_growth_pct": 0.5,
        "2025_2029_containerized_trade_growth_pct": 2.7,
    },
    "sources": [
        ("UNCTAD -- Review of Maritime Transport 2025", "https://unctad.org/publication/review-maritime-transport-2025"),
    ],
}
