import asyncio
import aiofiles
from typing import Dict, Union
from streamrec.interface import DataCleaner, DataCollector,Reader
from streamrec.types import DataCollectorConfig
import aiohttp
from datasets import load_dataset

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
    def __init__(self):
        super().__init__()

    async def _extract_content(self,data:Dict[content]):
        pass

    async def _universal_sanitize(self, data):
        return None




class UploadDocument(Reader):
    def __init__(self):
        super().__init__()
        self.types = 
    
    async def read_file(self, data):
        # get the file in the backend and see the content type ?! 
        # clean it, get the type 
        # put some limitation of using the resource
        # do some cache back for uploading ?! 

        match case:
            pdf 

    
    async def upload_docs(self, data):

        tasks = asyncio.gather(await self.read_file(data))
        return 
