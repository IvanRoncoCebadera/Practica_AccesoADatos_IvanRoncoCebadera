FROM python:alpine3.19

WORKDIR /usr/src/app

COPY requirements.txt ./
COPY src/.env ./

RUN apk --no-cache add mariadb-connector-c-dev gcc musl-dev
RUN pip install --no-cache-dir -r requirements.txt

COPY src .

CMD [ "python", "./app.py" ]