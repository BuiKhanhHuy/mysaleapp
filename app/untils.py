from app.models import *
from app import app
from flask_login import current_user
from sqlalchemy import func
from sqlalchemy.sql import extract
import hashlib


def load_categories():
    return Category.query.all()


def load_products(category_id=None, keyword=None, from_price=None, to_price=None, page=1):
    products = Product.query

    if category_id:
        products = products.filter(Product.category_id.__eq__(int(category_id)))
    if keyword:
        products = products.filter(Product.name.contains(keyword))
    if from_price:
        products = products.filter(Product.price.__ge__(from_price))
    if to_price:
        products = products.filter(Product.price.__le__(to_price))

    page_size = int(app.config["PAGE_SIZE"])
    start_page = (page - 1) * page_size

    return products.slice(start_page, start_page + page_size).all()


def count_product():
    return Product.query.count()


def get_product_by_id(product_id):
    return Product.query.get(product_id)


def get_user_by_id(user_id):
    return User.query.get(user_id)


def check_user(username, password, user_role=UserRole.USER):
    if username and password:
        password = hashlib.md5(password.strip().encode("utf-8")).hexdigest()
        user = User.query.filter(User.username.__eq__(username), User.password.__eq__(password),
                                 User.user_role.__eq__(user_role)).first()
        return user


def add_user(fullname, username, email, password, avatar=None):
    try:
        if User.query.filter(User.username.__eq__(username.strip())).first():
            raise ValueError('Tên người dùng đã tồn tại')
        if User.query.filter(User.email.__eq__(email.strip())).first():
            raise ValueError('Email đã tồn tại')
        password = hashlib.md5(password.strip().encode("utf-8")).hexdigest()
        user = User(name=fullname.strip(), username=username.strip(), email=email.strip(), password=password,
                    avatar=avatar)
        db.session.add(user)
        db.session.commit()
    except ValueError as ex:
        return ex
    except Exception as ex:
        return ex
    return None


def check_password(user_id, password):
    password = hashlib.md5(password.strip().encode("utf-8")).hexdigest()
    if User.query.filter(User.id.__eq__(user_id), User.password.__eq__(password)).count() > 0:
        return True
    return False


def change_password(user_id, password):
    user = User.query.get(user_id)
    user.password = hashlib.md5(password.strip().encode("utf-8")).hexdigest()
    db.session.add(user)
    try:
        db.session.commit()
    except:
        return False
    else:
        return True


def change_user(user_id, fullname, username, email, avatar=None):
    user = User.query.get(user_id)
    try:
        if User.query.filter(User.id != user_id, User.username.__eq__(username.strip())).count() > 0:
            raise ValueError('Tên người dùng đã tồn tại')
        if User.query.filter(User.id != user_id, User.email.__eq__(email.strip())).count() > 0:
            raise ValueError('Email đã tồn tại')

        user.name = fullname.strip()
        user.username = username.strip()
        user.email = email.strip()
        user.avatar = avatar

        db.session.add(user)
        db.session.commit()
    except ValueError as ex:
        return ex
    except Exception as ex:
        return ex
    return None


def total_quantity_and_price(cart):
    total_quantity = 0
    total_price = 0

    if cart:
        for product in cart.values():
            total_quantity = total_quantity + product.get("quantity")
            total_price = total_price + product.get("quantity") * product.get("price")

    return total_quantity, total_price


def add_receipt(cart):
    receipt = Receipt(user_id=current_user.id)
    db.session.add(receipt)
    for product in cart.values():
        receipt_detail = ReceiptDetail(
            product_id=product.get('id'),
            receipt=receipt,
            unit_price=product.get('price'),
            quantity=product.get('quantity')
        )
        db.session.add(receipt_detail)
    db.session.commit()


def product_statistics():
    return db.session.query(
        Category.id, Category.name, func.count(Product.id))\
        .join(Product, Product.category_id.__eq__(Category.id), isouter=True)\
        .group_by(Category.id, Category.name).all()


def product_sale_statistics():
    stats = db.session.query(Product.id, Product.name, func.sum(ReceiptDetail.unit_price * ReceiptDetail.quantity))\
        .join(ReceiptDetail, ReceiptDetail.product_id.__eq__(Product.id), isouter=True)\
        .group_by(Product.id, Product.name)
    return stats.all()


def product_sale_statistics_month(months):
    stats = db.session.query(extract('month', Receipt.created_date), func.sum(ReceiptDetail.unit_price * ReceiptDetail.quantity))\
        .join(ReceiptDetail, ReceiptDetail.receipt_id.__eq__(Receipt.id), isouter=True) \
        .filter(extract('month', Receipt.created_date).in_(months))\
        .group_by(extract('month', Receipt.created_date)).order_by(extract('month', Receipt.created_date))
    return stats.all()


if __name__ == "__main__":
    pass