from app.models import *
import hashlib


def load_categories():
    return Category.query.all()


def load_products(category_id=None, keyword=None, from_price=None, to_price=None):
    products = Product.query

    if category_id:
        products = products.filter(Product.category_id == int(category_id))
    if keyword:
        products = products.filter(Product.name.contains(keyword))
    if from_price:
        products = products.filter(Product.price.__ge__(from_price))
    if to_price:
        products = products.filter(Product.price.__le__(to_price))

    return products.all()


def get_product_by_id(product_id):
    return Product.query.get(product_id)


def get_user_by_id(user_id):
    return User.query.get(user_id)


def check_user(username, password):
    if username and password:
        password = hashlib.md5(password.strip().encode("utf-8")).hexdigest()
        user = User.query.filter(User.username == username, User.password == password).first()
        return user


def add_user(fullname, username, password, email=None, avatar=None):
    user = User(name=fullname, email=email, username=username, password=password, avatar=avatar)
    db.session.add(user)
    db.session.commit()
