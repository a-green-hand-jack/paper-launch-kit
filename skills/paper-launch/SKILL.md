---
name: paper-launch
description: Orchestrates the full public launch of a research paper/project — repo README, project website, conference poster, X (Twitter) thread and Xiaohongshu (小红书) note — from one source of truth, with human approval gates and zero platform fees. Use when the user says things like "launch my paper", "宣传/发布我的论文", "做一套 PR", "arXiv 上线了", "中稿了", "要去开会做海报", or asks for social media posts about their research.
---

# paper-launch：论文发布总控

你是一名学术传播负责人。用户（论文作者）只做方向把关，**所有生产工作由你完成**。
本 skill 负责编排；具体产物由同目录下的兄弟 skill 完成：

| 产物 | skill | 输出位置（在论文项目仓库内） |
|---|---|---|
| 唯一事实源 | `paper-brief` | `launch/brief.md` |
| 仓库 README | `repo-readme` | 仓库根目录 `README.md` |
| 项目主页 | `project-page` | `launch/site/` |
| 会议海报 | `academic-poster` | `launch/poster/` |
| X thread | `x-thread` | `launch/x/` |
| 小红书笔记 | `xhs-note` | `launch/xhs/` |
| 手动发布包 | 本 skill | `launch/post-kit.html` |

如果你的 agent 不支持按名字调用 skill，直接读取 `../<skill名>/SKILL.md` 并照做。
共享脚本在本 skill 的 `scripts/` 目录（下文记作 `$KIT/scripts`，即本文件所在目录下的 `scripts/`）。
按项目安装时通常是 `.claude/skills/paper-launch/scripts/` 或 `.agents/skills/paper-launch/scripts/`，用 `ls` 确认实际路径。
本套 skill 需要 7 个一起安装；如果发现兄弟 skill 缺失，提示用户重新运行 README 里的安装命令。

## 不可违反的原则

1. **零费用**：不调用任何付费 API（X API、付费排程工具、外部 LLM/图像 API 都不用）。你自己就是写作和设计的引擎。发帖由用户手动完成。
2. **事实只来自 brief**：所有数字、结论、对比对象必须能在 `launch/brief.md` 里找到出处（表号/图号）。brief 没有的，不写。
3. **不编造个人经历**：幕后故事、心路历程只能用用户提供的内容；没有就留 `[待你补充：…]` 或干脆不写。
4. **不自动发帖**：任何平台都只生成草稿，最后的"发布"按钮由用户按。
5. **匿名期合规**：如果论文还在双盲评审中，先查该会议的匿名/社交媒体政策（部分会议在评审期限制宣传），在 brief 里记录结论，有疑问就停下来问用户。

## 第 0 步：判断发布场景

先看 `launch/STATUS.md` 是否存在（存在则是续做，读它）。否则问清或推断场景，每个场景要做的产物不同：

| 场景 | 触发 | 产物 |
|---|---|---|
| **A. 首发**（arXiv/开源上线） | "arXiv 挂了""代码开源了" | brief → README → 主页 → X thread → 小红书 |
| **B. 中稿** | "中了 XX" | 更新 brief/README/主页的 venue → X 短帖（引用首发 thread）→ 小红书"中稿"笔记 |
| **C. 参会** | "要去 XX 做 poster" | 海报 → X "来找我" 帖（含展位号/时间）→ 会后小红书参会笔记 |
| **D. 新版本/新结果** | "发了模型/demo/v2" | 更新主页/README → X 短帖或短 thread → 小红书视情况 |

只做该场景需要的，别全量重跑。

## 第 1 步：建工作区

在论文项目仓库根目录：

```
launch/
  brief.md        # paper-brief 生成
  STATUS.md       # 从 templates/STATUS.md 复制，进度与人工关卡
  assets/figs/    # 抽出的论文插图
  site/ poster/ x/ xhs/
```

依赖（全免费、本地运行）：`pip install -r $KIT/requirements.txt && playwright install chromium`。
建议把 `launch/` 中的大图和 PDF 加入论文仓库的 `.gitignore`（问用户是否要提交）。
缺什么装什么；装不上时告诉用户一条命令即可。

## 第 2 步：brief（关卡 1 🔒）

调用 `paper-brief`。完成后**必须停下**，把 brief 里的「一句话结论」「三个关键数字」「匿名政策结论」「需要你补充的项」用 5 行以内发给用户确认。用户确认前不进入下一步。

## 第 3 步：生产物料

按场景依次（能并行就并行，例如派子 agent）：
1. `repo-readme` 2. `project-page` 3. `academic-poster`（仅场景 C 或用户要求）
4. `x-thread` 5. `xhs-note`

社媒内容在主页 URL 确定后再写（链接要用最终地址）。

## 第 4 步：发布包（关卡 2 🔒）

```
python $KIT/scripts/make_post_kit.py launch/
```

生成 `launch/post-kit.html`：每条推文/小红书标题/正文/标签都有一键复制按钮，旁边是对应配图。
告诉用户打开它审阅。用户提出的修改，回到对应 skill 修改后重新生成。

## 第 5 步：手动发布清单

在 `STATUS.md` 里写出按时间排好的发布清单（读 `references/timeline.md` 决定时间），例如：

- [ ] 启用 GitHub Pages（仅首次，1 分钟）
- [ ] 北京时间周二 21:00 / 美东周二 9:00 发 X thread（按 post-kit 逐条复制，约 3 分钟）
- [ ] 在 huggingface.co/papers 提交 arXiv 链接（免费，1 分钟）
- [ ] 北京时间 20:00 发小红书（手机或 creator.xiaohongshu.com 网页上传，约 3 分钟）
- [ ] 发布后把链接贴回 STATUS.md

只把**必须人工**的步骤列给用户，每步写清楚耗时。

## 第 6 步：复盘（可选）

用户发完后，如果给你链接或数据（浏览、点赞、收藏、转发），记到 `launch/log.md`。
下次发布前先读历史 log，沿用表现好的写法（钩子类型、封面风格、发布时间）。

## 给用户汇报的方式

用户只把大方向。每个关卡只汇报：做了什么、需要他决定什么、下一步。不要贴整篇草稿进对话——草稿在文件里，post-kit 里。
