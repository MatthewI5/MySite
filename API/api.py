import quart
import aiohttp
from aiocache import cached # Example: pip install aiocache

import os
import dotenv

app = quart.Quart(__name__)

dotenv.load_dotenv()

ALBUM_ID = os.getenv("IMMICH_ALBUM")
GALLERY_ROOT = os.getenv("IMMICH_BASE")

GHOST_ROOT = os.getenv("GHOST_BASE")
GHOST_KEY = os.getenv("GHOST_KEY")

ARGS = "?slug=website&withoutAssets=false"

# Global session to be initialized on startup
session = None

@app.before_serving
async def create_session():
    global session
    session = aiohttp.ClientSession()

@app.after_serving
async def close_session():
    await session.close()

def get_cors_headers():
    return {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Allow-Methods": "*"
    }


@app.route('/api/posts')
@cached(ttl=60)  # Cache the JSON response for 60 seconds
async def _posts():
    try:
        async with session.get(f'{GHOST_ROOT}/ghost/api/content/posts?key={GHOST_KEY}') as resp:
            data = await resp.json()
            return data, resp.status, get_cors_headers()
    except Exception as e:
        return {"error": str(e)}, 500, get_cors_headers()

@app.route('/api/gallery')
@cached(ttl=60) 
async def _gallery():
    try:
        async with session.get(f'{GALLERY_ROOT}/api/albums/{ALBUM_ID}{ARGS}') as resp:
            data = await resp.json()
            return data, resp.status, get_cors_headers()
    except Exception as e:
        return {"error": str(e)}, 500, get_cors_headers()

@app.route('/api/gallery/<photo_id>/<size>')
async def _gallery_photo(photo_id, size):
    url = f'{GALLERY_ROOT}/api/assets/{photo_id}/thumbnail{ARGS}&size={size}' if size != "original" else f'{GALLERY_ROOT}/api/assets/{photo_id}/original{ARGS}'
    
    resp = await session.get(url)
    
    if resp.status != 200:
        resp.close()
        return "Image not found", resp.status, get_cors_headers()

    @quart.stream_with_context
    async def stream_image():
        try:
            async for chunk in resp.content.iter_chunked(8192):
                yield chunk
        finally:
            resp.close()

    headers = get_cors_headers()
    headers["Content-Type"] = resp.headers.get("Content-Type", "image/jpeg")
    
    return stream_image(), resp.status, headers


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)