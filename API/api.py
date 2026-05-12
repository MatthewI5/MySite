


import quart 
import aiohttp

app = quart.Quart(__name__)

ALBUM_ID = "742c8e97-1a4a-4bbe-bc52-4a350855ae36"
GALLERY_ROOT = "https://photos.matprojects.xyz"
ARGS = "?slug=website&withoutAssets=false"

def cors_headers(headers : list):

    headers = [h for h in headers if h[0].lower() not in ["access-control-allow-origin", "access-control-allow-headers", "access-control-allow-methods"]]

    headers.append(("Access-Control-Allow-Origin", "*"))
    headers.append(("Access-Control-Allow-Headers", "*"))
    headers.append(("Access-Control-Allow-Methods", "*"))

    return headers

@app.route('/api/gallery')
async def _gallery():

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{GALLERY_ROOT}/api/albums/{ALBUM_ID}{ARGS}') as resp:
                data = await resp.json()

                headers = ( resp.headers).items()
                
                headers = list(headers)
                headers = cors_headers([])

                print(data, resp.status, headers )
                return data, resp.status, dict(headers) 
    except Exception as e:
        print(e)
        return {"error": "Failed to fetch gallery data"}, 500, [("Access-Control-Allow-Origin", "*"), ("Access-Control-Allow-Headers", "*"), ("Access-Control-Allow-Methods", "*")]

@app.route('/api/gallery/<photo_id>/<size>')
async def _gallery_photo(photo_id, size):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{GALLERY_ROOT}/api/assets/{photo_id}/thumbnail{ARGS}&size={size}') as resp:

            
            status = resp.status 
            
            # 2. content equivalent (MUST be awaited)
            content = await resp.read() 
            
            # 3. headers.items() equivalent
            headers = ( resp.headers).items()

            # add cors to headers 
            headers = list(headers)
            headers = cors_headers([])

            
            return content, status, headers


app.run(host='0.0.0.0', port=8000)