from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from groq import Groq
import requests
import re
from sympy import symbols, solve, sympify, SympifyError

load_dotenv()

app = FastAPI()

# Initialize clients
groq_api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=groq_api_key)
news_api_key = os.getenv("NEWS_API_KEY")
weather_api_key = os.getenv("OPENWEATHER_API_KEY")

class Message(BaseModel):
    message: str

# Store conversation history
conversation_history = []

def solve_math(equation):
    """Solve mathematical equations using sympy"""
    try:
        # Handle different equation formats
        x = symbols('x')
        
        # If it looks like "x2+2x+1=0", parse it
        if '=' in equation:
            left, right = equation.split('=')
            expr = sympify(left) - sympify(right)
        else:
            expr = sympify(equation)
        
        # Solve the equation
        solutions = solve(expr, x)
        
        if solutions:
            if len(solutions) == 1:
                return f"Solution: x = {solutions[0]}"
            else:
                return f"Solutions: x = {', '.join(str(sol) for sol in solutions)}"
        else:
            return "No solutions found"
    except (SympifyError, ValueError, Exception) as e:
        return None

def get_weather(city):
    """Fetch weather for a city"""
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"
        response = requests.get(url)
        data = response.json()
        
        if data.get("main"):
            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]
            description = data["weather"][0]["description"]
            
            weather_text = f"""
Weather in {city}:
- Temperature: {temp}°C (feels like {feels_like}°C)
- Condition: {description.capitalize()}
- Humidity: {humidity}%
            """
            return weather_text.strip()
        return f"City '{city}' not found"
    except Exception as e:
        return f"Error fetching weather: {str(e)}"

def get_news():
    """Fetch latest news headlines"""
    try:
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={news_api_key}"
        response = requests.get(url)
        data = response.json()
        
        if data.get("articles"):
            news_list = []
            for article in data["articles"][:5]:
                news_list.append(f"- {article['title']}")
            return "\n".join(news_list)
        return "No news found"
    except Exception as e:
        return f"Error fetching news: {str(e)}"

def extract_city_from_message(message):
    """Try to extract city name from message"""
    patterns = [
        r'in\s+([A-Za-z\s]+?)(?:\?|$)',
        r'for\s+([A-Za-z\s]+?)(?:\?|$)',
        r'weather\s+([A-Za-z\s]+?)(?:\?|$)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, message, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return None

@app.post("/api/chat")
def chat(data: Message):
    user_message = data.message.lower()
    
    # Check if user asked for weather
    if "weather" in user_message or "temperature" in user_message:
        city = extract_city_from_message(data.message)
        
        if city:
            weather = get_weather(city)
            response_text = weather
        else:
            response_text = "Please specify a city. For example: 'What's the weather in New York?'"
        
        conversation_history.append({
            "role": "user",
            "content": data.message
        })
        conversation_history.append({
            "role": "assistant",
            "content": response_text
        })
        
        return {"response": response_text}
    
    # Check if user asked for news
    if "news" in user_message or "headlines" in user_message:
        news = get_news()
        response_text = f"Here are the latest news headlines:\n\n{news}"
        
        conversation_history.append({
            "role": "user",
            "content": data.message
        })
        conversation_history.append({
            "role": "assistant",
            "content": response_text
        })
        
        return {"response": response_text}
    
    # Check if user asked a math question
    if any(keyword in user_message for keyword in ["solve", "equation", "math", "calculate"]) or ("=" in user_message and ("x" in user_message or "y" in user_message)):
        # Try to extract and solve equation
        # Look for patterns like "x2+2x+1=0" or "solve x+5=10"
        math_result = solve_math(data.message)
        
        if math_result:
            response_text = math_result
            conversation_history.append({
                "role": "user",
                "content": data.message
            })
            conversation_history.append({
                "role": "assistant",
                "content": response_text
            })
            return {"response": response_text}
    
    # Otherwise, use AI for general conversation
    conversation_history.append({
        "role": "user",
        "content": data.message
    })
    
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a helpful personal AI assistant named Nova. Be concise and friendly."},
                *conversation_history
            ]
        )
        
        assistant_message = response.choices[0].message.content
        conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        return {"response": assistant_message}
    
    except Exception as e:
        return {"response": f"Error: {str(e)}"}

# Serve static files
app.mount("/", StaticFiles(directory="static", html=True), name="static")