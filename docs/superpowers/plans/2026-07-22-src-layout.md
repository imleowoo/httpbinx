# src-layout Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 httpbinx 从扁平布局迁移到 src-layout（`src/httpbinx/`），并将版本号升至 `1.11.0`。

**Architecture:** 用 `git mv` 把 `httpbinx/` 整体移入 `src/`（保留 git 历史），更新 `pyproject.toml` 的 pdm-backend `package-dir` 与 version 路径，同步 `MANIFEST.in` 与 README 的图片路径，bump 版本号。包内业务代码零改动，Dockerfile 与 CI 安装/运行流不变。

**Tech Stack:** pdm-backend（构建后端，不变）、uv（环境与构建）、pytest、ruff、FastAPI。

## Global Constraints

- 构建后端保持 pdm-backend，不更换。
- 包内业务代码零改动（唯一例外：`__init__.py` 版本号 `1.10.2` → `1.11.0`）。
- `tests/` 保留在仓库根，不动到 `src/`。
- Dockerfile（`COPY . .` + `pip install .` + `CMD ["httpbinx", "server", ...]`）不变。
- CI 工作流（`check.yml` 的 `pip install .` + `pytest` + `ruff`、`publish.yml` 的 `python -m build`、`image.yml` 的 docker 构建）不变。
- Git commit message 与 PR 必须使用英文。
- 目标 Python：开发环境 3.14，CI 矩阵 3.10–3.14。
- 分支：`feature/src-layout`（已存在）。
- 远端：`git@github.com:imleowoo/httpbinx.git`，`gh` 已认证为 `imleowoo`。

---

## File Structure

改动文件清单：

| 文件 | 动作 | 职责 |
|------|------|------|
| `httpbinx/**` → `src/httpbinx/**` | 移动 | 包整体下移到 `src/`，内部结构不变 |
| `src/httpbinx/__init__.py` | 修改 | 版本号 `1.10.2` → `1.11.0` |
| `pyproject.toml` | 修改 | `[tool.pdm]` 加 `package-dir = "src"`；version 路径改为 `src/httpbinx/__init__.py` |
| `MANIFEST.in` | 修改 | `recursive-include httpbinx *` → `recursive-include src/httpbinx *` |
| `README.md` | 修改 | 第 1 行两处 GitHub raw 图片路径前缀 `httpbinx/` → `src/httpbinx/` |
| `Dockerfile` | 不变 | — |
| `.github/workflows/*.yml` | 不变 | — |
| `tests/**` | 不变 | — |

包内路径敏感代码（`helpers.py`、`main.py` 的 `Path(__file__).parent / ...`）无需改动：`__file__` 指向 `src/httpbinx/<module>.py`，`.parent` 即 `src/httpbinx/`，仍能正确定位 `static/` 与 `templates/`。

---

### Task 1: 前置环境恢复与基线验证

**Files:**
- 无改动

**Interfaces:**
- Consumes: 现有仓库
- Produces: 一个干净的 Python 3.14 venv 与可运行的基线测试，作为后续改动的对照

- [ ] **Step 1: 确认在 feature/src-layout 分支且工作区干净**

Run: `git status --short && git branch --show-current`
Expected: 空输出（工作区干净）+ `feature/src-layout`

- [ ] **Step 2: 恢复 venv 到 Python 3.14 并同步依赖**

Run: `uv venv --python 3.14 .venv && uv sync`
Expected: 输出 `Using CPython 3.14.x` 与 `Installed N packages`，无报错

- [ ] **Step 3: 安装包（editable）以确认基线可导入**

Run: `uv run pip install -e .`
Expected: `Successfully installed httpbinx-1.10.2`（editable 安装，版本仍为 1.10.2）

- [ ] **Step 4: 跑全量测试确认基线绿**

Run: `uv run pytest -q`
Expected: 全部测试 PASSED，无 failures/errors

- [ ] **Step 5: 跑 ruff 确认基线 lint 绿**

Run: `uv run ruff check .`
Expected: `All checks passed!`

---

### Task 2: 移动包到 src/ 并 bump 版本号

**Files:**
- Move: `httpbinx/` → `src/httpbinx/`（含全部子目录与文件）
- Modify: `src/httpbinx/__init__.py`

**Interfaces:**
- Consumes: 无
- Produces: `src/httpbinx/` 包目录；`src/httpbinx/__init__.py` 中 `__version__ = '1.11.0'`

- [ ] **Step 1: 创建 src 目录**

Run: `mkdir -p src`
Expected: 无输出，`src/` 目录存在

- [ ] **Step 2: 用 git mv 整体移动包**

Run: `git mv httpbinx src/httpbinx`
Expected: 无输出。`git status` 显示所有文件为 `renamed: httpbinx/... -> src/httpbinx/...`

- [ ] **Step 3: 验证移动后包结构完整**

Run: `find src/httpbinx -maxdepth 1 -not -path '*/__pycache__*' | sort`
Expected: 列出 `src/httpbinx`、`src/httpbinx/__init__.py`、`src/httpbinx/cli.py`、`src/httpbinx/constants.py`、`src/httpbinx/examples`、`src/httpbinx/helpers.py`、`src/httpbinx/main.py`、`src/httpbinx/meta.py`、`src/httpbinx/routers`、`src/httpbinx/schemas.py`、`src/httpbinx/static`、`src/httpbinx/templates`，与原 `httpbinx/` 顶层一致

Run: `git status --short | head`
Expected: 显示 `renamed: httpbinx/<...> -> src/httpbinx/<...>` 条目

> 说明：此时尚未改 `pyproject.toml`，editable 安装的 `.pth` 仍可能指向旧逻辑；import 验证放到 Task 5 重装后做，本步只核对文件结构。

- [ ] **Step 4: bump 版本号**

Edit `src/httpbinx/__init__.py`，将：

```python
__version__ = '1.10.2'
```

改为：

```python
__version__ = '1.11.0'
```

完整文件应为：

```python
"""HTTP Request & Response Service, written in Python + FastAPI."""

from .main import app

__version__ = '1.11.0'

app.version = __version__
```

- [ ] **Step 5: 暂不提交，进入 Task 3**

---

### Task 3: 更新 pyproject.toml 构建配置

**Files:**
- Modify: `pyproject.toml`（`[tool.pdm]` 段）

**Interfaces:**
- Consumes: Task 2 产出的 `src/httpbinx/`
- Produces: `[tool.pdm]` 含 `package-dir = "src"` 与 `version = { source = "file", path = "src/httpbinx/__init__.py" }`

- [ ] **Step 1: 修改 version 路径**

在 `pyproject.toml` 中找到：

```toml
[tool.pdm]
version = { source = "file", path = "httpbinx/__init__.py" }
distribution = true
```

改为：

```toml
[tool.pdm]
version = { source = "file", path = "src/httpbinx/__init__.py" }
package-dir = "src"
distribution = true
```

- [ ] **Step 2: 确认入口点段无需改动**

Run: `grep -n "project.scripts" pyproject.toml`
Expected: 输出 `httpbinx = "httpbinx.cli:execute"`，保持不变（入口点用已安装包名）

- [ ] **Step 3: 暂不提交，进入 Task 4**

---

### Task 4: 更新 MANIFEST.in 与 README.md 路径

**Files:**
- Modify: `MANIFEST.in`
- Modify: `README.md:1`

**Interfaces:**
- Consumes: Task 2 的 `src/httpbinx/` 路径
- Produces: manifest 与 README 引用的路径与实际文件位置一致

- [ ] **Step 1: 更新 MANIFEST.in**

将 `MANIFEST.in` 内容：

```
recursive-include httpbinx *
```

改为：

```
recursive-include src/httpbinx *
```

- [ ] **Step 2: 更新 README.md 第 1 行的图片路径**

将 `README.md` 第 1 行：

```markdown
![![cover](httpbinx/static/images/httpbinx_cover.png)](https://raw.githubusercontent.com/imleowoo/httpbinx/main/httpbinx/static/images/httpbinx_cover.png)
```

改为：

```markdown
![![cover](src/httpbinx/static/images/httpbinx_cover.png)](https://raw.githubusercontent.com/imleowoo/httpbinx/main/src/httpbinx/static/images/httpbinx_cover.png)
```

> 只改两处 `httpbinx/static/images/httpbinx_cover.png` 路径前缀为 `src/httpbinx/...`，其余文本不动。`README.md:24` 的 `[httpbinx](https://pypi.org/project/httpbinx/)` 指 PyPI 包名，不改。

- [ ] **Step 3: 确认没有遗漏的根级 `httpbinx/` 路径引用**

Run: `grep -rn "httpbinx/" pyproject.toml MANIFEST.in README.md .github/ Dockerfile .dockerignore 2>/dev/null | grep -v "src/httpbinx" | grep -v "pypi.org"`
Expected: 空输出（所有仓库内文件路径引用已更新为 `src/httpbinx/`）

> 预期无输出。仓库内当前仅 `README.md:1`（图片路径，本任务 Step 2 已改）、`pyproject.toml:49`（version path，Task 3 已改）含 `httpbinx/` 文件路径，均已处理。`README.md:24` 的 `[httpbinx](https://pypi.org/project/httpbinx/)` 是 PyPI 包名链接，非文件路径，保留；`httpbinx.cli:execute` 这类模块路径同保留。

---

### Task 5: 重装并验证测试与 lint

**Files:**
- 无文件改动

**Interfaces:**
- Consumes: Task 2–4 的全部改动
- Produces: src-layout 下测试与 lint 全绿

- [ ] **Step 1: 卸载旧 editable 安装并重新 editable 安装**

Run: `uv run pip uninstall -y httpbinx && uv run pip install -e .`
Expected: `Successfully uninstalled httpbinx-1.10.2` 后 `Successfully installed httpbinx-1.11.0`

- [ ] **Step 2: 确认导入路径指向 src/**

Run: `uv run python -c "import httpbinx; print(httpbinx.__file__); print(httpbinx.__version__)"`
Expected: 路径以 `src/httpbinx/__init__.py` 结尾，版本打印 `1.11.0`

- [ ] **Step 3: 确认 static/templates 资源可定位**

Run: `uv run python -c "from httpbinx import helpers, main; print(helpers._templates.directory); print(main.static_dir)"`
Expected: 两个路径分别以 `src/httpbinx/templates` 和 `src/httpbinx/static` 结尾

- [ ] **Step 4: 跑全量测试**

Run: `uv run pytest -q`
Expected: 全部 PASSED，无 failures/errors

- [ ] **Step 5: 跑 ruff**

Run: `uv run ruff check .`
Expected: `All checks passed!`

- [ ] **Step 6: 提交全部改动**

Run:
```bash
git add -A
git status --short
```
Expected: `src/httpbinx/` 下全部为 renamed/modified，`pyproject.toml`、`MANIFEST.in`、`README.md` 为 modified，根 `httpbinx/` 不复存在

Run:
```bash
git commit -m "refactor: migrate to src-layout and bump version to 1.11.0

Move the httpbinx package under src/ to adopt a src-layout, keeping
package internals unchanged. Update pdm-backend package-dir and version
source path, refresh MANIFEST.in and README asset paths accordingly.
Bump __version__ from 1.10.2 to 1.11.0."
```

> 按用户全局偏好，commit message **不附加** `Co-Authored-By` trailer。上面命令已是最终 message（无 trailer）。

Expected: pre-commit 钩子通过，提交成功；`git log --oneline -1` 显示新 commit

---

### Task 6: 构建产物验证（wheel + sdist）

**Files:**
- 无文件改动

**Interfaces:**
- Consumes: Task 5 提交后的仓库
- Produces: 确认打包后数据文件与版本号正确

- [ ] **Step 1: 清理并构建 sdist + wheel**

Run: `rm -rf dist && uv build`
Expected: 输出 `Building source distribution...` 与 `Building wheel...`，`Successfully built dist/httpbinx-1.11.0.tar.gz` 和 `dist/httpbinx-1.11.0-py3-none-any.whl`

- [ ] **Step 2: 列出 wheel 内容，确认数据文件在内**

Run:
```bash
uv run --with unzip python - <<'PY'
import zipfile, glob
whl = glob.glob("dist/*.whl")[0]
print("WHEEL:", whl)
names = zipfile.ZipFile(whl).namelist()
for must in [
    "httpbinx/__init__.py",
    "httpbinx/static/favicon.png",
    "httpbinx/templates/moby.html",
    "httpbinx/templates/sample.xml",
]:
    assert must in names, f"MISSING: {must}"
    print("OK", must)
PY
```
Expected: 打印 `WHEEL: dist/httpbinx-1.11.0-py3-none-any.whl` 与 4 行 `OK ...`，无 AssertionError

- [ ] **Step 3: 确认 METADATA 版本号与入口点**

Run:
```bash
uv run --with unzip python - <<'PY'
import zipfile, glob
whl = glob.glob("dist/*.whl")[0]
data = zipfile.ZipFile(whl).read([n for n in zipfile.ZipFile(whl).namelist() if n.endswith("METADATA")][0]).decode()
for line in data.splitlines():
    if line.startswith("Version:"):
        print(line)
ep = [n for n in zipfile.ZipFile(whl).namelist() if n.endswith("entry_points.txt")]
if ep:
    print(zipfile.ZipFile(whl).read(ep[0]).decode().strip())
PY
```
Expected: 打印 `Version: 1.11.0`，以及 entry_points 内容含 `httpbinx = httpbinx.cli:execute`

- [ ] **Step 4: 确认 sdist 也包含数据文件**

Run:
```bash
uv run --with unzip python - <<'PY'
import tarfile, glob
tgz = glob.glob("dist/*.tar.gz")[0]
members = [m.name for m in tarfile.open(tgz).getmembers()]
for must in [
    "src/httpbinx/static/favicon.png",
    "src/httpbinx/templates/moby.html",
    "src/httpbinx/__init__.py",
    "MANIFEST.in",
]:
    assert must in members, f"MISSING: {must}"
    print("OK", must)
PY
```
Expected: 4 行 `OK ...`，无 AssertionError

- [ ] **Step 5: 不提交构建产物**

Run: `git status --short dist/`
Expected: 无输出（`.gitignore:13` 已忽略 `dist/`，构建产物不会进入暂存区）

> 若意外有输出，`rm -rf dist` 清理后重新 `git status --short dist/` 确认干净。

---

### Task 7: 推送并创建英文 PR

**Files:**
- 无文件改动

**Interfaces:**
- Consumes: Task 5–6 的提交
- Produces: 远端分支与 PR

- [ ] **Step 1: 推送分支**

Run: `git push -u origin feature/src-layout`
Expected: 成功推送，显示分支与 `origin/feature/src-layout` 关联

- [ ] **Step 2: 用 gh 创建 PR（英文）**

Run:
```bash
gh pr create --base main --head feature/src-layout \
  --title "Migrate to src-layout and bump version to 1.11.0" \
  --body "$(cat <<'EOF'
## Summary

- Move the `httpbinx` package from the repo root into `src/httpbinx/` to adopt a src-layout.
- Update `pyproject.toml` (`[tool.pdm]`): add `package-dir = "src"` and point the version source at `src/httpbinx/__init__.py`.
- Refresh `MANIFEST.in` and the README cover image path to match the new `src/httpbinx/` location.
- Bump `__version__` from `1.10.2` to `1.11.0`.

## What does not change

- Build backend stays **pdm-backend**.
- Package internals are untouched (only the version literal changed).
- `Dockerfile` (`COPY . .` + `pip install .` + entry point) is unchanged.
- CI workflows (`check.yml`, `publish.yml`, `image.yml`) are unchanged.
- `tests/` stays at the repo root.

## Verification

- `uv run pytest -q` — all tests pass.
- `uv run ruff check .` — all checks pass.
- `uv build` produces `httpbinx-1.11.0` sdist + wheel; wheel contains `httpbinx/static/favicon.png`, `httpbinx/templates/*`, and `METADATA Version: 1.11.0`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```
Expected: 输出 PR URL，如 `https://github.com/imleowoo/httpbinx/pull/N`

- [ ] **Step 3: 确认 PR 创建成功**

Run: `gh pr view --json number,url,state -q '.number, .url, .state'` 2>/dev/null || gh pr view --json url,state -q '.url + " " + .state'`
Expected: 显示 PR 编号/URL 与 `OPEN`
