# fastapi-httpbin
HTTP Request &amp; Response Service, written in Python + FastAPI.

## Reference project

A  [Kenneth Reitz](http://kennethreitz.org/bitcoin) Project. See https://github.com/postmanlabs/httpbin

## Quick Start

### Run directly

```shell
$ uvicorn httpbin.main:app --host=0.0.0.0 --port=80
```

### Run with Docker

```shell
$ docker pull leowoo/fastapi-httpbin:latest
$ docker run -d -p 80:8000 --name fastapi-httpbin leowoo/fastapi-httpbin:latest
```
