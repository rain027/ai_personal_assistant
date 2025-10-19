from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

# Create app FIRST
app = FastAPI()

class Message(BaseModel):
    message: str

# Add CORS middleware IMMEDIATELY after creating app
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=".*",  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message" : "AI assistant API is running"}

@app.post("/api/chat")
def chat(data: Message):
    user_message = data.message
    return {"response" : f"You said : {user_message}"}