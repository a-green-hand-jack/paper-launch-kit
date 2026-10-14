#!/usr/bin/env python3
"""Validate an X thread draft (launch/x/thread.md).

Format: tweets separated by a line containing only '---'.
Images:  <!-- img: img/01.png | alt: description -->   (max 4 per tweet)
Other HTML comments are ignored (use them for alternative hooks/notes).

Checks: weighted length <= 280 (twitter-text rules: CJK/emoji = 2, URL = 23),
image files exist, links not in the first tweet, hype words to verify.
Exit code 1 if any ERROR.
"""
import re
import sys
from pathlib import Path

LIMIT = 280
URL_RE = re.compile(r"https?://\S+")
IMG_RE = re.compile(r"<!--\s*img:\s*([^|>]+?)\s*(?:\|\s*alt:\s*(.*?))?\s*-->", re.S)
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
HYPE = ["sota", "state-of-the-art", "state of the art", "revolution", "game-chang", "groundbreaking",
        "first ever", "the first", "unprecedented", "best ever", "crush"]

# twitter-text v3: these ranges weigh 1, everything else 2
LIGHT = [(0, 4351), (8192, 8205), (8208, 8223), (8242, 8247)]


def is_emoji(cp):
    return (0x1F000 <= cp <= 0x1FAFF) or (0x2600 <= cp <= 0x27BF) or (0x2B00 <= cp <= 0x2BFF)


def weighted_len(text):
    n = 0
    for u in URL_RE.findall(text):
        n += 23
    text = URL_RE.sub("", text)
    chars = list(text)
    i = 0
    while i < len(chars):
        cp = ord(chars[i])
        if is_emoji(cp):
            n += 2
            i += 1
            # swallow modifiers / ZWJ sequences belonging to this emoji
            while i < len(chars):
                c = ord(chars[i])
                if c in (0xFE0F, 0x20E3) or 0x1F3FB <= c <= 0x1F3FF:
                    i += 1
                elif c == 0x200D and i + 1 < len(chars):
                    i += 2
                else:
                    break
            continue
        if cp in (0xFE0F, 0x200D):
            i += 1
            continue
        n += 1 if any(a <= cp <= b for a, b in LIGHT) else 2
        i += 1
    return n


def parse(path: Path):
    raw = path.read_text(encoding="utf-8")
    blocks = re.split(r"^\s*---\s*$", raw, flags=re.M)
    tweets = []
    for b in blocks:
        imgs = [(m.group(1).strip(), (m.group(2) or "").strip()) for m in IMG_RE.finditer(b)]
        text = COMMENT_RE.sub("", b).strip()
        if text or imgs:
            tweets.append({"text": text, "imgs": imgs})
    return tweets


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    path = Path(sys.argv[1])
    tweets = parse(path)
    errors = 0
    print(f"{len(tweets)} tweets in {path}")
    for i, t in enumerate(tweets, 1):
        n = weighted_len(t["text"])
        flags = []
        if n > LIMIT:
            flags.append(f"ERROR {n}/{LIMIT} chars"); errors += 1
        if not t["text"]:
            flags.append("ERROR empty text"); errors += 1
        if len(t["imgs"]) > 4:
            flags.append("ERROR more than 4 images"); errors += 1
        for img, alt in t["imgs"]:
            if not (path.parent / img).exists():
                flags.append(f"ERROR missing image {img}"); errors += 1
            if not alt:
                flags.append(f"WARN no alt text for {img}")
        if i == 1 and URL_RE.search(t["text"]):
            flags.append("WARN link in first tweet (convention: links in the last tweet)")
        if i == 1 and not t["imgs"]:
            flags.append("WARN first tweet has no image/video")
        low = t["text"].lower()
        for h in HYPE:
            if h in low:
                flags.append(f"WARN '{h}' — verify it is supported by brief.md")
        print(f"[{i:02d}] {n:3d} chars, {len(t['imgs'])} img  " + ("; ".join(flags) if flags else "ok"))
    if errors:
        print(f"{errors} error(s)")
        sys.exit(1)
    print("all good")


if __name__ == "__main__":
    main()
