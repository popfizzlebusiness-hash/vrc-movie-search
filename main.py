from fastapi import FastAPI
from starlette.responses import Response
import requests
from bs4 import BeautifulSoup

app = FastAPI()

@app.get("/search")
def find_movie(title: str = ""):
    if not title:
        return Response("Error: No title provided", media_type="text/plain")
    
    # 1. Clean the search parameter string formatting cleanly
    cleaned = title.strip().replace(" ", "+")
    search_url = f"https://vr-m.net{cleaned}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        # 2. Silently pull the dynamic catalog search page in the background
        res = requests.get(search_url, headers=headers, timeout=6)
        if res.status_code != 200:
            return Response(f"https://vr-m.net{cleaned}.mp4", media_type="text/plain")
            
        # 3. Use BeautifulSoup to scan the page elements for video source streams
        soup = BeautifulSoup(res.text, 'html.parser')
        video_url = ""
        
        # Look through all video tag properties or file anchor sources
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            if '.mp4' in href or '.m3u8' in href or 'stream' in href:
                video_url = href
                break
                
        if not video_url:
            source_tag = soup.find('source', src=True)
            if source_tag:
                video_url = source_tag['src']
                
        # 4. Clean up the resulting layout link strings to ensure standard forward slashes
        if video_url:
            if video_url.startswith('//'):
                video_url = 'https:' + video_url
            elif video_url.startswith('/'):
                video_url = 'https://vr-m.net' + video_url
            return Response(content=str(video_url), media_type="text/plain")
            
        # 5. Direct fallback generation if parsing encounters unexpected HTML layouts
        fallback = f"https://vr-m.net{cleaned}.mp4"
        return Response(content=str(fallback), media_type="text/plain")
        
    except Exception:
        fallback = f"https://vr-m.net{cleaned}.mp4"
        return Response(content=str(fallback), media_type="text/plain")
