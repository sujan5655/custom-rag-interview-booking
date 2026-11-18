





def fixed_size_chunking(
    text: str,
    chunk_size: int = 500,
    overlap: int = 100,
) -> list[str]:
    """Split text into fixed-size character chunks."""

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "overlap must be non-negative and smaller than chunk_size."
        )

    chunks: list[str] = []

    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks

def recursive_chunking(
    text: str,
    chunk_size: int = 500,
    overlap: int = 100,
) -> list[str]:
    """Split text recursively using meaningful separators."""

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "overlap must be non-negative and smaller than chunk_size."
        )

    separators = ["\n\n", "\n", ". ", " ", ""]

    def split_text(
        content: str,
        separator_index: int,
    ) -> list[str]:

        content = content.strip()

        if not content:
            return []

        if len(content) <= chunk_size:
            return [content]

        if separator_index >= len(separators):
            return [
                content[i:i + chunk_size]
                for i in range(0, len(content), chunk_size)
            ]

        separator = separators[separator_index]

        if separator:
            parts = content.split(separator)
        else:
            parts = list(content)

        chunks: list[str] = []
        current = ""

        for part in parts:
            candidate = (
                current + separator + part
                if current
                else part
            )

            if len(candidate) <= chunk_size:
                current = candidate
                continue

            if current:
                chunks.append(current.strip())

            if len(part) > chunk_size:
                nested_chunks = split_text(
                    part,
                    separator_index + 1,
                )
                chunks.extend(nested_chunks)
                current = ""
            else:
                current = part

        if current.strip():
            chunks.append(current.strip())

        return chunks

    raw_chunks = split_text(text, 0)

    # Add overlap between consecutive chunks.
    final_chunks: list[str] = []

    for index, chunk in enumerate(raw_chunks):
        if index == 0 or overlap == 0:
            final_chunks.append(chunk)
            continue

        previous = raw_chunks[index - 1]
        prefix = previous[-overlap:]

        final_chunks.append(
            f"{prefix}{chunk}"
        )

    return final_chunks




from typing import Literal


ChunkingStrategy = Literal["fixed_size", "recursive"]


def chunk_document(
    text: str,
    strategy: ChunkingStrategy,
    chunk_size: int = 500,
    overlap: int = 100,
) -> list[str]:
    """Select the appropriate chunking strategy."""

    if strategy == "fixed_size":
        return fixed_size_chunking(
            text=text,
            chunk_size=chunk_size,
            overlap=overlap,
        )

    if strategy == "recursive":
        return recursive_chunking(
            text=text,
            chunk_size=chunk_size,
            overlap=overlap,
        )

    raise ValueError(
        f"Unsupported chunking strategy: {strategy}"
    )
