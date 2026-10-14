---
name: x-thread
description: Writes an X (Twitter) thread or single post announcing a research paper, acceptance, poster session or release, following AI-research community norms (hook-first, one figure per tweet, links last, 280 weighted-char limit), plus matching images. Produces drafts only — the user posts manually, no X API. Use for "推特/X 宣传", "写个 thread", tweets about a paper.
---

# x-thread：X 推文 / thread

**先读 `references/x-style-guide.md`**，它是平台生态和展现形式的依据。

## 输入

`launch/brief.md`（唯一事实源）、`launch/assets/figs/`、项目主页地址、发布场景（首发/中稿/参会/新版本）。
如果 `launch/log.md` 有历史数据，先看哪种钩子、哪种图表现好。

## 产出

```
launch/x/
  thread.md      # 每条推文之间用单独一行 --- 分隔
  img/01-teaser.png, img/03-method.png ...   # 文件名前缀 = 推文序号
```

`thread.md` 格式（`make_post_kit.py` 依赖此格式）：

```markdown
Hook sentence with a number. Introducing NAME 🧵
<!-- img: img/01-teaser.png | alt: one-line description -->
---
2/ The problem: ...
<!-- img: img/02-problem.png | alt: ... -->
---
...
---
📄 Paper: https://arxiv.org/abs/...
💻 Code: https://github.com/...
🌐 Page: https://....github.io/.../
Joint work with @coauthor and @advisor at @lab.
```

每条最多 4 张图（X 的上限），一般 1 张。

## 步骤

1. 选钩子：按风格指南列出 3 个候选钩子，挑最具体、最能单独成立的一个；其余两个写在 `thread.md` 末尾的 HTML 注释里供用户换。
2. 写正文：每条只讲一件事；数字从 brief 原样复制。
3. 配图：
   - 优先直接用论文图。图里字太小时：裁剪局部，或用 HTML 重新排一张 16:9 的图（大标题 + 局部图），用 `render.py --width 1600 --height 900` 渲染。
   - 有视频/GIF 素材（demo、生成结果）时优先用，放第 1 条。
4. 校验：
   ```
   python $KIT/scripts/check_x.py launch/x/thread.md
   ```
   所有条目必须 ≤ 280 加权字符，图片文件都存在。超长就删字，不要拆出无意义的新条目。
5. @ handle 只用 brief 里核实过的；`[待补充]` 的作者用全名代替，不猜。
6. 自检（逐条）：有没有 brief 里不存在的说法？有没有 "SOTA/first/revolutionary" 但 brief 不支持？第 1 条脱离上下文能看懂吗？链接是不是只在最后一条？

## 不要

- 不调用 X API、不用第三方排程工具、不登录用户账号。
- 不写中文 thread（除非用户要求）。
- 不使用 hashtag 堆砌、不 @ 无关的大 V。
