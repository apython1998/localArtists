from datetime import datetime
from app import db, login
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from hashlib import md5


class ArtistToEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))


class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    hometown = db.Column(db.String(64), index=True)
    description = db.Column(db.String(256))
    events = db.relationship('Event', secondary='artist_to_event')

    def __repr__(self):
        return '<Artist {}>'.format(self.name)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'))
    artists = db.relationship('Artist', secondary='artist_to_event')

    def __repr__(self):
        return '<Event {} on {}>'.format(self.name, self.time)


class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    address = db.Column(db.String(256), unique=True)
    hosting = db.relationship('Event', backref='venue', lazy='dynamic')

    def __repr__(self):
        return '<Venue {}>'.format(self.name)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
