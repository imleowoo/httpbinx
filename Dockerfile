FROM python:3.9-alpine

LABEL name="httpbinx"
LABEL version="0.1"
LABEL description="HTTP Request & Response Service, written in Python + FastAPI"

WORKDIR /httpbinx
ADD requirements.txt /httpbinx/
RUN pip install --upgrade pip setuptools &&  \
    pip install --no-cache -r requirements.txt
COPY . /httpbinx
EXPOSE 8000
CMD ["uvicorn", "httpbin.main:app", "--host=0.0.0.0"]
