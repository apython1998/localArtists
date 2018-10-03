from flask import render_template, url_for, redirect, flash, request
from app import app, db
from app.models import Artist, Event, Venue, ArtistToEvent
from app.forms import NewArtistForm
from datetime import datetime
from sqlalchemy import func


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/reset_db')
def reset_db():
    flash("Resetting database: deleting old data and repopulating with dummy data")
    # clear all data from all tables
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print('Clear table {}'.format(table))
        db.session.execute(table.delete())
    db.session.commit()
    default_venues = [
        Venue(name='Stewart Park', address='1 James L Gibbs Dr, Ithaca, NY 14850'),
        Venue(name='The Haunt', address='702 Willow Ave, Ithaca, NY 14850'),
        Venue(name='Ithaca College', address='953 Danby Rd, Ithaca, NY 14850')
    ]
    dates = [
        datetime(2018, 9, 21, 20, 0, 0),
        datetime(2018, 3, 7, 20, 0, 0),
        datetime(2034, 5, 18, 21, 0, 0)
    ]
    default_events = [
        Event(name='Cayuga Sound Festival', time=dates[0], venue_id=1),
        Event(name='Matt and Kim Concert', time=dates[1], venue_id=2),
        Event(name='Young The Giant Concert', time=dates[2], venue_id=2),
        Event(name='Jon Bellion Concert', time=dates[1], venue_id=3)
    ]
    default_artists = [
        Artist(name='X Ambassadors', hometown='Ithaca, NY', description='The X Ambassadors description'),
        Artist(name='Young The Giant', hometown='Irvine, CA', description='Young The Giant description'),
        Artist(name='Matt and Kim', hometown='Boston, MA', description='Matt and Kim description'),
        Artist(name='Roots', hometown='Philadelphia, PA', description='Roots description'),
        Artist(name='Jon Bellion', hometown='Smithtown, NY', description='Jon Bellion description')
    ]
    default_a_to_e = [
        ArtistToEvent(artist_id=1, event_id=1),
        ArtistToEvent(artist_id=2, event_id=1),
        ArtistToEvent(artist_id=3, event_id=1),
        ArtistToEvent(artist_id=3, event_id=2),
        ArtistToEvent(artist_id=2, event_id=3),
        ArtistToEvent(artist_id=4, event_id=1),
        ArtistToEvent(artist_id=5, event_id=4)
    ]
    db.session.add_all(default_artists)
    db.session.add_all(default_venues)
    db.session.add_all(default_events)
    db.session.add_all(default_a_to_e)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/artist/<artist_name>')
def view_artist(artist_name):
    artist = Artist.query.filter_by(name=artist_name).first_or_404()
    return render_template("artist.html", artist=artist)


@app.route('/artists')
def list_artists():
    artist_list = Artist.query.order_by(func.lower(Artist.name)).all()
    return render_template("artistList.html", artist_list=artist_list)


@app.route('/newArtist', methods=['GET', 'POST'])
def new_artist():
    form = NewArtistForm()
    if form.validate_on_submit():
        if Artist.query.filter_by(name=form.name.data).count() > 0:
            flash('Error! Artist ' + form.name.data + ' has already been created!')
            return redirect(url_for('new_artist'))
        else:
            form_artist = Artist(name=form.name.data, hometown=form.hometown.data, description=form.description.data)
            db.session.add(form_artist)
            db.session.commit()
            flash('New Artist Successfully Submitted!')
            return render_template("artist.html", artist=form_artist)
    return render_template("newArtist.html", title='New Artist', form=form)
