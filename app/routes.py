from flask import render_template, url_for, redirect, flash, request
from flask_login import login_required, login_user, logout_user, current_user
from app import app, db
from app.models import Artist, Event, Venue, ArtistToEvent, User
from app.forms import NewArtistForm, LoginForm, RegistrationForm, EditProfileForm, \
    NewEventForm, NewVenueForm
from datetime import datetime
from sqlalchemy import func
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
@login_required
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
    return render_template("artist_list.html", artist_list=artist_list)


@app.route('/newArtist', methods=['GET', 'POST'])
@login_required
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
    return render_template("new_artist_form.html", title='New Artist', form=form)


@app.route('/newEvent', methods=['GET', 'POST'])
@login_required
def new_event():
    form = NewEventForm()
    form.venue.choices = [(v.id, v.name) for v in Venue.query.distinct().order_by(Venue.name).all()]
    form.artists.choices = [(a.id, a.name) for a in Artist.query.distinct().order_by(Artist.name).all()]
    if form.validate_on_submit():
        form_event = Event(name=form.name.data, time=form.time.data, venue_id=form.venue.data)
        db.session.add(form_event)
        db.session.commit()
        for artist_id in form.artists.data:
            form_a_to_e = ArtistToEvent(artist_id=artist_id, event_id=form_event.id)
            db.session.add(form_a_to_e)
        db.session.commit()
        flash('New Event Successfully Submitted!')
        return redirect(url_for('index'))
    return render_template('new_event_form.html', title='New Event', form=form)


@app.route('/newVenue', methods=['GET', 'POST'])
@login_required
def new_venue():
    form = NewVenueForm()
    if form.validate_on_submit():
        if Venue.query.filter_by(address=form.address.data).count() > 0:
            flash('Venue with that address has already been created!')
            return redirect(url_for('new_venue'))
        form_venue = Venue(name=form.name.data, address=form.address.data)
        db.session.add(form_venue)
        db.session.commit()
        flash('New Venue Successfully Submitted!')
        return redirect(url_for('index'))
    return render_template('new_venue_form.html', title='New Venue', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid Username or Password')
            return redirect(url_for('login'))
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        login_user(user=user, remember=form.remember_me.data)
        return redirect(next_page)
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        newuser = User(username=form.username.data, email=form.email.data)
        newuser.set_password(form.password.data)
        db.session.add(newuser)
        db.session.commit()
        flash('Congratulations! You are now registered')
        login_user(newuser)
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)

