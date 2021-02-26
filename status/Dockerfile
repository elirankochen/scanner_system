
FROM python:alpine

EXPOSE 5002

WORKDIR /status

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "status.py"]
