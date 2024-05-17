from beanie import Document
from abc import ABC


class BaseStorage(ABC):
    document: Document | None = None
