
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
            title: `${asset.exifInfo.make} ${asset.exifInfo.model}`,
            description: asset.exifInfo.description == "" ? "No description provided" : asset.exifInfo.description
        })
    }

    tileWidth = Math.min(100 + (window.innerWidth/12), 300)

    $("#nanogallery").nanogallery2({
        thumbnailWidth: tileWidth,
        thumbnailHeight: 'auto',
        thumbnailAlignment: 'center',
        thumbnailGutterWidth : tileWidth / 10,
        thumbnailGutterHeight : tileWidth / 10,
        galleryTheme: {
            thumbnail : { borderColor: 'white', boxShadow: '5px 5px 20px rgba(0,0,0,0.1)' }
        },
        viewerTheme : { barColor: 'white', background: 'rgba(0,0,0,0.95)', barBackground:'rgba(0,0,0,0.8)', titleFontSize: 60},
        thumbnailDisplayTransition:          'slideUp2',
        thumbnailDisplayTransitionDuration:  1000,
        thumbnailDisplayInterval:            100,   
        galleryDisplayTransition:            'rotateX',
        galleryDisplayTransitionDuration:    2000,
        thumbnailHoverEffect2:'image_scale_1.05_1.0',
        thumbnailLabel: {
            display: false,
        },
        viewerToolbar: {
            display: true,
            standard: 'label'
        },
        viewerTools:    {
            topLeft:    'pageCounter, playPauseButton',
            topRight:   'closeButton'
        },
        viewerText: {
            display: true,              // Ensure text is enabled
            titleDisplay: true,        // Show the title
            descriptionDisplay: true   // Show the description
        },
        viewerHideToolsDelay: 30000000,
        viewerMaxZoom: 50,
        itemsBaseURL:     `${BASE}`,
        items: items
    });
}

window.onload = async function() {
    await Demo_Grid_Justified()
}