
FROM python:alpine

EXPOSE 5000

WORKDIR /ingest

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "ingest.py"]
