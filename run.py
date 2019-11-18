import os
import sys
from sqlalchemy import exc
from app import create_app, db
from constants import ARTISTS, SHOWS, VENUES
from models.artist import Artist
from models.show import Show
from models.venue import Venue

app = create_app(os.getenv("FLASK_CONFIG") or "development")


@app.before_first_request
def populate_db():
    if app.config["POPULATE_DB"]:
        for artist in ARTISTS:
            db.session.add(Artist(**artist))

        for show in SHOWS:
            db.session.add(Show(**show))

        for venue in VENUES:
            db.session.add(Venue(**venue))

        try:
            db.session.commit()
        except exc.SQLAlchemyError:
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()


if __name__ == "__main__":
    app.run()
