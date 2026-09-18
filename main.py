from fastapi import FastAPI
from starlette.responses import Response
import requests

app = FastAPI()

@app.get("/search")
def find_movie(title: str = ""):
    if not title:
        return Response("Error: No title provided", media_type="text/plain")
    
    cleaned_title = title.strip().replace(" ", "+")
    target_url = f"https://vr-m.net{cleaned_title}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(target_url, headers=headers, timeout=6)
        content_str = response.text
        
        start_idx = content_str.find("https://")
        video_url = ""
        
        while start_idx != -1:
            end_idx_mp4 = content_str.find(".mp4", start_idx)
            end_idx_m3u8 = content_str.find(".m3u8", start_idx)
            
            targets = [idx for idx in [end_idx_mp4, end_idx_m3u8] if idx != -1]
            if targets:
                end_pos = min(targets) + (4 if min(targets) == end_idx_mp4 else 5)
                potential_url = content_str[start_idx:end_pos]
                if "vr-m.net" in potential_url or "cdn" in potential_url:
                    video_url = potential_url
                    break
            
            start_idx = content_str.find("https://", start_idx + 8)

        # FIX: Added the missing forward slash after .net
        if not video_url:
            video_url = f"https://vr-m.net{cleaned_title}.mp4"
            
        return Response(content=video_url, media_type="text/plain")
        
    except Exception:
        # FIX: Added the missing forward slash after .net
        return Response(content=f"https://vr-m.net{cleaned_title}.mp4", media_type="text/plain")
