# Stage 1: Builder (Compile dependencies)
FROM python:3.11-slim-bullseye AS builder

WORKDIR /app

# Install system dependencies needed to compile python packages
# libpq-dev is required to compile psycopg if not using the binary
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
# This is a senior trick: We don't install poetry in the final image to save space.
# We use standard pip with poetry's output.
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes --with dev

# Stage 2: Final (Runtime)
FROM python:3.11-slim-bullseye

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

# Install system runtime dependencies (netcat is for the wait script)
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
RUN chmod +x /entrypoint.sh /start.sh

# Copy source code (although in dev it's overwritten with volumes, this is for prod)
COPY ./app /app

ENTRYPOINT ["/entrypoint.sh"]
