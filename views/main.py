from flask import Blueprint, render_template
from models.artist import Artist
from models.venue import Venue

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    artists = Artist.get_recent()
    venues = Venue.get_recent()
    return render_template("pages/home.html", artists=artists, venues=venues)


@bp.errorhandler(404)
def not_found_error(error):
    return render_template("errors/404.html", error=error), 404


@bp.errorhandler(500)
def server_error(error):
    return render_template("errors/500.html", error=error), 500
