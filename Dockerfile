FROM python:3.10.9

WORKDIR /rare-hashes-bot

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY main.py .
COPY database_operation.py .
COPY command_operation.py .
COPY telegram_utils.py .
COPY notification.py .
COPY .env .
COPY users_data.txt .

CMD ["python", "-u", "main.py"]