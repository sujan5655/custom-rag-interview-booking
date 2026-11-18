# Custom RAG Backend with Interview Booking

A modular backend application built with **FastAPI, Qdrant, PostgreSQL, Redis, Sentence Transformers, and Groq LLM**.

This project implements two major functionalities:

1. **Document Ingestion API:** Upload PDF and TXT documents, extract their content, split text using configurable chunking strategies, generate embeddings, and store vectors in Qdrant with document metadata in PostgreSQL.
2. **Conversational RAG API:** Answer questions using retrieved document context, maintain multi-turn conversation memory using Redis, and and support AI-powered interview booking through natural language.

## Features

### 1. Document Ingestion

- Upload PDF and TXT documents.
- Extract text using PyMuPDF and text decoding.
- Support two chunking strategies:
  - Fixed-size chunking
  - Recursive chunking
- Select the chunking strategy during ingestion.
- Generate vector embeddings using Sentence Transformers.
- Store embeddings and chunk metadata in Qdrant.
- Store document metadata in PostgreSQL.
- Maintain a modular document processing pipeline.

### 2. Conversational RAG

- Custom Retrieval-Augmented Generation pipeline.
- Retrieve relevant document chunks from Qdrant.
- Generate contextual responses using Groq LLM.
- Maintain multi-turn conversation history using Redis.
- Support session-based conversation memory.
- Rewrite follow-up questions using conversation history to improve retrieval.
- Combine retrieved context and conversation history when generating answers.

### 3. Interview Booking

The application supports conversational interview booking through an LLM-powered extraction workflow.

Required information:

- Full name
- Email address
- Interview date
- Interview time

Booking capabilities:

- Extract booking information from natural language.
- Collect missing information through conversation.
- Store temporary booking details in Redis.
- Merge information across multiple messages.
- Display a booking summary before confirmation.
- Confirm or reject booking requests.
- Store confirmed bookings in PostgreSQL.
- Detect duplicate confirmed bookings for the same email, date, and time.
- Enforce database-level uniqueness for email, interview date, and interview time.

## Technology Stack

| Component             | Technology            |
| --------------------- | --------------------- |
| Backend Framework     | FastAPI               |
| Programming Language  | Python 3.12           |
| Vector Database       | Qdrant                |
| Relational Database   | PostgreSQL            |
| Conversation Memory   | Redis                 |
| ORM                   | SQLAlchemy            |
| Database Migrations   | Alembic               |
| LLM Provider          | Groq                  |
| Embedding Model       | Sentence Transformers |
| PDF Extraction        | PyMuPDF               |
| Dependency Management | uv                    |
| Containerization      | Docker Compose        |

## Architecture

```text
                 Client
                   |
                   v
             FastAPI Backend
                   |
          +--------+---------+
          |                  |
          v                  v
   Document Ingestion   Conversational RAG
          |                  |
          v                  v
     PDF / TXT          Redis Memory
     Extraction              |
          |                  v
          v             Qdrant Retrieval
      Chunking                |
          |                  v
          v              Groq LLM
     Embeddings                |
          |                  v
          v              Response
       Qdrant
          |
          v
      PostgreSQL
   (Document Metadata)

   Interview Booking
          |
          v
       Groq LLM
   (Information Extraction)
          |
          v
       Redis
   (Temporary Booking Data)
          |
          v
      PostgreSQL
   (Confirmed Bookings)
```

## Prerequisites

Make sure you have installed:

- Python 3.12
- uv
- Docker Desktop
- Docker Compose
- Groq API key

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/sujan5655/custom-rag-interview-booking
cd Rag_Project
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Configure environment variables

Create a `.env` file in the project root.

```env
DEBUG=True

DATABASE_URL=postgresql+asyncpg://<database_user>:<database_password>@localhost:5433/rag_db

REDIS_URL=redis://localhost:6380/0

QDRANT_URL=http://localhost:6333
QDRANT_COLLECTION=documents

GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile

EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
EMBEDDING_DIMENSION=384

REDIS_CHAT_TTL_SECONDS=86400
```

Use the exact environment variable names defined in your application settings.

### 4. Start infrastructure services

Start PostgreSQL, Redis, and Qdrant using Docker Compose.

```bash
docker compose up -d
```

Check running containers:

```bash
docker compose ps
```

### 5. Run database migrations

```bash
uv run alembic upgrade head
```

### 6. Start the FastAPI application

```bash
uv run uvicorn rag_project.main:app --reload
```

The application should now be available at:

```text
http://127.0.0.1:8000
```

## API Documentation

FastAPI provides interactive API documentation through Swagger UI.

```text
http://127.0.0.1:8000/docs
```

Use Swagger UI to explore and test the document ingestion and conversational RAG endpoints, including interview booking.

## Testing

Run the automated test suite:

```bash
uv run pytest -v
```

Run an individual test:

```bash
uv run pytest tests/test_chunking.py -v
```

Additional API workflows can be verified through Swagger UI, including:

PDF and TXT ingestion.
Different chunking strategies.
Multi-turn document queries.
Interview information extraction.
Booking confirmation and cancellation.
Duplicate booking prevention.

## Infrastructure Services

| Service          | Local URL / Port                |
| ---------------- | ------------------------------- |
| FastAPI          | http://127.0.0.1:8000           |
| Swagger UI       | http://127.0.0.1:8000/docs      |
| Qdrant Dashboard | http://127.0.0.1:6333/dashboard |

| PostgreSQL  
localhost:5433 |
| Redis | localhost:6379 |

## Design Principles

- Modular service-based architecture.
- Separation of API, business logic, database, and infrastructure layers.
- Asynchronous database operations.
- Type annotations and structured schemas.
- Configurable document chunking.
- Custom RAG implementation without RetrievalQAChain.
- Redis-backed conversation and temporary booking memory.
- Persistent storage of document metadata and confirmed bookings.
- Database-level duplicate booking protection.

## Project Constraints

This project follows the assignment constraints:

- No FAISS.
- No Chroma.
- No RetrievalQAChain.
- No frontend or UI.
- Qdrant is used as the vector database.
- RAG retrieval and response generation are implemented using a custom pipeline.

## Security Notes

- Store API credentials in environment variables.
- Do not commit `.env` files or API keys.
- Use `.env.example` for documenting required configuration.
- Configure secure cookies and HTTPS for production deployments.
- Apply appropriate database access controls.

## Author

**Sujan Chaudhary**

GitHub: https://github.com/sujan5655/
