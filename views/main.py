from flask import Blueprint, render_template

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    return render_template("pages/home.html")


@bp.errorhandler(404)
def not_found_error(error):
    return render_template("errors/404.html", error=error), 404


@bp.errorhandler(500)
def server_error(error):
    return render_template("errors/500.html", error=error), 500
