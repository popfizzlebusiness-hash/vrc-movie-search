from fastapi import FastAPI
from starlette.responses import Response
import requests

app = FastAPI()

@app.get("/search")
def find_movie(title: str = ""):
    if not title:
        return Response("Error: No title provided", media_type="text/plain")
    
    # 1. Format the search string correctly for the database query
    cleaned_title = title.strip().replace(" ", "+")
    target_url = f"https://vr-m.net{cleaned_title}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        # 2. Silently fetch the search results page in the background
        response = requests.get(target_url, headers=headers, timeout=6)
        
        # 3. Look for the actual streaming video endpoints hidden in the text data
        # We search raw text loops to find direct streaming video files (.mp4 or .m3u8)
        content_str = response.text
        
        # Simple extraction search for absolute video links
        start_idx = content_str.find("https://")
        video_url = ""
        
        while start_idx != -1:
            # Look for standard video extensions in the web content data
            end_idx_mp4 = content_str.find(".mp4", start_idx)
            end_idx_m3u8 = content_str.find(".m3u8", start_idx)
            
            # Find whichever extension comes first
            targets = [idx for idx in [end_idx_mp4, end_idx_m3u8] if idx != -1]
            if targets:
                end_pos = min(targets) + (4 if min(targets) == end_idx_mp4 else 5)
                potential_url = content_str[start_idx:end_pos]
                # Filter out garbage layouts and grab the stream
                if "vr-m.net" in potential_url or "cdn" in potential_url:
                    video_url = potential_url
                    break
            
            start_idx = content_str.find("https://", start_idx + 8)

        # 4. Fallback safeguard: If no direct stream is visible, output a native stream fallback template
        if not video_url:
            video_url = f"https://vr-m.net{cleaned_title}.mp4"
            
        return Response(content=video_url, media_type="text/plain")
        
    except Exception:
        # Emergency backup fallback loop formatting
        return Response(content=f"https://vr-m.net{cleaned_title}.mp4", media_type="text/plain")
