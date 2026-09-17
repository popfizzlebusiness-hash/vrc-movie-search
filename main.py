import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI, Response

app = FastAPI()

@app.get("/search")
def find_movie(title: str = ""):
    if not title:
        return Response(content="Error: No title provided", media_type="text/plain")
        
    # Query the vr-m.net search directory endpoint
    search_url = f"https://vr-m.net/0/s?q={title}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    try:
        req = requests.get(search_url, headers=headers, timeout=8)
        if req.status_code != 200:
            return Response(content=f"Error: Target site returned {req.status_code}", media_type="text/plain")
            
        soup = BeautifulSoup(req.text, 'html.parser')
        video_url = None
        
        # Scrape all anchor elements looking for common video play strings
        for anchor in soup.find_all('a', href=True):
            href = anchor['href']
            if '.mp4' in href or '.m3u8' in href or 'stream' in href:
                video_url = href
                break
                
        # Backup: Look for standard video media source embeddings
        if not video_url:
            source = soup.find('source', src=True)
            if source:
                video_url = source['src']
                
        if not video_url:
            return Response(content="Error: Link not found", media_type="text/plain")
            
        # Clean relative endpoints to form fully qualified paths
        if video_url.startswith('//'):
            video_url = 'https:' + video_url
        elif video_url.startswith('/'):
            video_url = 'https://vr-m.net/0/s?q=' + video_url
            
        # Output ONLY raw plain text so the VRChat video system reads it natively
        return Response(content=video_url, media_type="text/plain")
        
    except Exception as e:
        return Response(content=f"Error: {str(e)}", media_type="text/plain")
