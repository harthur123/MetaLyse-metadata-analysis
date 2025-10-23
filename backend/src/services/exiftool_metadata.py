import exiftool

def extract_metadata_with_exiftool(file_path: str) -> dict:
    """Extrai metadados de qualquer arquivo usando o ExifTool."""
    with exiftool.ExifTool() as et:
        metadata = et.get_metadata(file_path)
    return metadata
