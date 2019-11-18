import sys
from datetime import date, datetime, time
from decimal import Decimal
from sqlalchemy import exc
from sqlalchemy.orm import collections
from app import db


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
