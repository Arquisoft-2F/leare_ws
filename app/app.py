from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes.documents import documents
from src.ws.chat_webscoket import ws

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ws)

app.include_router(documents, prefix="/documents", tags=["Documents"])
