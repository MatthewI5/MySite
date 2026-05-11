





import quart 
import aiohttp

app = quart.Quart(__name__)

ALBUM_ID = "e9ac43a4-c934-4836-8369-c8ad6087f120?at=8cd0f5c8-d007-4b91-9c57-dde68b147f5d"
GALLERY_ROOT = "https://photos.matprojects.xyz"

@app.route('/api/gallery')
async def _gallery():

    async with aiohttp.ClientSession() as session:
        async with session.get(f'{GALLERY_ROOT}/api/albums/{ALBUM_ID}') as resp:
            data = await resp.json()
            return data



app.run(host='0.0.0.0', port=8000)