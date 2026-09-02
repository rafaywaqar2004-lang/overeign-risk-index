"""
UPCOMING_CATALYSTS: a small, deliberately incomplete calendar of concrete,
dated, sourced forward-looking events -- scheduled elections, IMF program
review windows, and similar institutional milestones -- for the countries
where one is actually confirmed in a reliable, checkable source.

This is NOT a forecast and NOT an attempt at full 34-country coverage. Two
disciplines, both inherited from this project's existing "never silently
fill a gap" principle (see the driver_data.py radar chart's amber "not
reported" markers):

1. Every entry needs a real, checkable date and source -- either drawn
   directly from this repo's own already-sourced CURRENT_GOVERNMENT /
   FINANCING_ARRANGEMENTS entries in context_data.py, or freshly verified
   against an official/primary source (an IMF press release or program
   document, a national election authority, a major wire service) as of
   this module's last review date below.
2. A country with no confirmed dated catalyst gets nothing here -- the app
   shows an explicit "no confirmed near-term catalyst identified" message
   for it, rather than a manufactured placeholder. Silence here means
   "nothing verified," not "nothing happening."

Each entry: {
    'date': ISO 'YYYY-MM-DD' where a specific date is confirmed, otherwise
            a plain-language window ('2026 Q4', 'By mid-2028') -- never a
            guessed exact date where the source itself only gives a window,
    'category': one of Election / IMF Review / Program Milestone / Political Transition,
    'event': short title,
    'detail': 1-3 sentences of real, sourced context -- what's confirmed vs.
              still unconfirmed (e.g. mission timing "to be announced"),
    'sources': [(label, url), ...],
}
"""

LAST_REVIEWED = "2026-09-02"

UPCOMING_CATALYSTS = {
    'MAR': [{
        'date': '2026-09-23',
        'category': 'Election',
        'event': 'General/legislative elections',
        'detail': (
            "Morocco's next general election is set for September 23, 2026 (campaign period "
            "September 10-22). PM Aziz Akhannouch has already announced he will not seek "
            "re-election as leader of his RNI party, so even an RNI win would not automatically "
            "return him as head of government -- a confirmed near-term leadership-change signal, "
            "though King Mohammed VI's position as head of state is unaffected."
        ),
        'sources': [
            ('Wikipedia — 2026 Moroccan general election', 'https://en.wikipedia.org/wiki/2026_Moroccan_general_election'),
            ('North Africa Post — Morocco to hold legislative elections on September 23', 'https://northafricapost.com/95312-morocco-to-hold-legislative-elections-on-september-23.html'),
        ],
    }],
    'ISR': [{
        'date': '2026-10-27',
        'category': 'Election',
        'event': 'General election',
        'detail': (
            "Netanyahu's coalition itself set October 27, 2026 -- the last legally possible date -- "
            "as Israel's next election, after United Torah Judaism's mid-2025 exit over the "
            "draft-conscription law left the coalition fragile. Pre-election polling points to a "
            "prolonged stalemate, with opposition parties still refusing to sit with Netanyahu."
        ),
        'sources': [
            ("Haaretz — Netanyahu Coalition Announces Israel's 2026 Election Will Take Place on October 27", 'https://www.haaretz.com/israel-news/elections/2026-07-12/ty-article/.premium/israels-2026-election-will-take-place-on-october-27-netanyahu-coalition-says/0000019f-56aa-d9b4-abdf-dfebadd60000'),
        ],
    }],
    'SSD': [{
        'date': '2026-12-22',
        'category': 'Election',
        'event': 'First general election since independence',
        'detail': (
            "South Sudan's National Elections Commission officially set December 22, 2026 as the "
            "date for the country's first general election since 2011 independence, after five prior "
            "postponements (2018, 2021, 2023, 2024, and an earlier 2026 target). First Vice President "
            "Riek Machar remains suspended and on trial, and Second VP Benjamin Bol Mel was dismissed "
            "in November 2025 -- both signal continued elite instability heading into the vote."
        ),
        'sources': [
            ('Wikipedia — 2026 South Sudanese general election', 'https://en.wikipedia.org/wiki/2026_South_Sudanese_general_election'),
        ],
    }],
    'EGY': [{
        'date': '2026-12-15',
        'category': 'IMF Review',
        'event': 'EFF/RSF arrangement scheduled expiration — eighth/final review due',
        'detail': (
            "Egypt's 46-month, $8bn Extended Fund Facility (approved December 2022) was formally "
            "extended through December 15, 2026 when the IMF Executive Board completed the fifth and "
            "sixth combined reviews in February 2026. The seventh review was completed July 30, 2026 "
            "(unlocking ~$1.8bn); an eighth/closing review is expected before the program's scheduled "
            "expiration, timing not yet announced as of this review."
        ),
        'sources': [
            ('IMF — Executive Board Completes the Fifth and Sixth Reviews (Feb 26, 2026)', 'https://www.imf.org/en/news/articles/2026/02/26/pr-26064-egypt-imf-completes-5th-and-6th-revs-under-ext-arrange-under-eff-and-1st-rev-under-rsa'),
            ('IMF — Executive Board Completes the Seventh Review (Jul 30, 2026)', 'https://www.imf.org/en/news/articles/2026/07/30/pr26271-egypt-imf-completes-the-7th-review-under-eff-and-2nd-review-under-the-rsf'),
        ],
    }],
    'JOR': [{
        'date': '2026 Q4 (on or after Nov 1, 2026)',
        'category': 'IMF Review',
        'event': 'Sixth EFF/RSF review',
        'detail': (
            "Jordan's own IMF program design document sets the sixth review of the Extended Fund "
            "Facility/Resilience and Sustainability Facility arrangement as expected 'on or after "
            "November 1, 2026' (the fifth review, targeted for 'on or after May 1, 2026,' was actually "
            "completed June 17, 2026 -- program reviews have run slightly behind their own schedule)."
        ),
        'sources': [
            ('IMF eLibrary — Jordan program document (fifth/sixth review timing)', 'https://www.elibrary.imf.org/downloadpdf/view/journals/002/2025/338/002.2025.issue-338-en.pdf'),
            ('IMF — Executive Board Completes Fifth Review (Jun 17, 2026)', 'https://www.imf.org/en/news/articles/2026/06/17/pr26211-jordan-imf-completes-5th-review-under-eff-and-2nd-review-under-rsf-arrangements'),
        ],
    }],
    'PAK': [{
        'date': '2026-09 (exact dates unconfirmed)',
        'category': 'IMF Review',
        'event': 'Fourth EFF review / third RSF review mission',
        'detail': (
            "An IMF mission is expected in Pakistan in September 2026 to open discussions on the "
            "fourth review of the $7bn Extended Fund Facility and the third review of the $1.4bn "
            "Resilience and Sustainability Facility, per Pakistani press reporting; the Fund had not "
            "confirmed exact mission dates as of this review."
        ),
        'sources': [
            ('Arab News Pakistan — IMF mission expected in Pakistan in September for loan program reviews', 'https://www.arabnews.pk/node/2656146/pakistan'),
        ],
    }],
    'LKA': [{
        'date': 'TBA (pending, per IMF)',
        'category': 'IMF Review',
        'event': 'Seventh (expected final) EFF review',
        'detail': (
            "Sri Lanka's combined fifth and sixth EFF reviews were completed May 27, 2026. The IMF's "
            "own end-of-visit statement (June 30, 2026) confirms a seventh review is next but says "
            "mission dates 'will be announced in due course' -- i.e. genuinely pending, not yet fixed."
        ),
        'sources': [
            ('IMF — Executive Board Completes the Combined Fifth and Sixth Reviews (May 27, 2026)', 'https://www.imf.org/en/news/articles/2026/05/27/pr26172-sri-lanka-imf-completes-combined-5th-and-6th-reviews-under-eff'),
            ('IMF — Staff Concludes Visit to Sri Lanka (Jun 30, 2026)', 'https://www.imf.org/en/news/articles/2026/06/30/pr26229-sri-lanka-imf-staff-concludes-visit'),
        ],
    }],
    'BGD': [{
        'date': 'TBA (pending government follow-through)',
        'category': 'IMF Review',
        'event': 'Fifth combined ECF/EFF/RSF review',
        'detail': (
            "The IMF's own 2025 Article IV report states discussions on the fifth review 'are "
            "expected to resume following the formation of the new government' -- the BNP-led "
            "government that took office in February 2026 after the post-Yunus-interim election. No "
            "mission date has been confirmed as of this review."
        ),
        'sources': [
            ('IMF eLibrary — Bangladesh 2025 Article IV Consultation', 'https://www.elibrary.imf.org/view/journals/002/2026/024/article-A001-en.xml'),
        ],
    }],
    'LBN': [{
        'date': '2028 (window: May 1-10)',
        'category': 'Political Transition',
        'event': 'Parliamentary elections postponed from 2026 to 2028',
        'detail': (
            "Lebanon's parliamentary elections, originally due in May 2026, were postponed by two "
            "years: President Aoun and the Interior Minister had set May 1-10, 2026 by decree, but "
            "Parliament then voted in March 2026 to extend its own mandate by two years, citing the "
            "2026 Lebanon war and the need to prepare for a 'post-war' vote. The postponement itself "
            "is a live governance-risk signal worth tracking, independent of the eventual date."
        ),
        'sources': [
            ('Wikipedia — 2028 Lebanese general election', 'https://en.wikipedia.org/wiki/2028_Lebanese_general_election'),
            ("L'Orient Today — Parliament extends its mandate by two years", 'https://today.lorientlejour.com/article/1498203/parliament-extends-its-mandate-by-two-years.html'),
        ],
    }],
    'KWT': [{
        'date': 'By mid-2028',
        'category': 'Political Transition',
        'event': "Nominal cap on the National Assembly's suspension",
        'detail': (
            "The Emir's May 2024 dissolution of the National Assembly and suspension of related "
            "constitutional articles is capped, per the Emir's own decree, at up to four years -- "
            "i.e. a potential return to parliamentary politics (or a further extension) by mid-2028. "
            "No elections have been held since 2024 and none are confirmed before that horizon."
        ),
        'sources': [
            ("Carnegie Endowment — Will Kuwait's Parliamentary Democracy Be Restored, Reformed, or Repudiated?", 'https://carnegieendowment.org/research/2025/03/kuwaits-parliament-suspension-emir-democracy?lang=en'),
        ],
    }],
    'PSE': [{
        'date': 'Tentatively 2027',
        'category': 'Political Transition',
        'event': "Gaza technocratic administration (NCAG) handover to the Palestinian Authority",
        'detail': (
            "Under the US-brokered 20-point Gaza peace framework (UN Security Council Resolution "
            "2803), the National Committee for the Administration of Gaza is meant to hand over to "
            "the Palestinian Authority 'tentatively in 2027' -- but as of mid-2026 NCAG members had "
            "reportedly not been allowed to physically enter Gaza and Hamas had not committed to "
            "disarmament, so the timeline is explicitly provisional, not confirmed."
        ),
        'sources': [
            ('House of Commons Library — Gaza 2026: Board of Peace and National Transitional Committee', 'https://commonslibrary.parliament.uk/research-briefings/cbp-10492/'),
            ('CFR — A Guide to the Gaza Peace Deal', 'https://www.cfr.org/articles/guide-trumps-twenty-point-gaza-peace-deal'),
        ],
    }],
    'TUR': [{
        'date': '2028',
        'category': 'Election',
        'event': 'Next scheduled presidential/parliamentary election',
        'detail': (
            "Erdogan is constitutionally in his final term under the current two-term limit, with "
            "the next election due in 2028. The ruling AKP and its MHP ally have floated a "
            "constitutional amendment to permit a further term but currently lack the parliamentary "
            "supermajority to pass one without opposition votes -- making whether that changes the "
            "actual near-term political catalyst to watch before the scheduled vote itself."
        ),
        'sources': [],
    }],
}
