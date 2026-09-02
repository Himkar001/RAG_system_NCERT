FROM python:3.10-slim

WORKDIR /app

# Install system dependencies if required (e.g. for building C-extensions)
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

COPY requirements_prod.txt .
RUN pip install --no-cache-dir -r requirements_prod.txt

# Copy backend logic
COPY backend/ ./backend/
# Copy processed data so the API can serve static images from data/processed/rendered_pages
COPY data/ ./data/

EXPOSE 8000

CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
