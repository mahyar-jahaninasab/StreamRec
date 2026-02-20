#chunk.py
from server.config import FileConfig

from dataclasses import dataclass, field, asdict
from spacy.tokens import Doc, Span
from spacy.language import Language
import spacy
from langdetect import detect, LangDetectException

from typing import List, Dict, Optional, Any
import json
from functools import lru_cache

SUPPORTED_LANGUAGES = {
    "en", "zh", "zh-hant", "fr", "de", "nl"
}

LANG_MAPPING = {
    "zh-cn": "zh",
    "zh-tw": "zh", 
    "zh-hk": "zh",
}

@lru_cache(maxsize=10)
def load_nlp_for_language(language: str) -> spacy.Language:
    lang_code = language if language in SUPPORTED_LANGUAGES else "en"
    try:
        nlp = spacy.blank(lang_code)
    except ImportError:
        print(f"Warning: spaCy model for '{lang_code}' not found. Falling back to English.")
        nlp = spacy.blank("en")
    nlp.add_pipe("sentencizer")
    return nlp

def detect_language(text: str) -> str:
    if not text or not text.strip():
        return "en"
    try:
        detected = detect(text)
        return LANG_MAPPING.get(detected, detected)
    except LangDetectException:
        return "en"
    except Exception as e:
        print(f"Language detection error: {e}")
        return "en"

@dataclass
class Chunk:
    content: str = ""
    content_without_overlap: str = ""
    chunk_id: str = ""
    start_i: int = 0
    end_i: int = 0
    title: str = ""
    doc_uuid: Optional[str] = None
    embed: Optional[List[float]] = None
    labels: List[str] = field(default_factory=list)

    def to_json(self) -> dict:
        data = asdict(self)
        data.pop('embed', None)
        return {k: v for k, v in data.items() if v is not None}

    @classmethod
    def from_json(cls, data: dict) -> "Chunk":
        return cls(
            content=data.get("content", ""),
            content_without_overlap=data.get("content_without_overlap", ""),
            chunk_id=data.get("chunk_id", ""),
            start_i=int(data.get("start_i", 0)),
            end_i=int(data.get("end_i", 0)),
            title=data.get("title", ""),
            doc_uuid=data.get("doc_uuid"),  
            labels=data.get("labels", []),
        )

    

@dataclass
class Document:
    title: str = ""
    content: str = ""
    extension: str = ""
    file_size: int = 0  
    labels: List[str] = field(default_factory=list)  
    source: str = ""
    meta: Dict[str, Any] = field(default_factory=dict)
    metadata: str = ""
    owner: str = ""
    allowed_roles: List[str] = field(default_factory=list)
    chunks: List[Any] = field(default_factory=list) 
    _spacy_doc: Optional[Any] = field(init=False, repr=False, default=None)

    def analyze_content(self, batch_size: int = 500000) -> None:
        if not self.content:
            return
        try:
            detected_language = detect_language(self.content[:batch_size])
            nlp = load_nlp_for_language(detected_language)
        except NameError:
            print("Warning: NLP functions (detect_language, load_nlp_for_language) not defined.")
            return

        if len(self.content) > batch_size:
            docs = []
            for i in range(0, len(self.content), batch_size):
                batch = self.content[i : i + batch_size]
                docs.append(nlp(batch))
            self._spacy_doc = Doc.from_docs(docs) 
        else:
            self._spacy_doc = nlp(self.content)

    @property
    def spacy_doc(self):
        return self._spacy_doc

    def to_json(self) -> dict:
        return {
            "title": self.title,
            "content": self.content,
            "extension": self.extension,
            "fileSize": self.file_size,
            "labels": self.labels,
            "source": self.source,
            "meta": self.meta, 
            "metadata": self.metadata,
        }

    @classmethod
    def from_json(cls, doc_dict: dict) -> Optional["Document"]:
        required_keys = {"title", "content", "source"}
        if not required_keys.issubset(doc_dict.keys()):
            return None
        meta_data = doc_dict.get("meta", {})
        if isinstance(meta_data, str):
            try:
                meta_data = json.loads(meta_data)
            except json.JSONDecodeError:
                meta_data = {}

        return cls(
            title=doc_dict.get("title", ""),
            content=doc_dict.get("content", ""),
            extension=doc_dict.get("extension", ""),
            file_size=doc_dict.get("fileSize", 0),
            labels=doc_dict.get("labels", []),
            source=doc_dict.get("source", ""),
            meta=meta_data,
            metadata=doc_dict.get("metadata", ""),
        )

def create_document(content: str, file_config: FileConfig) -> Document:
    doc = Document(
        title=file_config.filename,
        content=content,
        extension=file_config.extension,
        labels=file_config.labels,
        allowed_roles=file_config.allowed_roles,
        owner=file_config.owner,
        source=file_config.source,
        file_size=file_config.file_size,
        metadata=file_config.metadata,
        meta={},
    )
    doc.analyze_content()
    return doc
