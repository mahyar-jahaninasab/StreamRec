from abc import ABC, abstractmethod
from typing import Any, Dict

class StreamRecComponent(ABC):

    def __init__(self, config: Dict[str, Any]):
        self.name = "STREAMREC"
        self.config = config[self.name]
        self.description = f""
        self.type = ""
        
    def get_meta(self):
        return {
            "name": self.name,
            "description": self.description,
            "type": self.type,
            "config": self.config
        }


class DataCollector(StreamRecComponent):
    def __init__(self):
        super().__init__()
        self.name = f"DataCollector"
        self.description = f"Collect dataset from ready to collect databses"
        parent_config = self.config
        self.config  = parent_config[self.name]
    
    @abstractmethod
    async def request(self):
        pass


class Preprocessing(StreamRecComponent):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.name = "Preprocessing"
        self.description += f"Cleaning Data and turning it into datalake"
        parent_config = self.config
        self.config = parent_config[self.name]
    @abstractmethod
    async def pipeline(self, data):
        # validating files before doing any operation on them
        pass
    @abstractmethod
    async def _validate(self, data):
        # parsing data
        pass






 