from fastapi import FastAPI, Response
import requests

app = FastAPI()

@app.get("/search")
def find_movie(title: str = ""):
    if not title:
        return Response(content="Error: No title provided", media_type="text/plain")
    
    cleaned = title.strip().replace(" ", "+")
    target_link = f"https://vr-m.net/?s={cleaned}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        check = requests.get(target_link, headers=headers, timeout=5)
        if check.status_code == 404:
            return Response(content=f"https://vr-m.net/0/s?q={cleaned}", media_type="text/plain")
        return Response(content=target_link, media_type="text/plain")
    except Exception:
        return Response(content=f"https://vr-m.net/?s={cleaned}", media_type="text/plain")
