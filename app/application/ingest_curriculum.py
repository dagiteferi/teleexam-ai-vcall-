from scripts.ingest_curriculum import ingest_curriculum as run_ingestion


async def ingest_curriculum() -> None:
    """
    Application use case for curriculum ingestion.

    Called by the admin endpoint.
    """

    await run_ingestion()