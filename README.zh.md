![httpbinx 封面](src/httpbinx/static/images/httpbinx_cover.png)

[![PyPI](https://img.shields.io/pypi/v/httpbinx)](https://pypi.org/project/httpbinx/)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue)](https://pypi.org/project/httpbinx/)
[![许可证](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![English](https://img.shields.io/badge/Language-English-blue)](README.md)

# httpbinx

基于 Python 和 FastAPI 构建的 HTTP 请求与响应测试服务。
灵感来自 [httpbin](https://github.com/postmanlabs/httpbin)。

可访问已部署实例：**https://httpbinx.wooe.cc**。

## 安装

需要 Python 3.10 或更高版本。

使用 pip：

```shell
pip install httpbinx
```

使用 uv：

```shell
uv tool install httpbinx
```

## 本地运行

```shell
httpbinx server --port 8000
```

在浏览器中打开 [http://localhost:8000/](http://localhost:8000/) 查看交互式 API 文档。

## Docker

```shell
docker pull leowoo/httpbinx:latest
docker run --rm -p 8080:80 --name httpbinx leowoo/httpbinx:latest
```

随后可在 [http://localhost:8080/](http://localhost:8080/) 访问 API 文档。

## 命令行工具

```shell
httpbinx version
httpbinx info
```

## 开发

```shell
pytest
ruff check .
ruff format --check .
```

## 许可证

[MIT](LICENSE)
