#!/usr/bin/env python3
"""Make a QR code PNG (free, offline).

  make_qr.py https://user.github.io/project/ launch/poster/qr.png

Setup: pip install "qrcode[pil]"
"""
import sys

if len(sys.argv) != 3:
    sys.exit(__doc__)
try:
    import qrcode
except ImportError:
    sys.exit('missing dependency: pip install "qrcode[pil]"')

qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=20, border=2)
qr.add_data(sys.argv[1])
qr.make(fit=True)
qr.make_image(fill_color="black", back_color="white").save(sys.argv[2])
print(f"wrote {sys.argv[2]}")
