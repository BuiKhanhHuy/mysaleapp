from app import db, admin
from flask import redirect
from flask_admin.contrib.sqla import ModelView
from flask_admin import expose, BaseView
from flask_login import current_user, logout_user
from app.models import *


class GeneralView(ModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    create_modal = True
    edit_modal = True
    details_modal = True


class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role


class UserView(GeneralView, AuthenticatedModelView):
    column_exclude_list = ["password", "avatar"]
    column_searchable_list = ["id", "email", "username"]
    column_filters = ["id", "email", "name", "username", "active", "joined_date", "user_role"]


class CategoryView(GeneralView, AuthenticatedModelView):
    column_searchable_list = ["id", "name"]


class ProductView(GeneralView, AuthenticatedModelView):
    column_searchable_list = ["id", "name", "price", "description"]
    column_filters = ["id", "name", "price", "description"]

class LogoutView(BaseView):
    @expose("/")
    def index(self):
        logout_user()
        return redirect("/admin")

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role


admin.add_view(UserView(User, db.session))
admin.add_view(CategoryView(Category, db.session))
admin.add_view(ProductView(Product, db.session))
admin.add_view(LogoutView(name="Logout"))


