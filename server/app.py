import json
import os
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import Dict, Any

from streamrec.context.context import CleanData

load_dotenv()

app = FastAPI()


config_path = os.getenv("CONFIG_PATH")
with open(config_path, 'r') as f:
    CONFIG = json.load(f)
    

@app.post("/api/upload")
async def upload_document(uploaded_file: UploadFile = File(...)):

    file_ext = uploaded_file.filename.split('.')[-1] if '.' in uploaded_file.filename else ''
    metadata = {
        "file_name": uploaded_file.filename,
        "type": file_ext,
        "content_type": uploaded_file.content_type,
        "size_bytes": uploaded_file.size
    }
    cleaner = CleanData(CONFIG)
    try:
        result = await cleaner.pipeline({
            "file": uploaded_file,
            "metadata": metadata
        })
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
