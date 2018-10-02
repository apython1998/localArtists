from datetime import datetime
from app import db


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
