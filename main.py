from fastapi import FastAPI
from starlette.responses import Response

app = FastAPI()

@app.get("/search")
def find_movie(title: str = ""):
    if not title:
        return Response("Error: No title provided", media_type="text/plain")
    
    # Clean the search phrase string
    cleaned = title.strip().replace(" ", "+")
    
    # Hardcode the clean /stream/ format explicitly to guarantee slashes
    final_output = f"https://vr-m.net/stream/{cleaned}.mp4"
    
    # Return raw text bytes directly to completely skip rendering wrappers
    return Response(content=str(final_output), media_type="text/plain")
