import asyncio
import re
import aiofiles
from typing import Any, Dict, Union
from streamrec.interface import DataCleaner, DataCollector,Reader
from streamrec.types import DataCollectorConfig
import aiohttp
from datasets import load_dataset
import magic

class HuggingFaceCollector(DataCollector):
    def __init__(self, config:dict[str, Union[list, int]]):
        super().__init__()
        self.config["Source"] = DataCollectorConfig(
                                                    type="HuggingFace",
                                                    value="dataset",
                                                    description="Collect dataset from Hugging Face Hub",
                                                    href="https://huggingface.com/datasets"
                                                    )
        self.links = config["address"]
        self._semaphore = asyncio.Semaphore(config['limit'])
    
    async def request(self):
        async with self._semaphore:
            loop = asyncio.get_event_loop()
            dataset = await loop.run_in_executor(
                None,
                load_dataset,
                self.links 
            )
            data = [item for item in dataset]
        return data 
    
class CleanData(DataCleaner):

    def __init__(self, config: dict[str, Any]):
        super().__init__()
        self.config = config

    async def _validate(self, data: Dict[str, Any]) -> None:
        content = data.get('content', b'')
        metadata = data.get('metadata', {})
        self._validate_structure(metadata)
        self._validate_size(content)
        self._validate_filename(metadata.get('file_name', ''))
        self._validate_file_type(content, metadata.get('type', ''))
        self._validate_metadata(metadata)

    def _validate_structure(self, metadata: Dict) -> None:
        if len(metadata) == 0:
            raise ValueError("All the fields for the meta data is missing")
        required_keys = self.config["metadata"]["required_keys"]  # set 
        if not required_keys.issubset(metadata.keys()):
            missing = required_keys - metadata.keys()
            raise ValueError(f"Missing metadata fields: {missing}")

    def _validate_size(self, content: bytes) -> None:
        file_size = len(content) 
        if file_size == 0: 
            raise ValueError("Empty file is not allowed")
        if file_size > self.config["limits"]["max_file_size"]:
            raise ValueError(f"File size {file_size} exceeds {self.config['limits']['max_file_size']} bytes")

    def _validate_filename(self, filename: str) -> None:
        pattern = r"^[a-zA-Z0-9_.-]+$"
        if not filename:
            raise ValueError("Filename must be provided")
        
        if len(filename) > self.config["limits"]["max_filename_length"]:
            raise ValueError(f"File name must not exceed {self.config['limits']['max_filename_length']} characters")
        
        if not re.fullmatch(pattern, filename):
            raise ValueError("Filename contains invalid characters")
        
        if '..' in filename or '/' in filename or '\\' in filename:
            raise ValueError("File name contains path traversal patterns")

    def _validate_file_type(self, content: bytes, claimed_type: str) -> None:
        buffer_size = min(self.config["limits"]["buffer_size"], len(content))
        extension = claimed_type.lstrip('.')
        if not extension in self.config["allowed_types"]:
            raise ValueError(f"Unsupported file type: {extension}")
        detected_mime = magic.from_buffer(content[:buffer_size], mime=True)
        expected_mime = self.config["allowed_types"][extension]
        if detected_mime != expected_mime:
            raise ValueError(
                f"File type mismatch: claimed '{extension}' "
                f"but detected '{detected_mime}'"
            )       
        
    def _validate_metadata(self, metadata: Dict) -> None:
        if len(metadata) > self.config['limits']['max_metadata_fields']:
            raise ValueError(f"Too many metadata fields (max {self.config['limits']['max_metadata_fields']})")

