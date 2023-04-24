FROM python:3.9

COPY . /src
WORKDIR src/

COPY requirements.txt /src
RUN pip install -r requirements.txt
CMD [ "python", "./bot.py"]

EXPOSE 80



