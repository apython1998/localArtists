from app import app, db
from app.models import Artist, Event, Venue, ArtistToEvent


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Artist': Artist, 'Event': Event, 'Venue': Venue, 'ArtistToEvent': ArtistToEvent}
