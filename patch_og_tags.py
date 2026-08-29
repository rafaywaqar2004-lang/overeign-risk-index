"""Injects Open Graph / Twitter Card meta tags, and a branded cold-start
loading screen, into Streamlit's own static index.html at deploy time.

Why this exists: Streamlit is a client-rendered single-page app -- the tab
title/description you set via st.set_page_config only apply after the JS
bundle loads and runs. Link-preview crawlers (LinkedIn, Slack, iMessage,
etc.) don't execute JS; they read the static HTML Streamlit ships as-is,
which has no OG tags and a generic "Streamlit" title. Streamlit Community
Cloud gives no way to touch that shipped file, which is the actual reason
this project moved off it -- self-hosting (Render) runs this script as a
build step, after `pip install`, patching the freshly-installed package's
index.html before the server ever starts.

The loading screen exists for the same "no way to touch the shipped shell"
reason, applied to a different problem: Render's free tier spins the
container down after a few idle minutes, so the first visitor after a
quiet spell hits a genuine ~20-30s cold start. Until Streamlit's own JS
bundle loads, connects its websocket, and runs the Python script, the
browser shows a blank page -- which reads as "broken," not "loading."
This block renders instantly (it's static HTML/CSS, no JS bundle needed)
and removes itself once the real app has actually rendered content.

Idempotent: safe to run on every build. If either managed block is already
present (e.g. a re-run without a fresh install), it's replaced rather than
duplicated.
"""
import os
import re
import streamlit

SITE_URL = os.environ.get("SITE_URL", "https://menasa-risk-monitor.onrender.com")
TITLE = "MENASA Risk Monitor"
DESCRIPTION = (
    "A composite sovereign risk score for 34 MENA, South Asia & Horn of Africa "
    "economies -- live World Bank data, a sourced Live Conflicts tracker, and a "
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

LOADER_BLOCK_START = "<!-- BEGIN cold-start-loader (managed by patch_og_tags.py) -->"
LOADER_BLOCK_END = "<!-- END cold-start-loader -->"

LOADER_BLOCK = f"""{LOADER_BLOCK_START}
  <div id="cold-start-loader" style="
      position: fixed; inset: 0; z-index: 999999;
      background: #0a0a0a; color: #f5f5f4;
      display: flex; flex-direction: column; align-items: center; justify-content: center;
      font-family: -apple-system, 'Inter', 'Segoe UI', sans-serif;
      text-align: center; padding: 1.5rem;
      transition: opacity 0.4s ease;
    ">
    <div style="
        width: 40px; height: 40px; border-radius: 50%;
        border: 3px solid rgba(13,148,136,0.25); border-top-color: #0d9488;
        animation: cold-start-spin 0.9s linear infinite; margin-bottom: 1.5rem;
      "></div>
    <div style="font-size: 1.1rem; font-weight: 600; letter-spacing: 0.02em;">MENASA Risk Monitor</div>
    <div style="font-size: 0.88rem; color: #a3a3a3; margin-top: 0.6rem; max-width: 320px; line-height: 1.5;">
      Waking up the live demo — this free-tier instance sleeps when idle,
      so the first load can take up to 30 seconds.
    </div>
  </div>
  <style>
    @keyframes cold-start-spin {{ to {{ transform: rotate(360deg); }} }}
  </style>
  <script>
    (function() {{
      var startedAt = Date.now();
      var maxWaitMs = 25000;
      var poll = setInterval(function() {{
        var appRoot = document.querySelector('[data-testid="stAppViewContainer"]');
        var hasContent = appRoot && appRoot.innerText && appRoot.innerText.trim().length > 0;
        if (hasContent || Date.now() - startedAt > maxWaitMs) {{
          clearInterval(poll);
          var loader = document.getElementById('cold-start-loader');
          if (loader) {{
            loader.style.opacity = '0';
            setTimeout(function() {{ loader.remove(); }}, 400);
          }}
        }}
      }}, 250);
    }})();
  </script>
  {LOADER_BLOCK_END}"""


def main():
    index_path = os.path.join(os.path.dirname(streamlit.__file__), "static", "index.html")
    with open(index_path, encoding="utf-8") as f:
        html = f.read()

    # Remove any previously-injected blocks first, so re-running this script
    # (e.g. a redeploy without a clean install) replaces rather than duplicates.
    for start, end in [(OG_BLOCK_START, OG_BLOCK_END), (LOADER_BLOCK_START, LOADER_BLOCK_END)]:
        html = re.sub(re.escape(start) + r".*?" + re.escape(end), "", html, flags=re.DOTALL)

    html = html.replace("<title>Streamlit</title>", f"<title>{TITLE}</title>")
    html = html.replace("</head>", OG_BLOCK + "\n  </head>")
    html = html.replace("</body>", LOADER_BLOCK + "\n</body>")

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Patched OG tags and cold-start loader into {index_path}")


if __name__ == "__main__":
    main()
