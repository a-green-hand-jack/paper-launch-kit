---
name: repo-readme
description: Writes or updates the README.md of a research code repository in the conventional ML-paper style (title, badges, teaser, news, install, quickstart, results, citation) from launch/brief.md. Use when releasing code for a paper, after acceptance (venue update), or when the user asks to polish the repo README.
---

# repo-readme：论文代码仓库 README

读 `launch/brief.md`；读仓库现有 README、代码结构、`requirements.txt`/`pyproject.toml`/`environment.yml`、脚本入口。
按 `templates/README.template.md` 的结构写仓库根目录 `README.md`。

## 规则

- **已有 README 时**：保留用户写的安装/使用细节，只补结构和宣传部分。改动前先说明会动哪些段落。
- **徽章**用 shields.io 静态徽章（免费，无需注册），只放真实存在的链接：arXiv、Project Page、HF 模型/数据、License、会议。
- **teaser 图**：把 brief 里的 teaser 复制到仓库 `assets/teaser.png`（或已有的图片目录），README 用相对路径引用。宽度 ≤ 1600px，体积尽量 < 1MB。
- **News** 用倒序日期列表；首发时只有一条。中稿、开源、新版本时往顶部加。
- **Quickstart 必须能跑**：命令从仓库真实脚本里来。看不出入口时，写 `[待补充]` 并在汇报里提一句，不要编命令。
- **结果表**只放主结果的精简版（最多 5 行），数字与 brief 完全一致，注明来自论文哪张表。
- **Citation** 用 brief 里的 BibTeX。
- 不放"⭐ star 我们"之类的乞求语；可以在末尾放一句致谢和联系方式。
- 中文用户为主的项目可加 `README_zh.md`，但默认只写英文版。

## 检查

- 所有相对路径的图片存在；所有链接不是占位符（或明确标了 TODO）。
- 在 GitHub 渲染下标题层级合理（只有一个 `#`）。
