# 将 httpbinx 改为 src-layout 设计文档

- 日期：2026-07-22
- 分支：`feature/src-layout`
- 构建后端：pdm-backend（保持不变）
- 目标 Python：3.14（开发），CI 矩阵 3.10–3.14

## 1. 背景与目标

当前 httpbinx 项目采用扁平布局（flat layout），包目录 `httpbinx/` 直接位于仓库根。本次工作将其改造为 src-layout：把包目录移入 `src/`，使项目源码与仓库根的其它文件（tests、配置、构建产物）在文件系统层面分离，避免测试时意外从当前工作目录导入未安装的包。

约束：
- 保持构建后端 pdm-backend 不变。
- 保持 CI 工作流、Dockerfile 的安装与运行方式不变。
- 保持包内代码零改动。
- 保持测试目录位置不变（仍为顶层 `tests/`）。

## 2. 现状摘要

```
httpbinx/                       # 仓库根
├── httpbinx/                   # 包目录（flat）
│   ├── __init__.py             # __version__ = '1.10.2'
│   ├── cli.py                  # entry: httpbinx = "httpbinx.cli:execute"
│   ├── main.py                 # Path(__file__).parent / 'static'
│   ├── helpers.py              # Path(__file__).parent / 'templates' / 'static' / 'bombs'
│   ├── constants.py, meta.py, schemas.py
│   ├── routers/ (含 inspection/)
│   ├── static/ (favicon、images、bombs、UTF-8-demo.txt)
│   ├── templates/ (moby.html, sample.xml)
│   └── examples/
├── tests/                      # __init__.py + conftest.py + 各路由测试
├── pyproject.toml              # [tool.pdm] version path = "httpbinx/__init__.py"
├── Dockerfile                  # COPY . . && pip install . && CMD httpbinx server
├── MANIFEST.in                # recursive-include httpbinx *
└── .github/workflows/         # check.yml(pip install . + pytest + ruff), publish.yml(python -m build), image.yml
```

路径敏感代码（均位置无关，搬入 src 后仍有效；`__file__` 指向 `src/httpbinx/<module>.py`，`.parent` 即 `src/httpbinx/`）：
- `httpbinx/helpers.py:15` `_templates = Jinja2Templates(directory=str(Path(__file__).parent / 'templates'))`
- `httpbinx/helpers.py:17` `_images_path = Path(__file__).parent / 'static' / 'images'`
- `httpbinx/helpers.py:19` `_bomb_files_path = Path(__file__).parent / 'static' / 'bombs'`
- `httpbinx/main.py:27` `static_dir = Path(__file__).parent / 'static'`

版本来源：`httpbinx/__init__.py` 中 `__version__ = '1.10.2'`。

## 3. 探针验证结论

在临时目录用 `uv build` 实测 pdm-backend 的 src 配置，确认：

1. `[tool.pdm]` 下 `package-dir = "src"` 生效，wheel 中包路径正确映射为 `httpbinx/...`。
2. 版本来源 `version = { source = "file", path = "src/httpbinx/__init__.py" }` 正确读出 `1.10.2` 并写入 `METADATA`。
3. `src/httpbinx/static/`、`templates/` 等数据文件被 pdm-backend 默认递归打包进 wheel，无需额外声明。

## 4. 方案选择

- **方案 A（采用）**：`git mv httpbinx src/httpbinx` + 配置改动，零代码改动。
- 方案 B：迁移 + 换构建后端为 hatchling——无必要的连带改动，否决。
- 方案 C：迁移 + 在 conftest 里 hack `sys.path`——src-layout 反模式，否决。

## 5. 目标布局

```
httpbinx/                       # 仓库根
├── src/
│   └── httpbinx/               # 原 httpbinx/ 整体搬入，内部结构不变
│       ├── __init__.py
│       ├── cli.py, main.py, helpers.py, constants.py, meta.py, schemas.py
│       ├── routers/ (含 inspection/)
│       ├── static/, templates/, examples/
├── tests/                      # 位置不变
├── pyproject.toml, Dockerfile, MANIFEST.in, README.md
└── .github/workflows/
```

`tests/` 保留在根目录（pytest 社区惯例，且 `tests/__init__.py` 仍存在）。

## 6. 改动清单

### 6.1 移动包
- `git mv httpbinx src/httpbinx`（保留 git 历史）。需先 `mkdir -p src`。

### 6.2 `pyproject.toml`
- `[tool.pdm]` 增加 `package-dir = "src"`。
- version 路径由 `httpbinx/__init__.py` 改为 `src/httpbinx/__init__.py`。
- 其余不变：`[project.scripts] httpbinx = "httpbinx.cli:execute"`（入口点用已安装包名，与位置无关）、`distribution = true`。

> `[project.scripts] httpbinx = "httpbinx.cli:execute"` 中的 `httpbinx.cli` 指已安装包的模块路径，与磁盘上 `src/httpbinx` 无关，无需改动。

### 6.3 `MANIFEST.in`
- `recursive-include httpbinx *` → `recursive-include src/httpbinx *`。MANIFEST.in 的模式按相对仓库根的文件系统路径匹配，移动后根目录不再有 `httpbinx/`，需更新为 `src/httpbinx/` 才能保留其原本对 sdist 的显式包含意图。即便不更新，pdm-backend 仍会自动把 `src/httpbinx/` 下数据文件打入 wheel（探针已验证），但保持 manifest 与实际路径一致是正确的维护。

### 6.4 `README.md`
- 第 1 行两处 GitHub raw 图片路径：`httpbinx/static/...` → `src/httpbinx/static/...`（这是仓库内真实文件路径，随移动而变）。

### 6.5 `Dockerfile`
- `COPY . .` + `pip install .` + `CMD ["httpbinx", "server", ...]` 不动。安装时按 `package-dir` 解析，运行走 entry point。

### 6.6 CI（`.github/workflows/`）
- `check.yml`：`pip install .` + `pytest` + `ruff check .` 不动。`pip install .`（非 editable）将 `httpbinx` 装入 site-packages，`from httpbinx import app` 命中已安装包。
- `publish.yml`：`python -m build` 不动。
- `image.yml`：Docker 构建上下文不变。

### 6.7 代码
- 零改动。`helpers.py`/`main.py` 的 `Path(__file__).parent / ...` 在新位置仍指向 `src/httpbinx/static` 与 `templates`。

### 6.8 可选加固
- `pyproject.toml` 增加：
  ```toml
  [tool.pytest.ini_options]
  testpaths = ["tests"]
  ```
  仅约束测试发现路径，不影响 import 解析（import 仍靠安装的包）。**决定不引入**：当前 CI 与本地均依赖先 `pip install .` 再跑 pytest，testpaths 对此无额外收益，保持现状以减少配置面。

## 7. 验证步骤（构建 + 测试都跑）

1. 恢复开发环境：`uv venv --python 3.14 .venv && uv sync`。
2. 安装包：`uv run pip install -e .`（或 `uv run pip install .`）。
3. 测试：`uv run pytest` 全量通过。
4. Lint：`uv run ruff check .` 通过。
5. 构建：`uv build` 产出 sdist + wheel。
6. 解包验证 wheel：
   - `httpbinx/__init__.py`、`httpbinx/static/favicon.png`、`httpbinx/templates/moby.html`、`httpbinx/templates/sample.xml` 均在 wheel 内；
   - `*.dist-info/METADATA` 中 `Version: 1.10.2`；
   - `*.dist-info/entry_points.txt` 含 `httpbinx = httpbinx.cli:execute`。
7. （可选）`docker build` 验证镜像可构建并启动。

## 8. 不在范围内

- 不更换构建后端。
- 不调整 routers 内部结构。
- 不修改测试代码本身。
- 不修改 `.github` 里的安装步骤。
- pre-commit、ruff 规则不变。

## 9. 完成定义

- `src/httpbinx/` 存在且包含原包全部内容；根目录 `httpbinx/` 不复存在。
- `pyproject.toml` 含 `package-dir = "src"` 与 version 路径 `src/httpbinx/__init__.py`。
- 第 7 节验证全部通过。
- 产出英文 commit message 与英文 PR。
