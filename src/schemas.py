from typing import Optional, TypedDict
from pydantic import BaseModel


class Base(BaseModel):
    service: str


class WriteFile(Base):
    content_b64: str
    prefix: str
    filename: str = "upload"
    allowed_ext: list[str] = []


class FileBase(Base):
    file_id: Optional[str] = None
    prefix: Optional[str] = None  # optionnel : list() fonctionne sans prefix


class GetFile(FileBase): ...
class ExistFile(FileBase): ...
class DeleteFile(FileBase): ...
class ListFile(FileBase): ...


class DeleteFilesPrefix(FileBase):
    file_id: str = ""  # champ Pydantic correctement annoté


class ZipFile(Base):
    prefix: str
    output_filename: str = "archive.zip"


class InstallModule(Base):
    module_name: str


# -- Schémas de validation de formulaire --

class WriteFileSchema(TypedDict):
    content_b64: tuple[type, ...]
    prefix: tuple[type, ...]
    filename: tuple[type, ...]
    allowed_ext: tuple[type, list]

class FileManipSchema(TypedDict):
    file_id: tuple[type, str]
    prefix: tuple[type, str]
    service: tuple[type, str]

class ZipFileSchema(TypedDict):
    service: tuple[type, str]
    prefix: tuple[type, str]
    output_filename: tuple[type, str]

class InstallModuleSchema(TypedDict):
    service: tuple[type, str]
    module_name: tuple[type, str]


WRITEFILE: WriteFileSchema = {
    "content_b64": (str, ...),
    "prefix":      (str, ...),
    "filename":    (str, ...),
    "allowed_ext": (list, []),
}

FILESMANIP: FileManipSchema = {
    "file_id": (str, ""),
    "prefix":  (str, ""),
    "service": (str, ""),
}

ZIPFILE: ZipFileSchema = {
    "service": (str, ...),
    "prefix":  (str, ...),
    "output_filename": (str, "archive.zip"),
}

INSTALLMODULE: InstallModuleSchema = {
    "service": (str, ...),
    "module_name": (str, ...),
}