---
name: decklint
description: After writing or editing any .pptx, run decklint as a quality gate before delivering. Use for slide QA, presentation review, Duarte/Zen/WCAG rule checks. 在生成或修改任何 .pptx 后，交付前用 decklint 做质量门禁。
---

# decklint skill / decklint 技能

You generate or edit PowerPoint. **Done means the verifier passes**, not that you think it looks fine.

你生成或修改 PowerPoint。**完成 = 校验器通过**，而不是「我觉得还行」。

## When / 何时

- After creating a `.pptx` / 创建 `.pptx` 之后
- After applying design changes / 改完设计之后
- Before sending a file to the user / 交给用户之前

## How / 怎么做

```bash
decklint check PATH.pptx --preset stage|reading|keynote|a11y --lang en|zh
decklint score PATH.pptx
decklint check PATH.pptx --fix   # safe only: strip banned animations
```

| Scenario 场景 | Preset |
|---|---|
| Live talk 现场演讲 | `stage` or `keynote` |
| Email / async 邮件异步 | `reading` |
| Accessibility 无障碍 | `a11y` |

- Fix every `error`. Treat `warning` as should-fix unless the user waived it.  
  修复所有 `error`；`warning` 默认也应修，除非用户豁免。
- Re-run until exit code 0 (or only waived warnings remain).  
  重跑直到退出码 0（或只剩已豁免警告）。
- Prefer `--format json` when parsing programmatically.  
  程序解析时优先 `--format json`。

## Do not / 不要

- Skip the check because “the generator is good” / 因为「生成器很强」而跳过检查
- Lower the preset to silence errors without asking / 擅自降低预设以消音
- Expect `--fix` to rewrite copy, fonts, colors, or layout / 指望 `--fix` 改文案/字体/颜色/版式
