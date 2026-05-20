import quart
import aiohttp
from aiocache import cached
import aiomysql

import os
import dotenv

app = quart.Quart(__name__)

dotenv.load_dotenv()

ALBUM_ID = os.getenv("IMMICH_ALBUM")
GALLERY_ROOT = os.getenv("IMMICH_BASE")

GHOST_ROOT = os.getenv("GHOST_BASE")
GHOST_KEY = os.getenv("GHOST_KEY")

DB_HOST = os.getenv("MYSQL_HOST")
DB_PORT = os.getenv("MYSQL_PORT")
DB_USER = os.getenv("MYSQL_USER")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD")

ARGS = "?slug=website&withoutAssets=false"

# Global session and database pool to be initialized on startup
session = None
db_pool = None

@app.before_serving
async def create_session():
    global session, db_pool
    session = aiohttp.ClientSession()
    
    # Create MySQL connection pool
    db_pool = await aiomysql.create_pool(
        host=DB_HOST,
        port=int(DB_PORT) if DB_PORT else 3306,
        user=DB_USER,
        password=DB_PASSWORD,
        minsize=5,
        maxsize=10
    )
    
    # Create database and table if they don't exist
    async with db_pool.acquire() as conn:
        async with conn.cursor() as cursor:
            # Create database
            await cursor.execute("CREATE DATABASE IF NOT EXISTS mysite")
            await conn.commit()
            
            # Select the database
            await cursor.execute("USE mysite")
            
            # Create visits table
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS visits (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                       page VARCHAR(255) NOT NULL UNIQUE,
                       visit_count INT DEFAULT 0,
                       last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            """)
            await conn.commit()
            

@app.after_serving
async def close_session():
    global db_pool
    await session.close()
    if db_pool:
        db_pool.close()
        await db_pool.wait_closed()

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


@app.route('/api/visits/', methods=['POST'])
@app.route('/api/visits/<page>', methods=['POST'])
async def _add_visit(page="/"):
    """Increment the visit counter for a specific page in the database"""
    try:
        async with db_pool.acquire() as conn:
            async with conn.cursor() as cursor:
                # Select the database
                await cursor.execute("USE mysite")
                
                   # Insert or update visit count for the page
                await cursor.execute(
                       "INSERT INTO visits (page, visit_count) VALUES (%s, 1) ON DUPLICATE KEY UPDATE visit_count = visit_count + 1",
                       (page,)
                )
                await conn.commit()
                
                # Get the updated count
                await cursor.execute("SELECT visit_count FROM visits WHERE page = %s", (page,))
                result = await cursor.fetchone()
                visit_count = result[0] if result else 0
                
                return {"success": True, "page": page, "visit_count": visit_count}, 200, get_cors_headers()
    except Exception as e:
        return {"error": str(e)}, 500, get_cors_headers()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)