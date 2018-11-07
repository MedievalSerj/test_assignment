from flask_security.datastore import Datastore, UserDatastore
from flask_security.utils import get_identity_attributes
from flask_security.forms import RegisterForm
from wtforms import StringField
from wtforms.validators import Required


class SQLAlchemyDatastore(Datastore):
    def commit(self):
        self.db_session.commit()

    def put(self, model):
        self.db_session.add(model)
        return model

    def delete(self, model):
        self.db_session.delete(model)


class SQLAlchemyUserDatastore(SQLAlchemyDatastore, UserDatastore):
    """A SQLAlchemy datastore implementation for Flask-Security that assumes the
    use of the Flask-SQLAlchemy extension (not anymore!).
    """
    def __init__(self, db_session, user_model, role_model):
        SQLAlchemyDatastore.__init__(self, db_session)
        self.db_session = db_session
        UserDatastore.__init__(self, user_model, role_model)

    def get_user(self, identifier):
        if self._is_numeric(identifier):
            return (self.db_session
                        .query(self.user_model)
                        .get(identifier))
        for attr in get_identity_attributes():
            query = getattr(self.user_model, attr).ilike(identifier)
            rv = (self.db_session
                      .query(self.user_model)
                      .filter(query)
                      .first())
            if rv is not None:
                return rv

    def _is_numeric(self, value):
        try:
            int(value)
        except (TypeError, ValueError):
            return False
        return True

    def find_user(self, **kwargs):
        return (self.db_session
                    .query(self.user_model)
                    .filter_by(**kwargs)
                    .first())

    def find_role(self, role):
        return (self.db_session
                    .query(self.role_model)
                    .filter_by(name=role)
                    .first())


class ExtendedRegisterForm(RegisterForm):
    username = StringField('Username', [Required()])
