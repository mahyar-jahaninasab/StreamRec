import json
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, UploadFile, File, Depends, Form, WebSocket
from typing import Dict, Any

from server.config import FileConfig
from streamrec.context.chunk import create_document
from streamrec.context.reader import Reader

load_dotenv()

app = FastAPI()


config_path = os.getenv("CONFIG_PATH")
with open(config_path, 'r') as f:
    CONFIG = json.load(f)
    



@app.get("/api/health")
async def health_check():
    pass 



@app.websocket("/ws/generate_stream")
async def websocket_generate_stream(websocket: WebSocket):
    pass

@app.get("/api/thread")
async def threads():
    pass



@app.post("/api/upload")
async def upload_document(uploaded_file: UploadFile = File(...)):

    file_extention = uploaded_file.filename.split('.')[-1] if '.' in uploaded_file.filename else ''
    
    # file_config = FileConfig(
    #     filename = uploaded_file.filename,
    #     extension= file_extention,
    #     labels= "user_specific",
    #     allowed_roles=user.role,
    #     owner= user.self,
    #     source= ,
    #     file_size= None,
    #     metadata = None
    # )
    metadata = {
        "file_name": uploaded_file.filename,
        "type": file_extention,
        "content_type": uploaded_file.content_type,
        "size_bytes": uploaded_file.size
    }
    # metadata = FileConfig
    cleaner = Reader(CONFIG)
    doc = create_document()
    try:
        result = await cleaner.pipeline({
            "file": uploaded_file,
            "metadata": metadata
        })
        print(type(result["text"]))
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))




### ADMIN


@app.post("/api/reset")
async def reset_streamrec():
    pass

@app.post("/api/get_meta")
async def get_meta():
    pass

@app.post("/api/get_suggestions")
async def get_suggestions():
    pass

@app.post("/api/get_all_suggestions")
async def get_all_suggestions():
    pass

@app.post("/api/delete_suggestion")
async def delete_suggestion():
    pass

@app.post("/api/delete_document")
async def delete_document():
    pass

@app.post("/api/set_rag_config")
async def update_rag_config():
    pass

@app.post("/api/get_rag_config")
async def retrieve_rag_config():
    pass