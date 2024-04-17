from fastapi import APIRouter, HTTPException, Depends, UploadFile, Form, Request, Response
import requests
import uuid

documents = APIRouter()

def get_token(request: Request):
    # Extract the Authorization token from the request headers
    token = request.headers.get('Authorization')
    print("ESTE ES EL TOKEN",token)
    if not token:
        return None
    return token

def isAuth(token):
    try:
        url = "http://auth-web:8080/Test/getRoute"
        headers = {"Authorization": token}
        json_data = {
            "route": "create/addVideo",
            "method": "post"
        }
        response = requests.post(url, json=json_data, headers=headers)
        response.raise_for_status()
        print(response)
        print("response")
        print(response)
        if response.text != "Authorized":
            return False
        return True
    except Exception as e:
        print("ERROR")
        print(e)
        return False
@documents.post("/upload")
async def upload_document(
    content: UploadFile,
    file_name: str = Form(...),
    data_type: str = Form(...),
    user_id: str = Form(...),
    token: str = Depends(get_token)
):

    try:
        if token is None:
            Response(content="Unauthorized access", status_code=401)
            return {"success": False, "file_id": None, "error": "NO token"}

        if isAuth(token)!= True:
            Response(content="Unauthorized access", status_code=401)
            return {"success":False,"file_id":None,"error":"Auth Error"}
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
    file_id: str = Form(...),
    token: str = Depends(get_token)
):
    try:
        if token is None:
            Response(content="Unauthorized access", status_code=401)
            return {"success": False, "file_id": None, "error": "NO token"}

        if isAuth(token)!= True:
            Response(content="Unauthorized access", status_code=401)
            return {"success":False,"file_id":None,"error":"Auth Error"}
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