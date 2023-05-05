FROM python:3.10-slim

LABEL name="httpbinx"
LABEL description="HTTP Request & Response Service, written in Python + FastAPI"

COPY . /httpbinx
WORKDIR /httpbinx
RUN python -m pip install .
EXPOSE 8000
CMD ["uvicorn", "httpbinx:app", "--host=0.0.0.0"]
