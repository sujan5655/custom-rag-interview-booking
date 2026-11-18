
from rag_project.services.embedding_service import generate_embeddings

def main() -> None:
    texts = [
        "Python is a programming language.",
        "FastAPI is a framework for building APIs.",
        "Qdrant is a vector database.",
    ]

    embeddings = generate_embeddings(texts)

    print("Total embeddings:", len(embeddings))
    print("Vector dimensions:", len(embeddings[0]))
    print("First embedding:", embeddings[0][:5])

    assert len(embeddings) == 3
    assert len(embeddings[0]) == 384

    print("Embedding test passed!")


if __name__ == "__main__":
    main()
