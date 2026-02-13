FROM python:3.14-slim

LABEL name="httpbinx" \
      description="HTTP Request & Response Service, written in Python + FastAPI"

WORKDIR /httpbinx
COPY . .
RUN python -m pip install --no-cache-dir .
RUN rm -rf /httpbinx
EXPOSE 80
CMD ["httpbinx", "server", "--host=0.0.0.0", "--port=80"]
