from fastapi import APIRouter, HTTPException, Depends, UploadFile, Form
import requests
import uuid

documents = APIRouter()

@documents.post("/upload")
async def upload_document(
    content: UploadFile,
    file_name: str = Form(...),
    data_type: str = Form(...),
    user_id: str = Form(...)
):
    try:
        url = "http://document-server:3004/create/addVideo/"
        # url = "http://127.0.0.1:3004/create/addVideo/"
        file_id =str(uuid.uuid4()) 
        files = {
            "content": content.file,
            "file_name": (None, file_name),
            "data_type": (None, data_type),
            "user_id": (None, user_id),
            "video_id": (None, file_id)
        }
        
        response = requests.post(url, files=files)
        response.raise_for_status()

        # Process the response from the document server
        # and return the appropriate data to the client
        return {"success": True,"file_id":file_id}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))


@documents.post("/update")
async def update_document(
    content: UploadFile,
    file_name: str = Form(...),
    data_type: str = Form(...),
    user_id: str = Form(...),
    file_id: str = Form(...)
):
    try:
        url = "http://document-server:3004/create/addVideo/"
        # url = "http://127.0.0.1:3004/create/addVideo/"
        files = {
            "content": content.file,
            "file_name": (None, file_name),
            "data_type": (None, data_type),
            "user_id": (None, user_id),
            "video_id": (None, file_id)
        }
        
        response = requests.post(url, files=files)
        response.raise_for_status()

        # Process the response from the document server
        # and return the appropriate data to the client
        return {"success": True,"file_id":file_id}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))