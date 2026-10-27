#!/usr/bin/env python3
"""Builds the C&F Solutions site from content/ into the repo root.

Run: python3 -I build.py
"""
import base64
import hashlib
import html
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
CONTENT = ROOT / "content"
SITE = json.loads((CONTENT / "site.json").read_text())
CONTACT = SITE["contact"]
SITE_URL = "https://c-fsolutions.github.io"
YEAR = 2026

PAGES = [("privacy", "Privacy Policy"), ("terms", "Terms of Use")]

ENCODED = base64.b64encode(CONTACT[::-1].encode()).decode()
FALLBACK = CONTACT.replace("@", " (at) ").replace(".", " (dot) ")
UNHIDE = ('<script>for(const a of document.querySelectorAll("a[data-e]")){const m=atob(a.dataset.e).split("").reverse().join("");'
          'a.href="mailto:"+m;if(a.hasAttribute("data-show"))a.textContent=m}</script>')

e = html.escape


def asset_version(name):
    return hashlib.sha256((ROOT / name).read_bytes()).hexdigest()[:8]


def asset(name):
    return f"/assets/{name}?v={asset_version(f'assets/{name}')}"


def email_link(label=None, cls=""):
    # Scrapers read raw HTML; the address only exists once the inline script rebuilds the link.
    class_attr = f' class="{cls}"' if cls else ""
    if label:
        return f'<a{class_attr} href="#" data-e="{ENCODED}">{label}</a>'
    return f'<a{class_attr} href="#" data-e="{ENCODED}" data-show>{e(FALLBACK)}</a>'


def head(title, description, path):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#011b45">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<link rel="canonical" href="{SITE_URL}{path}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{e(SITE["legalName"])}">
<meta property="og:url" content="{SITE_URL}{path}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:image" content="{SITE_URL}{asset("og.jpg")}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico?v={asset_version("favicon.ico")}" sizes="48x48">
<link rel="apple-touch-icon" href="{asset("apple-touch-icon.png")}">
<link rel="stylesheet" href="{asset("site.css")}">
</head>
<body>
"""


def hero(small=False):
    cls = "hero small" if small else "hero"
    return f"""  <header class="{cls}">
    <a href="/" class="logo"><img src="{asset("logo.webp")}" alt="{e(SITE["legalName"])}" width="900" height="593"></a>
  </header>
"""


def footer():
    links = " · ".join(f'<a href="/{slug}/">{title}</a>' for slug, title in PAGES)
    return f"""
  <footer>
    <p>{links} · {email_link("Contact")}</p>
    <p class="fine">© {YEAR} {e(SITE["legalName"])}</p>
  </footer>
{UNHIDE}
</body>
</html>
"""


def home():
    products = "".join(f"""
      <a class="product" href="{e(p["url"])}">
        <img src="{asset(p["icon"])}" alt="" width="64" height="64">
        <span><strong>{e(p["name"])}</strong><span>{e(p["summary"])}</span></span>
      </a>""" for p in SITE["products"])
    return head(SITE["legalName"], SITE["tagline"], "/") + hero() + f"""
  <main>
    <p class="tagline">{e(SITE["tagline"])}</p>

    <section class="card">
      <h2>About</h2>
      <p>{e(SITE["about"])}</p>
    </section>

    <section class="card">
      <h2>Products</h2>{products}
    </section>

    <section class="card">
      <h2>Contact</h2>
      <p>{email_link()}</p>
    </section>
  </main>
""" + footer()


def legal_page(slug, title):
    pyllar = SITE["products"][0]
    body = (CONTENT / f"{slug}.html").read_text().rstrip("\n").format(
        email=email_link(), legal_name=e(SITE["legalName"]),
        pyllar_privacy=e(pyllar["privacy"]), pyllar_terms=e(pyllar["terms"]))
    body = "\n".join(("      " + line) if line else "" for line in body.split("\n"))
    return head(f'{title} — {SITE["legalName"]}', f'{title} for the {SITE["legalName"]} website.', f"/{slug}/") + \
        hero(small=True) + f"""
  <main>
    <section class="card">
      <h1>{title}</h1>
      <p class="fine">Effective {e(SITE["effective"])}</p>
{body}
    </section>
  </main>
""" + footer()


def not_found():
    return head(f'Page not found — {SITE["legalName"]}', "Page not found.", "/404.html") + hero(small=True) + """
  <main>
    <section class="card">
      <h1>Not here</h1>
      <p>That page doesn't exist. <a href="/">Back to the home page</a>.</p>
    </section>
  </main>
""" + footer()


def write(path, text):
    assert CONTACT not in text, f"contact address left in plain text in {path}"
    path = ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def main():
    write("index.html", home())
    write("404.html", not_found())
    for slug, title in PAGES:
        write(f"{slug}/index.html", legal_page(slug, title))
    print(f"Built home, 404 and {len(PAGES)} legal pages.")


if __name__ == "__main__":
    main()
