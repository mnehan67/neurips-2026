#!/usr/bin/env python3
"""Check that relative website assets exist in the repository root."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / "index.html"

class Assets(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        for k in ("src", "href"):
            if k in a: self.links.append((tag,k,a[k]))

parser=Assets(); parser.feed(SITE.read_text(encoding="utf-8"))
missing=[]; checked=[]
for tag,k,link in parser.links:
    url=urlsplit(link)
    if url.scheme or url.netloc or not url.path or link.startswith('#'): continue
    relative=Path(unquote(url.path).lstrip('/'))
    candidate=(ROOT / relative).resolve()
    if not candidate.is_relative_to(ROOT.resolve()) or not candidate.is_file():
        missing.append((tag,k,link))
    else:checked.append(relative.as_posix())
if missing:raise SystemExit(f"Missing website assets: {missing}")
print(f"Website asset check: PASS ({len(checked)} local file references)")
