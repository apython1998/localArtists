from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/artist/<artist_name>')
def view_artist(artist_name):
    artist = {
        "artist_id": 1,
        "artist_name": artist_name,
        "artist_info": "some fake artist info"
    }
    return render_template("artist.html", artist=artist)

@app.route('/artists')
def list_artists():
    artist_list = [
        {
            "artist_id": 1,
            "artist_name": "Eric Clapton",
            "artist_info": "Some info"
        },
        {
            "artist_id": 2,
            "artist_name": "The Beatles",
            "artist_info": "Some info about the Beatles. John Lennon, Paul McCartney, George Harrison, and Ringo Starr are the best"
        },
        {
            "artist_id": 3,
            "artist_name": "Jon Bellion",
            "artist_info": ""
        }
    ]
    return render_template("artistList.html", artist_list=artist_list)

@app.route('/newArtist')
def create_artist():
    return render_template("newArtist.html")
