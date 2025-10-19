from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

class Message(BaseModel):
    message: str

@app.post("/api/chat")
def chat(data: Message):
    user_message = data.message
    return {"response": f"You said: {user_message}"}

# Serve static files (HTML, JS) at root
app.mount("/", StaticFiles(directory="static", html=True), name="static")