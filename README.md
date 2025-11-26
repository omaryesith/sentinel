# Sentinel - Distributed Synthetic Monitoring System

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0-green.svg)](https://www.djangoproject.com/)
[![CI](https://github.com/omaryesith/sentinel/actions/workflows/ci.yml/badge.svg)](https://github.com/omaryesith/sentinel/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Sentinel is a **distributed synthetic monitoring platform** designed to verify the availability and latency of web services in real-time. Monitor your critical endpoints with automated health checks, track performance metrics, and get instant insights into your service reliability.

Built with a focus on **Clean Architecture**, **Horizontal Scalability**, and **Observability**.

---

## ✨ Features

- 🔄 **Automated Monitoring**: Scheduled health checks every minute via Celery Beat
- ⚡ **Asynchronous Processing**: Non-blocking HTTP requests using Celery workers
- 📊 **Performance Tracking**: Store and query latency metrics over time
- 🎯 **RESTful API**: Clean, schema-driven API with Django Ninja
- 📈 **Real-time Observability**: Monitor task queues with Flower dashboard
- 🐳 **Fully Dockerized**: Reproducible development and deployment environment
- 🔍 **Automatic Documentation**: Interactive API docs with Swagger UI
- 💾 **Persistent Storage**: PostgreSQL for reliable data persistence
- 🔄 **CI/CD Pipeline**: Automated testing with GitHub Actions

---

## 🏗 Architecture

The system follows a **microservices pattern** orchestrated via Docker:

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Client    │─────▶│  Django API  │─────▶│ PostgreSQL  │
└─────────────┘      └──────────────┘      └─────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │    Redis     │
                     │   (Broker)   │
                     └──────────────┘
                            │
                ┌───────────┴───────────┐
                ▼                       ▼
         ┌─────────────┐         ┌─────────────┐
         │Celery Worker│         │ Celery Beat │
         │   (Tasks)   │         │ (Scheduler) │
         └─────────────┘         └─────────────┘
```

### Components

- **API Gateway & Management**: Python 3.11 + Django 5 + Django Ninja (Schema-driven development)
- **Asynchronous Workers**: Celery Workers for non-blocking execution of I/O tasks (HTTP Pings)
- **Scheduling**: Celery Beat for cronjob orchestration (automatic monitoring every minute)
- **Persistence**: PostgreSQL 15 (Relational data) and Redis 7 (Message broker & Result backend)
- **Observability**: Flower for queue monitoring and worker throughput

---

## 🚀 Quick Start

The project is fully dockerized to ensure a reproducible development environment.

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) (v20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) (v2.0+)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/omaryesith/sentinel.git
   cd sentinel
   ```

2. **Configure environment variables:**

   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Setup the entire project (recommended):**

   This will build containers, start services, run migrations, and create a superuser:

   ```bash
   make setup
   ```

   Or do it step by step:

   ```bash
   # Build containers
   make build

   # Start services
   make up

   # Run migrations
   make migrate

   # Create superuser (optional)
   docker compose exec web python manage.py createsuperuser
   ```

### Access the Services

- **API & Documentation (Swagger)**: http://localhost:8000/api/docs
- **Django Admin Panel**: http://localhost:8000/admin
- **Worker Monitor (Flower)**: http://localhost:5555

---

## 🧪 API Usage

### 1. Register a Domain

Register a new domain/endpoint to monitor:

```bash
POST /api/domains/
```

**Request Body:**
```json
{
  "name": "Production API",
  "url": "https://api.example.com",
  "is_active": true
}
```

**Response:**
```json
{
  "id": 1,
  "name": "Production API",
  "url": "https://api.example.com",
  "is_active": true,
  "created_at": "2025-11-26T01:00:00Z"
}
```

### 2. List All Domains

```bash
GET /api/domains/
```

### 3. Get Domain Details

```bash
GET /api/domains/{id}
```

### 4. Trigger Manual Check

Manually trigger a health check for a specific domain:

```bash
POST /api/monitoring/{id}/check
```

**Response:**
```json
{
  "message": "Check dispatched successfully",
  "task_id": "abc123-def456-ghi789",
  "domain": "Production API"
}
```

_Dispatches an asynchronous task to the Redis queue._

### 5. View Latency History

Query the performance history for a domain:

```bash
GET /api/monitoring/{id}/history
```

**Response:**
```json
[
  {
    "id": 1,
    "domain_id": 1,
    "checked_at": "2025-11-26T01:00:00Z",
    "latency_ms": 245.67,
    "status_code": 200,
    "is_success": true,
    "error_message": null
  }
]
```

_Returns the last 50 ping results._

---

## 📁 Project Structure

```
sentinel/
├── .github/                  # GitHub configuration
│   └── workflows/            # CI/CD workflows
│       └── ci.yml            # Automated testing pipeline
├── app/                      # Django application
│   ├── core/                 # Project settings and configuration
│   │   ├── settings.py       # Django settings
│   │   ├── celery.py         # Celery configuration
│   │   └── urls.py           # URL routing
│   ├── domains/              # Domain management app
│   │   ├── models.py         # Domain model
│   │   ├── api.py            # Domain API endpoints
│   │   └── schemas.py        # Pydantic schemas
│   └── monitoring/           # Monitoring app
│       ├── models.py         # PingResult model
│       ├── api.py            # Monitoring API endpoints
│       ├── tasks.py          # Celery tasks
│       ├── services.py       # Business logic
│       └── schemas.py        # Pydantic schemas
├── docker/                   # Docker configuration
│   └── django/
│       ├── Dockerfile        # Django container
│       └── start.sh          # Startup script
├── docker-compose.yml        # Service orchestration
├── Makefile                  # Development shortcuts
├── pyproject.toml            # Python dependencies (Poetry)
├── .env.example              # Environment variables template
└── README.md                 # This file
```

---

## 🔧 Environment Variables

Create a `.env` file in the root directory with the following variables:

```bash
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
POSTGRES_DB=sentinel
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Redis Configuration
REDIS_URL=redis://redis:6379/0
```

---

## 🛠 Development

### Available Make Commands

The project includes a Makefile with convenient shortcuts:

```bash
make help          # Show all available commands
make setup         # Build and initialize everything from scratch
make build         # Build Docker containers
make up            # Start services in background
make down          # Stop all services
make logs          # Show real-time logs
make test          # Run test suite
make shell         # Open Django shell
make migrate       # Run database migrations
make makemigrations # Create new migrations
make clean         # Clean pycache and volumes
```

### Running Tests

```bash
# Using Makefile (recommended)
make test

# Or directly with docker compose
docker compose run --rm web pytest
```

### Accessing the Django Shell

```bash
# Using Makefile
make shell

# Or directly
docker compose exec web python manage.py shell
```

### Viewing Logs

```bash
# All services (using Makefile)
make logs

# All services (docker compose)
docker compose logs -f

# Specific service
docker compose logs -f web
docker compose logs -f celery_worker
docker compose logs -f celery_beat
```

### Stopping Services

```bash
make down
```

### Rebuilding Containers

```bash
make build
make up
```

---

## 🔄 Continuous Integration

The project uses **GitHub Actions** for automated testing on every push and pull request to the `main` branch.

### CI Workflow

The CI pipeline automatically:

1. ✅ Checks out the code
2. 🏗️ Builds all Docker services
3. 🚀 Starts the service cluster
4. ⏳ Waits for database initialization
5. 🧪 Runs the test suite
6. 🧹 Tears down the environment

View the workflow configuration at [`.github/workflows/ci.yml`](.github/workflows/ci.yml)

### Running CI Locally

You can run the same CI steps locally:

```bash
make build
make up
make test
make down
```

---

## ⚙️ Technology Stack

| Category | Technology |
|----------|-----------|
| **Backend** | Python 3.11, Django 5.0 |
| **API Framework** | Django Ninja (Pydantic v2) |
| **Task Queue** | Celery 5.3 |
| **Scheduler** | Celery Beat |
| **Database** | PostgreSQL 15 (Driver: Psycopg 3) |
| **Broker** | Redis 7 |
| **HTTP Client** | HTTPX (Async ready) |
| **Monitoring** | Flower |
| **Containerization** | Docker Multi-stage builds |
| **Dependency Management** | Poetry |

---

## � Deployment

### Production Considerations

1. **Environment Variables**: Set `DEBUG=False` and use a strong `SECRET_KEY`
2. **Database**: Use managed PostgreSQL service (AWS RDS, Google Cloud SQL, etc.)
3. **Redis**: Use managed Redis service (AWS ElastiCache, Redis Cloud, etc.)
4. **Static Files**: Configure static file serving with WhiteNoise or CDN
5. **HTTPS**: Use a reverse proxy (Nginx) with SSL certificates
6. **Monitoring**: Set up application monitoring (Sentry, DataDog, etc.)
7. **Scaling**: Scale Celery workers horizontally based on load

### Docker Production Build

```bash
docker-compose -f docker-compose.prod.yml up -d
```

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## �👨‍💻 Author

**Omar Alvarado**  
Senior Backend Engineer  
📧 [omarjesith@gmail.com](mailto:omarjesith@gmail.com)  
🔗 [GitHub](https://github.com/omaryesith)

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/omaryesith/sentinel/issues).

---

## 🙏 Acknowledgments

- Built with [Django](https://www.djangoproject.com/)
- API powered by [Django Ninja](https://django-ninja.rest-framework.com/)
- Task processing by [Celery](https://docs.celeryq.dev/)
- Inspired by modern observability platforms
