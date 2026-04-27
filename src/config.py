

# ─────────────────────────────────────────────────────────────
# Extensions bloquées (exécutables / scripts)
# ─────────────────────────────────────────────────────────────
_BLOCKED_EXT = frozenset({
    ".exe", ".bat", ".cmd", ".com", ".msi", ".dll", ".sys",
    ".vbs", ".ps1", ".sh", ".bash", ".zsh", ".fish",
    ".rb", ".py", ".pl", ".php", ".asp", ".aspx", ".jsp",
    ".cgi", ".scr", ".pif", ".hta", ".js", ".ts",
    ".jar", ".class", ".war",
})

# Extensions acceptées par défaut
_ALLOWED_EXT = frozenset({
    ".pdf", ".doc", ".docx", ".odt", ".rtf", ".txt",
    ".xls", ".xlsx", ".csv", ".ods",
    ".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".bmp", ".tiff",
    ".zip", ".tar", ".gz", ".rar", ".7z",
    ".ppt", ".pptx", ".odp",
})

# Magic bytes → MIME
_MAGIC: list[tuple[bytes, str]] = [
    (b"%PDF",         "application/pdf"),
    (b"\xff\xd8\xff", "image/jpeg"),
    (b"\x89PNG\r\n",  "image/png"),
    (b"GIF87a",       "image/gif"),
    (b"GIF89a",       "image/gif"),
    (b"RIFF",         "image/webp"),
    (b"PK\x03\x04",  "application/zip"),
]


_OFFICE_EXT: dict[str, str] = {
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
}
