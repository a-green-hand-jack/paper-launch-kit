---
name: project-page
description: Builds a static academic project page (single self-contained HTML + images) for a paper from launch/brief.md, with link-preview cards for X/Slack, and deploys it for free on GitHub Pages. Use when the user needs a project website / 项目主页 / paper homepage, or needs it updated after acceptance or a new release.
---

# project-page：项目主页

产出 `launch/site/`：`index.html` + `static/`（teaser.png、method.png、result.png、og.png）。
纯静态，无构建步骤，免费托管在 GitHub Pages。

## 步骤

1. 读 `launch/brief.md`。
2. 复制 `templates/index.html` 到 `launch/site/index.html`，替换所有 `{{…}}` 占位符。
   - 作者数量、按钮数量按实际增删；不存在的链接（如还没有 demo）直接删按钮，不留死链。
   - 评审期间删掉 venue 徽章。
   - 摘要用论文原文摘要（作者自己的文字，可以原样用）。
   - Method/Results 的文字取自 brief 同行版，每段 ≤ 4 句。
   - 改 `--accent` 颜色使之与论文主图配色协调（从 teaser 图取主色）。
3. 图片：从 `launch/assets/figs/` 复制到 `launch/site/static/`。宽度压到 ≤ 2000px。
4. **og.png（链接预览卡）**：1200×630。X、微信、Slack 里贴主页链接时显示的就是它。做法：写一个小 HTML（项目名大字 + 一句话结论 + teaser 图），用
   ```
   python $KIT/scripts/render.py og.html launch/site/static/og.png --width 1200 --height 630
   ```
   渲染。`og:image` 必须是**绝对 URL**，所以 `{{PAGE_URL}}` 要填最终地址（以 `/` 结尾）。
5. 本地检查：`python $KIT/scripts/render.py launch/site/index.html launch/site-preview.png --width 1280 --full-page`，再用 `--width 390` 看手机版。打开截图逐段检查：没有残留 `{{`、图片都显示、手机端无横向滚动。也可以 `grep -n "{{" launch/site/index.html` 确认。

## 部署（免费）

推荐两种，选用户仓库里更方便的一种，把需要用户做的一次性步骤写进 STATUS.md：

- **方式 1：独立仓库** `<user>.github.io/<project>`：新建仓库 `<project>-page`（或直接用 `<project>`），把 `launch/site/` 内容推到 `gh-pages` 分支或 `main` 的 `/docs`。
- **方式 2：代码仓库的 `docs/` 目录**：把 site 内容复制到 `docs/`，仓库 Settings → Pages → Source 选 `main` / `docs`。

用户手动步骤只有一次：在 GitHub 仓库 Settings → Pages 里选好来源（约 1 分钟）。之后每次更新 push 即生效。
如果用户已经有个人学术主页（如 al-folio），可额外在主页 publications 里加一条，链接到本项目页。

## 不要

- 不引入 npm 构建、框架、付费字体或付费托管。
- 不放访客统计脚本（除非用户要求，且免费）。
- 不放与论文无关的夸张动效。
