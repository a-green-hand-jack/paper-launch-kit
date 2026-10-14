#!/usr/bin/env python3
"""Build launch/post-kit.html: everything the user needs to post by hand, with copy buttons.

  make_post_kit.py launch/

Reads (whatever exists):  x/thread.md, xhs/note.md, xhs/cards/*.png, STATUS.md
Open the result in a browser, review, then copy-paste into X / Xiaohongshu.
"""
import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from check_x import parse as parse_thread, weighted_len  # noqa: E402
from check_xhs import sections as parse_note  # noqa: E402

CSS = """
:root{--bg:#f6f5f1;--card:#fff;--ink:#1b1a18;--muted:#6d695f;--line:#e4e0d6;--accent:#2f5bd3;--ok:#1f8a4c;--bad:#c4372b}
@media (prefers-color-scheme:dark){:root{--bg:#141413;--card:#1d1c1a;--ink:#ecebe6;--muted:#a19d93;--line:#2e2d2a;--accent:#86a4ff;--ok:#4cc27e;--bad:#ff7a6b}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 -apple-system,BlinkMacSystemFont,"PingFang SC","Noto Sans CJK SC","Segoe UI",sans-serif}
.wrap{max-width:860px;margin:0 auto;padding:28px 16px 80px}
h1{font-size:26px;margin:0 0 4px}h2{font-size:21px;margin:40px 0 6px}.sub{color:var(--muted);margin:0 0 16px;font-size:14.5px}
.item{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 16px;margin:12px 0}
.row{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-bottom:8px;font-size:13.5px;color:var(--muted)}
.txt{white-space:pre-wrap;word-break:break-word}
button{font:600 13.5px/1 inherit;padding:8px 14px;border-radius:8px;border:1px solid var(--line);background:var(--ink);color:var(--bg);cursor:pointer;flex-shrink:0}
button.done{background:var(--ok);border-color:var(--ok)}
.imgs{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}.imgs img{height:150px;border-radius:8px;border:1px solid var(--line)}
.xhs .imgs img{height:220px}.over{color:var(--bad);font-weight:700}.okc{color:var(--ok)}
.steps{white-space:pre-wrap;font-size:15px}
"""

JS = """
function cp(id,btn){const t=document.getElementById(id).innerText;
 const ok=()=>{btn.textContent='已复制';btn.classList.add('done');};
 if(navigator.clipboard&&window.isSecureContext){navigator.clipboard.writeText(t).then(ok).catch(()=>fb(t,ok));}else{fb(t,ok);}}
function fb(t,ok){const a=document.createElement('textarea');a.value=t;document.body.appendChild(a);a.select();
 try{document.execCommand('copy');ok();}catch(e){}document.body.removeChild(a);}
"""


def esc(s):
    return html.escape(s, quote=True)


def item(uid, label, text, imgs=(), extra=""):
    pics = "".join(f'<img src="{esc(p)}" alt="{esc(a)}" title="{esc(a)}">' for p, a in imgs)
    return (f'<div class="item"><div class="row"><span>{label}{extra}</span>'
            f'<button onclick="cp(\'{uid}\',this)">复制</button></div>'
            f'<div class="txt" id="{uid}">{esc(text)}</div>'
            + (f'<div class="imgs">{pics}</div>' if pics else "") + "</div>")


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    root = Path(sys.argv[1])
    parts = ['<h1>发布包</h1><p class="sub">逐条复制粘贴即可。图片按显示顺序上传。</p>']

    status = root / "STATUS.md"
    if status.exists():
        m = re.search(r"##\s*需要你手动做的.*?\n(.*?)(?=\n##\s|\Z)", status.read_text(encoding="utf-8"), re.S)
        steps = re.sub(r"<!--.*?-->", "", m.group(1), flags=re.S).strip() if m else ""
        if steps:
            parts.append(f'<h2>手动步骤</h2><div class="item steps">{esc(steps)}</div>')

    thread = root / "x" / "thread.md"
    if thread.exists():
        tweets = parse_thread(thread)
        parts.append(f'<h2>X thread（{len(tweets)} 条）</h2><p class="sub">发帖框粘贴第 1 条并上传图片 → 点 “+” 依次添加后续 → 全部发布。</p>')
        for i, t in enumerate(tweets, 1):
            n = weighted_len(t["text"])
            cls = "over" if n > 280 else "okc"
            imgs = [(f"x/{p}", a) for p, a in t["imgs"]]
            parts.append(item(f"t{i}", f"第 {i} 条", t["text"], imgs, f' · <span class="{cls}">{n}/280</span>'))

    note = root / "xhs" / "note.md"
    if note.exists():
        s = parse_note(note.read_text(encoding="utf-8"))
        cards = sorted((root / "xhs" / "cards").glob("*.png"))
        parts.append('<h2 class="xhs">小红书</h2><p class="sub">把 xhs/cards 里的图按序号传到手机或创作服务平台 → 粘贴标题、正文 → 添加话题 → 勾选原创声明。</p>')
        pics = "".join(f'<img src="xhs/cards/{c.name}" alt="{c.name}">' for c in cards)
        parts.append(f'<div class="item xhs"><div class="row"><span>卡片 {len(cards)} 张（3:4）</span></div><div class="imgs">{pics}</div></div>')
        parts.append(item("xt", "标题", s.get("标题", ""), extra=f' · {len(s.get("标题", ""))}/20'))
        parts.append(item("xb", "正文", s.get("正文", ""), extra=f' · {len(s.get("正文", ""))}/1000'))
        parts.append(item("xg", "话题", s.get("话题", "")))

    page = (f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1"><title>发布包</title>'
            f'<style>{CSS}</style></head><body><div class="wrap">{"".join(parts)}</div><script>{JS}</script></body></html>')
    out = root / "post-kit.html"
    out.write_text(page, encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
