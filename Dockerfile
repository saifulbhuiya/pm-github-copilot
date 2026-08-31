FROM node:22-alpine AS frontend-builder

WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm ci

COPY frontend/ .
RUN npm run build

FROM python:3.11-slim

WORKDIR /app

# Install uv package manager
RUN pip install --no-cache-dir uv

# Copy requirements and install dependencies using uv
COPY backend/requirements.txt .
RUN uv pip install --no-cache-dir -r requirements.txt --system

# Copy backend code
COPY backend/ .

# Copy built frontend from builder stage (exported to out directory)
COPY --from=frontend-builder /app/frontend/out ../frontend/out

# Copy .env file
COPY .env .

EXPOSE 8000

CMD ["python", "main.py"]
