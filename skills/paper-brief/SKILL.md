---
name: paper-brief
description: Reads a research paper (LaTeX source or PDF) and writes launch/brief.md, the single source of truth for every promotional asset — claims, verified numbers with table/figure references, key figures, audience-level explanations, links and author handles. Use before writing any README, project page, poster or social post about a paper, or when the user says "提炼论文要点 / 做 brief".
---

# paper-brief：唯一事实源

后续所有物料（README、主页、海报、推文、小红书）只从 brief 取内容。brief 错了，全部错；所以这一步要慢、要准。

## 输入

按优先级找：LaTeX 源码目录（`main.tex` 等）> 论文 PDF > arXiv 链接（只用来下载 PDF/源码，不用付费服务）。
同时看论文仓库已有的 README、`figures/` 目录。

## 步骤

1. **通读全文**，不是只读摘要。重点：引言最后的贡献列表、方法总图、主结果表、消融、局限性。
2. **抽图**：
   ```
   python $KIT/scripts/extract_figures.py <paper.pdf 或 figures目录> launch/assets/figs/
   ```
   （`$KIT` = `../paper-launch`）。LaTeX 源码里的 `figures/*.pdf` 会被转成 PNG；PDF 会抽嵌入位图并把每页渲染成高清 PNG，供你裁剪矢量图。打开图片逐一看，挑出：
   - **teaser**：一眼能看懂"这篇做了什么/效果多好"的图（通常是 Figure 1）
   - **method**：方法总览图
   - **result**：最有说服力的结果图或表
   矢量图只能整页渲染时，用 PIL 按坐标裁出来，存为 `fig-teaser.png` 等。
3. **按 `templates/brief.md` 填写** `launch/brief.md`。规则：
   - 每个数字后面写出处，如 `(Tab. 2)`、`(Fig. 4)`。不抄错小数位，不四舍五入成更好看的值。
   - "相对提升"要算清楚基线是谁，算式写在出处旁。
   - 外行版解释不许出现术语；必须用到时紧跟一句白话。
   - 类比要准确，不准确宁可不要。
   - 作者的 X handle、单位、个人主页：能从论文/仓库/已有主页找到就填，找不到写 `[待补充]`。不要猜 handle。
4. **自检**：逐个数字回到原文核对一遍；检查一句话结论是否夸大（"首次""最好""SOTA"必须有原文明确支持，否则删掉）。
5. 把需要用户确认或补充的项集中列在 brief 末尾的「待确认」一节。

## 交付

告诉总控（或用户）：brief 写好了，以及「待确认」里有几项。不要把整个 brief 贴进对话。
