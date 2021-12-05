from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import cloudinary
# from flask_babelex import Babel


app = Flask(__name__)

app.secret_key = ":>\x8dT3H\xa3\xc4\x90[\x95\xf0\xcd\xd2X\x1b"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123456789@localhost/mysaledb?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True


db = SQLAlchemy(app=app)
login = LoginManager(app=app)
cloudinary.config(cloud_name="dtnpj540t",
                  api_key="371357798369383",
                  api_secret="9zy7ehlUetIxxl7ibee4y3tmdL4")

app.config["PAGE_SIZE"] = 6

# babel = Babel(app=app)

#
# @babel.localeselector
# def get_locale():
#     return 'vi'
