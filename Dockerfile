FROM python:3.11-slim

WORKDIR /app

# Install uv package manager
RUN pip install --no-cache-dir uv

# Copy requirements and install dependencies using uv
COPY backend/requirements.txt .
RUN uv pip install --no-cache-dir -r requirements.txt --system

# Copy backend code
COPY backend/ .

# Copy .env file
COPY .env .

EXPOSE 8000

CMD ["python", "main.py"]
