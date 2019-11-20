from flask import (
    abort,
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from forms import VenueForm
from models.venue import Venue

bp = Blueprint("venues", __name__)


@bp.route("/")
def venues():
    data = Venue.get_venues_by_location()
    return render_template("pages/venues.html", areas=data)


@bp.route("/search", methods=["POST"])
def search_venues():
    search_term = request.form.get("search_term", "")
    results = Venue.search(search_term)
    return render_template(
        "pages/search_venues.html", results=results, search_term=search_term,
    )


@bp.route("/<int:venue_id>", methods=["GET"])
def show_venue(venue_id):
    venue = Venue.get_venue(venue_id)
    if not venue:
        return render_template("pages/home.html")
    return render_template("pages/show_venue.html", venue=venue)


@bp.route("/<int:venue_id>/edit", methods=["GET"])
def edit_venue(venue_id):
    venue = Venue.get_by_id(venue_id)
    form = VenueForm(request.form, obj=venue)
    form.genres.process_data(venue.genres)
    form.seeking_talent.process_data(venue.seeking_talent)
    return render_template("forms/edit_venue.html", form=form, venue=venue)


@bp.route("/<int:venue_id>/edit", methods=["POST"])
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
    return redirect(url_for("venues.show_venue", venue_id=venue_id))


@bp.route("/<int:venue_id>", methods=["DELETE"])
def delete_venue(venue_id):
    venue = Venue.get_by_id(venue_id)
    venue_name = venue.name
    result = venue.delete_from_db()
    if result["error"]:
        flash(
            "An error occurred. Venue " + venue_name + " could not be deleted."
        )
        abort(500)
    flash("Venue " + venue_name + " was successfully deleted!")
    return render_template("pages/home.html")


@bp.route("/create", methods=["GET"])
def create_venue_form():
    form = VenueForm()
    return render_template("forms/new_venue.html", form=form)


@bp.route("/create", methods=["POST"])
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
