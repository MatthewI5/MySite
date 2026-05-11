


import quart 
import aiohttp

app = quart.Quart(__name__)

ALBUM_ID = "742c8e97-1a4a-4bbe-bc52-4a350855ae36"
GALLERY_ROOT = "https://photos.matprojects.xyz"
ARGS = "?slug=website&withoutAssets=false"

@app.route('/api/gallery')
async def _gallery():

    async with aiohttp.ClientSession() as session:
        async with session.get(f'{GALLERY_ROOT}/api/albums/{ALBUM_ID}{ARGS}') as resp:
            data = await resp.json()
            return data

@app.route('/api/gallery/<photo_id>/<size>')
async def _gallery_photo(photo_id, size):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{GALLERY_ROOT}/api/assets/{photo_id}/thumbnail{ARGS}&size={size}') as resp:

            
            status = resp.status 
            
            # 2. content equivalent (MUST be awaited)
            content = await resp.read() 
            
            # 3. headers.items() equivalent
            headers = resp.headers.items()
            
            return content, status, headers


app.run(host='0.0.0.0', port=8000)