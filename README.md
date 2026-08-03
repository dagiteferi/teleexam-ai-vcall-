# TeleExam AI — Video Call Tutor

A real-time AI tutoring backend for Ethiopian computer science exit-exam preparation. The project combines FastAPI, WebSockets, Postgres with pgvector, Redis caching, LangGraph orchestration, and LiveKit media sessions to deliver a tutoring experience where each student turn is classified, enriched with curriculum retrieval, and answered with an AI tutor response.

> [!NOTE]
> This repository contains the backend service and AI orchestration layer. It does not include a frontend client or mobile app.

---

## Badges

![License](https://img.shields.io/badge/license-MIT%20(recommended)-blue?style=for-the-badge)
![GitHub stars](https://img.shields.io/github/stars/dagiteferi/teleexam-ai-vcall-?style=for-the-badge)
![GitHub forks](https://img.shields.io/github/forks/dagiteferi/teleexam-ai-vcall-?style=for-the-badge)
![GitHub issues](https://img.shields.io/github/issues/dagiteferi/teleexam-ai-vcall-?style=for-the-badge)
![Last commit](https://img.shields.io/github/last-commit/dagiteferi/teleexam-ai-vcall-?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-supported-2496ED?logo=docker&logoColor=white)
![CI](https://img.shields.io/badge/CI-not%20configured-lightgrey)

---

## Table of Contents

- [Project Title](#teleexam-ai--video-call-tutor)
- [Badges](#badges)
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Running the Project](#running-the-project)
- [API Documentation](#api-documentation)
- [Database](#database)
- [AI Components](#ai-components)
- [Configuration](#configuration)
- [Security](#security)
- [Testing](#testing)
- [Deployment](#deployment)
- [Development Workflow](#development-workflow)
- [Performance Considerations](#performance-considerations)
- [Troubleshooting](#troubleshooting)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

## Features

- Real-time tutoring session lifecycle with Postgres-backed session tracking
- FastAPI HTTP API for session start/end and learner profiles
- WebSocket-based live interaction at `/vcall/ws/{session_id}`
- LangGraph-based intent routing for:
  - concept search
  - YouTube lookup
  - YouTube summary
  - exam-question RAG
  - memory/profile lookup
  - general tutoring
- Redis caching for intent classification, conversation state, RAG hits, and learner profiles
- Curriculum ingestion pipeline that reads local text materials and stores embeddings in Postgres via pgvector
- Vector similarity search over curriculum chunks using cosine distance
- Learner profiling with weak topics, average score, and exam count
- Built-in admin ingestion endpoint for curriculum loading
- LiveKit room creation and participant token issuance
- Extensible provider architecture via ports and adapters for LLM, STT, TTS, embeddings, search, and media

---

## Architecture

This project follows a layered, adapter-based architecture with clear separation between domain logic, application use cases, ports, and infrastructure implementations.

### Overall design

- Inbound adapters:
  - `app/adapters/inbound/http/`
  - `app/adapters/inbound/ws/`
- Application services:
  - `app/application/`
- Agent orchestration:
  - `app/agents/`
- Domain models:
  - `app/domain/models.py`
- Core infrastructure:
  - `app/core/`
- Outbound adapters:
  - `app/adapters/outbound/`
- Ports:
  - `app/ports/`

### Design patterns

- Hexagonal/ports-and-adapters pattern
- Dependency injection through `app/core/di.py`
- Repository pattern for database access
- Strategy/adapter pattern for AI providers
- LangGraph state machine for multi-step agent orchestration
- Cache-aside pattern using Redis

### Layers

1. HTTP and WebSocket entrypoints
   - `app/main.py`
   - `app/adapters/inbound/http/*`
   - `app/adapters/inbound/ws/websocket.py`

2. Application services
   - `start_call_session.py`
   - `end_call_session.py`
   - `process_turn.py`
   - `ingest_curriculum.py`

3. Domain models
   - `CallSession`
   - `Turn`
   - `LearnerProfile`
   - `CurriculumChunk`

4. Infrastructure adapters
   - LLM: Groq
   - STT: AssemblyAI
   - TTS: Cartesia
   - Embeddings: Voyage AI
   - Search: Tavily
   - Cache: Redis
   - Media: LiveKit
   - Database: Postgres + pgvector

### Request flow

A typical tutoring request follows this path:

1. A client starts a session with `POST /vcall/sessions/start`
2. The service creates a record in PostgreSQL and a LiveKit room
3. A WebSocket connection is opened at `/vcall/ws/{session_id}`
4. The client sends a transcript message
5. `process_turn()` loads or creates the session state in Redis
6. `CALL_GRAPH` routes the transcript through `supervisor -> agent -> synthesizer`
7. The answer is stored as a `Turn` in Postgres and the new state is cached in Redis
8. The response is sent back over the WebSocket

### Data flow

- Chat transcript enters the WebSocket handler
- `process_turn()` sets the transcript in `AgentState`
- The supervisor classifies intent with structured LLM output
- Based on intent:
  - `curriculum_agent` performs RAG using pgvector
  - `search_agent` performs web search
  - `memory_agent` loads learner profile
  - `youtube_*` nodes handle video lookups/summaries
- `synthesizer` assembles response context and streams the final answer through the LLM and TTS layers

---

## Tech Stack

| Language | Framework | Purpose |
| --- | --- | --- |
| Python 3.11 | FastAPI | Application API and WebSocket server |
| Python 3.11 | SQLAlchemy 2.0 | Async ORM for Postgres access |
| Python 3.11 | Alembic | Database schema migrations |
| Python 3.11 | LangGraph | Agent workflow orchestration |
| Python 3.11 | LangChain Core / LangChain Groq | Structured LLM calls |
| Python 3.11 | Pydantic / Pydantic Settings | Config and validation |
| PostgreSQL 16 | pgvector | Vector storage and semantic retrieval |
| Redis 7 | redis.asyncio | Session and result caching |
| LiveKit | livekit-api | Real-time media room orchestration |
| Docker | Compose | Local service orchestration |
| Pytest | pytest | Automated testing |

---

## Project Structure

```text
teleexam-ai-vcall/
├── .env.example
├── .gitignore
├── .venv/                     # local virtual environment (if created)
├── Dockerfile
├── README.md
├── alembic.ini
├── docker-compose.yml
├── pytest.ini
├── requirements.txt
├── alembic/
│   ├── README
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       ├── 97ea79826c79_create_initial_tables.py
│       ├── 377b79dc45a1_add_learner_profiles_table.py
│       ├── 5d908fe32ea4_add_hnsw_index_on_curriculum_chunks_.py
│       └── da3a7466e408_add_learner_profiles_table.py
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── adapters/
│   │   ├── inbound/
│   │   │   ├── http/
│   │   │   │   ├── admin.py
│   │   │   │   ├── sessions.py
│   │   │   │   └── users.py
│   │   │   └── ws/
│   │   │       └── websocket.py
│   │   └── outbound/
│   │       ├── cache/
│   │       │   └── redis_adapter.py
│   │       ├── db/
│   │       │   ├── postgres_call_repo.py
│   │       │   ├── postgres_curriculum_repo.py
│   │       │   ├── postgres_profile_repo.py
│   │       │   └── postgres_vector_search.py
│   │       ├── embeddings/
│   │       │   ├── cohere_adapter.py
│   │       │   └── voyage_adapter.py
│   │       ├── llm/
│   │       │   ├── cerebras_adapter.py
│   │       │   └── groq_adapter.py
│   │       ├── media/
│   │       │   └── livekit_adapter.py
│   │       ├── search/
│   │       │   ├── __init__.py
│   │       │   └── tavily_adapter.py
│   │       ├── stt/
│   │       │   ├── assemblyai_adapter.py
│   │       │   ├── deepgram_adapter.py
│   │       │   └── groq_whisper_adapter.py
│   │       ├── tts/
│   │       │   ├── cartesia_adapter.py
│   │       │   └── elevenlabs_adapter.py
│   │       └── video/
│   │           └── youtube_adapter.py
│   ├── agents/
│   │   ├── curriculum_agent.py
│   │   ├── deps.py
│   │   ├── graph.py
│   │   ├── memory_agent.py
│   │   ├── search_agent.py
│   │   ├── state.py
│   │   ├── supervisor.py
│   │   ├── synthesizer.py
│   │   └── youtube_agent.py
│   ├── application/
│   │   ├── end_call_session.py
│   │   ├── ingest_curriculum.py
│   │   ├── process_turn.py
│   │   └── start_call_session.py
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── di.py
│   │   ├── logging.py
│   │   ├── tables.py
│   │   └── utils.py
│   ├── domain/
│   │   └── models.py
│   ├── ports/
│   │   ├── cache_port.py
│   │   ├── embedding_port.py
│   │   ├── llm_port.py
│   │   ├── media_session_port.py
│   │   ├── repositories.py
│   │   ├── stt_port.py
│   │   ├── tts_port.py
│   │   ├── vector_search_port.py
│   │   ├── video_search_port.py
│   │   └── web_search_port.py
│   └── voice/
│       └── vad.py
├── data/
│   └── exit_exam_materials/
│       ├── computer_networks.txt
│       └── data_structures.txt
├── scripts/
│   └── ingest_curriculum.py
├── tests/
│   ├── conftest.py
│   ├── fakes.py
│   ├── test_adapters.py
│   ├── test_agent_state.py
│   ├── test_agents.py
│   ├── test_db_integration.py
│   ├── test_domain_models.py
│   ├── test_e2e.py
│   ├── test_redis_integration.py
│   ├── test_supervisor.py
│   ├── test_utils.py
│   └── test_voyage_adapter.py
└── ...
```

### Important directories

- `app/agents/` — LangGraph workflow and intent routing
- `app/application/` — orchestration for sessions, turn processing, and ingestion
- `app/adapters/outbound/db/` — Postgres repositories and pgvector search
- `app/adapters/outbound/cache/` — Redis cache adapter
- `app/adapters/outbound/embeddings/` — embedding providers
- `app/adapters/outbound/llm/` — LLM provider adapters
- `app/adapters/inbound/ws/` — WebSocket interaction layer
- `app/core/` — common settings, DI, database, utils
- `alembic/` — migration scripts
- `data/exit_exam_materials/` — source teaching materials used for curriculum ingestion
- `scripts/` — admin and ingestion scripts
- `tests/` — unit and integration tests

---

## Installation

### Local development

1. Clone the repository:
   ```bash
   git clone https://github.com/dagiteferi/teleexam-ai-vcall-.git
   cd teleexam-ai-vcall-
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. Create your environment file:
   ```bash
   cp .env.example .env
   ```

4. Update `.env` with your API keys and local service settings.

5. Start the required infrastructure:
   ```bash
   docker compose up -d postgres redis livekit
   ```

6. Apply database migrations:
   ```bash
   alembic upgrade head
   ```

7. Start the FastAPI service:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
   ```

### Docker

The repository includes a `Dockerfile` and `docker-compose.yml` to run the application and the backing services together.

```bash
docker compose up --build
```

This starts:

- Postgres on `5432`
- Redis on `6379`
- LiveKit on `7880` and `7881`
- The API service on `8001`

### Production

The project does not currently include a production-ready deployment manifest such as Kubernetes or Helm files. The service is designed to run in a containerized environment behind a reverse proxy and with proper environment variable management.

Recommended production prerequisites:

- Managed Postgres with pgvector
- Managed Redis
- LiveKit server with valid credentials
- Secret management for `GROQ_API_KEY`, `VOYAGE_API_KEY`, etc.
- HTTPS termination
- Auth and rate limiting for public-facing endpoints

---

## Environment Variables

The project reads values from `.env` via `pydantic-settings` with `env_file=".env"`.

| Variable | Required | Description | Default |
| --- | --- | --- | --- |
| `APP_ENV` | No | Application environment label | `development` |
| `LOG_LEVEL` | No | Logging level | `INFO` |
| `PORT` | No | HTTP server port | `8001` |
| `LLM_PROVIDER` | No | LLM provider selection | `groq` |
| `STT_PROVIDER` | No | Speech-to-text provider | `assemblyai` |
| `TTS_PROVIDER` | No | Text-to-speech provider | `cartesia` |
| `EMBEDDING_PROVIDER` | No | Embedding provider | `voyage` |
| `GROQ_API_KEY` | Yes for Groq | Groq API key for `ChatGroq` | `None` |
| `GROQ_MODEL` | No | Groq model to use | `llama-3.1-8b-instant` |
| `ASSEMBLYAI_API_KEY` | Yes for AssemblyAI STT | STT provider key | `None` |
| `CARTESIA_API_KEY` | Yes for Cartesia TTS | TTS provider key | `None` |
| `VOYAGE_API_KEY` | Yes for Voyage embeddings | Embedding provider key | `None` |
| `TAVILY_API_KEY` | No | Web search provider key | `None` |
| `SQLALCHEMY_DATABASE_URL` | Yes | Async Postgres connection string | `postgresql://user:password@localhost:5432/teleexam` |
| `REDIS_HOST` | No | Redis host | `localhost` |
| `REDIS_PORT` | No | Redis port | `6379` |
| `LIVEKIT_URL` | No | LiveKit WebSocket URL | `ws://localhost:7880` |
| `LIVEKIT_API_KEY` | Yes for media sessions | LiveKit API key | `None` |
| `LIVEKIT_API_SECRET` | Yes for media sessions | LiveKit secret | `None` |
| `ADMIN_API_KEY` | No | Admin header value required for `/vcall/admin/ingest` | `None` |

> [!IMPORTANT]
> The repository contains additional provider keys in configuration (`OPENAI_API_KEY`, `CEREBRAS_API_KEY`, `DEEPGRAM_API_KEY`, `ELEVENLABS_API_KEY`, `COHERE_API_KEY`) but the active runtime wiring in `app/core/di.py` uses Groq, AssemblyAI, Cartesia, Voyage, and Tavily.

---

## Running the Project

### Standard local development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
docker compose up -d postgres redis livekit
alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

### Docker

```bash
docker compose up --build
```

### Ingestion

```bash
python scripts/ingest_curriculum.py
```

### Admin route

```bash
curl -X POST http://localhost:8001/vcall/admin/ingest \
  -H "X-Admin-Key: <ADMIN_API_KEY>"
```

### Health check

```bash
curl http://localhost:8001/health
```

---

## API Documentation

The service exposes a FastAPI app with `app.main:app`. All routes are prefixed under `/vcall` unless explicitly under `/health` or `/vcall/admin`.

### Health

| Method | Path | Description | Auth |
| --- | --- | --- | --- |
| `GET` | `/health` | Service heartbeat endpoint | None |

Response:
```json
{
  "status": "ok",
  "service": "vcall-service",
  "version": "2.0.0"
}
```

### Session endpoints

#### Start session

| Method | Path | Description | Auth |
| --- | --- | --- | --- |
| `POST` | `/vcall/sessions/start` | Creates a call session and LiveKit room | None |

Request body:
```json
{
  "telegram_id": 123456789,
  "user_id": 1
}
```

Response:
```json
{
  "session": {
    "session_id": "uuid",
    "user_id": 1,
    "telegram_id": 123456789,
    "room_name": "room_abc12345",
    "status": "active",
    "started_at": "2026-08-03T12:00:00Z",
    "ended_at": null
  },
  "token": "livekit-jwt-token"
}
```

#### End session

| Method | Path | Description | Auth |
| --- | --- | --- | --- |
| `POST` | `/vcall/sessions/{session_id}/end` | Marks a session as ended | None |

Response:
```json
{
  "status": "ended"
}
```

#### Get session

| Method | Path | Description | Auth |
| --- | --- | --- | --- |
| `GET` | `/vcall/sessions/{session_id}` | Fetches a session by ID | None |

Response:
```json
{
  "session_id": "uuid",
  "user_id": 1,
  "telegram_id": 123456789,
  "room_name": "room_abc12345",
  "status": "active",
  "started_at": "2026-08-03T12:00:00Z",
  "ended_at": null
}
```

### User profile endpoint

| Method | Path | Description | Auth |
| --- | --- | --- | --- |
| `GET` | `/vcall/users/{telegram_id}/profile` | Fetches stored learner profile | None |

Response:
```json
{
  "user_id": 1,
  "telegram_id": 123456789,
  "weak_topics": ["Math", "Physics"],
  "avg_score": 82.5,
  "exams_done": 4,
  "last_seen_at": "2026-08-03T08:30:00Z"
}
```

### Admin endpoint

| Method | Path | Description | Auth |
| --- | --- | --- | --- |
| `POST` | `/vcall/admin/ingest` | Starts curriculum ingestion | `X-Admin-Key` header |

Headers:
```http
X-Admin-Key: <ADMIN_API_KEY>
```

Response:
```json
{
  "status": "ingestion started"
}
```

### WebSocket endpoint

| Method | Path | Description | Auth |
| --- | --- | --- | --- |
| `WS` | `/vcall/ws/{session_id}` | Real-time tutoring connection | Session ownership check |

Required query parameter:

```text
telegram_id=<numeric telegram id>
```

Example:
```text
ws://localhost:8001/vcall/ws/session_123?telegram_id=123456789
```

Messages accepted from client:

#### Ping
```json
{
  "type": "ping"
}
```

Response:
```json
{
  "type": "pong"
}
```

#### Transcript
```json
{
  "type": "transcript",
  "text": "Explain binary search"
}
```

Response:
```json
{
  "type": "response",
  "text": "Binary search works by...",
  "intent": "exam_question",
  "latency_ms": 1024
}
```

#### Audio chunk
```json
{
  "type": "audio_chunk"
}
```

Response:
```json
{
  "type": "audio_received"
}
```

The websocket verifies that the session exists and `session.telegram_id` matches the provided `telegram_id` before accepting the connection.

---

## Database

### Database choice

The project uses PostgreSQL 16 with the `pgvector` extension for semantic retrieval.

`docker-compose.yml` runs:
- `pgvector/pgvector:pg16`

### ORM

The application uses SQLAlchemy 2.0 async ORM:

- `app/core/database.py`
- `app/core/tables.py`

The base model is `Base`, and session factories are created with `create_async_engine` and `async_sessionmaker`.

### Schema

The schema is defined in `app/core/tables.py` and includes:

- `call_sessions`
  - `session_id` (PK)
  - `user_id`
  - `telegram_id`
  - `room_name`
  - `status`
  - `started_at`
  - `ended_at`

- `call_turns`
  - `turn_id` (PK)
  - `session_id` (FK)
  - `transcript`
  - `intent`
  - `ai_response`
  - `latency_ms`
  - `created_at`

- `curriculum_chunks`
  - `chunk_id` (PK)
  - `topic`
  - `content`
  - `source`
  - `embedding`
  - `created_at`

- `learner_profiles`
  - `id` (PK)
  - `telegram_id` (unique)
  - `weak_topics`
  - `avg_score`
  - `exams_done`
  - `last_seen_at`

### Migrations

The repository uses Alembic for migration management:

- `alembic.ini`
- `alembic/env.py`
- `alembic/versions/*.py`

Important migrations:

- `97ea79826c79_create_initial_tables.py`
- `5d908fe32ea4_add_hnsw_index_on_curriculum_chunks_.py`
- `377b79dc45a1_add_learner_profiles_table.py`
- `da3a7466e408_add_learner_profiles_table.py`

The HNSW index is created on `curriculum_chunks.embedding` with `vector_cosine_ops`.

### Models

Domain models live in `app/domain/models.py`:

- `CallSession`
- `Turn`
- `LearnerProfile`
- `CurriculumChunk`

---

## AI Components

### Models and providers

The active runtime wiring in `app/core/di.py` uses:

- LLM: Groq via `ChatGroq`
- STT: AssemblyAI
- TTS: Cartesia
- Embeddings: Voyage AI
- Search: Tavily
- Video: placeholder `YouTubeAdapter` stub

The config defaults are:
- `LLM_PROVIDER=groq`
- `STT_PROVIDER=assemblyai`
- `TTS_PROVIDER=cartesia`
- `EMBEDDING_PROVIDER=voyage`

### Prompt pipeline

The AI flow is implemented through LangGraph:

1. `supervisor` classifies intent
2. Branches to specialized nodes:
   - `curriculum`
   - `search`
   - `youtube_find`
   - `youtube_summarize`
   - `memory`
   - `synthesizer`
3. The `synthesizer` receives context and builds a prompt from:
   - learner profile
   - retrieved curriculum
   - web search content
   - YouTube summary
   - recent chat history

### Retrieval (RAG)

The curriculum-use path performs:

- embedding generation from the student transcript
- retrieval from `curriculum_chunks` using pgvector cosine distance
- context assembly into a single `rag_context` string
- Redis caching for 5 minutes

Implementation:
- `app/agents/curriculum_agent.py`
- `app/adapters/outbound/db/postgres_vector_search.py`
- `scripts/ingest_curriculum.py`

### Embeddings

The ingestion script reads local files in `data/exit_exam_materials` and generates embeddings with Voyage AI.

Actual embedding adapter:
- `app/adapters/outbound/embeddings/voyage_adapter.py`

### Vector database

The project stores and searches vector data in Postgres using `pgvector`, not in a dedicated vector database service.

### Agent framework

The agent orchestration is implemented with `langgraph.StateGraph`:

- `app/agents/graph.py`
- `app/agents/state.py`

The graph compiles a pipeline from `supervisor` to specialized nodes and finally to `synthesizer`.

### Memory

Memory is composed of:
- Redis caches for turn and state persistence
- Learner profile data stored in Postgres via `learner_profiles`
- `memory_agent.py` loads profile data and caches it for 120 seconds

### Tool calling

The codebase does not implement explicit tool-calling abstractions beyond adapters and agent nodes. Instead, actions are executed by direct adapter calls inside agent nodes.

### Workflow

The actual AI workflow in repository code is:

```text
WebSocket transcript
  -> supervisor intent classification
  -> curriculum/search/youtube/memory/synthesizer
  -> TTS output
  -> turn saved to Postgres
  -> conversation state cached in Redis
```

> [!WARNING]
> The YouTube-specific nodes exist, but the default `YouTubeAdapter` implementation returns empty values. That means the repository currently contains the scaffold for YouTube retrieval/summarization, but not a completed external integration.

---

## Configuration

Important configuration files:

- `app/core/config.py`
  - Central environment config and provider choice
- `.env.example`
  - Example environment variables
- `alembic.ini`
  - Alembic database setup
- `docker-compose.yml`
  - Local orchestrator for Postgres, Redis, LiveKit, and API service
- `Dockerfile`
  - Build image for the API service
- `pytest.ini`
  - Test configuration and async pytest mode
- `requirements.txt`
  - Python dependencies

The application loads environment variables using `pydantic-settings` and sets `env_file=".env"`.

---

## Security

### Authentication and authorization

The service currently uses very limited security controls:

- Admin ingestion is guarded by `X-Admin-Key` compared to `ADMIN_API_KEY`
- WebSocket session ownership is checked by comparing the provided `telegram_id` with `session.telegram_id`
- There is no JWT-based auth, OAuth, or per-user access control layer

### Secrets

Secrets are expected to be set in environment variables (for example `.env` locally or runtime secrets in deployment).

### Rate limiting

There is no rate limiting implementation in the current repository.

### Validation

- Pydantic models are used for request validation in HTTP endpoints
- WebSocket message handling does not perform deep validation beyond checking `message.get("type")`

---

## Testing

The repository includes a suite of unit and integration tests under `tests/`.

### Test framework

- `pytest`
- `pytest-asyncio`
- async tests enabled in `pytest.ini`

### Run tests

```bash
pytest
```

To run only integration tests:

```bash
pytest -m integration
```

### Coverage

There is no explicit coverage configuration or plugin in the project (`pytest-cov` is not installed in `requirements.txt`), so coverage reporting is not configured.

### Key tests

- `test_domain_models.py`
- `test_agents.py`
- `test_supervisor.py`
- `test_db_integration.py`
- `test_e2e.py`
- `test_redis_integration.py`

---

## Deployment

### Local deployment

Use Docker Compose for local infrastructure and run the app with Uvicorn.

```bash
docker compose up --build
```

### Docker deployment

`Dockerfile` builds the service image and exposes port `8001`.

### Production guidance

The repository contains no production deployment manifests for:
- Kubernetes
- Helm
- ECS
- Cloud Run
- Azure App Service
- Railway
- Render
- Fly.io

For production, this service should be deployed behind:
- a reverse proxy
- HTTPS termination
- secret management
- managed Postgres and Redis
- a managed LiveKit deployment or self-hosted LiveKit cluster

---

## Development Workflow

- Use a virtual environment for local Python dependencies
- Store local configuration in `.env`
- Run migrations after schema changes:
  ```bash
  alembic upgrade head
  ```
- Keep all provider logic behind adapter interfaces in `app/ports/`
- Prefer adding new adapters rather than hard-coding provider logic into `app/core/di.py`
- Use the existing tests to validate behavior before submitting changes

### Contributor flow

1. Create a branch
2. Make focused changes
3. Run pytest
4. Update migrations when database schema changes
5. Verify `.env` changes are documented in `.env.example`
6. Submit a pull request with clear notes

---

## Performance Considerations

- Redis caching is used for:
  - intent classification
  - session state
  - retrieved curriculum context
  - user profile data
  - YouTube results
- `curriculum_chunks` includes an HNSW index established with `pgvector`
- `scripts/ingest_curriculum.py` batches embedding generation for curriculum documents
- `NullPool` is used in `app/core/database.py`, which can reduce connection reuse but keeps a simpler local-development configuration
- `stable_hash` reduces text to a short key for cache names

---

## Troubleshooting

### FAQ

#### The app does not start
Check:
- Python dependencies are installed
- `.env` exists and contains required keys
- Postgres/Redis/LiveKit are running if using local infrastructure

#### I get a database connection error
Ensure:
- `SQLALCHEMY_DATABASE_URL` is correct
- Postgres is running
- `pgvector` extension is available to the database

#### Curriculum ingestion fails
Check:
- `VOYAGE_API_KEY` is configured
- `data/exit_exam_materials` contains `.txt` files
- the database is reachable and migrations have been applied

#### The admin endpoint returns `403`
Ensure:
- `ADMIN_API_KEY` is set in `.env`
- the request includes the `X-Admin-Key` header with the same value

#### WebSocket connection is rejected
Check:
- the session exists
- `telegram_id` in the query string matches the stored `session.telegram_id`
- the target session ID is valid

#### LiveKit token generation fails
Ensure:
- `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET` are set
- the LiveKit server is running and reachable

#### I cannot run Alembic
Make sure:
- `alembic.ini` points to the correct DB URL
- `pgvector` is installed and the DB can accept the migration

---

## Roadmap

The current codebase suggests several realistic next steps:

- Complete the YouTube search/summarization integration
- Implement full STT streaming into session transcript processing
- Connect TTS audio to LiveKit media output rather than returning text
- Add real auth and session validation for public deployment
- Add rate limiting and request throttling
- Add structured observability and metrics
- Introduce OpenAPI examples and response schema documentation
- Add user management and profile update endpoints
- Introduce background tasks for ingestion and long-running AI jobs
- Add role-based admin access beyond a single static header key

---

## Contributing

Contributions are welcome. Please keep changes scoped and aligned with the repository’s ports-and-adapters design.

### Contributors

- **Lidiya Mergiya**
  GitHub: https://github.com/lidiyamergiya

- **Dagmawi (Dagi) Teferi**
  GitHub: https://github.com/dagiteferi

Repository:

https://github.com/dagiteferi/teleexam-ai-vcall-

---

## License

This repository does not currently include a `LICENSE` file. As a result, the project is not explicitly licensed in the repository state reviewed here.

A standard MIT license is recommended for open-source distribution, but the final decision should be confirmed by the maintainers before publication or commercial use.

---

## Acknowledgements

This project builds on several open-source technologies and services:

- FastAPI
- SQLAlchemy
- Alembic
- pgvector
- Redis
- LiveKit
- LangGraph
- LangChain
- Groq
- Voyage AI
- AssemblyAI
- Cartesia
- Tavily
- Docker
- pytest

These components are used directly in the application and infrastructure layers described above.