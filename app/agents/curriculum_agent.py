from app.agents.deps import AgentDependencies
from app.agents.state import AgentState
from app.core.utils import stable_hash


async def curriculum_agent_node(
    state: AgentState,
    deps: AgentDependencies,
) -> AgentState:
    """
    Retrieves relevant curriculum content using RAG.

    Checks Redis cache first. If not cached:
    1. Convert the student's question into an embedding.
    2. Search the vector database.
    3. Join the retrieved curriculum chunks.
    4. Cache the result for 5 minutes.
    """

    # Build cache key
    cache_key = f"vcall:rag:{stable_hash(state['transcript'])}"

    # Check Redis cache
    cached = await deps.cache.get(cache_key)

    if cached:
        state["rag_context"] = cached
        return state

    # Convert the transcript into an embedding vector
    embeddings = await deps.embeddings.embed(
        [state["transcript"]]
    )

    # Use the first (and only) embedding
    query_embedding = embeddings[0]

    # Search the vector database
    results = await deps.vector_search.search(
        query_embedding=query_embedding,
        top_k=5,
    )

    # Join the retrieved curriculum chunks
    context = "\n".join(results)

    # Cache for 5 minutes (300 seconds)
    await deps.cache.set(
        cache_key,
        context,
        ttl_seconds=300,
    )

    # Save context into AgentState
    state["rag_context"] = context

    return state