from sqlalchemy import exc
from app import db
from constants import GENRE_CHECK
from .mixin import ModelMixin
from .show import Show


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
    genres = db.Column(db.ARRAY(db.String(30)), nullable=False)
    website = db.Column(db.String(500))
    seeking_talent = db.Column(db.Boolean, default=True)
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
    def past_shows_count(cls, _id):
        return len(cls.past_shows(_id))

    @classmethod
    def upcoming_shows(cls, _id):
        return Show.upcoming_shows_by_venue(_id)

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
