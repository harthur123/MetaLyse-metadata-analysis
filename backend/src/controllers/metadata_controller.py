from src.services.image_metadata import extract_image_metadata
from src.services.pdf_metadata import extract_pdf_metadata
from src.services.exiftool_metadata import extract_metadata_with_exiftool

import os

def analyze_file(file_path: str) -> dict:
    """Decide qual método usar com base na extensão do arquivo."""
    ext = os.path.splitext(file_path)[1].lower()

    if ext in [".jpg", ".jpeg", ".png"]:
        return {"type": "image", "metadata": extract_image_metadata(file_path)}
    elif ext == ".pdf":
        return {"type": "pdf", "metadata": extract_pdf_metadata(file_path)}
    else:
        return {"type": "generic", "metadata": extract_metadata_with_exiftool(file_path)}
