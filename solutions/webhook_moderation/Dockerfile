FROM ubuntu:focal

RUN groupadd -r webhook && useradd --no-log-init -r -m -g webhook webhook

RUN apt-get update && apt-get -y upgrade && apt-get --no-install-recommends -y install \
    python3 \
    python3-pip \
     --no-install-recommends

RUN pip3 install flask gunicorn boonsdk PyJWT slack_sdk

RUN mkdir /app
WORKDIR /app

COPY ./webhook.py .

USER webhook
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 webhook:app
