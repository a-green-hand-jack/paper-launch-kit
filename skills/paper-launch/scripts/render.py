#!/usr/bin/env python3
"""Render a local HTML file to PNG(s) or PDF with headless Chromium (Playwright). Free, offline.

Examples
  # one screenshot of the viewport (e.g. og image 1200x630)
  render.py og.html og.png --width 1200 --height 630
  # full-page screenshot (website preview, phone width)
  render.py index.html preview.png --width 390 --full-page
  # every element matching a selector -> out_dir/01.png, 02.png ... (xiaohongshu cards)
  render.py cards.html cards/ --selector .card --width 1080
  # print-size PDF (poster)
  render.py poster.html poster.pdf --pdf --width-in 48 --height-in 36
  # poster preview PNG scaled to a given pixel width
  render.py poster.html poster.png --poster-in 48x36 --width-px 2400

Setup: pip install playwright && playwright install chromium
"""
import argparse
import sys
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("html")
    ap.add_argument("out")
    ap.add_argument("--width", type=int, default=1280, help="viewport width in CSS px")
    ap.add_argument("--height", type=int, default=800, help="viewport height in CSS px")
    ap.add_argument("--scale", type=float, default=1.0, help="device scale factor")
    ap.add_argument("--full-page", action="store_true")
    ap.add_argument("--selector", help="screenshot each matching element into OUT directory")
    ap.add_argument("--pdf", action="store_true", help="print to PDF")
    ap.add_argument("--width-in", type=float, help="PDF page width in inches")
    ap.add_argument("--height-in", type=float, help="PDF page height in inches")
    ap.add_argument("--poster-in", help="WxH inches, render the poster page to PNG")
    ap.add_argument("--width-px", type=int, default=2400, help="target PNG width for --poster-in")
    ap.add_argument("--wait", type=int, default=400, help="ms to wait after load (fonts/images)")
    a = ap.parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit("playwright missing: pip install playwright && playwright install chromium")

    src = Path(a.html).resolve()
    if not src.exists():
        sys.exit(f"not found: {src}")
    url = src.as_uri()
    out = Path(a.out)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        if a.poster_in:
            w_in, h_in = (float(x) for x in a.poster_in.lower().split("x"))
            vw, vh = int(w_in * 96), int(h_in * 96)
            page = browser.new_page(viewport={"width": vw, "height": vh},
                                    device_scale_factor=a.width_px / vw)
        else:
            page = browser.new_page(viewport={"width": a.width, "height": a.height},
                                    device_scale_factor=a.scale)
        page.goto(url, wait_until="networkidle")
        page.evaluate("document.fonts && document.fonts.ready")
        page.wait_for_timeout(a.wait)

        broken = page.evaluate(
            "[...document.images].filter(i => !i.complete || i.naturalWidth === 0).map(i => i.getAttribute('src'))")
        if broken:
            print(f"WARN missing/broken images: {broken}", file=sys.stderr)
        leftovers = page.evaluate("document.body.innerText.includes('{{')")
        if leftovers:
            print("WARN page still contains '{{' placeholders", file=sys.stderr)

        if a.pdf:
            if not (a.width_in and a.height_in):
                sys.exit("--pdf needs --width-in and --height-in")
            page.set_viewport_size({"width": int(a.width_in * 96), "height": int(a.height_in * 96)})
            out.parent.mkdir(parents=True, exist_ok=True)
            page.pdf(path=str(out), width=f"{a.width_in}in", height=f"{a.height_in}in",
                     print_background=True, margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
                     page_ranges="1")
            print(f"wrote {out}")
        elif a.selector:
            out.mkdir(parents=True, exist_ok=True)
            els = page.query_selector_all(a.selector)
            if not els:
                sys.exit(f"no elements match {a.selector}")
            for i, el in enumerate(els, 1):
                # report overflow: content taller/wider than the card gets clipped silently
                over = el.evaluate("e => [...e.querySelectorAll('*')].some(c => { const r=c.getBoundingClientRect(), b=e.getBoundingClientRect(); return r.bottom > b.bottom + 1 || r.right > b.right + 1; })")
                path = out / f"{i:02d}.png"
                el.screenshot(path=str(path))
                print(f"wrote {path}" + ("   WARN content overflows this card" if over else ""))
        elif a.poster_in:
            out.parent.mkdir(parents=True, exist_ok=True)
            page.screenshot(path=str(out), full_page=False)
            print(f"wrote {out}")
        else:
            out.parent.mkdir(parents=True, exist_ok=True)
            page.screenshot(path=str(out), full_page=a.full_page)
            sw = page.evaluate("document.documentElement.scrollWidth")
            if sw > a.width + 1:
                print(f"WARN horizontal overflow: page is {sw}px wide at viewport {a.width}px", file=sys.stderr)
            print(f"wrote {out}")
        browser.close()


if __name__ == "__main__":
    main()
