FROM python:slim

LABEL name="httpbinx"
LABEL description="HTTP Request & Response Service, written in Python + FastAPI"

WORKDIR /httpbinx
COPY . .
RUN python -m pip install .
RUN rm -rf /httpbinx
EXPOSE 80
CMD ["uvicorn", "httpbinx:app", "--host=0.0.0.0", "--port=80"]
