from flask import render_template
from app import app


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/artist/<artist_name>')
def view_artist(artist_name):
    artist = {
        "name": artist_name,
        "hometown": "City, State",
        "info": "some fake artist info",
        "events": ["Fake Event", "Fake Event 2"]
    }
    return render_template("artist.html", artist=artist)


@app.route('/artists')
def list_artists():
    artist_list = [
        {
            "name": "Eric Clapton",
            "hometown": "City, State",
            "info": "Some info",
            "events": []
        },
        {
            "name": "The Beatles",
            "hometown": "City, State",
            "info": "Some info about the Beatles. John Lennon, Paul McCartney, George Harrison, and Ringo Starr are the best",
            "events": []
        },
        {
            "name": "Jon Bellion",
            "hometown": "Smithtown, NY",
            "info": "Some info",
            "events": []
        }
    ]
    return render_template("artistList.html", artist_list=artist_list)


@app.route('/newArtist')
def new_artist():
    return render_template("newArtist.html")
