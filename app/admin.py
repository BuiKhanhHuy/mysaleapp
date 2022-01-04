from wtforms import PasswordField

from app import app, db, untils
from flask import redirect, request
from flask_admin.contrib.sqla import ModelView
from flask_admin import expose, BaseView, Admin, AdminIndexView
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
        if current_user.is_authenticated and current_user.user_role == UserRole.ADMIN:
            return True


class UserView(GeneralView, AuthenticatedModelView):
    # column_exclude_list = ["password", "avatar"]
    column_searchable_list = ["id", "email", "username"]
    column_filters = ["id", "email", "name", "username",
                      "active", "joined_date", "user_role"]
    column_descriptions = dict(
        email='First and Last name'
    )


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
        if current_user.is_authenticated and current_user.user_role == UserRole.ADMIN:
            return True


class MyAdminIndexView(AdminIndexView):
    @expose("/")
    def index(self):
        stats = untils.product_statistics()
        return self.render("admin/index.html", stats=stats)


class StatsView(BaseView):
    @expose("/", methods=['post', 'get'])
    def index(self):
        checks = request.json
        months = [x for x in range(1, 13)]
        for x in range(0, 12):
            months.append(True)
        if checks:
            months = checks['checkValue']
        print(months)
        product_sale_staticstics = untils.product_sale_statistics()
        product_sale_statistics_month = untils.product_sale_statistics_month(
            months)
        return self.render("admin/stats.html", product_sale_staticstics=product_sale_staticstics,
                           product_sale_statistics_month=product_sale_statistics_month)


admin = Admin(app=app, name='Administrator',
              template_mode='bootstrap4',
              index_view=MyAdminIndexView())

admin.add_view(UserView(User, db.session))
admin.add_view(CategoryView(Category, db.session))
admin.add_view(ProductView(Product, db.session))
admin.add_view(StatsView(name="Stats"))
admin.add_view(LogoutView(name="Logout"))
