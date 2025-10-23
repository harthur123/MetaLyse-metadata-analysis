from PyPDF2 import PdfReader

def extract_pdf_metadata(file_path: str) -> dict:
    """Extrai metadados de um PDF."""
    reader = PdfReader(file_path)
    metadata = reader.metadata
    result = {}
    if metadata:
        for key, value in metadata.items():
            result[key] = str(value)
    return result
