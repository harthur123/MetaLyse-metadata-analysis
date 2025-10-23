import exifread

def extract_image_metadata(file_path: str) -> dict:
    """Extrai metadados EXIF de uma imagem."""
    metadata = {}
    with open(file_path, "rb") as f:
        tags = exifread.process_file(f)
        for tag, value in tags.items():
            metadata[tag] = str(value)
    return metadata
