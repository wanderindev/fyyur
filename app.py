import babel
import dateutil.parser
import logging
from flask import (
    abort,
    flash,
    Flask,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_moment import Moment
from logging import Formatter, FileHandler
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import config
from forms import ArtistForm, ShowForm, VenueForm


db = SQLAlchemy()
migrate = Migrate()
moment = Moment()


def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)

    from models.artist import Artist
    from models.show import Show
    from models.venue import Venue

    def format_datetime(value, _format="medium"):
        date = dateutil.parser.parse(value)
        if _format == "full":
            _format = "EEEE MMMM, d, y 'at' h:mma"
        elif _format == "medium":
            _format = "EE MM, dd, y h:mma"
        return babel.dates.format_datetime(date, _format, locale="en_US")

    app.jinja_env.filters["datetime"] = format_datetime

    @app.route("/")
    def index():
        return render_template("pages/home.html")

    @app.route("/venues")
    def venues():
        data = Venue.get_venues_by_location()
        return render_template("pages/venues.html", areas=data)

    @app.route("/venues/search", methods=["POST"])
    def search_venues():
        search_term = request.form.get("search_term", "")
        results = Venue.search(search_term)
        return render_template(
            "pages/search_venues.html",
            results=results,
            search_term=search_term,
        )

    @app.route("/venues/<int:venue_id>", methods=["GET"])
    def show_venue(venue_id):
        venue = Venue.get_venue(venue_id)
        if not venue:
            return render_template("pages/home.html")
        return render_template("pages/show_venue.html", venue=venue)

    @app.route("/venues/<int:venue_id>/edit", methods=["GET"])
    def edit_venue(venue_id):
        venue = Venue.get_by_id(venue_id)
        form = VenueForm(request.form, obj=venue)
        form.genres.process_data(venue.genres)
        form.seeking_talent.process_data(venue.seeking_talent)
        return render_template("forms/edit_venue.html", form=form, venue=venue)

    @app.route("/venues/<int:venue_id>/edit", methods=["POST"])
    def edit_venue_submission(venue_id):
        genres = request.form.getlist("genres")
        data = request.form.to_dict()
        data["genres"] = genres
        data["seeking_talent"] = (
            True if data.get("seeking_talent", False) is "y" else False
        )
        result = Venue.update(venue_id, data)
        if result["error"]:
            flash(
                "An error occurred. Venue "
                + data["name"]
                + " could not be updated."
            )
            abort(500)
        flash("Venue " + data["name"] + " was successfully updated!")
        return redirect(url_for("show_venue", venue_id=venue_id))

    @app.route("/venues/<int:venue_id>", methods=["DELETE"])
    def delete_venue(venue_id):
        venue = Venue.get_by_id(venue_id)
        venue_name = venue.name
        result = venue.delete_from_db()
        if result["error"]:
            flash(
                "An error occurred. Venue "
                + venue_name
                + " could not be deleted."
            )
            abort(500)
        flash("Venue " + venue_name + " was successfully deleted!")
        return render_template("pages/home.html")

    @app.route("/venues/create", methods=["GET"])
    def create_venue_form():
        form = VenueForm()
        return render_template("forms/new_venue.html", form=form)

    @app.route("/venues/create", methods=["POST"])
    def create_venue_submission():
        genres = request.form.getlist("genres")
        data = request.form.to_dict()
        data["genres"] = genres
        data["seeking_talent"] = (
            True if data.get("seeking_talent", False) is "y" else False
        )
        venue = Venue(**data)
        result = venue.save_to_db()
        if result["error"]:
            flash(
                "An error occurred. Venue "
                + data["name"]
                + " could not be listed."
            )
            abort(500)
        flash("Venue " + data["name"] + " was successfully listed!")
        return render_template("pages/home.html")

    @app.route("/artists")
    def artists():
        data = Artist.get_artists()
        return render_template("pages/artists.html", artists=data)

    @app.route("/artists/search", methods=["POST"])
    def search_artists():
        search_term = request.form.get("search_term", "")
        results = Artist.search(search_term)
        return render_template(
            "pages/search_artists.html",
            results=results,
            search_term=search_term,
        )

    @app.route("/artists/<int:artist_id>")
    def show_artist(artist_id):
        artist = Artist.get_artist(artist_id)
        print(artist)
        if not artist:
            return render_template("pages/home.html")
        return render_template("pages/show_artist.html", artist=artist)

    @app.route("/artists/<int:artist_id>/edit", methods=["GET"])
    def edit_artist(artist_id):
        artist = Artist.get_by_id(artist_id)
        form = ArtistForm(request.form, obj=artist)
        form.genres.process_data(artist.genres)
        form.seeking_venue.process_data(artist.seeking_venue)
        return render_template(
            "forms/edit_artist.html", form=form, artist=artist
        )

    @app.route("/artists/<int:artist_id>/edit", methods=["POST"])
    def edit_artist_submission(artist_id):
        genres = request.form.getlist("genres")
        data = request.form.to_dict()
        data["genres"] = genres
        data["seeking_venue"] = (
            True if data.get("seeking_venue", False) is "y" else False
        )
        result = Artist.update(artist_id, data)
        if result["error"]:
            flash(
                "An error occurred. Artist "
                + data["name"]
                + " could not be updated."
            )
            abort(500)
        flash("Artist " + data["name"] + " was successfully updated!")
        return redirect(url_for("show_artist", artist_id=artist_id))

    @app.route("/artist/<int:artist_id>", methods=["DELETE"])
    def delete_artist(artist_id):
        artist = Artist.get_by_id(artist_id)
        artist_name = artist.name
        result = artist.delete_from_db()
        if result["error"]:
            flash(
                "An error occurred. Artist "
                + artist_name
                + " could not be deleted."
            )
            abort(500)
        flash("Artist " + artist_name + " was successfully deleted!")
        return render_template("pages/home.html")

    @app.route("/artists/create", methods=["GET"])
    def create_artist_form():
        form = ArtistForm()
        return render_template("forms/new_artist.html", form=form)

    @app.route("/artists/create", methods=["POST"])
    def create_artist_submission():
        genres = request.form.getlist("genres")
        data = request.form.to_dict()
        data["genres"] = genres
        data["seeking_venue"] = (
            True if data.get("seeking_venue", False) is "y" else False
        )
        artist = Artist(**data)
        result = artist.save_to_db()
        if result["error"]:
            flash(
                "An error occurred. Artist "
                + data["name"]
                + " could not be listed."
            )
            abort(500)
        flash("Artist " + data["name"] + " was successfully listed!")
        return render_template("pages/home.html")

    @app.route("/shows")
    def shows():
        data = Show.get_shows()
        return render_template("pages/shows.html", shows=data)

    @app.route("/shows/create")
    def create_shows():
        form = ShowForm()
        return render_template("forms/new_show.html", form=form)

    @app.route("/shows/create", methods=["POST"])
    def create_show_submission():
        data = request.form.to_dict()
        show = Show(**data)
        result = show.save_to_db()
        if result["error"]:
            flash("An error occurred. Show could not be listed.")
            abort(500)
        flash("Show was successfully listed!")
        return render_template("pages/home.html")

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template("errors/404.html", error=error), 404

    @app.errorhandler(500)
    def server_error(error):
        return render_template("errors/500.html", error=error), 500

    if not app.debug:
        file_handler = FileHandler("error.log")
        file_handler.setFormatter(
            Formatter(
                "%(asctime)s %(levelname)s: %(message)s "
                "[in %(pathname)s:%(lineno)d]"
            )
        )
        app.logger.setLevel(logging.INFO)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.info("errors")

    return app
