FROM python:3.9
ENV BOT_NAME=$BOT_NAME

WORKDIR ufc_bot/

COPY requirements.txt ufc_bot/requirements.txt
RUN pip install -r ufc_bot/requirements.txt
ADD . .

EXPOSE 80/tcp



