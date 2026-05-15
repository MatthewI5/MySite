

async function loadPosts() {
    r = await fetch("https://api.matprojects.xyz/api/posts");
    posts = await r.json();

    container = document.getElementById("tag-container");

    i = 0;
    for (post of posts.posts) {
        if (i < 3) {
            template = document.getElementById("tag-template").innerHTML;

            let date = new Date(post.published_at);
            let formattedDate = date.toLocaleDateString('en-GB', {
                day: 'numeric',
                month: 'long',
                year: 'numeric'
            });



            tag = template.replaceAll("{{title}}", post.title);
            tag = tag.replaceAll("{{description}}", post.excerpt);
            tag = tag.replaceAll("{{date}}", formattedDate);
            tag = tag.replaceAll("{{slug}}", post.slug);
            tag = tag.replaceAll("{{image_src}}", post.feature_image);
            tag = tag.replaceAll("{{read_time}}", post.reading_time);
            tag = tag.replaceAll("{{fade_delay}}", 0.25+(i*0.25));
            container.innerHTML += tag;

            i++;
        }
        
    }
    
}

loadPosts();