import uuid
from datetime import datetime
from io import StringIO
from time import time

import jsonlines
import pytz
from flask import abort, current_app, make_response, redirect
from flask_admin import expose
from flask_security import current_user
from wtforms import TextAreaField

from celery_tasks.instance import save_to_jsonl
from documents_admin.marshalling import DocumentSchema

from .basic_view import BasicUserView


def format_date(timestamp):
    return (datetime
            .fromtimestamp(timestamp)
            .replace(tzinfo=pytz.utc)
            .strftime('%Y-%m-%d %X'))


def user_can_edit(current_user_id, is_admin_user, model_user_id, model_added_at):
    if is_admin_user:
        return True
    if (current_user_id == model_user_id and int(time())
            - model_added_at <= current_app.config['TIME_USER_CAN_EDIT']):
        return True
    return False


class DocumentView(BasicUserView):

    list_template = 'document_list.html'

    column_searchable_list = (
        'source.name',
        'source.sid',
        'created',
        'user.username',
        'updated',
        'title',
        'text')

    column_filters = (
        'source.name',
        'source.sid',
        'created',
        'user.username',
        'updated',
        'title',
        'text'
    )

    form_columns = ('source', 'title', 'text', 'url', 'created')
    form_overrides = {
        'text': TextAreaField,
    }
    column_formatters = {
        'added_at': lambda v, c, m, p: format_date(m.added_at),
        'updated': lambda v, c, m, p: format_date(m.updated)
    }

    def render(self, template, **kwargs):
        return super().render(template,
                              current_user_id=current_user.id,
                              is_admin_user=current_user.has_role('admin'),
                              user_can_edit=user_can_edit,
                              **kwargs)

    def delete_model(self, model):
        if not user_can_edit(current_user.id,
                             current_user.has_role('admin'),
                             model.user_id,
                             model.added_at):
            abort(403)
        return super().delete_model(model)

    def update_model(self, form, model):
        if not user_can_edit(current_user.id,
                             current_user.has_role('admin'),
                             model.user_id,
                             model.added_at):
            abort(403)
        return super().update_model(form, model)

    def on_model_change(self, form, model, is_created):
        model.user = current_user
        if model.times_edited is None:
            model.times_edited = 0
        else:
            model.times_edited += 1

    def _get_data_for_export(self):
        view_args = self._get_list_extra_args()

        # Map column index to column name
        sort_column = self._get_column_by_idx(view_args.sort)
        if sort_column is not None:
            sort_column = sort_column[0]

        _, query = self.get_list(view_args.page,
                                 sort_column,
                                 view_args.sort_desc,
                                 view_args.search,
                                 view_args.filters,
                                 execute=False)
        return query.limit(None).all()

    def _create_jsonl(self, data_dict):
        io = StringIO()
        with jsonlines.Writer(io) as writer:
            writer.write_all(data_dict)
        io.seek(0)
        return io.getvalue()

    @expose('/export_jsonl/')
    def export_jsonl(self):
        if not current_user.has_role('admin'):
            abort(403)
        data = self._get_data_for_export()
        file_content = self._create_jsonl(
            DocumentSchema().dump(data, many=True))
        response = make_response(file_content)
        response.mimetype = 'text/jsonl'
        response.headers['Content-Disposition'] = (
            'attachment; filename={}.jsonl'
                .format(uuid.uuid1()))
        return response

    @expose('/save_jsonl/')
    def save_jsonl(self):
        if not current_user.has_role('admin'):
            abort(403)
        data = self._get_data_for_export()
        save_to_jsonl.delay(
            DocumentSchema().dump(data, many=True),
            'jsonl_storage',
            '{}.jsonl'.format(uuid.uuid1()))
        return redirect('document')
