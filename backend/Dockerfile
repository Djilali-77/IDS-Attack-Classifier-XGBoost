FROM python:3.11-slim

WORKDIR /app

# Install system dependencies that might be needed by some python packages (especially XGBoost/Scikit-Learn)
RUN apt-get update && apt-get install -y --no-install-recommends     build-essential     libgomp1     && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# We use api.main_api because your file is api/main_api.py based on earlier context
CMD ["uvicorn", "api.main_api:app", "--host", "0.0.0.0", "--port", "8000"]
