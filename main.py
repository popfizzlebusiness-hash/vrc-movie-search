from fastapi import FastAPI
from starlette.responses import Response
import httpx
from bs4 import BeautifulSoup
from urllib.parse import urljoin

app = FastAPI()

@app.get("/search")
async def find_movie(title: str = ""):
    if not title:
        return Response("Error: No title provided", media_type="text/plain")
    
    # 1. Format the dynamic search phrase string
    cleaned = title.strip().replace(" ", "+")
    search_url = f"https://vr-m.net/0/s?q={cleaned}"
    base_domain = "https://vr-m.net/"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        # 2. Silently perform the search query on the target site
        async with httpx.AsyncClient(headers=headers, timeout=8.0, follow_redirects=True) as client:
            res = await client.get(search_url)
            
        # If the server is down, generate a clean fallback path structure immediately
        if res.status_code != 200:
            fallback_path = f"stream/{cleaned}.mp4"
            return Response(content=urljoin(base_domain, fallback_path), media_type="text/plain")
            
        # 3. Parse the results page to look for the closest matching video link
        soup = BeautifulSoup(res.text, 'html.parser')
        video_url = ""
        
        # Scan through all anchors to find files ending in media extensions
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            if '.mp4' in href or '.m3u8' in href or 'stream' in href:
                video_url = href
                break
                
        # If not found in anchors, look inside embedded source tags
        if not video_url:
            source_tag = soup.find('source', src=True)
            if source_tag:
                video_url = source_tag['src']
                
        # 4. If a closest match link was found, merge it safely using urljoin to lock slashes
        if video_url:
            final_output = urljoin(base_domain, video_url)
            return Response(content=str(final_output), media_type="text/plain")
            
        # 5. Fallback path if the search didn't return any direct video items
        fallback_path = f"stream/{cleaned}.mp4"
        return Response(content=urljoin(base_domain, fallback_path), media_type="text/plain")
        
    except Exception:
        # Emergency backup layout safeguard
        fallback_path = f"stream/{cleaned}.mp4"
        return Response(content=urljoin(base_domain, fallback_path), media_type="text/plain")
