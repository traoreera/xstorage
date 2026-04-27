from __future__ import annotations
import re
from pathlib import Path
from .utils import sanitize_path_component

class StorageBase:
    _DATA_DIR = Path("data")
    _FILES_ROOT = _DATA_DIR / "files"

    def _find_file(self, file_id: str, prefix: str, service: str) -> Path | None:
        if not file_id or not re.fullmatch(r"[a-f0-9]{32}", file_id):
            return None

        base = self._safe_dir(service, prefix or "")
        if base is None or not base.exists() or not base.is_dir():
            return None

        target_prefix = file_id + "_"
        try:
            for entry in base.iterdir():
                if entry.is_file() and entry.name.startswith(target_prefix):
                    return entry
        except OSError:
            return None
        return None

    def _safe_dir(self, service: str, prefix: str) -> Path | None:
        try:
            safe_service = sanitize_path_component(service, allow_slashes=False)
            safe_prefix = sanitize_path_component(prefix, allow_slashes=True)
            if not safe_service:
                return None

            service_dir = (self._FILES_ROOT / safe_service).resolve()
            service_dir.mkdir(parents=True, exist_ok=True)
            
            resolved = (service_dir / safe_prefix).resolve()
            
            try:
                resolved.relative_to(service_dir)
                return resolved
            except ValueError:
                return None
        except Exception:
            return None
