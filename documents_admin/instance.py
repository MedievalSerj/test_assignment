import logging
import os
from .admin import init_admin
from .db.models import User, Role

from flask import Flask, url_for
from documents_admin.utils.db import get_scoped_session
from flask_admin import helpers as admin_helpers
from flask_security import Security
from .flask_security import SQLAlchemyUserDatastore, ExtendedRegisterForm


class App(Flask):
    def __init__(self, *args,
                 db_session=None,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self._db_session = db_session

    @property
    def db_session(self):
        return self._db_session

    def set_db_session(self, db_session):
        self._db_session = db_session


def configure_from_default_config(app):
    config_name = os.getenv('ENV', 'development').lower().title()
    app.config.from_object('documents_admin.config.{}Config'
                           .format(config_name))
    app.logger.info('Config: %s', config_name)


def configure_app(app, config_obj):
    """Flask application instance configuration."""
    if config_obj:
        app.config.from_object(config_obj)
    else:
        configure_from_default_config(app)


# def configure_logging(app):
#     """Logging configuration."""
#     logging.basicConfig(
#         level=app.config['LOGLEVEL'],
#         format='[%(levelname)s] %(asctime)s|%(name)s:%(lineno)d  %(message)s',
#         datefmt='%Y%m%d-%H:%M%p'
#     )


def get_db_session(app):
    return get_scoped_session(app.config['DB_URL'])


def create_app(app_name='documents_admin', config_obj=None):
    """App factory."""
    app = App(app_name, template_folder='templates', static_folder='static')
    configure_app(app, config_obj=config_obj)
    # configure_logging(app)
    app.set_db_session(get_db_session(app))
    return app


app = create_app()
user_datastore = SQLAlchemyUserDatastore(app.db_session, User, Role)
security = Security(app, user_datastore)
                    # register_form=ExtendedRegisterForm)
admin = init_admin(app)


@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )


@app.teardown_appcontext
def shutdown_zoning_session(response_or_exc):
    app.db_session.remove()
    return response_or_exc


if __name__ == '__main__':
    app.run()
