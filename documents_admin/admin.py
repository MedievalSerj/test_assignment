from flask_admin import Admin
from .views.basic_view import BasicAdminView, BasicUserView
from .views.user_view import UserView
from documents_admin.db.models import (Role,
                                       User,
                                       Source,
                                       Document)


def init_admin(app):
    admin = Admin(
        app,
        name='documents admin',
        base_template='my_master.html',
        template_mode='bootstrap3',
        url='/',
    )
    admin.add_view(BasicAdminView(Role, app.db_session))
    admin.add_view(UserView(User, app.db_session))
    admin.add_view(BasicUserView(Source, app.db_session))
    admin.add_view(BasicUserView(Document, app.db_session))
    return admin
