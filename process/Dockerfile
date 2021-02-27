
FROM python:alpine

EXPOSE 5001

WORKDIR /process

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

COPY requirements.txt .
COPY process.py /process

RUN pip install -r requirements.txt

COPY . .


CMD ["python", "process.py"]

