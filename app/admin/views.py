from flask import redirect, url_for, request
from flask_admin.contrib.sqla import ModelView
from flask.ext.admin import AdminIndexView
from wtforms import PasswordField
from wtforms.validators import InputRequired
from flask.ext.login import current_user

from .widgets import CKTextAreaField

class BaseAdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated


    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login', next=request.path))


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated


    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login', next=request.path))


class UserAdminView(BaseAdminView):
    column_searchable_list = ('username', 'email')
    column_sortable_list = ('username', 'email')
    column_exclude_list = ('pwdhash',)
    form_excluded_columns = ('pwdhash',)
    form_edit_rules = ('username', 'email')


    def scaffold_form(self):
        form_class = super(UserAdminView, self).scaffold_form()
        form_class.password = PasswordField('Password', [InputRequired()])
        return form_class


    def create_model(self, form):
        model = self.model(form.email.data, form.username.data, form.password.data)
        form.populate_obj(model)
        self.session.add(model)
        self._on_model_change(form, model, True)
        self.session.commit()


class PostAdminView(BaseAdminView):
    column_exclude_list = ('content',)
    form_overrides = {
        'content': CKTextAreaField
    }
    create_template = 'ckeditor.html'
    edit_template = 'ckeditor.html'


class CategoryAdminView(BaseAdminView):
    form_excluded_columns = ('posts',)