# pptx-eslint / decklint

**PowerPoint 的 ESLint** · 质量门禁，不是生成器

对照 Duarte · Presentation Zen · Microsoft · WCAG 幻灯片清单 · 优设 等**公开**设计原则，给任意 `.pptx` 打分，输出机器可读违规（JSON / SARIF / HTML），并对可安全修复的项提供 `--fix`。

> 生成器到处都是。**校验器几乎空白。** 本仓库补上这块缺口。

English → [`README.md`](README.md) · 完整用法 → [`docs/USAGE.zh-CN.md`](docs/USAGE.zh-CN.md) · [`docs/USAGE.md`](docs/USAGE.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![CLI](https://img.shields.io/badge/cli-decklint-black)](#30-秒上手)
[![Python](https://img.shields.io/badge/python-≥3.10-blue)](pyproject.toml)
[![version](https://img.shields.io/badge/version-0.3.0-green)](pyproject.toml)

## 为什么存在

GitHub 上已有大量 **AI PPT 生成器**。几乎没人给原生 `.pptx` 做像 ESLint 那样的**质量门禁**。

无论是人还是 Agent 生成幻灯片，仍会交付：子弹墙「幻灯片文档」、后排不可读的小字、Excel 默认图表垃圾、无意义彩虹色、弹跳动画。

`decklint` 把经典公开教程原则变成可在 CI / 本地 / Agent Skill 中运行的**检查 + 评分**（生成之后再验）。

## 不是又一个生成器

| 拥挤赛道 | 本仓库 |
|---|---|
| Prompt → PPTX | PPTX → **评分 + 修复** |
| 模板 / 主题 | **规则即代码** |
| 「做得好看点」感觉论 | 可度量门禁（字号、WCAG 对比度、占版率…） |
| 取代 Duarte/Zen 原著 | 仅引用公开页；只编码可测启发式 |

## 30 秒上手

```bash
git clone https://github.com/mumu-2025/pptx-eslint.git
cd pptx-eslint
python -m venv .venv && source .venv/bin/activate   # Windows: .\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
python scripts/make_fixtures.py
decklint check fixtures/bad/slideument.pptx --preset stage --lang zh
decklint check 你的文件.pptx --preset reading --lang zh --format html --out 质检.html
```

当违规达到 `--fail-on`（默认 `error`）时退出码为 `1`。

| 你想… | 命令 |
|---|---|
| 上台讲的稿 | `decklint check x.pptx --preset stage --lang zh` |
| 发邮件给人看 | `decklint check x.pptx --preset reading --lang zh` |
| 发布会极简风 | `decklint check x.pptx --preset keynote --lang zh` |
| 无障碍抽查 | `decklint check x.pptx --preset a11y --lang zh` |
| 企业 / 品牌质检 | `decklint check x.pptx --preset corporate --lang zh` |
| 严格 WCAG | `decklint check x.pptx --preset wcag-strict --lang zh` |
| 无人讲解交接稿 | `decklint check x.pptx --preset async-doc --lang zh` |
| 看有哪些规则 | `decklint rules --lang zh` |
| 分类打分 | `decklint score x.pptx --lang zh` |
| 导出 HTML / JSON / SARIF | `... --format html\|json\|sarif --out …` |
| 安全自动修复动画 | `... --fix`（生成 `*.linted.pptx`） |

👉 **详细步骤、场景选型、CI / Agent 接法、FAQ：** [`docs/USAGE.zh-CN.md`](docs/USAGE.zh-CN.md) · English [`docs/USAGE.md`](docs/USAGE.md)

## 功能亮点（v0.3）

| 类别 | 规则 |
|---|---|
| 排版 | `max-text`, `no-slideument`, `min-font`, `font-families`, `font-embed`, `bullet-depth` |
| 颜色 / 无障碍 | `accent-colors`, `text-contrast`, `image-alt`, `a11y-title`, `unique-titles`, `vague-links`, `auto-advance`, `deck-properties` |
| 版式 | `occupancy`, `alignment-near-miss`, `box-overlap`, `image-bleed`, `safe-margins`, `max-shapes` |
| 设计主张 | `one-idea`, `title-as-claim`, `title-length`, `empty-slide`, `speaker-notes`, `canvas` |
| 图表 | `chart-junk`, `notes-for-charts` |
| 动画 | `animation-policy` |

详见 [`docs/rules.zh-CN.md`](docs/rules.zh-CN.md) / [`docs/rules.md`](docs/rules.md)。

## 预设

| 预设 | 场景 | 更严项 |
|---|---|---|
| `stage` | 现场演讲 | 文字密度、字号 |
| `reading` | 邮件 / 异步审阅 | 允许更密文字 |
| `keynote` | 发布会美学 | 1 个强调色、极简文字 |
| `a11y` | 无障碍门禁 | WCAG 对比度 + 强制图片 alt |
| `corporate` | 企业 / 品牌质检 | 字体≤2、强调色、边距、嵌字、Title |
| `wcag-strict` | 严格无障碍 | 唯一标题 / alt / 定时进片 → error |
| `async-doc` | 无人讲解交接 | 内容页强制演讲者备注 |

规则包：[`rules/duarte-zen-microsoft.yaml`](rules/duarte-zen-microsoft.yaml) · [`rules/accessibility.yaml`](rules/accessibility.yaml) · [`rules/corporate.yaml`](rules/corporate.yaml) · [`rules/wcag-strict.yaml`](rules/wcag-strict.yaml) · [`rules/async-doc.yaml`](rules/async-doc.yaml)

## `--fix`（仅安全项）

**会做：** 从 OOXML 中剥离可识别的禁用动画/切换节点 → 写出 `*.linted.pptx`。

**不会做：** 改写标题、字体、颜色、版式、图表、替代文本、备注、边距或画布比例。

## Agent Skill

[`skills/decklint`](skills/decklint) — 任意 `.pptx` 写完后，先跑 `decklint check`，修完错误再交付。

## GitHub Action

见 [`.github/workflows/decklint.yml`](.github/workflows/decklint.yml) — 安装、fixtures、pytest、坏/好样例门禁、SARIF 产物。

## 许可

MIT。教程品牌与图书版权归原权利人。
