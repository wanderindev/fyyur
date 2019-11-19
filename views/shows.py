from flask import (
    abort,
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from forms import ShowForm
from models.artist import Show

bp = Blueprint("shows", __name__)


@bp.route("/")
def shows():
    data = Show.get_shows()
    return render_template("pages/shows.html", shows=data)


@bp.route("/create")
def create_shows():
    form = ShowForm()
    return render_template("forms/new_show.html", form=form)


@bp.route("/create", methods=["POST"])
def create_show_submission():
    data = request.form.to_dict()
    show = Show(**data)
    result = show.save_to_db()
    if result["error"]:
        flash("An error occurred. Show could not be listed.")
        abort(500)
    flash("Show was successfully listed!")
    return render_template("pages/home.html")
