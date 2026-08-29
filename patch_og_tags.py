"""Injects Open Graph / Twitter Card meta tags into Streamlit's own static
index.html at deploy time.

Why this exists: Streamlit is a client-rendered single-page app -- the tab
title/description you set via st.set_page_config only apply after the JS
bundle loads and runs. Link-preview crawlers (LinkedIn, Slack, iMessage,
etc.) don't execute JS; they read the static HTML Streamlit ships as-is,
which has no OG tags and a generic "Streamlit" title. Streamlit Community
Cloud gives no way to touch that shipped file, which is the actual reason
this project moved off it -- self-hosting (Render) runs this script as a
build step, after `pip install`, patching the freshly-installed package's
index.html before the server ever starts.

Idempotent: safe to run on every build. If the OG block is already present
(e.g. a re-run without a fresh install), it's replaced rather than duplicated.
"""
import os
import re
import streamlit

SITE_URL = os.environ.get("SITE_URL", "https://menasa-risk-monitor.onrender.com")
TITLE = "MENASA Risk Monitor"
DESCRIPTION = (
    "A composite sovereign risk score for 27 MENA & South Asia economies -- "
    "live World Bank data, a sourced Live Conflicts tracker, and a "
    "Geo-Economic Interdependence Dashboard."
)
IMAGE_URL = f"{SITE_URL}/app/static/og-image.png"

OG_BLOCK_START = "<!-- BEGIN og-tags (managed by patch_og_tags.py) -->"
OG_BLOCK_END = "<!-- END og-tags -->"

OG_BLOCK = f"""{OG_BLOCK_START}
    <meta name="description" content="{DESCRIPTION}" />
    <meta property="og:type" content="website" />
    <meta property="og:title" content="{TITLE}" />
    <meta property="og:description" content="{DESCRIPTION}" />
    <meta property="og:image" content="{IMAGE_URL}" />
    <meta property="og:url" content="{SITE_URL}" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{TITLE}" />
    <meta name="twitter:description" content="{DESCRIPTION}" />
    <meta name="twitter:image" content="{IMAGE_URL}" />
    {OG_BLOCK_END}"""


def main():
    index_path = os.path.join(os.path.dirname(streamlit.__file__), "static", "index.html")
    with open(index_path, encoding="utf-8") as f:
        html = f.read()

    # Remove any previously-injected block first, so re-running this script
    # (e.g. a redeploy without a clean install) replaces rather than duplicates.
    html = re.sub(
        re.escape(OG_BLOCK_START) + r".*?" + re.escape(OG_BLOCK_END),
        "",
        html,
        flags=re.DOTALL,
    )

    html = html.replace("<title>Streamlit</title>", f"<title>{TITLE}</title>")
    html = html.replace("</head>", OG_BLOCK + "\n  </head>")

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Patched OG tags into {index_path}")


if __name__ == "__main__":
    main()
