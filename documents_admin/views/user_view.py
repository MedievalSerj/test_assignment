from flask_security.utils import hash_password
from wtforms.fields import PasswordField
from wtforms.fields.html5 import EmailField

from .basic_view import BasicAdminView


class UserView(BasicAdminView):

    column_list = ('username', 'email', 'roles')
    form_columns = ('roles', 'email', 'username', 'password', 'active')

    form_overrides = {
        'email': EmailField,
        'password': PasswordField
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_model_change(self, form, model, is_created):
        if form.password.data:
            model.password = hash_password(form.password.data)
