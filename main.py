pythonfrom fastapi import FastAPI, Response
import requests

app = FastAPI()

@app.get("/search")
def find_movie(title: str = ""):
    if not title:
        return Response(content="Error: No title provided", media_type="text/plain")
    
    # 1. Format the search string correctly
    cleaned_title = title.strip().replace(" ", "+")
    target_link = f"https://vr-m.net/?s={cleaned_title}"
    
    # 2. Add realistic browser headers so the site doesn't reject us with a 404
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5"
    }
    
    try:
        # Test connection to make sure it answers successfully
        check = requests.get(target_link, headers=headers, timeout=5)
        
        # If it returns a 404 anyway, fall back to the root database link directly
        if check.status_code == 404:
            fallback_link = f"https://vr-m.net/0/s?q={cleaned_title}"
            return Response(content=fallback_link, media_type="text/plain")
            
        # If the page layout is good, return the valid target link path
        return Response(content=target_link, media_type="text/plain")
        
    except Exception as e:
        # Fallback safeguard layout if a timeout or connection issue occurs
        safe_fallback = f"https://vr-m.net/?s={cleaned_title}"
        return Response(content=safe_fallback, media_type="text/plain")
        return Response(content=safe_fallback, media_type="text/plain")
