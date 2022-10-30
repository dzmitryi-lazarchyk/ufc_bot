FROM python:3.9
ENV BOT_NAME=$BOT_NAME

WORKDIR app/

COPY requirements.txt app/requirements.txt
RUN pip install -r app/requirements.txt
ADD . .



