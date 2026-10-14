#!/usr/bin/env python3
"""Validate a Xiaohongshu draft folder (launch/xhs/): note.md + cards/*.png

note.md sections: '# 标题', '# 正文', '# 话题' (HTML comments ignored).
Checks: title <= 20 chars, body <= 1000 chars, 5-10 topics, no links / contact info /
off-platform redirects, ad-law superlatives, card images exist and are 3:4.
Exit code 1 if any ERROR.
"""
import re
import sys
from pathlib import Path

COMMENT_RE = re.compile(r"<!--.*?-->", re.S)

# ERROR: very likely to be throttled
BLOCK = [
    (r"https?://|www\.|\.com\b|\.io\b|\.org\b|arxiv\.org|github\.com", "外部链接（改为写论文名/arXiv编号/“GitHub 搜 xxx”）"),
    (r"微信|vx|v信|wx[:：]|加我|私信领取|私信我|扣\s*1|评论区扣|二维码|QQ群|qq群|公众号", "导流/联系方式"),
    (r"[\w.+-]+@[\w-]+\.[\w.]+", "邮箱"),
    (r"B站|b站|抖音|知乎|去推特|去 ?X ?看", "引导到其他平台"),
]
# WARN: ad-law style superlatives; academic claims must be rephrased and supported by brief
WARN = ["最强", "最好", "最佳", "第一", "首个", "首次", "唯一", "顶级", "国家级", "全网", "史上", "绝对", "100%", "碾压", "吊打", "遥遥领先"]


def sections(text):
    text = COMMENT_RE.sub("", text)
    out, cur = {}, None
    for line in text.splitlines():
        m = re.match(r"^#\s*(标题|正文|话题)\s*$", line.strip())
        if m:
            cur = m.group(1); out[cur] = []
        elif cur:
            out[cur].append(line)
    return {k: "\n".join(v).strip() for k, v in out.items()}


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    d = Path(sys.argv[1])
    note = d / "note.md"
    if not note.exists():
        sys.exit(f"missing {note}")
    s = sections(note.read_text(encoding="utf-8"))
    errs, warns = [], []

    title, body, tags = s.get("标题", ""), s.get("正文", ""), s.get("话题", "")
    if not title: errs.append("缺少标题")
    if len(title) > 20: errs.append(f"标题 {len(title)} 字 > 20")
    if not body: errs.append("缺少正文")
    if len(body) > 1000: errs.append(f"正文 {len(body)} 字 > 1000")
    elif len(body) < 150: warns.append(f"正文只有 {len(body)} 字，偏短")
    topics = re.findall(r"#[^\s#]+", tags + "\n" + body)
    if not (5 <= len(topics) <= 10): warns.append(f"话题 {len(topics)} 个（建议 5–10）")

    full = f"{title}\n{body}\n{tags}"
    for pat, why in BLOCK:
        for m in re.finditer(pat, full, flags=re.I):
            errs.append(f"{why}: “{m.group(0)}”")
    for w in WARN:
        if w in full:
            warns.append(f"极限词“{w}”：确认 brief 支持，否则改写")

    cards = sorted((d / "cards").glob("*.png")) if (d / "cards").exists() else []
    if not cards:
        errs.append("cards/ 下没有图片")
    else:
        try:
            from PIL import Image
            for c in cards:
                with Image.open(c) as im:
                    w, h = im.size
                if abs(w / h - 3 / 4) > 0.01:
                    errs.append(f"{c.name} 比例 {w}x{h} 不是 3:4")
                elif w < 1080:
                    warns.append(f"{c.name} 宽 {w}px < 1080，可能不清晰")
        except ImportError:
            warns.append("未安装 Pillow，跳过图片比例检查")
        if len(cards) > 18: errs.append(f"{len(cards)} 张图，超过上限")
        elif not (6 <= len(cards) <= 9): warns.append(f"{len(cards)} 张图（建议 6–9）")

    print(f"标题 {len(title)}/20 · 正文 {len(body)}/1000 · 话题 {len(topics)} · 卡片 {len(cards)}")
    for e in errs: print("ERROR", e)
    for w in warns: print("WARN ", w)
    if errs:
        sys.exit(1)
    print("all good" if not warns else "no errors")


if __name__ == "__main__":
    main()
