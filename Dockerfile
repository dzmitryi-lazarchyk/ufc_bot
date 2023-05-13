FROM python:3.9-bullseye

COPY . /src
WORKDIR src/

COPY requirements.txt /src
RUN pip install -r requirements.txt

EXPOSE 80

CMD ["python", "-b", "0.0.0.0:80", "src:bot"]

