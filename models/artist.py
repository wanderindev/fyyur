from datetime import datetime
from sqlalchemy import exc
from app import db
from constants import GENRE_CHECK
from .mixin import ModelMixin
from .show import Show


class Artist(db.Model, ModelMixin):
    __tablename__ = "artists"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(30)), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(500))
    seeking_venue = db.Column(db.Boolean, default=True)
    seeking_description = db.Column(db.String(500))
    date_created = db.Column(db.DateTime, nullable=False,
                             default=datetime.utcnow)
    shows = db.relationship(
        "Show", backref="artist", lazy=True, cascade="delete"
    )

    def __init__(self, **kwargs):
        super(Artist, self).__init__(**kwargs)
        check_genres = all(genre in GENRE_CHECK for genre in self.genres)
        if not check_genres:
            raise exc.ProgrammingError(
                "Invalid genre",
                {"Genres passed": self.genres},
                {"Genres allowed": GENRE_CHECK},
            )

    @classmethod
    def past_shows(cls, _id):
        return Show.past_shows_by_artist(_id)

    @classmethod
    def past_shows_count(cls, _id):
        return len(cls.past_shows(_id))

    @classmethod
    def upcoming_shows(cls, _id):
        return Show.upcoming_shows_by_artist(_id)

    @classmethod
    def upcoming_shows_count(cls, _id):
        return len(cls.upcoming_shows(_id))

    @classmethod
    def get_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def get_artists(cls):
        return [
            {"id": artist.id, "name": artist.name,}
            for artist in cls.query.all()
        ]

    @classmethod
    def search(cls, search_term):
        artists = cls.query.filter(cls.name.ilike(f"%{search_term}%")).all()
        return {
            "data": [
                {
                    "id": artist.id,
                    "name": artist.name,
                    "num_upcoming_shows": cls.upcoming_shows_count(artist.id),
                }
                for artist in artists
            ],
            "count": len(artists),
        }

    @classmethod
    def get_artist(cls, _id):
        _obj = {
            "past_shows": cls.past_shows(_id),
            "past_shows_count": cls.past_shows_count(_id),
            "upcoming_shows": cls.upcoming_shows(_id),
            "upcoming_shows_count": cls.upcoming_shows_count(_id),
        }
        artist = cls.get_by_id(_id)
        if not artist:
            return None
        return cls.to_dict(artist, _obj)

    @classmethod
    def update(cls, _id, data):
        artist = cls.get_by_id(_id)
        artist.name = data.get("name", "")
        artist.city = data.get("city", "")
        artist.state = data.get("state", "")
        artist.phone = data.get("phone", "")
        artist.genres = data.get("genres", [])
        artist.image_link = data.get("image_link", "")
        artist.facebook_link = data.get("facebook_link", "")
        artist.website = data.get("website", "")
        artist.seeking_venue = data.get("seeking_venue", False)
        artist.seeking_description = data.get("seeking_description", "")
        return artist.save_to_db()
