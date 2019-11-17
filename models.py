import sys
from datetime import date, datetime, time
from decimal import Decimal
from sqlalchemy import exc
from sqlalchemy.orm import collections
from app import db
from constants import GENRE_CHECK


class ModelMixin(object):
    def __iter__(self):
        return ((k, v) for k, v in vars(self).items() if not k.startswith("_"))

    def __repr__(self):
        class_name = type(self).__name__
        attributes = ", ".join([f"{k!r}={v!r}" for k, v in self])

        return f"<{class_name}({attributes})>"

    def delete_from_db(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return {"error": False}
        except exc.SQLAlchemyError as e:
            print(e)
            print(sys.exc_info())
            db.session.rollback()
            return {"error": True}
        finally:
            db.session.close()

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
            return {"error": False}
        except exc.SQLAlchemyError as e:
            print(e)
            print(sys.exc_info())
            db.session.rollback()
            return {"error": True}
        finally:
            db.session.close()

    @staticmethod
    def to_dict(_model, _obj):
        _obj = _obj or {}
        for k, v in _model:
            if type(v) == collections.InstrumentedList:
                _obj[k] = [item.to_dict() for item in v]
            elif isinstance(v, (date, datetime, time)):
                _obj[k] = v.isoformat()
            elif isinstance(v, (float, Decimal)):
                _obj[k] = str(v)
            else:
                _obj[k] = v

        return _obj


class Venue(db.Model, ModelMixin):
    __tablename__ = "venues"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(30)))
    website = db.Column(db.String(500))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship(
        "Show", backref="venue", lazy=True, cascade="delete"
    )

    def __init__(self, **kwargs):
        super(Venue, self).__init__(**kwargs)
        check_genres = all(genre in GENRE_CHECK for genre in self.genres)
        if not check_genres:
            raise exc.ProgrammingError(
                "Invalid genre",
                {"Genres passed": self.genres},
                {"Genres allowed": GENRE_CHECK},
            )

    @classmethod
    def past_shows(cls, _id):
        return Show.past_shows_by_venue(_id)

    @classmethod
    def upcoming_shows(cls, _id):
        return Show.upcoming_shows_by_venue(_id)

    @classmethod
    def past_shows_count(cls, _id):
        return len(cls.past_shows(_id))

    @classmethod
    def upcoming_shows_count(cls, _id):
        return len(cls.upcoming_shows(_id))

    @classmethod
    def get_locations(cls):
        return cls.query.with_entities(cls.city, cls.state).distinct().all()

    @classmethod
    def get_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def get_venues_by_location(cls):
        return [
            {
                "city": _city,
                "state": _state,
                "venues": [
                    {
                        "id": venue.id,
                        "name": venue.name,
                        "num_upcoming_shows": cls.upcoming_shows_count(
                            venue.id
                        ),
                    }
                    for venue in cls.query.filter_by(city=_city).all()
                ],
            }
            for _city, _state in cls.get_locations()
        ]

    @classmethod
    def search(cls, search_term):
        venues = cls.query.filter(cls.name.ilike(f"%{search_term}%")).all()
        return {
            "data": [
                {
                    "id": venue.id,
                    "name": venue.name,
                    "num_upcoming_shows": cls.upcoming_shows_count(venue.id),
                }
                for venue in venues
            ],
            "count": len(venues),
        }

    @classmethod
    def get_venue(cls, _id):
        _obj = {
            "past_shows": cls.past_shows(_id),
            "past_shows_count": cls.past_shows_count(_id),
            "upcoming_shows": cls.upcoming_shows(_id),
            "upcoming_shows_count": cls.upcoming_shows_count(_id),
        }
        venue = cls.get_by_id(_id)
        if not venue:
            return None
        return cls.to_dict(venue, _obj)

    @classmethod
    def update(cls, _id, data):
        venue = cls.get_by_id(_id)
        venue.name = data.get("name", "")
        venue.city = data.get("city", "")
        venue.state = data.get("state", "")
        venue.phone = data.get("phone", "")
        venue.genres = data.get("genres", [])
        venue.image_link = data.get("image_link", "")
        venue.facebook_link = data.get("facebook_link", "")
        venue.website = data.get("website", "")
        venue.seeking_talent = data.get("seeking_talent", False)
        venue.seeking_description = data.get("seeking_description", "")
        return venue.save_to_db()


class Artist(db.Model, ModelMixin):
    __tablename__ = "artists"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(30)))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(500))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship("Show", backref="artist", lazy=True)

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
    def upcoming_shows(cls, _id):
        return Show.upcoming_shows_by_artist(_id)

    @classmethod
    def past_shows_count(cls, _id):
        return len(cls.past_shows(_id))

    @classmethod
    def upcoming_shows_count(cls, _id):
        return len(cls.upcoming_shows(_id))

    @classmethod
    def get_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def get_artists(cls):
        return [
            {"id": artist.id, "name": artist.name, }
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
