![![cover](httpbinx/static/images/httpbinx_cover.png)](https://raw.githubusercontent.com/imleowoo/httpbinx/main/httpbinx/static/images/httpbinx_cover.png)

[![thanks](https://img.shields.io/badge/thanks-httpbin-green)](https://github.com/postmanlabs/httpbin)
![python](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-blue)

# httpbinx

HTTP Request & Response Service, written in Python + FastAPI.

## Reference project

A  [Kenneth Reitz](http://kennethreitz.org/bitcoin) Project. See https://github.com/postmanlabs/httpbin

## Quick Start

## Installation

### PyPI

**[httpbinx](https://pypi.org/project/httpbinx/)** is available on PyPI

```shell
$ pip install httpbinx
```

### Source Code

```shell
$ git clone https://github.com/imleowoo/httpbinx.git
$ python setup.py install # or `pip install .`
```

## Run it

### Run directly

```shell
$ httpbinx server --host=0.0.0.0 --port=80
```

### Run with Docker

```shell
$ docker pull leowoo/httpbinx:latest
$ docker run -p 80:80 --name httpbinx leowoo/httpbinx:latest
```

### It starts running

```text
INFO:     Started server process [17044]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:80 (Press CTRL+C to quit)
...
```
