from __future__ import annotations

import base64
import logging
import zipfile
from pathlib import Path
from uuid import uuid4

from xcore.sdk import error, ok

from .schemas import WriteFile, GetFile, ExistFile, DeleteFile, ListFile, DeleteFilesPrefix, ZipFile
from .config import _ALLOWED_EXT, _BLOCKED_EXT
from .utils import sanitize_filename, detect_mime
from .core import StorageBase

logger = logging.getLogger("xstorage.sandbox")

class StorageOperations(StorageBase):

    async def write(self, payload: WriteFile) -> dict:
        try:
            content = base64.b64decode(payload.content_b64)
        except Exception as exc:
            return error(f"Base64 invalide : {exc}", code ="decode_error")

        if not content:
            return error("Contenu vide.", code = "empty_content")

        safe_name = sanitize_filename(payload.filename)
        ext = Path(safe_name).suffix.lower()

        allowed = _ALLOWED_EXT | {e.lower() for e in payload.allowed_ext}
        if ext in _BLOCKED_EXT:
            return error(f"Extension interdite : {ext}", code ="blocked_ext")
        if ext not in allowed:
            return error(msg=f"Extension non autorisée : {ext}", code= "disallowed_ext")

        file_id = uuid4().hex
        stored_name = f"{file_id}_{safe_name}"

        dest_dir = self._safe_dir(payload.service, payload.prefix)
        if dest_dir is None:
            return error("Prefix invalide", "invalid_prefix")

        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_path = dest_dir / stored_name

        tmp_path = dest_dir / f".tmp_{file_id}"
        try:
            tmp_path.write_bytes(content)
            tmp_path.rename(dest_path)
        except Exception as exc:
            if tmp_path.exists():
                tmp_path.unlink()
            return error(msg=f'Écriture échouée : {exc}', code="write_error")

        mime = detect_mime(content, safe_name)
        rel_path = str(dest_path.relative_to(self._FILES_ROOT))

        logger.info("write OK: %s (%d bytes)", rel_path, len(content))
        return ok(
            result = {
                "file_id":       file_id,
                "path":          rel_path,
                "size_bytes":    len(content),
                "mime_type":     mime,
                "original_name": payload.filename,}
        )

    async def read(self, payload: GetFile) -> dict:
        path = self._find_file(file_id=payload.file_id, prefix=payload.prefix, service=payload.service)
        if path is None:
            return error("Fichier introuvable.", code ="not_found")
        try:
            content = path.read_bytes()
        except Exception as exc:
            return error(f"erreur de lecture: {exc}", code= "read_error")

        original_name = path.name[len(payload.file_id) + 1:]
        return ok(
            result = {
                "content_b64":   base64.b64encode(content).decode(),
                "size_bytes":    len(content),
                "mime_type":     detect_mime(content, original_name),
                "original_name": original_name,
            },
        )

    async def exists(self, payload: ExistFile) -> dict:
        exists = self._find_file(payload.file_id, payload.prefix, payload.service) is not None
        return ok(exist=exists)

    async def delete(self, payload: DeleteFile) -> dict:
        path = self._find_file(payload.file_id, payload.prefix, payload.service)
        if path is None:
            return error("file not found", "notFound")

        try:
            path.unlink()
            return ok(
                result={
                    "deleted": True,
                    "path": str(path.relative_to(self._FILES_ROOT))
                }
            )
        except Exception as exc:
            return error(f'error {exc}')

    async def list(self, payload: ListFile) -> dict:
        base = self._safe_dir(payload.service, payload.prefix or "")
        if base is None:
            return error('not found prefix')

        files = []
        if base.exists():
            for f in base.rglob("*"):
                if f.is_file() and not f.name.startswith("."):
                    files.append({
                        "path":       str(f.relative_to(self._FILES_ROOT)),
                        "name":       f.name,
                        "size_bytes": f.stat().st_size,
                    })
        return ok(
            files= files,
            count=len(files)
        )

    async def delete_all_prefix(self, payload: DeleteFilesPrefix) -> dict:
        if not payload.prefix:
            return error('missing params prefix')

        base = self._safe_dir(payload.service, payload.prefix)
        if base is None:
            return error("Préfixe invalide.", "invalid_prefix")

        count = 0
        if base.exists():
            for f in sorted(base.rglob("*"), reverse=True):
                if f.is_file():
                    f.unlink()
                    count += 1
                elif f.is_dir():
                    try:
                        f.rmdir()
                    except OSError:
                        pass
            try:
                base.rmdir()
            except OSError:
                pass

        return ok(msg="files deleted", count=count)

    async def original_name(self, payload: GetFile) -> dict:
        path = self._find_file(payload.file_id, payload.prefix, payload.service)
        if path is None:
            return error("Fichier introuvable.", "not_found")
        return ok(original_name= path.name[len(payload.file_id) + 1:])

    async def zip_files(self, payload: ZipFile) -> dict:
        base = self._safe_dir(payload.service, payload.prefix)
        if base is None or not base.exists():
            return error("Prefix introuvable", "not_found")

        output_filename = sanitize_filename(payload.output_filename)
        if not output_filename.endswith(".zip"):
            output_filename += ".zip"
        
        output_path = base / output_filename

        try:
            with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in base.rglob("*"):
                    if file_path.is_file() and file_path != output_path:
                        arcname = file_path.relative_to(base)
                        zipf.write(file_path, arcname)
            
            return ok(result={
                "filename": output_filename,
                "path": str(output_path.relative_to(self._FILES_ROOT)),
                "size_bytes": output_path.stat().st_size
            })
        except Exception as exc:
            return error(f"Erreur lors du zipping: {exc}", "zip_error")
