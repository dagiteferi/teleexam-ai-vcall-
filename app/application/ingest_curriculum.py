async def ingest_curriculum() -> None:
    """
    Application use case for curriculum ingestion.

    This is called by the admin API endpoint.
    The actual ingestion pipeline reads curriculum files,
    creates embeddings, and stores chunks in the database.
    """

    print("Curriculum ingestion started")

    # TODO:
    # Connect this to the real ingestion pipeline:
    #
    # from scripts.ingest_curriculum import run_ingestion
    # await run_ingestion()

    print("Curriculum ingestion finished")