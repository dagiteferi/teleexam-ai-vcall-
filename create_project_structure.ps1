$dirs = @(
"app",
"app/core",
"app/domain",
"app/application",
"app/ports",
"app/adapters",
"app/adapters/inbound",
"app/adapters/inbound/http",
"app/adapters/inbound/ws",
"app/adapters/outbound",
"app/adapters/outbound/llm",
"app/adapters/outbound/stt",
"app/adapters/outbound/tts",
"app/adapters/outbound/embeddings",
"app/adapters/outbound/search",
"app/adapters/outbound/video",
"app/adapters/outbound/media",
"app/adapters/outbound/cache",
"app/adapters/outbound/db",
"app/agents",
"app/voice",
"scripts",
"tests",
"data",
"data/exit_exam_materials"
)

foreach ($dir in $dirs) {
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
}

$files = @(
"app/__init__.py",
"app/main.py",

"app/core/__init__.py",
"app/core/config.py",
"app/core/logging.py",
"app/core/di.py",

"app/domain/__init__.py",
"app/domain/models.py",

"app/application/__init__.py",
"app/application/start_call_session.py",
"app/application/end_call_session.py",
"app/application/process_turn.py",
"app/application/ingest_curriculum.py",

"app/ports/__init__.py",
"app/ports/llm_port.py",
"app/ports/stt_port.py",
"app/ports/tts_port.py",
"app/ports/embedding_port.py",
"app/ports/vector_search_port.py",
"app/ports/web_search_port.py",
"app/ports/video_search_port.py",
"app/ports/media_session_port.py",
"app/ports/cache_port.py",
"app/ports/repositories.py",

"app/adapters/__init__.py",

"app/adapters/inbound/__init__.py",

"app/adapters/inbound/http/__init__.py",
"app/adapters/inbound/http/sessions.py",
"app/adapters/inbound/http/users.py",
"app/adapters/inbound/http/admin.py",

"app/adapters/inbound/ws/__init__.py",
"app/adapters/inbound/ws/websocket.py",

"app/adapters/outbound/__init__.py",

"app/adapters/outbound/llm/__init__.py",
"app/adapters/outbound/llm/groq_adapter.py",
"app/adapters/outbound/llm/cerebras_adapter.py",

"app/adapters/outbound/stt/__init__.py",
"app/adapters/outbound/stt/assemblyai_adapter.py",
"app/adapters/outbound/stt/deepgram_adapter.py",
"app/adapters/outbound/stt/groq_whisper_adapter.py",

"app/adapters/outbound/tts/__init__.py",
"app/adapters/outbound/tts/cartesia_adapter.py",
"app/adapters/outbound/tts/elevenlabs_adapter.py",

"app/adapters/outbound/embeddings/__init__.py",
"app/adapters/outbound/embeddings/voyage_adapter.py",
"app/adapters/outbound/embeddings/cohere_adapter.py",

"app/adapters/outbound/search/__init__.py",
"app/adapters/outbound/search/tavily_adapter.py",

"app/adapters/outbound/video/__init__.py",
"app/adapters/outbound/video/youtube_adapter.py",

"app/adapters/outbound/media/__init__.py",
"app/adapters/outbound/media/livekit_adapter.py",

"app/adapters/outbound/cache/__init__.py",
"app/adapters/outbound/cache/redis_adapter.py",

"app/adapters/outbound/db/__init__.py",
"app/adapters/outbound/db/postgres_call_repo.py",
"app/adapters/outbound/db/postgres_profile_repo.py",
"app/adapters/outbound/db/postgres_curriculum_repo.py",

"app/agents/__init__.py",
"app/agents/state.py",
"app/agents/deps.py",
"app/agents/graph.py",
"app/agents/supervisor.py",
"app/agents/search_agent.py",
"app/agents/youtube_agent.py",
"app/agents/curriculum_agent.py",
"app/agents/memory_agent.py",
"app/agents/synthesizer.py",

"app/voice/__init__.py",
"app/voice/vad.py",

"scripts/ingest_curriculum.py",

"tests/__init__.py",
"tests/test_domain_models.py",
"tests/test_agent_state.py",

"data/exit_exam_materials/.gitkeep",

".env.example",
"Dockerfile",
"docker-compose.yml"
)

foreach ($file in $files) {
    if (!(Test-Path $file)) {
        New-Item -ItemType File -Path $file | Out-Null
    }
}

Write-Host "Project skeleton created successfully!"