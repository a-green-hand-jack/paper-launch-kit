# paper-launch-kit (fallback entry for agents without Agent Skills support)

When the user asks to launch, announce or promote a research paper — or to make its README,
project page, poster, X/Twitter thread or Xiaohongshu (小红书) note — read
`skills/paper-launch/SKILL.md` (or, once installed into a project, `.agents/skills/paper-launch/SKILL.md`)
and follow it. It routes to the other six skills.

Shared scripts live in `paper-launch/scripts/`.
Hard rules: no paid APIs, no automatic posting, every number must come from `launch/brief.md`.
