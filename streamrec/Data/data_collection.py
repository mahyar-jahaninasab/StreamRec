import asyncio
import aiofiles
from typing import Union
from streamrec.interface import DataCollector
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
            self.data = [item for item in dataset]






class UploadDocument(DataCollector):
    def __init__(self):
        super().__init__()
