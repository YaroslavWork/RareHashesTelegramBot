FROM python:3.13

WORKDIR /rare-hashes-bot

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY main.py .
COPY .env .
COPY users_id.txt .

CMD ["python", "./main.py"]