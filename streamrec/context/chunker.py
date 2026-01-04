import unicodedata
from streamrec.interface import Preprocessing
import re 

# example from langchain documentation-
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# 
# # Load example document
# with open("state_of_the_union.txt") as f:
#     state_of_the_union = f.read()
# 
# text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size=100,
#     chunk_overlap=20,
#     length_function=len,
#     is_separator_regex=False,
# )
# texts = text_splitter.create_documents([state_of_the_union])
# print(texts[0])
# print(texts[1])


class Chunker(Preprocessing):
    def __init__(self, config):
        super().__init__(config)
        self.name = "Chunker"
        parent_config = self.config
        self.config = parent_config[self.name]
    
    async def pipeline(self, data: str):
        
        #step1  Email signatures, disclaimers, ticket IDs, reply chains
        #step3  broken words, overlapping lines, random symbols
        #step4 Template clutter: “click here”, “last updated”, pagination, etc.

        ## after chunking drop if 
        # too short 
        # mostly numbers / symbols 
        # highly repetitive
        # exact and near duplicate
        # give each chunk some meta data 

        pass

    async def _validate(self, content: str):
        pass

    async def chunker(self, content: str):
        chunking_strategy = self.config["strategy"]
        pass

    async def _useless_content(self, content:str):
        if not content:
            return "" 
        pattern = r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]'
        content = re.sub(pattern,'',content)
        content = content.replace('\ufffd', '')
        content = unicodedata.normalize('NFKC', content)
        content = re.sub(r'[ \t]+', ' ', content)
        content = re.sub(r'\n{3,}', '\n\n', content)
        return content.strip()

    async def _ocr_noise(self, content:str):
        if not content:
            return ""
        content = re.sub(r'(?<=[a-z])-\s+(?=[a-z])', '', content)
        list_content = content.split("\n")
        set_content = set(list_content)
        return ".\n".join(set_content)



