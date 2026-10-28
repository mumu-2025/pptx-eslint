# 使用说明（简体中文）

`decklint` 检查**已经生成好的** `.pptx`，给出分数和违规项。它**不会**替你写 PPT。

English → [`USAGE.md`](USAGE.md)

---

## 1. 环境要求

- Python **3.10+**
- 系统：macOS / Linux / Windows（WSL 亦可）
- 不需要安装 Microsoft PowerPoint

---

## 2. 安装

### 方式 A：从 GitHub 克隆（推荐）

```bash
git clone https://github.com/mumu-2025/pptx-eslint.git
cd pptx-eslint
python -m venv .venv
source .venv/bin/activate          # Windows: .\.venv\Scripts\Activate.ps1
pip install -U pip
pip install -e ".[dev]"
decklint --version                 # 应显示 0.3.x
```

### 方式 B：本地目录

```bash
cd /path/to/pptx-eslint
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

---

## 3. 五分钟上手

```bash
python scripts/make_fixtures.py
decklint check fixtures/bad/slideument.pptx --preset stage --lang zh
decklint check fixtures/good/claim-slide.pptx --preset stage --lang zh
decklint check /path/to/your.pptx --preset reading --lang zh
```

传入目录时会递归扫描 `*.pptx`。

---

## 4. 选择预设

| 预设 | 场景 | 说明 |
|---|---|---|
| `stage` | 现场演讲（默认） | 文字少、字号大 |
| `reading` | 邮件 / 异步审阅 | 允许更密文字 |
| `keynote` | 发布会极简风 | 强调色更少、密度更严 |
| `a11y` | 无障碍门禁 | WCAG 对比度 + 图片 alt |
| `corporate` | 企业 / 品牌质检 | 字体≤2、强调色≤2、边距、嵌字、文件 Title |
| `wcag-strict` | 严格无障碍 | 唯一标题 + alt + 禁止定时进片（**error**） |
| `async-doc` | 无人讲解的交接稿 | 内容页必须有演讲者备注 |

---

## 5. 命令参考

### `decklint check`

```bash
decklint check PATH... [--preset stage|reading|keynote|a11y|corporate|wcag-strict|async-doc]
                       [--lang en|zh]
                       [--format text|json|sarif|html]
                       [--out FILE]
                       [--fail-on error|warning|info]
                       [--fix]
                       [--rules RULES.yaml]
```

| 参数 | 含义 | 默认 |
|---|---|---|
| `--preset` | 规则包 | `stage` |
| `--lang` | 界面/消息语言 | `en` |
| `--format` | 输出格式 | `text` |
| `--out` | 写入报告文件 | — |
| `--fail-on` | 达到该级别即退出码 1 | `error` |
| `--fix` | 安全自动修复 → `*.linted.pptx` | 关 |

示例：

```bash
decklint check deck.pptx --lang zh --format html --out 质检.html
decklint check deck.pptx --preset corporate --fail-on warning --lang zh
decklint check deck.pptx --preset wcag-strict --lang zh
decklint check deck.pptx --preset async-doc --lang zh
decklint check deck.pptx --fix
decklint score deck.pptx --preset keynote --lang zh
decklint rules --lang zh
```

**自动修复会做：** 剥离可识别的禁用 OOXML 动画/切换。  
**不会做：** 改字体、颜色、标题、版式、图表、alt、备注或边距。

---

## 6. 全部规则（v0.3）

| 规则 id | 分类 | 检查内容 |
|---|---|---|
| `max-text` | typography | 每页字符数 |
| `no-slideument` | typography | 子弹墙 / 过长条目 |
| `min-font` | typography | 最小显式字号 |
| `font-families` | typography | 字体种类数 |
| `font-embed` | typography | OOXML 是否嵌入字体（企业） |
| `bullet-depth` | typography | 项目符号嵌套深度 |
| `accent-colors` | color | 非灰强调色数量 |
| `text-contrast` | a11y | WCAG 对比度（纯色 RGB） |
| `image-alt` | a11y | 图片 descr / 替代文本 |
| `a11y-title` | a11y | 带标题版式的标题占位 |
| `unique-titles` | a11y | 幻灯片标题唯一（且尽量存在） |
| `vague-links` | a11y | 禁止「click here / 了解更多」 |
| `auto-advance` | a11y | 定时 `advTm` 自动进片 |
| `deck-properties` | a11y | 核心属性 Title |
| `occupancy` | layout | 占版率 |
| `alignment-near-miss` | layout | 近乎对齐 |
| `box-overlap` | layout | 不透明重叠 |
| `image-bleed` | layout | 图片过多 |
| `safe-margins` | layout | 约 5% 外边距安全区 |
| `max-shapes` | layout | 形状数量上限 |
| `one-idea` | design | 多个顶部文本框 |
| `title-as-claim` | design | 空泛标题 |
| `title-length` | design | 标题过短 / 过长 |
| `empty-slide` | design | 空白页 |
| `speaker-notes` | design | 内容页备注（async-doc） |
| `canvas` | design | 优先约 16:9 |
| `chart-junk` | chart | 3D / 标注提醒 |
| `notes-for-charts` | chart | 图表页需要备注 |
| `animation-policy` | animation | 禁用装饰动画；限制切换种类 |

完整百科：[`rules.zh-CN.md`](rules.zh-CN.md)

---

## 7. 工作流

**人工：** 导出 `.pptx` → `decklint check` → 修改 → 再跑到退出码 0。

**Agent / CI：** 生成 → `decklint check --fail-on error` → 非 0 表示**未完成**。

### CI 示例（GitHub Actions）

```yaml
- run: pip install -e ".[dev]"
- run: decklint check decks/ --preset corporate --fail-on warning --lang zh --format sarif --out decklint.sarif
```

参见 [`.github/workflows/decklint.yml`](../.github/workflows/decklint.yml) 与 [`skills/decklint/SKILL.md`](../skills/decklint/SKILL.md)。

---

## 8. 如何读结果

| 字段 | 含义 |
|---|---|
| `score` | 0–100 |
| `Sev` / 级别 | `error` / `warning` / `info` |
| `Rule` / 规则 | 规则 id（`decklint rules`） |
| `Slide` / 页 | 从 1 起；空表示整稿 |

---

## 9. 常见问题

**`command not found`** — 先激活 venv 再 `pip install -e .`。

**对比度明明很差却没报** — 只度量可解析的纯色 RGB；主题色/渐变/图片底会跳过，避免误报。

**旧版 `.ppt`** — 不支持；请另存为 `.pptx`。

**和生成器（ppt-master、Gamma…）的关系** — 它们负责生成；`decklint` 负责验收。可以串联。

**为什么新稿一上来就有 info？** — `deck-properties` / `font-embed` 默认较软；需要强制时用 `corporate` 或 `wcag-strict`。

---

## 10. 开发 / 测试

```bash
pip install -e ".[dev]"
python scripts/make_fixtures.py
pytest -q
```

---

## 11. 帮助

```bash
decklint --help
decklint check --help
```

仓库：https://github.com/mumu-2025/pptx-eslint
