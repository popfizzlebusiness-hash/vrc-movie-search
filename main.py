from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
import requests

app = FastAPI()

@app.get("/search", response_class=PlainTextResponse)
def find_movie(title: str = ""):
    if not title:
        return "Error: No title provided"
    
    cleaned = title.strip().replace(" ", "+")
    target_link = f"https://vr-m.net/?s={cleaned}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        check = requests.get(target_link, headers=headers, timeout=5)
        if check.status_code == 404:
            return f"https://vr-m.net/0/s?q={cleaned}"
        return target_link
    except Exception:
        return f"https://vr-m.net/?s={cleaned}"
