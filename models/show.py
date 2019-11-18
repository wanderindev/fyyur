from datetime import datetime
from app import db
from .mixin import ModelMixin


class Show(db.Model, ModelMixin):
    __tablename__ = "shows"

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    artist_id = db.Column(
        db.Integer, db.ForeignKey("artists.id"), nullable=False
    )
    venue_id = db.Column(
        db.Integer, db.ForeignKey("venues.id"), nullable=False
    )

    def __init__(self, **kwargs):
        super(Show, self).__init__(**kwargs)

    @classmethod
    def upcoming_shows_by_venue(cls, _venue_id):
        shows = cls.query.filter(
            cls.venue_id == _venue_id, Show.start_time > datetime.now()
        ).all()
        return [
            {
                "artist_id": show.artist.id,
                "artist_name": show.artist.name,
                "artist_image_link": show.artist.image_link,
                "start_time": show.start_time.isoformat(),
            }
            for show in shows
        ]

    @classmethod
    def past_shows_by_venue(cls, _venue_id):
        shows = cls.query.filter(
            cls.venue_id == _venue_id, Show.start_time < datetime.now()
        ).all()
        return [
            {
                "artist_id": show.artist.id,
                "artist_name": show.artist.name,
                "artist_image_link": show.artist.image_link,
                "start_time": show.start_time.isoformat(),
            }
            for show in shows
        ]

    @classmethod
    def upcoming_shows_by_artist(cls, _artist_id):
        shows = cls.query.filter(
            cls.artist_id == _artist_id, Show.start_time > datetime.now()
        ).all()
        return [
            {
                "venue_id": show.venue.id,
                "venue_name": show.venue.name,
                "venue_image_link": show.venue.image_link,
                "start_time": show.start_time.isoformat(),
            }
            for show in shows
        ]

    @classmethod
    def past_shows_by_artist(cls, _artist_id):
        shows = cls.query.filter(
            cls.artist_id == _artist_id, Show.start_time < datetime.now()
        ).all()
        return [
            {
                "venue_id": show.venue.id,
                "venue_name": show.venue.name,
                "venue_image_link": show.venue.image_link,
                "start_time": show.start_time.isoformat(),
            }
            for show in shows
        ]

    @classmethod
    def get_shows(cls):
        return [
            {
                "venue_id": show.venue.id,
                "venue_name": show.venue.name,
                "artist_id": show.artist.id,
                "artist_name": show.artist.name,
                "artist_image_link": show.artist.image_link,
                "start_time": show.start_time.isoformat(),
            }
            for show in cls.query.all()
        ]
