"""
Generates a downloadable one-page-plus country risk brief as a PDF,
pulling together the same data shown in the Country Deep Dive tab into a
format suitable for printing, emailing, or attaching to an application.
"""
import re
from datetime import datetime, timezone
from fpdf import FPDF

NAVY = (13, 27, 42)
GOLD = (201, 168, 76)
TEXT_DARK = (30, 30, 30)
TEXT_MUTED = (100, 100, 100)


_UNICODE_REPLACEMENTS = {
    "—": "-", "–": "-",   # em dash, en dash
    "‘": "'", "’": "'",   # curly single quotes
    "“": '"', "”": '"',   # curly double quotes
    "…": "...",                 # ellipsis
    "→": "->", "←": "<-",  # arrows
    "↑": "^", "↓": "v",
    "▲": "^", "▼": "v",   # triangle up/down (used for YoY arrows)
    "•": "-",                   # bullet
    "·": "-",                   # middle dot
}


def sanitize_text(text):
    """Replaces Unicode characters outside Latin-1 (the core PDF font's range)
    with ASCII-safe equivalents, so the PDF never fails to render."""
    if text is None:
        return ""
    for char, replacement in _UNICODE_REPLACEMENTS.items():
        text = text.replace(char, replacement)
    # Catch-all: drop any remaining character the latin-1 codec can't handle
    return text.encode("latin-1", errors="replace").decode("latin-1")


def _strip_html(text):
    """Removes simple HTML tags (b, br, etc.) so narrative text renders as plain text in the PDF."""
    text = re.sub(r"<br\s*/?>", "\n", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = text.replace("&amp;", "&").replace("&nbsp;", " ")
    return sanitize_text(text)


class CountryBriefPDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*TEXT_MUTED)
        self.cell(0, 8, "Sovereign Risk Scorecard - Country Brief", align="L")
        self.cell(0, 8, f"Page {self.page_no()}", align="R", new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*TEXT_MUTED)
        self.cell(0, 10, "Research/screening tool - not investment advice. Not a live feed; see in-app Methodology for sourcing details.", align="C")

    def section_title(self, text):
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(*NAVY)
        self.cell(0, 8, sanitize_text(text), new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*GOLD)
        self.set_line_width(0.6)
        y = self.get_y()
        self.line(self.l_margin, y, self.l_margin + 30, y)
        self.ln(4)

    def body_text(self, text, size=9.5):
        self.set_font("Helvetica", "", size)
        self.set_text_color(*TEXT_DARK)
        self.multi_cell(0, 5.2, sanitize_text(text))
        self.ln(1)

    def simple_table(self, rows, col_widths=None):
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*TEXT_DARK)
        if col_widths is None:
            col_widths = [45, 135]
        for row in rows:
            y_before = self.get_y()
            x_before = self.get_x()
            self.set_font("Helvetica", "B", 9)
            self.multi_cell(col_widths[0], 5, sanitize_text(str(row[0])), new_x="RIGHT", new_y="TOP")
            y_after_label = self.get_y()
            self.set_xy(x_before + col_widths[0], y_before)
            self.set_font("Helvetica", "", 9)
            self.multi_cell(col_widths[1], 5, sanitize_text(str(row[1])), new_x="LMARGIN", new_y="NEXT")
            y_after_value = self.get_y()
            self.set_y(max(y_after_label, y_after_value))
        self.ln(2)


def generate_country_pdf(
    country_name, country_code, row, brief_text, ratings,
    trade_profile, events, arrangements, partner_info, last_refreshed
):
    pdf = CountryBriefPDF(format="A4")
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()

    # ---- Masthead ----
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(*NAVY)
    pdf.cell(0, 12, "Sovereign Risk Brief", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "B", 15)
    pdf.set_text_color(*GOLD)
    pdf.cell(0, 9, sanitize_text(country_name), new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 8.5)
    pdf.set_text_color(*TEXT_MUTED)
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    pdf.cell(0, 6, sanitize_text(f"Generated {generated} | Data last refreshed {last_refreshed} | MENASA Sovereign Risk Scorecard"), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    # ---- Score summary ----
    pdf.section_title("Composite Risk Score")
    score_display = f"{row['risk_score']:.1f} / 100" if row.get("risk_score") == row.get("risk_score") else "N/A"
    summary_rows = [
        ["Score", score_display],
        ["Risk Tier", str(row.get("risk_tier", "N/A"))],
        ["Regional Rank", f"{int(row['risk_rank'])} of 26" if row.get("risk_rank") == row.get("risk_rank") else "N/A"],
        ["Factors Used", f"{int(row.get('risk_score_factors_used', 0))} of 10"],
    ]
    if row.get("yoy_change") == row.get("yoy_change"):
        direction = "worsening" if row["yoy_change"] > 0 else "improving"
        summary_rows.append(["YoY Change", f"{row['yoy_change']:+.1f} ({direction})"])
    pdf.simple_table(summary_rows)

    if ratings:
        pdf.section_title("Actual Credit Ratings (S&P / Moody's / Fitch)")
        pdf.simple_table([
            ["S&P", ratings["sp"]],
            ["Moody's", ratings["moodys"]],
            ["Fitch", ratings["fitch"]],
        ])

    # ---- Country brief narrative ----
    pdf.section_title("Analyst Brief")
    pdf.body_text(_strip_html(brief_text))

    # ---- Trade profile ----
    if trade_profile:
        pdf.section_title("Key Sectors & Trade Profile")
        pdf.simple_table([
            ["Main Sectors", trade_profile["sectors"]],
            ["Biggest Exports", trade_profile["exports"]],
            ["Biggest Imports", trade_profile["imports"]],
            ["Leading Partners", trade_profile["partners"]],
        ])

    # ---- Financing arrangements ----
    if arrangements:
        pdf.section_title("Financing Arrangements")
        for a in arrangements:
            pdf.simple_table([
                ["Program", a["program"]],
                ["Amount", a["amount"]],
                ["Approved", a["approved"]],
                ["Status", a["status"]],
            ])

    # ---- Key economic partners ----
    if partner_info:
        pdf.section_title("Key Economic Partners")
        pdf.body_text(partner_info["summary"])

    # ---- Historical context ----
    if events:
        pdf.section_title("Key Historical Context")
        for year, event, source_name, source_url in sorted(events, key=lambda e: e[0]):
            pdf.set_font("Helvetica", "B", 9)
            pdf.set_text_color(*NAVY)
            pdf.write(5, f"{year}: ")
            pdf.set_font("Helvetica", "", 9)
            pdf.set_text_color(*TEXT_DARK)
            pdf.write(5, sanitize_text(f"{event} "))
            pdf.set_font("Helvetica", "I", 7.5)
            pdf.set_text_color(*TEXT_MUTED)
            pdf.write(5, sanitize_text(f"[{source_name}]"))
            pdf.ln(7)

    return bytes(pdf.output())
