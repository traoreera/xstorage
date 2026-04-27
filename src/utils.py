import mimetypes
import re
import unicodedata
from pathlib import Path
from .config import _MAGIC, _OFFICE_EXT

def sanitize_path_component(component: str, allow_slashes: bool = False) -> str:
    if not component:
        return ""
    clean = component.replace("..", "")
    if allow_slashes:
        clean = re.sub(r"[^\w\./-]", "_", clean)
    else:
        clean = re.sub(r"[^\w\.-]", "_", clean)
    return clean.strip("/")


def sanitize_filename(filename: str) -> str:
    name = unicodedata.normalize("NFKD", filename)
    name = name.encode("ascii", "ignore").decode("ascii")
    name = Path(name).name
    stem = Path(name).stem
    suffix = Path(name).suffix.lower()
    stem = re.sub(r"[^\w\s.-]", "", stem)
    stem = re.sub(r"\s+", "_", stem.strip())
    stem = stem[:200]
    return f"{stem}{suffix}" if stem else f"file{suffix}"


def detect_mime(content: bytes, filename: str) -> str:
    for magic, mime in _MAGIC:
        if content[:len(magic)] == magic:
            if mime == "application/zip":
                ext = Path(filename).suffix.lower()
                return _OFFICE_EXT.get(ext, "application/zip")
            return mime
    guessed, _ = mimetypes.guess_type(filename)
    return guessed or "application/octet-stream"
