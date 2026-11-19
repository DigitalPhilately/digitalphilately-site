"""Builds index.html from a template so the inline mark stays in step with mark.svg."""
import html as _html
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent
MARK = (ROOT / "mark.svg").read_text().replace('width="64" height="56"', 'width="40" height="35"').replace('fill="#161A23"', 'fill="currentColor"').replace('stroke="#161A23"', 'stroke="currentColor"')

AREAS = [
    ("identify", "Digital identification",
     "Scanning stamps, recognising designs and decoding barcodes. Software can now tell you which stamp you are holding, sometimes faster than a catalogue can.",
     [("Stamp Decoder", "https://stampdecoder.app/", "scan a Royal Mail barcoded stamp and see, in plain collector terms, exactly which stamp it is")]),
    ("collections", "Digital collections",
     "Virtual albums, collection databases and records of individual stamps, so a collection can be searched, valued and passed on.",
     []),
    ("research", "Philatelic research",
     "Online catalogues, searchable databases and digitised archives. Research that once needed a society library can now start from a phone.",
     [("Barcoded Stamps", "https://barcodedstamps.com/", "a free reference catalogue of Royal Mail barcoded definitives and Christmas stamps")]),
    ("exhibiting", "Digital exhibiting",
     "Virtual exhibitions, online displays and presentations that let a collection reach people who will never see the album.",
     []),
    ("digital-stamps", "Digital stamps",
     "Stamps issued in digital form, including crypto stamps and NFT stamps. The Universal Postal Union has published a taxonomy for these products and runs a Digital Philately Academy.",
     []),
    ("connected", "Connected collecting",
     "Online communities, shared research and digital marketplaces: the way collectors now find each other, swap knowledge and buy stamps.",
     []),
]


def area_card(slug, title, body, projects):
    proj = ""
    if projects:
        items = "".join(
            f'<li><a href="{url}">{name}</a> &mdash; {desc}</li>' for name, url, desc in projects
        )
        proj = f'<p class="from-us">From Modern GB</p><ul class="projects">{items}</ul>'
    return f'''<article class="area" id="{slug}">
<h3>{title}</h3>
<p>{body}</p>
{proj}</article>'''


# Latest finds teaser: newest finds from the Barcoded Stamps catalogue.
FINDS_SOURCE = ROOT.parent / "modern-gb-stamp-decoder/website/src/content/latest-finds.json"
FINDS_COPY = ROOT / "latest-finds.json"
FINDS_URL = "https://barcodedstamps.com/latest-finds/"
STATUS = {"reported": "Reported", "corroborated": "Corroborated", "catalogued": "Catalogued", "available_in_app": "Available in app"}
if FINDS_SOURCE.exists():
    FINDS_COPY.write_text(FINDS_SOURCE.read_text())
finds = json.loads(FINDS_COPY.read_text())
finds.sort(key=lambda f: f["id"])
finds.sort(key=lambda f: f["publishedAt"], reverse=True)


def nice_date(d):
    y, m, dd = map(int, d.split("-"))
    return date(y, m, dd).strftime("%-d %b %Y")


def find_item(f):
    e = _html.escape
    return (f'<li><a href="{FINDS_URL}#{e(f["id"])}">'
            f'<span class="find-meta"><time datetime="{e(f["publishedAt"])}">{nice_date(f["publishedAt"])}</time> · {e(STATUS.get(f["status"], f["status"]))}</span>'
            f'<strong>{e(f["title"])}</strong>'
            f'<span class="find-detail">{e(f["encodedValue"])} · {e(f["sourceFormat"])}</span></a></li>')


FINDS = "\n".join(find_item(f) for f in finds[:3])


cards = "\n".join(area_card(*a) for a in AREAS)
html = (ROOT / "template.html").read_text().replace("{{MARK}}", MARK).replace("{{AREAS}}", cards).replace("{{FINDS}}", FINDS)
(ROOT / "index.html").write_text(html)
(ROOT / "privacy.html").write_text((ROOT / "privacy.template.html").read_text().replace("{{MARK}}", MARK))
print("index.html written", len(html))
