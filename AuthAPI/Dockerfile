FROM python:3.10

ENV TZ=Europe/Moscow

WORKDIR /src
COPY requirements.txt .

RUN apt-get update && apt-get install -y netcat-traditional

RUN pip install --upgrade pip --no-cache-dir \
     && pip install -r requirements.txt --no-cache-dir

COPY ./entrypoint.sh /
RUN chmod 777 /entrypoint.sh

COPY . /src
ENTRYPOINT ["/entrypoint.sh"]