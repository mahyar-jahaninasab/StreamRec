from abc import ABC, abstractmethod

class StreamRecComponent(ABC):

    def __init__(self):
        self.name = ""
        self.config = {}
        self.description = ""
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
        self.name = "DataCollector"
        self.description = "Collect dataset from ready to collect databses"
    
    @abstractmethod
    async def request(self):
        pass


class DataCleaner(StreamRecComponent):
    def __init__(self):
        super().__init__()
        self.name = "DataCleaner"
        self.description = "Cleaning Data and turning it into datalake"
    
    @abstractmethod
    async def to_datalake(self):
        pass

    @abstractmethod
    async def transform(self):
        pass

    @abstractmethod
    async def _filter(self):
        pass 

    @abstractmethod
    async def _feature_creation(self):
        pass



class UploadDoc(StreamRecComponent):
    def __init__(self):
        super().__init__()
        self.name = "UploadDocument"
        self.description = "Get the document from the users"
    
    @abstractmethod
    async def upload_doc(self):
        pass 




 