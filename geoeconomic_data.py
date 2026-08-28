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
