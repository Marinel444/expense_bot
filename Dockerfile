FROM python:3.11-slim


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
WORKDIR /app


ENV PYTHONUNBUFFERED=1

CMD ["python", "-m", "bot.main"]

