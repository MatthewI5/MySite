
const BASE = "https://api.matprojects.xyz";

async function Demo_Grid_Justified() {
    // 1. Fetch data first
    const r = await fetch(`${BASE}/api/gallery`);
    const data = await r.json();

    const tileWidth = Math.min(100 + (window.innerWidth / 12), 300);
    const $gallery = $("#nanogallery");

    // 2. Initialize the gallery empty
    $gallery.nanogallery2({
        thumbnailWidth: tileWidth,
        thumbnailHeight: 'auto',
        thumbnailAlignment: 'center',
        thumbnailGutterWidth: tileWidth / 10,
        thumbnailGutterHeight: tileWidth / 10,
        galleryTheme: {
            thumbnail: { borderColor: 'white', boxShadow: '5px 5px 20px rgba(0,0,0,0.1)' }
        },
        viewerTheme: { barColor: 'white', background: 'rgba(0,0,0,0.95)', barBackground: 'rgba(0,0,0,0.8)', titleFontSize: 60 },
        thumbnailDisplayTransition: 'slideUp2',
        thumbnailDisplayTransitionDuration: 1000,
        thumbnailDisplayInterval: 0,
        galleryDisplayTransition: 'rotateX',
        galleryDisplayTransitionDuration: 2000,
        thumbnailHoverEffect2: 'image_scale_1.05_1.0',
        thumbnailLabel: { display: false },
        viewerToolbar: { display: true, standard: 'label' },
        viewerTools: { topLeft: 'pageCounter, playPauseButton', topRight: 'closeButton' },
        viewerText: { display: true, titleDisplay: true, descriptionDisplay: true },
        viewerHideToolsDelay: 30000000,
        viewerMaxZoom: 50,
        items: [] 
    });

    // 3. Ensure NGY2Item is accessible
    // If NGY2Item is not global, we grab it from the plugin's internal scope
    const ItemClass = (typeof NGY2Item !== 'undefined') ? NGY2Item : $.nanogallery2.Item;

    if (!ItemClass) {
        console.error("nanogallery2 Item class not found. Ensure the library is loaded correctly.");
        return;
    }

    const ngy2data = $gallery.nanogallery2('data');
    const instance = $gallery.nanogallery2('instance');

    // 4. Load images one by one, delay each by 100ms each time

    

    function loadImage(asset) {

        const thumbURL = `${BASE}/api/gallery/${asset.id}/thumbnail`;
        const fullsizeURL = `${BASE}/api/gallery/${asset.id}/fullsize`;
        
        const img = new Image();
        img.src = thumbURL;

        img.onload = function() {


            let date = new Date(asset.exifInfo.dateTimeOriginal);
            let formattedDate = date.toLocaleDateString('en-GB', {
                day: 'numeric',
                month: 'long',
                year: 'numeric'
            });

            // Create the new item using the identified class
            const newItem = ItemClass.New(
                instance, 
                `${asset.exifInfo.make} ${asset.exifInfo.model} - ${formattedDate}`, 
                asset.exifInfo.description || "", 
                asset.id, 
                '0', 
                'image', 
                ''
            );

            // Configure the item
            newItem.thumbSet(thumbURL, img.width, img.height);
            newItem.setMediaURL(fullsizeURL, 'img');

            // Add to the Gallery Object Model (GOM)
            if (ngy2data.items[ngy2data.gallery.albumIdx].GetID() == 0) {
                newItem.addToGOM();
                // Refresh the layout
                $gallery.nanogallery2('resize');
            }
        };
    };

    i = 0;
    for (asset of data.assets) {
        await new Promise(resolve => setTimeout(resolve, i*75));
        loadImage(asset);
        i++;
    }
}

// Use jQuery ready to ensure the library is fully initialized
$(document).ready(function() {
    // Track page visit
    fetch("https://api.matprojects.xyz/api/visits/gallery", { method: "POST" });
    
    Demo_Grid_Justified();
});