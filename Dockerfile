FROM mcr.microsoft.com/playwright/python:v1.61.0-noble
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["sh", "-c", "python -m backend.database.init_db && uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-10000}"]