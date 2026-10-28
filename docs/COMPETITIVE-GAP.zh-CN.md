# 竞争缺口（调研 2026-10-28，v0.2 更新）

English → [`COMPETITIVE-GAP.md`](COMPETITIVE-GAP.md)

## 拥挤（不要再做一个）

| 领域 | 例子（星标量级） |
|---|---|
| AI → PPTX 生成器 | ppt-master（约 70k）、presenton、banana-slides、PPTist |
| *生成*幻灯片的 Agent Skill | 各类 ppt-skill / 画述设计 |
| HTML 幻灯片框架 | reveal.js、slidev、marp、spectacle |
| Office Agent 底座 | OfficeCLI、Univer、genoffice |

## 几乎空白

| 领域 | 现有项目 | 星标 |
|---|---|---|
| 原生 `.pptx` 设计 linter | leppardwang/pptx-lint、TomiLabo/tmng-pptx-linter | ≤1 |
| 仅 Slidev 的 linter | Th3Mouk/slidev-linter | ~3 |
| Markdown「演示清单」gist | 若干个人列表 | 0–2 |

## v0.2 相对「薄骨架」的升级

多数所谓 linter 停在字符数启发式。**decklint v0.2** 提供：

- 纯色 RGB 文本/填充的 WCAG 相对亮度对比度
- OOXML 计时/切换解析 + 安全剥离（`--fix`）
- 版式几何：占版率、近失对齐、框重叠
- 颜色/字体数量预算、16:9 画布门禁
- 图表 3D 垃圾 + 标注提醒
- a11y 预设（alt + 更严对比度）
- GitHub Code Scanning SARIF、HTML 报告、中英双语 CLI

## 定位

**生成器提案。pptx-eslint 拍板。**

需求驱动：AI 放大幻灯片产量；质量塌方；团队需要幻灯片 CI，就像代码生成爆发时需要 ESLint。
