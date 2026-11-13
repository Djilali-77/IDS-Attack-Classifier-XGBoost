FROM python:3.11-slim

WORKDIR /app

# libgomp is needed by XGBoost at runtime
RUN apt-get update && apt-get install -y --no-install-recommends build-essential libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# api.py sits in the backend root, so the app is "api:app"
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]