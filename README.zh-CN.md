# pptx-eslint / decklint

**PowerPoint 的 ESLint** · 质量门禁，不是生成器

对照 Duarte · Presentation Zen · Microsoft · 优设 等**公开**设计原则，给任意 `.pptx` 打分，输出机器可读违规（JSON / SARIF / HTML），并对可安全修复的项提供 `--fix`。

> 生成器到处都是。**校验器几乎空白。** 本仓库补上这块缺口。

English → [`README.md`](README.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![version](https://img.shields.io/badge/version-0.2.0-green)](pyproject.toml)

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

## 快速开始

```bash
pip install -e ".[dev]"
python scripts/make_fixtures.py
decklint check path/to/deck.pptx --preset stage --lang zh
decklint check deck.pptx --format json --lang zh
decklint check deck.pptx --format sarif --out report.sarif
decklint check deck.pptx --fix
decklint rules --lang zh
decklint score deck.pptx
```

当违规达到 `--fail-on`（默认 `error`）时退出码为 `1`。

## 预设

| 预设 | 场景 | 更严项 |
|---|---|---|
| `stage` | 现场演讲 | 文字密度、字号 |
| `reading` | 邮件 / 异步审阅 | 允许更密文字 |
| `keynote` | 发布会美学 | 1 个强调色、极简文字 |
| `a11y` | 无障碍门禁 | WCAG 对比度 + 强制图片 alt |

## v0.2 检查项

排版、颜色/无障碍、版式、设计主张、图表垃圾、OOXML 动画策略等。详见 [`docs/rules.zh-CN.md`](docs/rules.zh-CN.md)。

## `--fix`（仅安全项）

**会做：** 从 OOXML 中剥离可识别的禁用动画/切换节点 → 写出 `*.linted.pptx`。

**不会做：** 改写标题、字体、颜色、版式、图表、替代文本或画布比例。

## 许可

MIT。教程品牌与图书版权归原权利人。
