# Etapa 1: Builder (Compilar dependencias)
FROM python:3.11-slim-bullseye as builder

WORKDIR /app

# Instalar dependencias de sistema necesarias para compilar python packages
# libpq-dev es necesario para compilar psycopg si no se usa el binario
RUN apt-get update && apt-get install -y \
  build-essential \
  libpq-dev \
  && rm -rf /var/lib/apt/lists/*

# Instalar Poetry
RUN pip install --upgrade pip
RUN pip install poetry==1.8

# Copiar archivos de configuración de poetry
COPY ./pyproject.toml ./poetry.lock* /app/

# Exportar requirements.txt. 
# Esto es un truco de Senior: No instalamos poetry en la imagen final para ahorrar espacio.
# Usamos pip standard con el output de poetry.
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# Etapa 2: Final (Runtime)
FROM python:3.11-slim-bullseye

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

# Instalar dependencias de runtime del sistema (netcat es para el script de espera)
RUN apt-get update && apt-get install -y \
  libpq5 \
  netcat \
  && rm -rf /var/lib/apt/lists/*

# Copiar requirements desde el builder
COPY --from=builder /app/requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar scripts de arranque y dar permisos
COPY ./docker/django/entrypoint.sh /entrypoint.sh
COPY ./docker/django/start.sh /start.sh
RUN chmod +x /entrypoint.sh /start.sh

# Copiar el código fuente (aunque en dev se sobreescribe con volumenes, esto es para prod)
COPY ./app /app

ENTRYPOINT ["/entrypoint.sh"]
