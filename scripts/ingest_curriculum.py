import asyncio
from pathlib import Path
from uuid import uuid4

from app.adapters.outbound.db.postgres_curriculum_repo import (
    PostgresCurriculumRepository,
)
from app.adapters.outbound.embeddings.voyage_adapter import VoyageAdapter
from app.core.config import settings
from app.core.database import async_session
from app.domain.models import CurriculumChunk


DATA_DIR = Path("data/exit_exam_materials")
CHUNK_SIZE = 500


def read_curriculum_files():
    """
    Read all txt files from the curriculum directory.
    """

    documents = []

    for file in DATA_DIR.iterdir():

        if file.suffix.lower() == ".txt":

            text = file.read_text(
                encoding="utf-8"
            )

            documents.append(
                (
                    file.name,
                    text,
                )
            )

    return documents


def split_into_chunks(
    text: str,
    chunk_size: int = CHUNK_SIZE,
):
    """
    Split text into chunks around 500 characters.
    Prefer splitting at paragraph boundaries.
    """

    paragraphs = text.split("\n\n")

    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:

        paragraph = paragraph.strip()

        if not paragraph:
            continue


        if len(current_chunk) + len(paragraph) <= chunk_size:

            current_chunk += paragraph + "\n\n"

        else:

            if current_chunk:

                chunks.append(
                    current_chunk.strip()
                )

            current_chunk = paragraph + "\n\n"


    if current_chunk:

        chunks.append(
            current_chunk.strip()
        )


    return chunks


async def ingest_curriculum():

    print("📚 Reading curriculum files...")


    documents = read_curriculum_files()


    if not documents:

        print("No curriculum files found.")

        return


    curriculum_chunks = []


    for filename, text in documents:

        chunks = split_into_chunks(text)


        for content in chunks:

            chunk = CurriculumChunk(
                chunk_id=str(uuid4()),
                topic=filename,
                content=content,
                source=filename,
                embedding=None,
            )

            curriculum_chunks.append(chunk)


    print(
        f"Created {len(curriculum_chunks)} chunks"
    )


    print("🔢 Generating embeddings...")


    voyage = VoyageAdapter(settings)


    # Batch embedding: all chunks in ONE API call
    contents = [
        chunk.content
        for chunk in curriculum_chunks
    ]


    embeddings = await voyage.embed(contents)


    for chunk, embedding in zip(
        curriculum_chunks,
        embeddings,
    ):

        chunk.embedding = embedding



    print("💾 Saving chunks to database...")


    async with async_session() as session:

        repository = PostgresCurriculumRepository(
            session
        )


        for chunk in curriculum_chunks:

            await repository.save_chunk(
                chunk
            )


    print(
        f"✅ Successfully saved {len(curriculum_chunks)} chunks"
    )



if __name__ == "__main__":

    asyncio.run(
        ingest_curriculum()
    )