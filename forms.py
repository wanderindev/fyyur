from datetime import datetime
from flask_wtf import Form
from wtforms import (
    BooleanField,
    DateTimeField,
    SelectField,
    SelectMultipleField,
    StringField,
)
from wtforms.validators import DataRequired, URL
from constants import GENRES, STATES


class ShowForm(Form):
    artist_id = StringField("artist_id")
    venue_id = StringField("venue_id")
    start_time = DateTimeField(
        "start_time", validators=[DataRequired()], default=datetime.today()
    )


class VenueForm(Form):
    name = StringField("name", validators=[DataRequired()])
    city = StringField("city", validators=[DataRequired()])
    state = SelectField("state", validators=[DataRequired()], choices=STATES,)
    address = StringField("address", validators=[DataRequired()])
    phone = StringField("phone")
    image_link = StringField("image_link")
    genres = SelectMultipleField(
        "genres", validators=[DataRequired()], choices=GENRES,
    )
    facebook_link = StringField("facebook_link", validators=[URL()])
    website = StringField("website")
    seeking_talent = BooleanField(
        "seeking_talent", default=True, false_values=("false", "")
    )
    seeking_description = StringField("seeking_description")


class ArtistForm(Form):
    name = StringField("name", validators=[DataRequired()])
    city = StringField("city", validators=[DataRequired()])
    state = SelectField("state", validators=[DataRequired()], choices=STATES,)
    phone = StringField("phone")
    genres = SelectMultipleField(
        "genres", validators=[DataRequired()], choices=GENRES,
    )
    image_link = StringField("image_link", validators=[URL()],)
    facebook_link = StringField("facebook_link", validators=[URL()],)
    website = StringField("website", validators=[URL()],)
    seeking_venue = BooleanField(
        "seeking_venue", default=True, false_values=(False, "false", "")
    )
    seeking_description = StringField("seeking_description")
