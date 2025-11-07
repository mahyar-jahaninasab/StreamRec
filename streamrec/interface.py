from abc import ABC, abstractmethod

class StreamRecComponent(ABC):

    def __init__(self):
        self.name = ""
        self.config = {}
        self.description = ""
        self.type = ""
    
    def get_meta(self):

        #1 get it from internet
        #have it
        #get it from the parent class
        pass


class DataCollector(StreamRecComponent):
    def __init__(self):
        super().__init__()
        self.name = "HuggingFaceDataCollector"
        self.description = "Collect dataset from ready to collect databses in Hugging Face"
    
    @abstractmethod
    def request(self):
        pass

    @abstractmethod
    def to_paraquet(self):
        pass 


class DataCleaner(StreamRecComponent):
    def __init__(self):
        super().__init__()
        self.name = "Handling data in parallel using PySpark"
        self.description = "Cleaning Data and turning it into datalake"
    
    @abstractmethod
    def to_datalake(self):
        pass

    @abstractmethod
    def transform(self):
        pass

    @abstractmethod
    def _filter(self):
        pass 

    @abstractmethod
    def _feature_creation(self):
        pass

 