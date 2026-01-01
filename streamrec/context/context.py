import asyncio
import io
import re
from typing import Any, Dict
from streamrec.interface import Preprocessing, DataCollector
from streamrec.types import DataCollectorConfig
from datasets import load_dataset
import magic


    
class CleanData(Preprocessing):

    def __init__(self, 
                 config: Dict[str, Any]):
        
        super().__init__(config)

        self.name = "CleanData"
        parent_config = self.config
        self.config = parent_config[self.name]


    async def pipeline(self, 
                       data: Dict[str, Any]) -> Dict[str, Any]:
        uploaded_file = data.get('file')
        metadata = data.get('metadata', {})
        content = await uploaded_file.read()
        metadata['size'] = len(content)
        await self._validate(content, metadata)
        result = await self.parse_data(content, metadata)
        return result 
    
    async def _validate(self, 
                        content:bytes,
                        metadata: Dict[str, Any]) -> None:
        self._validate_structure(metadata)
        self._validate_size(content)
        self._validate_filename(metadata.get('file_name', ''))
        self._validate_file_type(content, metadata.get('type', ''))
        self._validate_metadata(metadata)    
    
    async def parse_data(self,
                         content:bytes,
                         metadata: Dict[str, Any]) -> Dict[str, Any]:
        file_type = metadata.get('type', '').lstrip('.')
        extracted_data = await self._extract_content(content, file_type)
        return {
            "text": extracted_data,
            "metadata": metadata, 
            "status": "success"
            }

        
    async def _extract_content(self, content: bytes, file_type: str) -> str:
        if file_type == "pdf":
            return await self.parse_pdf(content)
        elif file_type == "txt":
            return content.decode('utf-8')
        elif file_type in ["doc", "docx"]:
            return await self.load_docx_file(content)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

    async def parse_pdf(self, 
                        file_stream: bytes):
        try:
            from pypdf import PdfReader
        except ImportError:
            raise ImportError("PDF support is not installed.")
        pdf_bytes = io.BytesIO(file_stream)
        reader = PdfReader(pdf_bytes)
        return "\n\n".join(page.extract_text() for page in reader.pages) 

    async def load_docx_file(self, 
                             file_stream: bytes):
        try:
            import docx
        except ImportError:
            raise ImportError("Docx support is not installed")
        docx_bytes = io.BytesIO(file_stream)
        reader = docx.Document(docx_bytes)
        return "\n\n".join(pargraph.text for pargraph in reader.paragraphs)
    
    def _validate_structure(self, 
                            metadata: Dict) -> None:
        
        required_keys = self.config["metadata"]["required_keys"]
        required_keys = set(required_keys)
        provided_keys = set(metadata.keys())
        if not required_keys.issubset(provided_keys):
            missing = required_keys - provided_keys
            raise ValueError(f"Missing metadata fields: {missing}")
        
    def _validate_size(self, 
                       content: bytes) -> None:
        
        file_size = len(content) 
        if file_size == 0: 
            raise ValueError("Empty file is not allowed")
        if file_size > self.config["limits"]["max_file_size"]:
            raise ValueError(f"File size {file_size} exceeds {self.config['limits']['max_file_size']} bytes")

    def _validate_filename(self, 
                           filename: str) -> None:
        
        pattern = r"^[a-zA-Z0-9_.-]+$"
        if not filename:
            raise ValueError("Filename must be provided")
        if len(filename) > self.config["limits"]["max_filename_length"]:
            raise ValueError(f"File name must not exceed {self.config['limits']['max_filename_length']} characters")
        if not re.fullmatch(pattern, filename):
            raise ValueError("Filename contains invalid characters")
        
        if '..' in filename or '/' in filename or '\\' in filename:
            raise ValueError("File name contains path traversal patterns")

    def _validate_file_type(self, 
                            content: bytes, 
                            claimed_type: str) -> None:
        
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
        
    def _validate_metadata(self, 
                           metadata: Dict) -> None:
        
        if len(metadata) > self.config['limits']['max_metadata_fields']:
            raise ValueError(f"Too many metadata fields (max {self.config['limits']['max_metadata_fields']})")
        
    async def _universal_sanitize(self, data):
        return None
    
class HuggingFaceCollector(DataCollector):
    def __init__(self, config:Dict[str, Any]):
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
        try:
            async with self._semaphore:
                loop = asyncio.get_event_loop()
                dataset = await loop.run_in_executor(
                    None,
                    load_dataset,
                    self.links 
                )
                data = [item for item in dataset]
        except Exception as e:
            raise e
        return data 