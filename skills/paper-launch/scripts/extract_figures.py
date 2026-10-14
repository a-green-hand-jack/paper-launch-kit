#!/usr/bin/env python3
"""Collect paper figures as PNGs for promo assets.

  extract_figures.py paper.pdf     launch/assets/figs/
  extract_figures.py latex/figures launch/assets/figs/

PDF input  -> pages/page-NN.png (every page at 200 dpi, crop vector figures from these)
              embedded/  (embedded raster images >= 300 px)
Dir input  -> every figure file (.pdf/.png/.jpg/.jpeg/.svg) converted/copied to PNG (PDF figures at 300 dpi)

Uses PyMuPDF if installed (pip install pymupdf); otherwise falls back to poppler (pdftoppm/pdfimages).
"""
import shutil
import subprocess
import sys
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None


def have(cmd):
    return shutil.which(cmd) is not None


def pdf_pages(pdf: Path, out: Path, dpi=200):
    out.mkdir(parents=True, exist_ok=True)
    if fitz:
        doc = fitz.open(pdf)
        for i, page in enumerate(doc, 1):
            page.get_pixmap(dpi=dpi).save(out / f"page-{i:02d}.png")
        return len(doc)
    if have("pdftoppm"):
        subprocess.run(["pdftoppm", "-r", str(dpi), "-png", str(pdf), str(out / "page")], check=True)
        return len(list(out.glob("page-*.png")))
    sys.exit("need PyMuPDF (pip install pymupdf) or poppler (pdftoppm)")


def pdf_embedded(pdf: Path, out: Path, min_px=300):
    out.mkdir(parents=True, exist_ok=True)
    n = 0
    if fitz:
        doc = fitz.open(pdf)
        seen = set()
        for pno, page in enumerate(doc, 1):
            for img in page.get_images(full=True):
                xref = img[0]
                if xref in seen:
                    continue
                seen.add(xref)
                pix = fitz.Pixmap(doc, xref)
                if pix.width < min_px or pix.height < min_px:
                    continue
                if pix.n - pix.alpha >= 4:
                    pix = fitz.Pixmap(fitz.csRGB, pix)
                n += 1
                pix.save(out / f"p{pno:02d}-img{n:02d}.png")
        return n
    if have("pdfimages"):
        subprocess.run(["pdfimages", "-png", "-p", str(pdf), str(out / "img")], check=True)
        try:
            from PIL import Image
            for f in out.glob("img-*.png"):
                with Image.open(f) as im:
                    small = im.width < min_px or im.height < min_px
                if small:
                    f.unlink()
        except ImportError:
            pass
        return len(list(out.glob("img-*.png")))
    return 0


def single_pdf_to_png(pdf: Path, dst: Path, dpi=300):
    if fitz:
        doc = fitz.open(pdf)
        doc[0].get_pixmap(dpi=dpi, alpha=False).save(dst)
    elif have("pdftoppm"):
        subprocess.run(["pdftoppm", "-r", str(dpi), "-png", "-singlefile", str(pdf), str(dst.with_suffix(""))], check=True)
    else:
        print(f"skip {pdf}: no PDF renderer", file=sys.stderr)


def from_dir(src: Path, out: Path):
    out.mkdir(parents=True, exist_ok=True)
    n = 0
    for f in sorted(src.rglob("*")):
        ext = f.suffix.lower()
        rel = "_".join(f.relative_to(src).with_suffix("").parts)
        if ext == ".pdf":
            single_pdf_to_png(f, out / f"{rel}.png"); n += 1
        elif ext in (".png", ".jpg", ".jpeg"):
            shutil.copy2(f, out / f"{rel}{ext}"); n += 1
        elif ext == ".svg":
            shutil.copy2(f, out / f"{rel}.svg"); n += 1
    return n


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    if src.is_dir():
        print(f"{from_dir(src, out)} figure files -> {out}")
    elif src.suffix.lower() == ".pdf":
        print(f"{pdf_pages(src, out / 'pages')} pages -> {out/'pages'}")
        print(f"{pdf_embedded(src, out / 'embedded')} embedded images -> {out/'embedded'}")
        print("Next: look at the pages, crop teaser/method/result figures into fig-*.png")
    else:
        sys.exit("input must be a PDF or a directory of figures")


if __name__ == "__main__":
    main()
