
from pathlib import Path

import pymupdf


class DocumentExtractionError(Exception):
    """Raised when document text extraction fails."""


def extract_pdf_text(file_path: Path) -> str:
    """Extract text from a PDF file."""

    try:
        with pymupdf.open(str(file_path)) as document:
            pages: list[str] = []

            for page_number, page in enumerate(document, start=1):
                text = page.get_text("text").strip()

                if text:
                    pages.append(
                        f"[Page {page_number}]\n{text}"
                    )

            extracted_text = "\n\n".join(pages)

            if not extracted_text.strip():
                raise DocumentExtractionError(
                    "No extractable text found in PDF."
                )

            return extracted_text

    except DocumentExtractionError:
        raise

    except Exception as exc:
        raise DocumentExtractionError(
            f"PDF extraction failed: {exc}"
        ) from exc


def extract_txt_text(file_path: Path) -> str:
    """Extract text from a TXT file."""

    try:
        text = file_path.read_text(encoding="utf-8-sig")

        if not text.strip():
            raise DocumentExtractionError(
                "The TXT file is empty."
            )

        return text

    except UnicodeDecodeError as exc:
        raise DocumentExtractionError(
            "TXT file must use UTF-8 encoding."
        ) from exc

    except OSError as exc:
        raise DocumentExtractionError(
            f"TXT extraction failed: {exc}"
        ) from exc


def extract_document_text(file_path: Path) -> str:
    """Extract text based on file extension."""

    extension = file_path.suffix.lower()

    if extension == ".pdf":
        return extract_pdf_text(file_path)

    if extension == ".txt":
        return extract_txt_text(file_path)

    raise DocumentExtractionError(
        "Only PDF and TXT files are supported."
    )
