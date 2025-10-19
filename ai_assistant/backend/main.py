from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

app = FastAPI()

# Initialize Groq client
groq_api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=groq_api_key)

class Message(BaseModel):
    message: str

# Store conversation history
conversation_history = []

@app.post("/api/chat")
def chat(data: Message):
    user_message = data.message
    
    # Add user message to history
    conversation_history.append({
        "role": "user",
        "content": user_message
    })
    
    try:
        # Call Groq API
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a helpful personal AI assistant. Be concise and friendly."},
                *conversation_history
            ]
        )
        
        assistant_message = response.choices[0].message.content
        
        # Add assistant response to history
        conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        return {"response": assistant_message}
    
    except Exception as e:
        return {"response": f"Error: {str(e)}"}

# Serve static files
app.mount("/", StaticFiles(directory="static", html=True), name="static")