# Stage 1: Builder (Compile dependencies)
FROM python:3.11-slim-bullseye AS builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
  build-essential \
  libpq-dev \
  && rm -rf /var/lib/apt/lists/*

# Instalar Poetry
RUN pip install --upgrade pip
RUN pip install poetry==1.8

# Copy poetry configuration files
COPY ./pyproject.toml ./poetry.lock* /app/

# Export requirements.txt. 
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes --with dev

# Stage 2: Final (Runtime)
FROM python:3.11-slim-bullseye

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

# Install system runtime dependencies
RUN apt-get update && apt-get install -y \
  libpq5 \
  netcat \
  && rm -rf /var/lib/apt/lists/*

# Copy requirements from builder
COPY --from=builder /app/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy startup scripts and grant permissions
COPY ./docker/django/entrypoint.sh /entrypoint.sh
COPY ./docker/django/start.sh /start.sh
COPY ./docker/django/start-prod.sh /start-prod.sh
RUN chmod +x /entrypoint.sh /start.sh /start-prod.sh

# Copy source code
COPY ./app /app

ENTRYPOINT ["/entrypoint.sh"]
