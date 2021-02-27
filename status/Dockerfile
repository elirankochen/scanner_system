
FROM python:alpine

EXPOSE 5002

ENV FLASK_RUN_HOST=0.0.0.0

WORKDIR /status

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

COPY requirements.txt .
COPY status_logic.py /status

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "status.py"]
