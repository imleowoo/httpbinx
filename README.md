![httpbinx cover](src/httpbinx/static/images/httpbinx_cover.png)

[![PyPI](https://img.shields.io/pypi/v/httpbinx)](https://pypi.org/project/httpbinx/)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue)](https://pypi.org/project/httpbinx/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![中文文档](https://img.shields.io/badge/Language-%E4%B8%AD%E6%96%87-red)](README.zh.md)

# httpbinx

An HTTP request and response testing service built with Python and FastAPI.
Inspired by [httpbin](https://github.com/postmanlabs/httpbin).

Try the hosted instance at **https://httpbinx.wooe.cc**.

## Install

Requires Python 3.10 or later.

With pip:

```shell
pip install httpbinx
```

With uv:

```shell
uv tool install httpbinx
```

## Run Locally

```shell
httpbinx server --port 8000
```

Open [http://localhost:8000/](http://localhost:8000/) for the interactive API documentation.

## Docker

```shell
docker pull leowoo/httpbinx:latest
docker run --rm -p 8080:80 --name httpbinx leowoo/httpbinx:latest
```

The API documentation is then available at [http://localhost:8080/](http://localhost:8080/).

## CLI

```shell
httpbinx version
httpbinx info
```

## Development

```shell
pytest
ruff check .
ruff format --check .
```

## License

[MIT](LICENSE)
