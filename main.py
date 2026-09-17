from fastapi import FastAPI, Response

app = FastAPI()

@app.get("/search")
def find_movie(title: str = ""):
    if not title:
        return Response(content="Error: No title provided", media_type="text/plain")
    
    # 1. Clean up any accidental spaces the user types
    cleaned_title = title.strip().replace(" ", "+")
    
    # 2. Build the exact search query format that vr-m.net reads
    target_link = f"https://vr-m.net/0/s?q={cleaned_title}"
    
    # 3. Return it as plain text for VRChat to use
    return Response(content=target_link, media_type="text/plain")
