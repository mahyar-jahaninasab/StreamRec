from streamrec.interface import DataCollector
from streamrec.types import DataCollectorConfig


class HuggingFaceCollector(DataCollector):
    def __init__(self, config):
        super().__init__()
        self.type = "HuggingFace"
        self.config["Source"] = DataCollectorConfig(
                                                    type="huggingface",
                                                    value="dataset",
                                                    description="Collect dataset from Hugging Face Hub",
                                                    href="https://huggingface.co/datasets"
                                                    )
    async def request(self):
        pass 

    async def to_paraquet(self):
        pass 



