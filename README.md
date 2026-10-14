# paper-launch-kit

一套给 coding agent 用的论文发布 skill：从一篇论文出发，自动产出 **仓库 README、项目主页、会议海报、X thread、小红书图文**。你只在两个关卡点头，然后花几分钟手动点"发布"。

- **推荐 Claude Code**，同时兼容其他 agent：遵循开放的 Agent Skills 标准（`SKILL.md`），Codex、Gemini CLI、Cursor 等也能用。
- **零平台费用**：不用 X API、不用排程工具、不调外部 LLM/图像 API。渲染全部在本地用免费的 headless Chromium 完成，主页托管在 GitHub Pages。
- **按平台生态写**：X 和小红书各有一份风格指南（受众、展现形式、钩子写法、限流雷区），附检查脚本。

## 安装（按项目安装）

在**论文的代码仓库根目录**运行：

```bash
npx skills add a-green-hand-jack/paper-launch-kit -a claude-code --skill '*' -y
pip install -r .claude/skills/paper-launch/requirements.txt && playwright install chromium
```

- 默认装在当前项目的 `.claude/skills/`（实体文件在 `.agents/skills/`），只对这个项目生效。**不要加 `-g`**——每篇论文的仓库各装一份，互不影响，也方便把 skill 版本和论文一起提交。
- `--skill '*'` 一次装齐 7 个 skill。它们共用 `paper-launch/scripts/`，必须一起装。
- 更新：`npx skills update`。
- 用其他 agent：把 `-a claude-code` 换成 `-a codex`、`-a gemini-cli`、`-a cursor` 等；不支持 skill 的 agent，在项目的 `AGENTS.md` 里加一行"发布论文时读取 `.agents/skills/paper-launch/SKILL.md` 并照做"。

### 为什么推荐 Claude Code

- 原生支持 Agent Skills，按描述自动触发，也可以直接 `/paper-launch` 调用。
- 能**看图**：渲染出的卡片、海报、网页截图，它会自己打开检查有没有溢出、错位、字太小，这是本流程质量的关键一环。
- 支持子 agent 并行：README、主页、推文、小红书可以同时做。
- 两个人工关卡可以在对话里直接停下来等你确认。

其他 agent 也能跑完流程，但"自查渲染图"这一步可能需要你多看一眼。

## 使用

在论文代码仓库里对 agent 说：

> arXiv 明天上线，帮我做一套发布（论文源码在 paper/ 目录）

agent 会：

1. 读论文，写 `launch/brief.md`（所有数字带表号/图号出处）→ **关卡 1：你确认结论和数字**
2. 写 README、做主页、写 X thread、做小红书卡片（参会时还做海报）
3. 生成 `launch/post-kit.html`：每条内容都有复制按钮 → **关卡 2：你审阅**
4. 在 `launch/STATUS.md` 列出你要手动做的事和时间（发 X、发小红书、提交 HF Papers、启用 GitHub Pages）

其他场景直接说："中稿了""下周去 XX 做 poster""发了 v2 模型"。

## 结构

```
skills/
  paper-launch/      总控：场景判断、关卡、时间线；scripts/ 是共享脚本
  paper-brief/       唯一事实源 brief.md
  repo-readme/       仓库 README
  project-page/      项目主页（含 X/微信链接预览卡）
  academic-poster/   会议海报 PDF
  x-thread/          X thread + 风格指南
  xhs-note/          小红书图文卡片 + 风格指南
```

| 脚本 | 作用 |
|---|---|
| `render.py` | HTML → PNG / PDF（卡片、海报、预览、og 图） |
| `extract_figures.py` | 从 PDF 或 LaTeX figures 目录取图 |
| `check_x.py` | 推文 280 加权字符、图片、链接位置、夸大用词 |
| `check_xhs.py` | 小红书字数、外链/导流/极限词、3:4 比例 |
| `make_qr.py` | 海报二维码 |
| `make_post_kit.py` | 生成带复制按钮的发布包 |

## 需要你手动做的（都很快）

| 事项 | 频率 | 耗时 |
|---|---|---|
| 确认 brief | 每次 | 2 分钟 |
| 审阅 post-kit | 每次 | 5 分钟 |
| 发 X thread（逐条复制） | 每次 | 3 分钟 |
| 发小红书（传图 + 粘贴） | 每次 | 3 分钟 |
| 在 huggingface.co/papers 提交论文 | 首发时 | 1 分钟 |
| GitHub Pages 选来源 | 每个项目一次 | 1 分钟 |

## 可选

- 小红书自动发布：`xiaohongshu-mcp`（开源免费）可以做，但属于非官方方式、有账号风控风险，kit 默认不启用。
- 复盘：发完把数据告诉 agent，它会记到 `launch/log.md`，下次沿用效果好的写法。
