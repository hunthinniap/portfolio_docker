from flask import Flask, request, render_template, g

import requests
from reader import (
    read_collections,
    read_cover,
    read_page_title,
    read_page_description,
    read_music_cover,
    read_music_specs,
    read_blog_spces,
    read_blog_content,
    read_video_link,
    read_video_specs,
    read_podcast_specs,
)


app = Flask(__name__)

def detect_device():
    user_agent = request.headers.get('User-Agent')
    mobile_agents = ['Mobile', 'Android', 'iPhone', 'iPad', 'iPod', 'BlackBerry', 'Opera Mini', 'IEMobile']
    return any(agent in user_agent for agent in mobile_agents)

@app.before_request
def before_request():
    g.is_mobile = detect_device()
    if g.is_mobile:
        g.header = 'mobile/'
    else:
        g.header = ''



@app.route("/")
def home():
    return render_template(g.header+"home.html")


@app.route("/photography")
def photography():
    photo_collections = read_cover()
    return render_template(g.header+"photography.html", collections=photo_collections)


@app.route("/music")
def music():
    cover_collections = read_music_cover()
    return render_template(g.header+"music.html", collections=cover_collections)


@app.route("/music/<music_title>")
def music_template(music_title):
    music_specs = read_music_specs(music_title)
    lyrics = requests.get(music_specs['lyrics']).text
    motivation = requests.get(music_specs['Motivation']).text
    return render_template(
        g.header+"music_template.html",
        specs = music_specs,
        lyrics = lyrics,
        motivation=motivation,
    )


@app.route("/photography/<collection_name>")
def photo_template(collection_name):
    # Fetch the photo collection details based on collection_name
    photos = read_collections(collection_name)
    title = read_page_title(collection_name)
    description = read_page_description(collection_name)
    return render_template(
        g.header+"photo_template.html",
        page=collection_name,
        photos=photos,
        title=title,
        description=description,
    )

@app.route("/blog")
def blog():
    specs = read_blog_spces()
    return render_template(g.header+"blog.html", specs = specs) 

@app.route("/blog/<blog_name>")
def blog_template(blog_name):
    blog, is_podcast = read_blog_content(blog_name)
    if is_podcast:
        specs = read_podcast_specs(blog_name)
        return render_template(g.header+"blog_template_podcast.html", blog = blog, title=blog_name,specs = specs)
    else:
        return render_template(g.header+"blog_template.html", blog = blog, title=blog_name) 

@app.route("/videography")
def videography():
    specs = read_video_specs()
    return render_template(g.header+"videography.html", videos = specs) 

@app.route("/videography/<video_name>")
def video_template(video_name):
    ytb_id = read_video_link(video_name)
    return render_template(g.header+"video_template.html", ytb_id = ytb_id, title=video_name) 

@app.route("/about")
def about():
    # Read the content from the text file
    response = requests.get('https://raw.githubusercontent.com/hunthinniap/portfolio_asset/main/About/journal.txt')
    dev_journey_content = response.text

    response = requests.get("https://raw.githubusercontent.com/hunthinniap/portfolio_asset/main/About/description.txt")
    description = response.text 
        
    # Render the about.html template with the content of the text file
    return render_template(g.header+'about.html', dev_journey_content=dev_journey_content, description=description)


@app.route("/template")
def template():
    return render_template("template.html")


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
