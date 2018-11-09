from flask_admin import Admin

from documents_admin.db.models import Document, Source, User

from .views.document_view import DocumentView
from .views.source_view import SourceView
from .views.user_view import UserView


def init_admin(app):
    admin = Admin(
        app,
        name='documents admin',
        base_template='my_master.html',
        template_mode='bootstrap3',
        url='/',
    )
    admin.add_view(UserView(User, app.db_session))
    admin.add_view(SourceView(Source, app.db_session))
    admin.add_view(DocumentView(Document, app.db_session))
    return admin
