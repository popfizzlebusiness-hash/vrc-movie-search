from fastapi import FastAPI
from starlette.responses import Response
import requests

app = FastAPI()

@app.get("/search")
def find_movie(title: str = ""):
    if not title:
        return Response("Error: No title provided", media_type="text/plain")
    
    cleaned = title.strip().replace(" ", "+")
    target_link = f"https://vr-m.net/?s={cleaned}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        check = requests.get(target_link, headers=headers, timeout=5)
        if check.status_code == 404:
            output = f"https://vr-m.net/0/s?q={cleaned}"
        else:
            output = target_link
    except Exception:
        output = f"https://vr-m.net/?s={cleaned}"

    # Return raw text bytes directly to completely prevent metadata wrappers
    return Response(content=str(output), media_type="text/plain")
