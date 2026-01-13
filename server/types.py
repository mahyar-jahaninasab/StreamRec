from typing import Literal
from pydantic import BaseModel
from enum import Enum

class Status(str, Enum):
    UPLOADING = "UPLOADING"
    PREPROCESSING = "PREPROCESSING"
    CHUNKING = "CHUNKING"
    EMBEDDING = "EMBEDDING"
    INJESTING = "INJESTING"
    RETRIVING = "RETRIVING"
    ACCESS = "ALOWED"
    GENERATION = "GENERATION"
    DONE = "DONE"
    ERROR = "ERROR"

class Roles(Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user" 
    GUEST = "guest"

class User(BaseModel):
    id: str 
    username: str 
    role: Roles 

class FileConfig(BaseModel):
    fileID: str
    filename: str
    isURL: bool
    overwrite: bool
    extension: str
    source: str
    owner: str
    allowed_roles: list[str]
    content: str
    labels: list[str]
    file_size: int
    status: Status
    metadata: str
    status_report: dict