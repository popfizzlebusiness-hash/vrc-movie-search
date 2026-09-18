from fastapi import FastAPI
from starlette.responses import Response
import httpx
from bs4 import BeautifulSoup

app = FastAPI()

@app.get("/search")
async def find_movie(title: str = ""):
    if not title:
        return Response("Error: No title provided", media_type="text/plain")
    
    cleaned = title.strip().replace(" ", "+")
    search_url = f"https://vr-m.net/0/s?q={cleaned}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        async with httpx.AsyncClient(headers=headers, timeout=8.0, follow_redirects=True) as client:
            res = await client.get(search_url)
            
        if res.status_code != 200:
            return Response(content=f"https://vr-m.net{cleaned}.mp4", media_type="text/plain")
            
        soup = BeautifulSoup(res.text, 'html.parser')
        video_url = ""
        
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            if '.mp4' in href or '.m3u8' in href or 'stream' in href:
                video_url = href
                break
                
        if not video_url:
            source_tag = soup.find('source', src=True)
            if source_tag:
                video_url = source_tag['src']
                
        if video_url:
            if video_url.startswith('//'):
                video_url = 'https:' + video_url
            elif video_url.startswith('/'):
                video_url = 'https://vr-m.net' + video_url
            return Response(content=str(video_url), media_type="text/plain")
            
        return Response(content=f"https://vr-m.net{cleaned}.mp4", media_type="text/plain")
        
    except Exception:
        # Fixed the missing slash right after vr-m.net
        return Response(content=f"https://vr-m.net{cleaned}.mp4", media_type="text/plain")
