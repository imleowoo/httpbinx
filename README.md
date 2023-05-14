![cover](httpbinx/static/images/httpbinx_cover.png)

# httpbinx
HTTP Request & Response Service, written in Python + FastAPI.

## Reference project

A  [Kenneth Reitz](http://kennethreitz.org/bitcoin) Project. See https://github.com/postmanlabs/httpbin

## Quick Start

### Run directly

```shell
$ python setup.py install
$ uvicorn httpbinx:app --host=0.0.0.0 --port=80
```

### Run with Docker

```shell
$ docker pull leowoo/httpbinx:latest
$ docker run -p 80:80 --name httpbinx leowoo/httpbinx:latest
```
