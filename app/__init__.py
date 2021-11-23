from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager
# from flask_babelex import Babel


app = Flask(__name__)

app.secret_key = ":>\x8dT3H\xa3\xc4\x90[\x95\xf0\xcd\xd2X\x1b"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123456789@localhost/saledb?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True


db = SQLAlchemy(app=app)
admin = Admin(app=app, name='QUẢN LÍ BÁN HÀNG', template_mode='bootstrap4')
login = LoginManager(app=app)
# babel = Babel(app=app)

#
# @babel.localeselector
# def get_locale():
#     return 'vi'
