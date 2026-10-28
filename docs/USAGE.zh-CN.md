# 使用说明（简体中文）

`decklint` 检查**已经生成好的** `.pptx`，给出分数和违规项。它**不会**替你写 PPT。

English → [`USAGE.md`](USAGE.md)

---

## 1. 环境要求

- Python **3.10+**
- 系统：macOS / Linux / Windows（WSL 亦可）
- 不需要安装 Microsoft PowerPoint

---

## 2. 安装（三种方式任选）

### 方式 A：从 GitHub 克隆（推荐）

```bash
git clone https://github.com/mumu-2025/pptx-eslint.git
cd pptx-eslint
python -m venv .venv

# macOS / Linux
source .venv/bin/activate
# Windows PowerShell
# .\.venv\Scripts\Activate.ps1

pip install -U pip
pip install -e ".[dev]"
```

安装成功后，终端里应能运行：

```bash
decklint --version
# 应显示 0.2.x
```

### 方式 B：直接对本地目录安装

若你已有解压好的源码目录：

```bash
cd /path/to/pptx-eslint
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

### 方式 C：仅作库依赖（进阶）

```bash
pip install -e /path/to/pptx-eslint
```

---

## 3. 五分钟上手

### 3.1 生成演示样例（可选）

仓库不提交二进制 `.pptx`，请先生成：

```bash
python scripts/make_fixtures.py
```

会得到：

| 文件 | 含义 |
|---|---|
| `fixtures/bad/slideument.pptx` | 故意很差的「幻灯片文档」 |
| `fixtures/good/claim-slide.pptx` | 结论式大标题好页 |
| `fixtures/contrast-fail/low-contrast.pptx` | 对比度不足 |

### 3.2 检查一个文件（中文输出）

```bash
decklint check fixtures/bad/slideument.pptx --preset stage --lang zh
```

- 退出码 **1** = 有 `error` 级问题（默认）
- 退出码 **0** = 通过（或只有你允许的更低级别问题）

好样例应通过：

```bash
decklint check fixtures/good/claim-slide.pptx --preset stage --lang zh
```

### 3.3 检查你自己的 PPT

```bash
decklint check ~/Desktop/周报.pptx --preset reading --lang zh
```

也可以传**目录**（会递归找所有 `.pptx`）：

```bash
decklint check ./exports/ --preset stage --lang zh
```

---

## 4. 该选哪个预设？

| 预设 | 什么时候用 | 特点 |
|---|---|---|
| `stage` | **你要上台讲** | 字要少、字要大（默认） |
| `reading` | **发邮件 / 飞书 / 让人自己看** | 允许更密的文字 |
| `keynote` | **发布会 / 极简大数字风** | 强调色更少、文字更狠 |
| `a11y` | **无障碍 / 合规抽查** | WCAG 对比度 + 图片替代文本更严 |

示例：

```bash
# 招标附件给人读
decklint check bid.pptx --preset reading --lang zh

# 发布会演讲稿
decklint check launch.pptx --preset keynote --lang zh

# 无障碍门禁
decklint check deck.pptx --preset a11y --lang zh
```

---

## 5. 常用命令一览

### 5.1 `decklint check` — 主命令

```bash
decklint check PATH [PATH...] [选项]
```

| 选项 | 说明 | 默认 |
|---|---|---|
| `--preset` | `stage` / `reading` / `keynote` / `a11y` | `stage` |
| `--lang` | 界面与违规文案：`zh` 或 `en` | `en` |
| `--format` | `text` / `json` / `sarif` / `html` | `text` |
| `--out` | 把报告写到文件（json/sarif/html 常用） | 无 |
| `--fail-on` | 达到该级别就退出 1：`error` / `warning` / `info` | `error` |
| `--fix` | 安全自动修复（目前主要剥禁用动画）→ `*.linted.pptx` | 关 |
| `--rules` | 自定义规则 YAML 路径 | 内置 |

### 5.2 输出 JSON（给脚本 / Agent）

```bash
decklint check deck.pptx --preset stage --lang zh --format json --out report.json
echo $?   # 看退出码
```

### 5.3 输出 HTML 报告（给人看）

```bash
decklint check deck.pptx --lang zh --format html --out report.html
# 用浏览器打开 report.html
```

### 5.4 输出 SARIF（GitHub Code Scanning）

```bash
decklint check deck.pptx --format sarif --out decklint.sarif
```

### 5.5 分类打分

```bash
decklint score deck.pptx --preset stage --lang zh
```

### 5.6 列出规则

```bash
decklint rules --lang zh
```

### 5.7 尝试安全修复

```bash
decklint check deck.pptx --fix --lang zh
# 成功时旁边会出现 deck.linted.pptx
```

**会自动修：** 可识别的禁用动画 / 转场节点。  
**不会自动修：** 字号、颜色、标题文案、版式、图表、替代文本（需人工或生成器改）。

---

## 6. 典型工作流

### 人：做完 PPT 再验

```bash
# 1. 你用 PowerPoint / Keynote / AI 工具导出 .pptx
# 2. 选对场景预设
decklint check 终稿.pptx --preset stage --lang zh --format html --out 质检.html
# 3. 按报告改完再查，直到退出码 0
```

### Agent / CI：生成后必须过门禁

```bash
# 生成步骤（任意工具）→ out.pptx
decklint check out.pptx --preset stage --fail-on error
# 非 0 则视为任务未完成，禁止交付
```

GitHub Actions 可参考本仓库 [`.github/workflows/decklint.yml`](../.github/workflows/decklint.yml)。

把下面片段放进你自己的仓库：

```yaml
- uses: actions/setup-python@v5
  with:
    python-version: '3.11'
- run: pip install -e ".[dev]"
  working-directory: path/to/pptx-eslint   # 或先 checkout 本仓库
- run: decklint check path/to/*.pptx --preset reading --fail-on error
```

### Agent Skill

见 [`skills/decklint/SKILL.md`](../skills/decklint/SKILL.md)：写完 `.pptx` 后先跑 `decklint`，**以校验器通过为准**，不要自称「看起来不错」。

---

## 7. 读懂结果

文本模式大致长这样：

```
fixtures/bad/slideument.pptx  score=xx/100  preset=stage
┌─────────┬──────────────┬───────┬────────────────────────────┐
│ Sev     │ Rule         │ Slide │ Message                    │
│ error   │ max-text     │ 1     │ 本页 … 个字符（上限 80）…   │
└─────────┴──────────────┴───────┴────────────────────────────┘
```

| 字段 | 含义 |
|---|---|
| `score` | 0–100，越高越好 |
| `Sev` | `error` / `warning` / `info` |
| `Rule` | 规则 ID（可用 `decklint rules` 查） |
| `Slide` | 页码（从 1 开始） |

完整规则说明：[`rules.zh-CN.md`](rules.zh-CN.md)

---

## 8. 常见问题

**Q: `decklint: command not found`**  
A: 没激活虚拟环境，或没 `pip install -e .`。先 `source .venv/bin/activate`。

**Q: 对比度明明很差却没报？**  
A: 当前只检查**能解析成纯色 RGB** 的文字/底。主题色、渐变、图片底会跳过，避免误报。需要时可改成显式 RGB，或用 `--preset a11y` 加强其它项。

**Q: 可以检查 `.ppt` 旧格式吗？**  
A: 否，只支持 `.pptx`。请先另存为 `.pptx`。

**Q: 和 ppt-master / Gamma 什么关系？**  
A: 那些是**生成器**；本工具是生成之后的**质检门禁**，可串在任何生成器后面。

**Q: Windows 路径有空格？**  
A: 给路径加引号：`decklint check "D:\My Decks\Q3.pptx" --lang zh`

---

## 9. 开发与测试（贡献者）

```bash
pip install -e ".[dev]"
python scripts/make_fixtures.py
pytest -q
decklint check fixtures/bad --preset stage --lang zh   # 期望失败
decklint check fixtures/good --preset stage            # 期望成功
```

---

## 10. 获取帮助

```bash
decklint --help
decklint check --help
decklint rules --lang zh
```

仓库主页：https://github.com/mumu-2025/pptx-eslint  
问题反馈：开 GitHub Issue。
