from .basic_view import BasicUserView
from flask_security import current_user
from wtforms import TextAreaField
from datetime import datetime
import pytz


def format_date(timestamp):
    return (datetime
            .fromtimestamp(timestamp)
            .replace(tzinfo=pytz.utc)
            .astimezone(tz=pytz.timezone('Europe/Kiev'))
            .strftime('%x %X'))


class DocumentView(BasicUserView):

    can_view_details = True

    form_columns = ('source', 'title', 'text', 'url', 'created')
    form_overrides = {
        'text': TextAreaField,
    }
    column_formatters = {
        'added_at': lambda v, c, m, p: format_date(m.added_at),
        'updated': lambda v, c, m, p: format_date(m.updated)
    }

    def on_model_change(self, form, model, is_created):
        model.user = current_user

    def is_accessible(self):
        if current_user.has_role('admin'):
            self.can_edit = True
        else:
            self.can_edit = False
        return True
