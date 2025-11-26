# Sentinel - Distributed Synthetic Monitoring System

Sentinel is a distributed synthetic monitoring platform designed to verify the availability and latency of web services in real-time.

Built with a focus on **Clean Architecture**, **Horizontal Scalability**, and **Observability**.

## 🏗 Architecture

The system follows a microservices pattern orchestrated via Docker:

- **API Gateway & Management:** Python 3.11 + Django 5 + **Django Ninja** (Schema-driven development).
- **Asynchronous Workers:** Celery Workers for non-blocking execution of I/O tasks (HTTP Pings).
- **Scheduling:** Celery Beat for cronjob orchestration (automatic monitoring every minute).
- **Persistence:** PostgreSQL 15 (Relational data) and Redis 7 (Message broker & Result backend).
- **Observability:** Flower for queue monitoring and worker throughput.

## 🚀 Quick Start

The project is fully dockerized to ensure a reproducible development environment.

### Prerequisites

- Docker & Docker Compose

### Installation

1.  Clone the repository:

    ```bash
    git clone [https://github.com/tu-usuario/sentinel.git](https://github.com/tu-usuario/sentinel.git)
    cd sentinel
    ```

2.  Start the service cluster:

    ```bash
    docker-compose up --build
    ```

3.  Access the services:
    - **API & Documentation (Swagger):** [http://localhost:8000/api/docs](http://localhost:8000/api/docs)
    - **Worker Monitor (Flower):** [http://localhost:5555](http://localhost:5555)

## 🧪 API Usage

### 1. Register a Domain

`POST /api/domains/`

```json
{
  "name": "Production API",
  "url": "[https://api.tudominio.com](https://api.tudominio.com)"
}
```

### 2. Trigger Manual Check

`POST /api/monitoring/{id}/check`
_Dispatches an asynchronous task to the Redis queue._

### 3. View Latency History

`GET /api/monitoring/{id}/history`
_Queries the time series of stored results._

## ⚙️ Technology Stack

- **Backend:** Python 3.11, Django 5.0
- **API Framework:** Django Ninja (Pydantic v2)
- **Task Queue:** Celery 5.3
- **Database:** PostgreSQL 15 (Driver: Psycopg 3)
- **Broker:** Redis 7
- **HTTP Client:** HTTPX (Async ready)
- **Containerization:** Docker Multi-stage builds

## 👨‍💻 Author

Omar Alvarado [omarjesith@gmail.com] - Senior Backend Engineer
