from streamrec.interface import Preprocessing
import re 
# example from langchain documentation
# from langchain_text_splitters import RecursiveCharacterTextSplitter

# # Load example document
# with open("state_of_the_union.txt") as f:
#     state_of_the_union = f.read()

# text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size=100,
#     chunk_overlap=20,
#     length_function=len,
#     is_separator_regex=False,
# )
# texts = text_splitter.create_documents([state_of_the_union])
# print(texts[0])
# print(texts[1])


class Cleaner(Preprocessing):
    def __init__(self, config):
        super().__init__(config)
        self.name = "Cleaner"
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

    async def _validate(self, data: str):
        pass

    async def frequncey_analysis(self, content: str):
        pass

    async def _useless_content(self, data:str):
        # ASCII control characters, an unsuall long word, bad charachters
        pattern = r"[\x00-\x1F\x7F]"  

        pattern = r""
        pass 
    
    async def _remove_reptition(self, data:str):
        #step 1 find out is there a character that is repeated more than three times and if yes delete replace it with white space
        #step 2 if a word has unusuall length delete it 
        pattern = r""

    async def _normalize_whitespace(self, data:str):
        pass 

    async def _validate_encoding(self, text:str):
        pass 

    async def content(self, raw_data:str):
        pass 
