from fastapi import FastAPI, Response
import requests

app = FastAPI()

@app.get("/search")
def find_movie(title: str = ""):
    if not title:
        return Response(content="Error: No title provided", media_type="text/plain")
    
    # Clean the input text and direct it straight to vr-m's specific movie search syntax
    cleaned_title = title.replace(" ", "+")
    target_link = f"https://vr-m.net{cleaned_title}"
    
    # We return the target link directly as plain text for ProTV to evaluate 
    return Response(content=target_link, media_type="text/plain")
