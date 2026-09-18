from fastapi import FastAPI
from starlette.responses import Response

app = FastAPI()

@app.get("/search")
def find_movie(title: str = ""):
    if not title:
        return Response("Error: No title provided", media_type="text/plain")
    
    # 1. Clean the input string and swap spaces out for query operators
    cleaned = title.strip().replace(" ", "+")
    
    # 2. Build the exact redirect syntax that resolves dynamic searches
    final_query_url = f"https://vr-m.net{cleaned}"
    
    # 3. Return it as pure plain text bytes for the VRChat client to parse
    return Response(content=str(final_query_url), media_type="text/plain")
