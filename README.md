# TeleExam AI VCall

TeleExam AI VCall is an AI-powered real-time video call tutor for Ethiopian Computer Science Exit Exam preparation. It uses FastAPI, LiveKit, LangGraph, PostgreSQL with pgvector, and Redis to provide interactive tutoring and AI-assisted learning.

## Getting Started

Start all services with Docker:

```bash
docker compose up --build
```

## API Documentation

Swagger UI is available at:

```
http://localhost:8001/docs
```

## Running Tests

Run unit tests:

```bash
pytest tests/ -m "not integration"
```

Run integration tests:

```bash
pytest tests/ -m integration
```

## Curriculum Ingestion

Run the curriculum ingestion script:

```bash
python scripts/ingest_curriculum.py
```
