from flask import (
    abort,
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from forms import ArtistForm
from models.artist import Artist

bp = Blueprint("artists", __name__)


@bp.route("/")
def artists():
    data = Artist.get_artists()
    return render_template("pages/artists.html", artists=data)


@bp.route("/search", methods=["POST"])
def search_artists():
    search_term = request.form.get("search_term", "")
    results = Artist.search(search_term)
    return render_template(
        "pages/search_artists.html", results=results, search_term=search_term,
    )


@bp.route("/<int:artist_id>")
def show_artist(artist_id):
    artist = Artist.get_artist(artist_id)
    if not artist:
        return render_template("pages/home.html")
    return render_template("pages/show_artist.html", artist=artist)


@bp.route("/<int:artist_id>/edit", methods=["GET"])
def edit_artist(artist_id):
    artist = Artist.get_by_id(artist_id)
    form = ArtistForm(request.form, obj=artist)
    form.genres.process_data(artist.genres)
    form.seeking_venue.process_data(artist.seeking_venue)
    return render_template("forms/edit_artist.html", form=form, artist=artist)


@bp.route("/<int:artist_id>/edit", methods=["POST"])
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
    return redirect(url_for("artists.show_artist", artist_id=artist_id))


@bp.route("/<int:artist_id>", methods=["DELETE"])
def delete_artist(artist_id):
    print("delete")
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


@bp.route("/create", methods=["GET"])
def create_artist_form():
    form = ArtistForm()
    return render_template("forms/new_artist.html", form=form)


@bp.route("/create", methods=["POST"])
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
