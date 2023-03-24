FROM python:slim

LABEL name="httpbinx"
LABEL version="1.1.0"
LABEL description="HTTP Request & Response Service, written in Python + FastAPI"

COPY . /httpbinx
WORKDIR ./httpbinx
RUN python setup.py install
EXPOSE 8000
CMD ["uvicorn", "httpbinx.main:app", "--host=0.0.0.0"]
