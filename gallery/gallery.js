
BASE = "https://api.matprojects.xyz"


async function Demo_Grid_Justified() {


    r = await fetch(`${BASE}/api/gallery`)
    data = await r.json()
    console.log(data)

    items = []
    for (asset of data.assets) {
        items.push({
            src: `${BASE}/api/gallery/${asset.id}/fullsize`,
            srct: `${BASE}/api/gallery/${asset.id}/thumbnail`,
            title: asset.name
        })
    }

    $("#nanogallery").nanogallery2({
        thumbnailWidth:   400,
        thumbnailHeight: 300,
        itemsBaseURL:     `${BASE}`,
        items: items
    });
}

Demo_Grid_Justified();