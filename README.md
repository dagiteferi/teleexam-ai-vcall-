# TeleExam AI VCall

TeleExam AI VCall is an AI-powered real-time tutoring service designed to help students prepare for the Ethiopian Computer Science Exit Exam. The application combines FastAPI, LangGraph, LiveKit, PostgreSQL with pgvector, and Redis to provide AI-assisted tutoring, real-time communication, curriculum retrieval, and learner session management.

## Prerequisites

Before starting the project, make sure you have:

- Docker Desktop installed and running
- Docker Compose available
- A `.env` file containing the required API keys and configuration values

## Starting the Application

Build the Docker images and start all project services by running:

```bash
docker compose up --build
```

This command starts the following services:

- FastAPI application
- PostgreSQL database with pgvector
- Redis
- LiveKit server

After all containers are running successfully, the API will be available on port **8001**.

## API Documentation

Swagger UI is available at:

```
http://localhost:8001/docs
```

Open this URL in your browser after the application starts. Swagger provides interactive documentation where you can test all available API endpoints, including session creation, learner profile retrieval, and session management.

## Running Tests

Run the unit tests:

```bash
pytest tests/ -m "not integration"
```

Run the integration tests:

```bash
pytest tests/ -m integration
```

The unit tests verify individual components, while the integration tests validate interactions between services such as PostgreSQL, Redis, and the application.

## Curriculum Ingestion

To ingest the curriculum into PostgreSQL and generate vector embeddings for semantic search, run:

```bash
python scripts/ingest_curriculum.py
```

Run this script after the database is available to populate the curriculum used by the AI tutor during question answering.