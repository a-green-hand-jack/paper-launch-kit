---
name: academic-poster
description: Designs a print-ready conference poster (PDF) for a paper from launch/brief.md using an HTML/CSS template rendered locally with headless Chromium, sized to the venue's poster requirements, with a QR code to the project page. Use when the user is presenting a poster at a conference / 做会议海报 / poster session.
---

# academic-poster：会议海报

产出 `launch/poster/poster.pdf`（打印用）和 `poster.png`（发社媒用的缩略图）。全部本地渲染，免费。

## 第 1 步：确认尺寸（必须查，不要猜）

在会议官网 "Call for Posters / Poster Instructions" 查：尺寸（英寸或厘米）、横竖版、是否必须用会议模板。
- 查不到或会议提供了强制模板：停下问用户。
- 记到 `launch/brief.md` 的基本信息里。

## 第 2 步：布局

复制 `templates/poster.html` 到 `launch/poster/`。在 `:root` 设置 `--w-in`、`--h-in`（厘米 ÷ 2.54），竖版时把 `--cols` 改成 2。

海报是给"走过路过 3 秒"的人看的，规则：
- **标题区**一眼看到项目名和一句话结论（`.tldr`）。
- **图 > 字**：每栏至少一张大图。正文用要点，每条 ≤ 2 行；整张海报正文总字数控制在 ~500 词以内。
- **三个大数字**放在 Results 顶部，与 brief 完全一致。
- 内容顺序按阅读路径：左→右、上→下：Motivation → Idea → Method → Results → Takeaways。
- 二维码指向项目主页（不是 arXiv）：
  ```
  python $KIT/scripts/make_qr.py <PAGE_URL> launch/poster/qr.png
  ```
- 单位 logo 由用户提供；没有就删掉 `.logos`。
- 配色：`--accent` 取论文主图配色，保证白字在其上可读。

## 第 3 步：渲染与检查

```
python $KIT/scripts/render.py launch/poster/poster.html launch/poster/poster.pdf --pdf --width-in 48 --height-in 36
python $KIT/scripts/render.py launch/poster/poster.html launch/poster/poster.png --width-px 2400 --poster-in 48x36
```

打开 PNG 逐块检查：
- 没有内容被裁掉（`overflow: hidden` 会悄悄吞掉溢出内容——最后一栏底部尤其要看）
- 正文在 A4 缩略图上依然能辨认 → 打印出来 2 米外可读
- 没有残留 `{{`
- 图片没有被拉伸变形

溢出时的处理顺序：删字 > 缩图 > 减小 `html` 根字号（最多减 15%）。

## 交付

告诉用户：PDF 在哪、尺寸、打印提醒（多数会议推荐提前在当地打印店或会议现场打印服务下单；布质海报方便携带）。打印费用由用户自理，不在本流程内。
