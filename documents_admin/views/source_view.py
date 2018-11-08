from .basic_view import BasicAdminView


class SourceView(BasicAdminView):

    column_list = ('name', 'sid', 'url')
    form_columns = ('name', 'sid', 'url')
