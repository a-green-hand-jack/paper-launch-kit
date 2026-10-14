---
name: xhs-note
description: Creates a Xiaohongshu (小红书 / RedNote) image-carousel note about a research paper or PhD life — 3:4 card images rendered from an HTML template, a ≤20-char title, a ≤1000-char conversational body and topic tags — following the platform's ecosystem (search + recommendation feed, no external links, avoid restricted words). Drafts only; the user posts manually. Use for "小红书宣传", "发小红书", "做小红书图文".
---

# xhs-note：小红书图文笔记

**先读 `references/xhs-style-guide.md`。** 小红书和 X 的受众、展现形式、限流规则完全不同，不能翻译 X thread 了事。

## 输入

`launch/brief.md`（外行版解释、一句话中文结论、幕后故事）、`launch/assets/figs/`、发布场景、`launch/log.md`（如有）。
用户提供的照片（海报前合影、会场）放在 `launch/xhs/photos/`，有就优先用于封面。

## 产出

```
launch/xhs/
  note.md          # 标题 / 正文 / 话题，格式见下
  cards.html       # 卡片源文件
  figs/            # 卡片用到的图（从 assets/figs 复制并裁剪）
  cards/01.png …   # 渲染结果，1080x1440
```

`note.md` 格式（`make_post_kit.py` 依赖此格式）：

```markdown
# 标题
（≤20 字的标题，一行）

# 正文
（正文，≤1000 字）

# 话题
#人工智能 #AI #大模型 #论文分享 …

<!-- 备选标题：
1. …
2. …
-->
```

## 步骤

1. **定角度**：按场景选笔记类型——首发用"干货/分享型"，中稿用"经历型"（需要用户的故事，没有就用分享型并在汇报里提醒），参会用"见闻型"。
2. **写卡片大纲**：6–9 张，每张一句话主题。外行能不能看懂第 2 张？不能就重写。
3. **做卡片**：复制 `templates/cards.html` 到 `launch/xhs/cards.html`，按大纲增删 `<section class="card">`（四种版式：cover / point / number / info，可复制组合）。
   - 封面大字 ≤ 15 字，关键词 `<mark>` 高亮。
   - 论文图要裁出最直观的局部，不要整张塞进去；英文图配中文标题解释。
   - 页码按实际顺序改。
   - 同一用户的所有笔记沿用同一套配色（第一次做完后把配色记到 `launch/log.md`，以后复用）。
4. **渲染**：
   ```
   python $KIT/scripts/render.py launch/xhs/cards.html launch/xhs/cards/ --selector .card --width 1080
   ```
   逐张打开 PNG 检查：文字没溢出、没被裁、图清晰、手机上（把图缩到 30%）字仍可读。
5. **写 note.md**：标题 ≤20 字、正文 ≤1000 字，口语化第一人称，结尾提问 + 5–10 个话题。另给 2 个备选标题。
6. **校验**：
   ```
   python $KIT/scripts/check_xhs.py launch/xhs/
   ```
   它会检查字数、外链、导流词、广告法极限词、图片比例。所有 ERROR 必须修掉，WARN 逐条判断。
7. 不编造幕后故事、不替用户表达情绪（如"激动到哭"）——用户没说过的不写。

## 可选：自动发布（默认关闭）

开源免费的 `xiaohongshu-mcp`（github.com/xpzouying/xiaohongshu-mcp）可以用浏览器自动化发布，但属于非官方方式，有账号风控风险。
**只有用户明确要求时才配置**，并且每次发布前仍需用户在对话里明确确认。默认走手动发布（约 3 分钟）。
