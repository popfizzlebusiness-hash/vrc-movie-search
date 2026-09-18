from fastapi import FastAPI, Response
import requests

app = FastAPI()

@app.get("/search")
def find_movie(title: str = ""):
    if not title:
        return Response(content="Error: No title provided", media_type="text/plain")
    
    # 1. Clean up spaces and format the search term
    cleaned_title = title.strip().replace(" ", "+")
    
    # 2. Updated direct link parameter pattern for the media provider catalog
    target_link = f"https://vr-m.net{cleaned_title}"
    
    # 3. Return it as clean text for ProTV to parse natively
    return Response(content=target_link, media_type="text/plain")
