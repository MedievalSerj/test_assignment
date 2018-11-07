from .basic_view import BasicAdminView
from flask_security.utils import hash_password


class UserView(BasicAdminView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_model_change(self, form, model, is_created):
        if form.password.data:
            model.password = hash_password(form.password.data)
