
BASE = "/"
ALBUM_ID = "e9ac43a4-c934-4836-8369-c8ad6087f120?at=8cd0f5c8-d007-4b91-9c57-dde68b147f5d"

async function Demo_Grid_Justified() {


    r = await fetch(`${BASE}/api/albums/${ALBUM_ID}?withoutAssets=false`)
    data = await r.json()
    console.log(data)

    $("#nanogallery").nanogallery2({
        thumbnailHeight:  200,
        thumbnailWidth:   200,
        itemsBaseURL:     `${BASE}`,
        items: [
            { src: '/assets/8cd0f5c8-d007-4b91-9c57-dde68b147f5d/thumbnail?size=preview&c=oPcJHYJYeHh%2Fhoh8d4d4lGaPZ%2FZ4&edited=true', srct: '/assets/8cd0f5c8-d007-4b91-9c57-dde68b147f5d/thumbnail?size=thumbnail&c=oPcJHYJYeHh%2Fhoh8d4d4lGaPZ%2FZ4&edited=true', title: 'Title 1' }
        ]
    });
}

Demo_Grid_Justified();